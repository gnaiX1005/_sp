# 第二章：詞法分析 (Lexer)

## 2.1 什麼是詞法分析

詞法分析（Lexical Analysis）是編譯器或直譯器的第一個階段。它的任務是將原始碼的字串串流，轉換為一系列具有意義的記號（Token）。

舉例來說，對於以下原始碼：

```c
sum = a + 10;
```

詞法分析器會產生以下的 Token 序列：

```
ID("sum")   ASSIGN   ID("a")   PLUS   INT(10)   SEMI
```

## 2.2 Token 的設計

在實作詞法分析器之前，我們需要先定義 Token 的資料結構。每個 Token 至少需要包含：

- **類型（Type）**：記號的種類（如 INT、PLUS、ID）
- **值（Value）**：記號的實際內容（如變數名稱、數字值）
- **位置（Position）**：原始碼中的行號與列號（用於錯誤報告）

```python
class Token:
    def __init__(self, type, value, line, col):
        self.type = type
        self.value = value
        self.line = line
        self.col = col
```

常見的 Token 類型包含：

| 類別 | Token 類型 | 範例 |
|------|-----------|------|
| 識別字 | ID | `x`, `sum`, `factorial` |
| 整數 | INT | `42`, `0`, `-5` |
| 浮點數 | FLOAT | `3.14`, `-0.5` |
| 字串 | STRING | `"hello"` |
| 運算子 | PLUS, MINUS, STAR, SLASH | `+`, `-`, `*`, `/` |
| 比較 | EQ, NE, LT, GT, LE, GE | `==`, `!=`, `<`, `>` |
| 括號 | LPAREN, RPAREN, LBRACE, RBRACE | `(`, `)`, `{`, `}` |
| 關鍵字 | IF, ELSE, WHILE, FOR, RETURN | `if`, `else`, `while` |
| 特殊 | EOF | 檔案結束 |

## 2.3 實作詞法分析器

### 基本架構

詞法分析器通常以狀態機的方式實作。它從原始碼的第一個字元開始，依據當前的字元決定下一步動作。

```python
class Lexer:
    def __init__(self, text):
        self.text = text      # 原始碼
        self.pos = 0          # 目前位置
        self.line = 1         # 目前行號
        self.col = 1          # 目前列號
        self.tokens = []      # 產生的 Token 列表
```

### 讀取數字

當遇到數字字元時，我們需要連續讀取直到非數字字元，以獲得完整的數字。

```python
def read_number(self):
    num_str = ''
    has_dot = False
    while self.pos < len(self.text) and \
          (self.text[self.pos].isdigit() or self.text[self.pos] == '.'):
        if self.text[self.pos] == '.':
            if has_dot:
                break        # 避免 3.14.15 這種情況
            # 檢查是否為範圍運算子 '..'
            if self.pos + 1 < len(self.text) and \
               self.text[self.pos + 1] == '.':
                break
            has_dot = True
        num_str += self.text[self.pos]
        self.advance()
    if has_dot:
        return Token('FLOAT', float(num_str), self.line, start_col)
    return Token('INT', int(num_str), self.line, start_col)
```

### 讀取識別字與關鍵字

識別字以字母或底線開頭，後續可包含字母、數字和底線。

```python
def read_id(self):
    s = ''
    while self.pos < len(self.text) and \
          (self.text[self.pos].isalnum() or self.text[self.pos] == '_'):
        s += self.text[self.pos]
        self.advance()
    if s in self.keywords:
        return Token(s.upper(), s, self.line, start_col)
    return Token('ID', s, self.line, start_col)
```

### 多字元運算子

某些運算子由兩個字元組成（如 `==`, `!=`, `<=`, `>=`, `+=`, `..`），需要在讀取第一個字元後檢查下一個字元。

```python
elif ch == '+':
    self.advance()
    if self.peek() == '=':
        self.advance()
        self.tokens.append(Token('PLUSEQ', '+=', ...))
    elif self.peek() == '+':
        self.advance()
        self.tokens.append(Token('INCREMENT', '++', ...))
    else:
        self.tokens.append(Token('PLUS', '+', ...))
```

## 2.4 完整詞法分析流程

```python
def tokenize(self):
    while self.pos < len(self.text):
        # 跳過空白字元
        self.skip_whitespace()
        if self.pos >= len(self.text):
            break
        # 跳過註解
        if self.text[self.pos] == '/' and ...:
            self.skip_comment()
            continue
        ch = self.text[self.pos]
        if ch.isdigit():
            self.tokens.append(self.read_number())
        elif ch.isalpha() or ch == '_':
            self.tokens.append(self.read_id())
        elif ch == '+': ...   # 處理 +, +=, ++
        elif ch == '-': ...   # 處理 -, -=, --
        # ... 其他運算子
    self.tokens.append(Token('EOF', None, self.line, self.col))
    return self.tokens
```

## 2.5 處理註解

支援單行註解 `//` 和區塊註解 `/* */` 能讓語言更實用。

```python
def skip_comment(self):
    if self.peek() == '/' and self.text[self.pos + 1] == '/':
        # 單行註解：跳過直到換行
        while self.pos < len(self.text) and self.text[self.pos] != '\n':
            self.advance()
    elif self.peek() == '/' and self.text[self.pos + 1] == '*':
        # 多行註解：跳過直到 */
        self.advance(); self.advance()
        while self.pos < len(self.text):
            if self.text[self.pos] == '*' and \
               self.pos + 1 < len(self.text) and \
               self.text[self.pos + 1] == '/':
                self.advance(); self.advance()
                break
            self.advance()
```

## 練習題

1. 請為你的語言加入 `<<` 和 `>>`（位元移位）運算子
2. 請實作十六進位數字（如 `0xFF`）的支援
3. 請加入字元字面值（如 `'a'`）的支援

## 本章重點

- 詞法分析是編譯/直譯過程的第一個階段
- Token 包含類型、值和位置資訊
- 詞法分析器以狀態機方式逐字元讀取原始碼
- 需要處理多字元運算子、關鍵字、註解等特殊情況
- 正確的位置資訊對於錯誤報告非常重要
