# HW4 — 系統程式入門：從理論到實作

使用 AI (OpenCode + BigPickle) 撰寫的系統程式教學書。

## 書籍位置

`book/` 目錄下包含完整十章內容：

| 章節 | 主題 | 說明 |
|------|------|------|
| [第一章](book/ch01-intro.md) | 系統程式概論 | 系統程式定義、編譯器 vs 直譯器 |
| [第二章](book/ch02-lexer.md) | 詞法分析 (Lexer) | Token 設計、實作詞法分析器 |
| [第三章](book/ch03-parser.md) | 語法分析 (Parser) | AST、遞迴下降剖析、運算子優先順序 |
| [第四章](book/ch04-interpreter.md) | 直譯器實作 | 樹狀走訪直譯、作用域、函式呼叫 |
| [第五章](book/ch05-advanced.md) | 進階語言功能 | 陣列、類別、複合賦值、範圍迭代 |
| [第六章](book/ch06-vm.md) | 虛擬機與中間碼 | 堆疊機、暫存機、LLVM IR、RISC-V |
| [第七章](book/ch07-os.md) | 作業系統概論 | 行程、記憶體管理、檔案系統、xv6 |
| [第八章](book/ch08-asm.md) | 組合語言與 RISC-V | 指令集、組譯器實作 |
| [第九章](book/ch09-network.md) | 網路程式設計 | Socket、HTTP、TCP/IP |
| [第十章](book/ch10-ai.md) | AI 輔助系統程式開發 | 提示工程、實例分析 |

## 主題

本書涵蓋系統程式的主要領域，以**實作**為導向，包含大量程式碼範例與說明。內容與本課程（HW1 編譯器、HW2-3 EasyLang 直譯器）互相呼應，可作為學習系統程式的參考資料。
