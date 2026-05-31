# 第七章：作業系統概論

## 7.1 什麼是作業系統

作業系統（Operating System, OS）是管理電腦硬體與軟體資源的系統程式。它提供了使用者與硬體之間的抽象層，讓應用程式開發者不需要直接操作硬體。

作業系統的核心功能包含：

- **行程管理**：建立、排程、終止行程
- **記憶體管理**：分配與回收記憶體
- **檔案系統**：組織與存取儲存裝置上的資料
- **裝置驅動**：管理輸入/輸出裝置
- **網路通訊**：提供網路協定堆疊
- **安全保護**：防止非法存取

## 7.2 行程與執行緒

### 行程 (Process)

行程是正在執行的程式的實例。每個行程擁有獨立的：

- 記憶體空間（程式碼、資料、堆疊）
- 暫存器狀態
- 開啟的檔案
- 行程 ID (PID)

```
行程控制區塊 (PCB)
┌─────────────────────────┐
│ 行程 ID (PID)           │
│ 程式計數器 (PC)          │
│ 暫存器狀態              │
│ 記憶體配置              │
│ 開啟的檔案列表          │
│ 行程狀態 (就緒/執行/等待)│
│ CPU 排程資訊            │
└─────────────────────────┘
```

### 行程狀態轉換

```
新增 → 就緒 → 執行 → 終止
         ↕     ↕
        等待 ← I/O 事件
```

### 執行緒 (Thread)

執行緒是行程內的輕量級執行單元。同一個行程的多個執行緒共享：

- 共享：記憶體空間、檔案描述子、程式碼
- 獨立：程式計數器、堆疊、暫存器

```c
// POSIX Threads 範例
#include <pthread.h>

void *worker(void *arg) {
    int id = *(int*)arg;
    printf("Thread %d is running\n", id);
    return NULL;
}

int main() {
    pthread_t t1, t2;
    int id1 = 1, id2 = 2;
    pthread_create(&t1, NULL, worker, &id1);
    pthread_create(&t2, NULL, worker, &id2);
    pthread_join(t1, NULL);
    pthread_join(t2, NULL);
    return 0;
}
```

## 7.3 系統呼叫

系統呼叫（System Call）是使用者程式請求作業系統服務的唯一方式。常見的系統呼叫包含：

| 分類 | 系統呼叫 | 說明 |
|------|---------|------|
| 行程控制 | `fork()` | 建立子行程 |
| 行程控制 | `exec()` | 執行程式 |
| 行程控制 | `exit()` | 終止行程 |
| 行程控制 | `wait()` | 等待子行程 |
| 檔案操作 | `open()` | 開啟檔案 |
| 檔案操作 | `read()` | 讀取檔案 |
| 檔案操作 | `write()` | 寫入檔案 |
| 檔案操作 | `close()` | 關閉檔案 |
| 記憶體 | `mmap()` | 記憶體映射 |
| 通訊 | `socket()` | 建立網路插座 |
| 通訊 | `pipe()` | 建立管線 |

### 系統呼叫流程

```
使用者程式
  ↓ open("file.txt", O_RDONLY)
C library (glibc)
  ↓ syscall(SYS_open, "file.txt", O_RDONLY)
核心模式
  ↓ vfs_open("file.txt")
  ↓ filesystem driver
  ↓ block device driver
硬體
```

## 7.4 檔案系統

檔案系統負責組織和存取儲存裝置上的資料。

### 虛擬檔案系統 (VFS)

大多數現代作業系統使用 VFS 來抽象化不同的檔案系統實作：

```c
// VFS 結構範例
struct file_operations {
    int (*open)(struct inode *inode, struct file *file);
    ssize_t (*read)(struct file *file, char *buf, size_t len);
    ssize_t (*write)(struct file *file, const char *buf, size_t len);
    int (*close)(struct inode *inode, struct file *file);
};
```

### 常見的檔案系統

| 檔案系統 | 特點 | 常見於 |
|---------|------|--------|
| ext4 | 日誌式、穩定 | Linux |
| NTFS | 日誌式、權限控制 | Windows |
| FAT32 | 簡單、相容性高 | 隨身碟 |
| ZFS | 寫入時複製、高容量 | Solaris, FreeBSD |

## 7.5 xv6 — 教學用作業系統

xv6 是 MIT 為作業系統課程設計的教學用作業系統，執行在 RISC-V 架構上。它是 UNIX v6 的現代重製版。

### xv6 的核心模組

```c
// 行程管理 (proc.c)
struct proc *alloc_proc(void) {
    struct proc *p;
    for (p = table; p < &table[NPROC]; p++)
        if (p->state == UNUSED)
            goto found;
    return 0;
found:
    p->state = USED;
    p->pid = alloc_pid();
    return p;
}

// 上下文切換 (swtch.S)
.globl swtch
swtch:
    sd ra, 0(a0)
    sd sp, 8(a0)
    // ... 儲存其他暫存器
    ld ra, 0(a1)
    ld sp, 8(a1)
    // ... 載入其他暫存器
    ret
```

### xv6 系統呼叫範例

```c
// 使用者程式
int main() {
    int fd = open("README", O_RDONLY);
    char buf[128];
    read(fd, buf, sizeof(buf));
    write(1, buf, n);   // fd=1 為 stdout
    close(fd);
    exit(0);
}
```

## 7.6 記憶體管理

### 虛擬記憶體

虛擬記憶體讓每個行程擁有獨立的位址空間，透過 MMU（Memory Management Unit）將虛擬位址轉換為實體位址。

```
虛擬位址 → [分頁表] → 實體位址

虛擬位址 (32-bit):
[頁號 (20-bit)][頁內偏移 (12-bit)]
    ↓ 分頁表
實體位址:
[頁框號 (20-bit)][頁內偏移 (12-bit)]
```

### 分頁置換

當實體記憶體不足時，作業系統會將不常用的分頁移到磁碟上（swap）：

```
最近最少使用 (LRU) 置換演算法：
1. 每個分頁有存取位元
2. 定期清除存取位元
3. 需要置換時，選擇存取位元為 0 的分頁
4. 若所有分頁都被存取過，清除所有位元重新開始
```

## 7.7 行程排程

排程器決定下一個要執行的行程：

```c
// 簡易排程器範例
struct proc *scheduler(void) {
    struct proc *p;
    for (p = table; p < &table[NPROC]; p++) {
        if (p->state == RUNNABLE) {
            p->state = RUNNING;
            return p;
        }
    }
    return NULL;
}
```

排程演算法：

| 演算法 | 原則 | 優點 | 缺點 |
|--------|------|------|------|
| FCFS | 先到先服務 | 簡單 | 平均等待時間長 |
| SJF | 最短工作優先 | 最小平均等待 | 需要預估執行時間 |
| RR | 輪詢 | 公平回應快 | 上下文切換開銷 |
| MLFQ | 多層回饋佇列 | 兼顧互動與批次 | 實作複雜 |

## 練習題

1. 請在 Linux 上使用 `strace` 觀察程式的系統呼叫
2. 請閱讀 xv6 原始碼，追蹤一次系統呼叫的完整流程
3. 請實作一個簡單的 Round-Robin 行程排程器

## 本章重點

- 作業系統管理硬體與軟體資源
- 行程是獨立的執行單元；執行緒是行程內的輕量級執行單元
- 系統呼叫是使用者程式請求核心服務的唯一方式
- VFS 抽象化不同檔案系統的實作細節
- 虛擬記憶體透過分頁表提供隔離和保護
- 行程排程決定 CPU 資源的分配方式
