#include <stdio.h>
#include <pthread.h>

#define LOOPS 100000

pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;
int balance = 0;

void *deposit(void *arg)
{
    for (int i = 0; i < LOOPS; i++) {
        pthread_mutex_lock(&mutex);
        balance = balance + 1;
        pthread_mutex_unlock(&mutex);
    }
    return NULL;
}

void *withdraw(void *arg)
{
    for (int i = 0; i < LOOPS; i++) {
        pthread_mutex_lock(&mutex);
        balance = balance - 1;
        pthread_mutex_unlock(&mutex);
    }
    return NULL;
}

int main()
{
    pthread_t t1, t2;

    pthread_create(&t1, NULL, deposit, NULL);
    pthread_create(&t2, NULL, withdraw, NULL);

    pthread_join(t1, NULL);
    pthread_join(t2, NULL);

    printf("Final balance: %d (expected: 0)\n", balance);

    return 0;
}
