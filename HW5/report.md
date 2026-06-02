# 作業五實作說明

## 1. bank_race.c — 銀行存提款（無互斥鎖）

模擬銀行帳戶的存款與提款操作，分別由兩個執行緒執行 100,000 次。

由於 `balance = balance + 1` 和 `balance = balance - 1` 並非原子操作（在底層分為 LOAD、運算、STORE 三個步驟），兩個執行緒交錯執行會導致競爭情況（race condition），最終餘額不為 0。

**編譯與執行：**
```bash
gcc bank_race.c -lpthread -o bank_race
./bank_race
```

## 2. bank.c — 銀行存提款（使用 mutex）

與 bank_race.c 相同邏輯，但使用 `pthread_mutex_lock/unlock` 保護臨界區段（critical section），確保同一時間只有一個執行緒能修改餘額，因此最終餘額永遠正確為 0。

**編譯與執行：**
```bash
gcc bank.c -lpthread -o bank
./bank
```

## 3. producer_consumer.c — 生產者消費者問題

- 使用一個大小為 10 的環形緩衝區（circular buffer）
- 生產者（producer）產生隨機資料放入緩衝區
- 消費者（consumer）從緩衝區取出資料
- 使用 mutex 保護緩衝區的存取
- 使用 condition variable（`cond_full`, `cond_empty`）處理緩衝區滿/空的情況：
  - 緩衝區滿時，生產者等待 `cond_empty` 訊號
  - 緩衝區空時，消費者等待 `cond_full` 訊號

**編譯與執行：**
```bash
gcc producer_consumer.c -lpthread -o producer_consumer
./producer_consumer
```

## 4. dining_philosophers.c — 哲學家用餐問題

五位哲學家，每位需要兩根筷子才能吃飯。使用 mutex 保護狀態檢查，並用 condition variable 避免 busy waiting。

- 每個哲學家有三種狀態：THINKING、HUNGRY、EATING
- `test()` 函數檢查左右鄰居是否在用餐，若無則允許當前哲學家吃飯
- 吃完後通知左右鄰居，讓他們有機會吃飯
- 使用 condition variable 避免哲學家不斷輪詢檢查狀態

此實作避免了死結（deadlock），因為一次只允許一位哲學家修改狀態，且只有在兩位鄰居都沒在吃飯時才會開始用餐。

**編譯與執行：**
```bash
gcc dining_philosophers.c -lpthread -o dining_philosophers
./dining_philosophers
```
