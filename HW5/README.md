# Thread、Race Condition、Mutex、Deadlock 說明

## Thread（執行緒）

Thread 是程式中的一個執行流程，同一個行程（process）可以有多個執行緒同時執行，共享相同的記憶體空間。使用 pthread 函式庫可以在 C 語言中建立多執行緒。

```c
pthread_t thread1, thread2;
pthread_create(&thread1, NULL, func1, NULL);
pthread_create(&thread2, NULL, func2, NULL);
pthread_join(thread1, NULL);
pthread_join(thread2, NULL);
```

- `pthread_create()` 建立一個新執行緒
- `pthread_join()` 等待執行緒結束

## Race Condition（競爭情況）

當多個執行緒同時存取共享變數，且至少有一個執行緒在寫入時，就會發生競爭情況。由於執行緒的排程順序不確定，最終結果取決於執行緒的執行順序。

範例：`bank_race.c` 中兩個執行緒同時對同一個帳戶進行存提款，沒有使用 mutex 保護，導致最終餘額錯誤。

```c
// 沒有 mutex 保護
void *deposit() {
    for (int i = 0; i < LOOPS; i++)
        balance = balance + 1; // 非原子操作
}
void *withdraw() {
    for (int i = 0; i < LOOPS; i++)
        balance = balance - 1; // 非原子操作
}
```

`balance = balance + 1` 在底層其實是三個步驟：
1. LOAD R1, balance
2. R1 = R1 + 1
3. STORE R1, balance

若兩個執行緒同時執行，可能發生：執行緒 A 讀取 balance=100，執行緒 B 也讀取 balance=100，A 加 1 寫回 101，B 減 1 寫回 99，最後 balance=99 而非正確的 100。

## Mutex（互斥鎖）

Mutex 用來保護共享資源，確保同一時間只有一個執行緒能存取共享資料。

```c
pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;

void *deposit() {
    pthread_mutex_lock(&mutex);
    balance = balance + 1; // 受保護的臨界區段
    pthread_mutex_unlock(&mutex);
}
```

- `pthread_mutex_lock()`：取得鎖，若鎖已被其他執行緒持有則等待
- `pthread_mutex_unlock()`：釋放鎖

使用 mutex 後，`bank_mutex.c` 的執行結果永遠是正確的 balance=0。

## Deadlock（死結）

死結發生在兩個以上的執行緒互相等待對方釋放資源，導致所有執行緒都無法繼續執行。

死結形成的四個必要條件：
1. **互斥（Mutual Exclusion）**：資源一次只能被一個執行緒使用
2. **持有並等待（Hold and Wait）**：執行緒持有資源的同時等待其他資源
3. **不可搶佔（No Preemption）**：資源不能被強制從執行緒中取走
4. **循環等待（Circular Wait）**：存在一組執行緒形成循環等待鏈

### 死結範例

執行緒 A 持有鎖 X 並等待鎖 Y，同時執行緒 B 持有鎖 Y 並等待鎖 X。

```
執行緒 A: lock(X) → lock(Y) → unlock(Y) → unlock(X)
執行緒 B: lock(Y) → lock(X) → unlock(X) → unlock(Y)
```

### 避免死結

固定鎖的取得順序，所有執行緒都先鎖 X 再鎖 Y，就不會產生循環等待。

```
執行緒 A: lock(X) → lock(Y) → unlock(Y) → unlock(X)
執行緒 B: lock(X) → lock(Y) → unlock(Y) → unlock(X)
```
