#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>

int main() {
    printf("%-5d: before fork\n", getpid());
    pid_t pid = fork();
    if (pid == 0) {
        printf("%-5d: I am child (parent=%d)\n", getpid(), getppid());
    } else {
        printf("%-5d: I am parent, child pid=%d\n", getpid(), pid);
    }
    printf("%-5d: finished\n", getpid());
}
