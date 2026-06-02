#include <stdio.h>
#include <pthread.h>

#define LOOPS 100000

int balance = 0;

void *deposit(void *arg)
{
    for (int i = 0; i < LOOPS; i++)
        balance = balance + 1;
    return NULL;
}

void *withdraw(void *arg)
{
    for (int i = 0; i < LOOPS; i++)
        balance = balance - 1;
    return NULL;
}

int main()
{
    pthread_t t1, t2;

    pthread_create(&t1, NULL, deposit, NULL);
    pthread_create(&t2, NULL, withdraw, NULL);

    pthread_join(t1, NULL);
    pthread_join(t2, NULL);

    printf("Final balance: %d (expected: 0, but race condition causes error)\n", balance);

    return 0;
}
