#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <unistd.h>

#define BUFFER_SIZE 10

int buffer[BUFFER_SIZE];
int count = 0;
int in = 0;
int out = 0;

pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;
pthread_cond_t cond_empty = PTHREAD_COND_INITIALIZER;
pthread_cond_t cond_full = PTHREAD_COND_INITIALIZER;

void *producer(void *arg)
{
    int data;
    for (int i = 0; i < 20; i++) {
        data = rand() % 100;

        pthread_mutex_lock(&mutex);
        while (count == BUFFER_SIZE)
            pthread_cond_wait(&cond_empty, &mutex);

        buffer[in] = data;
        in = (in + 1) % BUFFER_SIZE;
        count++;
        printf("Producer: produce %d, buffer has %d items\n", data, count);

        pthread_cond_signal(&cond_full);
        pthread_mutex_unlock(&mutex);

        sleep(rand() % 3);
    }
    return NULL;
}

void *consumer(void *arg)
{
    int data;
    for (int i = 0; i < 20; i++) {
        pthread_mutex_lock(&mutex);
        while (count == 0)
            pthread_cond_wait(&cond_full, &mutex);

        data = buffer[out];
        out = (out + 1) % BUFFER_SIZE;
        count--;
        printf("Consumer: consume %d, buffer has %d items\n", data, count);

        pthread_cond_signal(&cond_empty);
        pthread_mutex_unlock(&mutex);

        sleep(rand() % 3);
    }
    return NULL;
}

int main()
{
    pthread_t producer_thread, consumer_thread;

    setbuf(stdout, NULL);
    pthread_create(&producer_thread, NULL, producer, NULL);
    pthread_create(&consumer_thread, NULL, consumer, NULL);

    pthread_join(producer_thread, NULL);
    pthread_join(consumer_thread, NULL);

    pthread_mutex_destroy(&mutex);
    pthread_cond_destroy(&cond_empty);
    pthread_cond_destroy(&cond_full);

    return 0;
}
