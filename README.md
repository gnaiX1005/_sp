# 課程：系統程式 -- 筆記、習題與報告

欄位 | 內容
-----|--------
學期 | 114 學年下學期
學生 |  張鈞翔
學號末兩碼 | 52
教師 | [陳鍾誠](https://www.nqu.edu.tw/educsie/index.php?act=blog&code=list&ids=4)
學校科系 | [金門大學資訊工程系](https://www.nqu.edu.tw/educsie/index.php)
課程教材 | https://github.com/ccc114b/cpu2os

## 使用聲明

> **AI 使用**：本作業使用 Claude Code 輔助開發與撰寫。
>
> **參考來源**：部分程式參考自課程教材 [ccc114b/cpu2os](https://github.com/ccc114b/cpu2os) 與教師提供的範例程式碼，經理解後自行修改與擴充。
>
> **原創聲明**：除上述註明外，其餘均為本人原創。

## 平時作業彙總

| 作業 | 主題 | 說明 |
|------|------|------|
| [HW1](HW1/) | C Compiler + Quadruple VM | 用 C 實作詞法/語法分析器，產生四元組，並以堆疊式 VM 執行。支援變數、運算、while 迴圈、函式呼叫。 |
| [HW2](HW2/) | EasyLang 直譯器 | 用 Python 實作完整直譯器 (lexer + parser + interpreter)，支援 int/float/string/bool/array 型別、內建函式、遞迴與 closures。 |
| [HW3](HW3/) | EasyLang3 擴充直譯器 | 擴充 HW2，加入 class/object、for-in、range、複合賦值 (+= 等)、++/--、檔案 I/O。 |
| [HW4](HW4/) | 系統程式教材（10 章） | 編寫教材涵蓋：lexer、parser、interpreter、VM、OS、RISC-V 組合語言、網路程式、AI 輔助開發。 |
| [HW5](HW5/) | Thread / Race Condition / Mutex / Deadlock | 用 C (pthread) 實作 race condition 範例、mutex 保護、producer-consumer、dining philosophers。 |
| [HW6](HW6/) | Process & File System Calls | 用 C 實作 fork、exec、pipe、dup2、file I/O 等系統呼叫範例。 |
| [期中作業](期中作業/) | Mini Telnet Server | 用 C 實作 telnet 伺服器，支援多連線、PTY、select 多工、SIGCHLD 處理。 |
