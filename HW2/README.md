# EasyLang

一個簡單的教學用程式語言，配有直譯器。

## 語言特性

- **強型態**：型態在執行前確定
- **直譯器**：直接執行原始碼
- **虛擬機**：基於堆疊機的位元組碼執行
- **無垃圾回收**：手動記憶體管理

## 設計目標

1. 語法簡潔易懂，適合初學者
2. 支援基本資料型態與運算
3. 具備函式、條件判斷、迴圈等結構
4. 內建常用函式（print, input, len 等）

## 資料型態

| 型態 | 說明 | 範例 |
|------|------|------|
| int | 整數 | `42`, `-5` |
| float | 浮點數 | `3.14`, `-0.5` |
| string | 字串 | `"Hello"` |
| bool | 布林值 | `true`, `false` |
| array | 陣列 | `[1, 2, 3]` |
| null | 空值 | `null` |

## 運算子

- 算術：`+`, `-`, `*`, `/`, `%`
- 比較：`==`, `!=`, `<`, `>`, `<=`, `>=`
- 邏輯：`and`, `or`, `not`
- 賦值：`=`

## 內建函式

| 函式 | 說明 | 範例 |
|------|------|------|
| `print(...)` | 輸出訊息 | `print("Hello")` |
| `input(prompt)` | 取得使用者輸入 | `input("Name: ")` |
| `len(arr)` | 取得陣列長度 | `len([1,2,3])` |
| `push(arr, val)` | 加入元素 | `push(arr, 4)` |
| `pop(arr)` | 移除最後元素 | `pop(arr)` |
| `exit(code)` | 結束程式 | `exit(0)` |
| `time()` | 取得時間戳 | `time()` |
| `random()` | 取得隨機數 | `random()` |
| `int(x)` | 轉換為整數 | `int("42")` |
| `str(x)` | 轉換為字串 | `str(42)` |

## 執行方式

```bash
python interpreter.py program.easy
```

## 範例

```
func factorial(n) {
    if (n <= 1) {
        return 1;
    }
    return n * factorial(n - 1);
}

print("5! =", factorial(5));

i = 0;
while (i < 5) {
    print(i);
    i = i + 1;
}
```