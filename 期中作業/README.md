# 期中作業：mini telnet

## 專案說明

本專案實作一個精簡的 Telnet 伺服器（telnetd），支援多人同時連線。

當客戶端（如 PuTTY、telnet 指令）連線時，伺服器會為每個連線建立一個 pseudo-terminal (PTY) 並啟動 shell，讓使用者可以遠端執行命令。

## 使用方式

### 編譯

```bash
make
```

### 執行

```bash
./telnetd [port]
```

預設 port 為 2323（避免需要 root 權限的 23）。

### 連線

```bash
telnet localhost 2323
```

## 系統程式概念

本專案涵蓋以下系統程式主題：

| 概念 | 使用方式 |
|------|----------|
| **socket** | `socket()`, `bind()`, `listen()`, `accept()` — TCP 伺服器 |
| **fork** | 每個連線 fork 子行程處理，同時服務多人 |
| **exec** | `execlp()` 啟動 shell |
| **pipe/pty** | `openpty()` 建立虛擬終端機，連接 shell 與網路 |
| **dup2** | 將 PTY slave 重導向至 stdin/stdout/stderr |
| **signal** | `SIGCHLD` 處理子行程結束 |
| **select** | I/O 多工，同時監控 socket 與 PTY |
| **file descriptor** | `read()`, `write()`, `close()` 操作 fd |
| **telnet protocol** | IAC 協商（WILL/WONT/DO/DONT） |

## 架構

```
Client 1 ──┐
            ├── socket ──→ [fork] ──→ PTY ──→ /bin/sh
Client 2 ──┘                          ↑
                                  [select 雙向轉送]
```

## 使用 AI 聲明

本作業使用 AI（Claude Code）協助生成程式碼。貢獻說明：
- AI 產生初始架構與程式邏輯
- 人工調整編譯選項、測試連線功能
- 所有程式碼皆有理解與手動修改

## 參考資料

- [ccc114b/cpu2os](https://github.com/ccc114b/cpu2os)
- [ccckmit/course0 - 系統程式](https://github.com/ccckmit/course0/tree/main/code/%E7%B3%BB%E7%B5%B1%E7%A8%8B%E5%BC%8F)
- [RFC 854 - Telnet Protocol Specification](https://tools.ietf.org/html/rfc854)
