#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#define SMAX 128

int main() {
    close(0);
    close(1);
    int a = open("a.txt", O_RDWR);
    int b = open("b.txt", O_CREAT | O_RDWR, 0644);
    char line[SMAX];
    int n = read(0, line, SMAX);
    write(1, line, n);
    printf("a=%d, b=%d\n", a, b);
}
