#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>

int main() {
    int fd[2];
    pipe(fd);
    pid_t pid = fork();
    if (pid == 0) {
        close(fd[0]);
        dup2(fd[1], 1);
        close(fd[1]);
        execlp("ls", "ls", "-l", NULL);
        perror("execlp failed");
        exit(1);
    } else {
        close(fd[1]);
        dup2(fd[0], 0);
        close(fd[0]);
        execlp("wc", "wc", "-l", NULL);
        perror("execlp failed");
        exit(1);
    }
}
