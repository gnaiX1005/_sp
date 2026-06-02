#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>

int main() {
    pid_t pid = fork();
    if (pid == 0) {
        char *arg[] = {"ls", "-l", NULL};
        execvp(arg[0], arg);
        perror("execvp failed");
        exit(1);
    } else {
        wait(NULL);
        printf("parent: child %d finished\n", pid);
    }
}
