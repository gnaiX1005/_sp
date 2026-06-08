#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <signal.h>
#include <sys/socket.h>
#include <sys/select.h>
#include <sys/wait.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <pty.h>
#include <errno.h>

static void safe_write(int fd, const void *buf, size_t n)
{
    ssize_t r = write(fd, buf, n);
    (void)r;
}

#define PORT 2323
#define BACKLOG 10
#define BUFSIZE 4096

#define IAC   255
#define DONT  254
#define DO    253
#define WONT  252
#define WILL  251
#define SB    250
#define SE    240

#define TELOPT_ECHO   1
#define TELOPT_SGA    3

static void handle_client(int fd);
static void telnet_negotiate(int fd, unsigned char *buf, int *len);
static void sigchld_handler(int sig)
{
    (void)sig;
    while (waitpid(-1, NULL, WNOHANG) > 0);
}

int main(int argc, char *argv[])
{
    int port = PORT;
    if (argc > 1) port = atoi(argv[1]);

    int sfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sfd < 0) { perror("socket"); return 1; }

    int opt = 1;
    setsockopt(sfd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));

    struct sockaddr_in addr = {0};
    addr.sin_family = AF_INET;
    addr.sin_addr.s_addr = INADDR_ANY;
    addr.sin_port = htons(port);

    if (bind(sfd, (struct sockaddr *)&addr, sizeof(addr)) < 0) {
        perror("bind"); return 1;
    }
    if (listen(sfd, BACKLOG) < 0) {
        perror("listen"); return 1;
    }

    printf("telnetd: listening on port %d\n", port);
    signal(SIGCHLD, sigchld_handler);

    while (1) {
        struct sockaddr_in client;
        socklen_t len = sizeof(client);
        int cfd = accept(sfd, (struct sockaddr *)&client, &len);
        if (cfd < 0) {
            if (errno == EINTR) continue;
            perror("accept"); continue;
        }
        printf("connection from %s:%d\n",
               inet_ntoa(client.sin_addr), ntohs(client.sin_port));

        pid_t pid = fork();
        if (pid == 0) {
            close(sfd);
            handle_client(cfd);
            close(cfd);
            exit(0);
        }
        close(cfd);
    }
    close(sfd);
    return 0;
}

static void handle_client(int fd)
{
    int amaster, aslave;
    if (openpty(&amaster, &aslave, NULL, NULL, NULL) < 0) {
        perror("openpty"); return;
    }

    pid_t pid = fork();
    if (pid == 0) {
        close(amaster);
        setsid();
        dup2(aslave, 0);
        dup2(aslave, 1);
        dup2(aslave, 2);
        close(aslave);
        execlp("/bin/sh", "sh", NULL);
        perror("execlp");
        exit(1);
    }
    close(aslave);

    fd_set fds;
    unsigned char buf[BUFSIZE];

    while (1) {
        FD_ZERO(&fds);
        FD_SET(fd, &fds);
        FD_SET(amaster, &fds);
        int maxfd = (fd > amaster) ? fd : amaster;

        if (select(maxfd + 1, &fds, NULL, NULL, NULL) < 0) break;

        if (FD_ISSET(fd, &fds)) {
            int n = read(fd, buf, BUFSIZE);
            if (n <= 0) break;
            telnet_negotiate(fd, buf, &n);
            if (n > 0)
                safe_write(amaster, buf, n);
        }

        if (FD_ISSET(amaster, &fds)) {
            int n = read(amaster, buf, BUFSIZE);
            if (n <= 0) break;
            safe_write(fd, buf, n);
        }
    }
    kill(pid, SIGTERM);
    waitpid(pid, NULL, 0);
}

static void telnet_negotiate(int fd, unsigned char *buf, int *len)
{
    int i, j;
    for (i = 0, j = 0; i < *len; i++) {
        if (buf[i] == IAC && i + 2 < *len) {
            unsigned char cmd = buf[i+1];
            unsigned char opt = buf[i+2];
            unsigned char resp[3] = {IAC, 0, opt};

            if (cmd == DO) {
                resp[1] = WONT;
                safe_write(fd, resp, 3);
                i += 2; continue;
            } else if (cmd == DONT) {
                i += 2; continue;
            } else if (cmd == WILL) {
                resp[1] = DO;
                resp[2] = TELOPT_SGA;
                safe_write(fd, resp, 3);
                if (opt != TELOPT_SGA) {
                    resp[1] = DONT;
                    resp[2] = opt;
                    safe_write(fd, resp, 3);
                }
                i += 2; continue;
            } else if (cmd == WONT) {
                i += 2; continue;
            } else if (cmd == SB) {
                while (i + 1 < *len && !(buf[i] == IAC && buf[i+1] == SE))
                    i++;
                i++; continue;
            } else if (cmd == SE) {
                continue;
            }
        }
        buf[j++] = buf[i];
    }
    *len = j;
}
