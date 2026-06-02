# 作業六實作說明

## 1. fork_basic.c — fork 基本範例

展示 `fork()` 如何分裂父子行程。父行程印出子行程 PID，子行程印出自己的 PID 與父行程 PID。

```bash
gcc fork_basic.c -o fork_basic
./fork_basic
```

## 2. fork_exec.c — fork + execvp

父行程 fork 子行程，子行程用 `execvp()` 執行 `ls -l`，父行程用 `wait()` 等待子行程結束。

```bash
gcc fork_exec.c -o fork_exec
./fork_exec
```

## 3. pipe_dup2.c — 管道 + dup2 實作 ls | wc -l

父子行程間建立管道，子行程將 stdout 透過 `dup2` 導向管道的寫入端（執行 `ls -l`），父行程將 stdin 導向管道的讀取端（執行 `wc -l`），實作類似 shell 的 pipe 功能。

```bash
gcc pipe_dup2.c -o pipe_dup2
./pipe_dup2
```

## 4. file_io.c — open/read/write/close

用低階系統呼叫讀取 `a.txt` 並寫入 `b.txt`，展示 `open`、`read`、`write`、`close` 的使用方式。

```bash
echo "Hello system programming!" > a.txt
gcc file_io.c -o file_io
./file_io
cat b.txt
```

## 5. redirect.c — dup2 重新導向 stdin/stdout

關閉 stdin（0）與 stdout（1），再 open 檔案，此時新開啟的檔案會自動佔用最小的可用描述子（0 和 1），實現輸入輸出重新導向。

```bash
echo "Redirect test" > a.txt
gcc redirect.c -o redirect
./redirect
cat b.txt
```
