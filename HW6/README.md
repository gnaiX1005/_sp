# 行程與檔案相關系統呼叫說明

## fork() — 建立新行程

`fork()` 會複製當前行程，產生一個子行程。子行程從 fork 回傳處繼續執行。

- 父行程收到子行程的 PID（>0）
- 子行程收到 0
- 失敗時回傳 -1

## execvp() — 執行程式

`execvp()` 將當前行程置換為指定的程式。成功時不回傳，失敗時回傳 -1。

```c
char *arg[] = {"ls", "-l", NULL};
execvp(arg[0], arg);
```

## pipe() — 建立管道

`pipe(fd)` 建立一對檔案描述子：`fd[0]` 用於讀取，`fd[1]` 用於寫入。常用於父子行程間通訊（IPC）。

## dup2() — 複製檔案描述子

`dup2(oldfd, newfd)` 將 `newfd` 關閉後複製 `oldfd`，使 `newfd` 指向與 `oldfd` 相同的檔案。

常用來重新導向 stdin（0）、stdout（1）、stderr（2）。

## open/read/write/close — 檔案操作

- `open()`：開啟檔案，回傳檔案描述子（整數）
- `read()`：從檔案描述子讀取資料
- `write()`：將資料寫入檔案描述子
- `close()`：關閉檔案描述子

## stdin / stdout / stderr

- `stdin` (0)：標準輸入，預設為鍵盤
- `stdout` (1)：標準輸出，預設為螢幕
- `stderr` (2)：標準錯誤，預設為螢幕

這三者都是檔案描述子，可以被重新導向。
