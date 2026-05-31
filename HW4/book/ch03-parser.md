# 第三章：語法分析 (Parser)

## 3.1 什麼是語法分析

語法分析（Parsing）是編譯器/直譯器的第二個階段。它將詞法分析產生的 Token 序列，依照語法規則轉換為抽象語法樹（Abstract Syntax Tree, AST）。

## 3.2 抽象語法樹 (AST)

AST 是一種樹狀資料結構，用來表示程式碼的語法結構。每個節點代表一個語法結構，子節點代表其組成部分。

例如，`a + b * 3` 的 AST：

```
     binop(+)
     /     \
  id(a)   binop(*)
          /     \
       id(b)   lit(3)
```

### AST 節點設計

```python
# 字面值：整數、浮點數、字串
{'type': 'lit', 'value': 42}

# 變數
{'type': 'id', 'name': 'x'}

# 二元運算
{'type': 'binop', 'op': '+', 'left': ..., 'right': ...}

# 賦值
{'type': 'assign', 'target': ..., 'value': ...}

# 函式呼叫
{'type': 'call', 'func': ..., 'args': [...]}

# if 陳述
{'type': 'if', 'cond': ..., 'then': [...], 'else': [...]}

# while 迴圈
{'type': 'while', 'cond': ..., 'body': [...]}

# 函式定義
{'type': 'func_def', 'name': 'foo', 'params': [...], 'body': [...]}
```

## 3.3 遞迴下降剖析法

遞迴下降剖析（Recursive Descent Parsing）是最直觀的手寫剖析方法。它為每個語法規則撰寫對應的函式，函式之間可以互相遞迴呼叫。

### 語法規則範例

```
expression  ::= term { ("+" | "-") term }
term        ::= factor { ("*" | "/") factor }
factor      ::= integer | "(" expression ")"
```

### 對應的剖析函式

```python
def parse_expression(self):
    left = self.parse_term()           # 左運算元
    while self.peek().type in ('PLUS', 'MINUS'):
        op = self.advance().value
        right = self.parse_term()      # 右運算元
        left = {'type': 'binop', 'op': op, 'left': left, 'right': right}
    return left

def parse_term(self):
    left = self.parse_factor()
    while self.peek().type in ('STAR', 'SLASH'):
        op = self.advance().value
        right = self.parse_factor()
        left = {'type': 'binop', 'op': op, 'left': left, 'right': right}
    return left

def parse_factor(self):
    if self.peek().type == 'INT':
        t = self.advance()
        return {'type': 'lit', 'value': t.value}
    elif self.peek().type == 'LPAREN':
        self.advance()
        e = self.parse_expression()
        self.expect('RPAREN')
        return e
```

## 3.4 運算子優先順序

運算子優先順序（Operator Precedence）決定了表達式的解析方式。在遞迴下降剖析中，優先順序透過剖析函式的層級來實作：

```
parse_expression()   # 最低優先順序
  → parse_or()
    → parse_and()
      → parse_compare()
        → parse_add()
          → parse_term()
            → parse_unary()
              → parse_primary()    # 最高優先順序
```

| 層級 | 運算子 | 結合性 |
|------|--------|--------|
| primary | 字面值、變數、括號 | — |
| unary | `-` (負號), `not` | 右到左 |
| term | `*`, `/`, `%` | 左到右 |
| add | `+`, `-` | 左到右 |
| compare | `==`, `!=`, `<`, `>`, `<=`, `>=` | 左到右 |
| and | `and` | 左到右 |
| or | `or` | 左到右 |

## 3.5 處理各類陳述

### if 陳述

```python
def parse_if(self):
    self.advance()                    # 消耗 'if'
    self.expect('LPAREN')
    cond = self.parse_expression()    # 條件式
    self.expect('RPAREN')
    then = self.parse_block()         # if 區塊
    else_b = None
    if self.peek().type == 'ELSE':
        self.advance()
        else_b = self.parse_block()   # else 區塊
    return {'type': 'if', 'cond': cond, 'then': then, 'else': else_b}
```

### while 迴圈

```python
def parse_while(self):
    self.advance()
    self.expect('LPAREN')
    cond = self.parse_expression()
    self.expect('RPAREN')
    body = self.parse_block()
    return {'type': 'while', 'cond': cond, 'body': body}
```

### for 迴圈

```python
def parse_for(self):
    self.advance()
    if self.peek().type == 'ID' and self.tokens[self.pos + 1].type == 'IN':
        # for i in expr { ... }
        var_name = self.expect('ID').value
        self.expect('IN')
        iterable = self.parse_expression()
        body = self.parse_block()
        return {'type': 'for_in', 'var': var_name, 'iterable': iterable, 'body': body}
    else:
        # for (init; cond; update) { ... }
        self.expect('LPAREN')
        init = self.parse_expression() if self.peek().type != 'SEMI' else None
        self.expect('SEMI')
        cond = self.parse_expression() if self.peek().type != 'SEMI' else None
        self.expect('SEMI')
        update = self.parse_expression() if self.peek().type != 'RPAREN' else None
        self.expect('RPAREN')
        body = self.parse_block()
        return {'type': 'for', 'init': init, 'cond': cond, 'update': update, 'body': body}
```

## 3.6 後綴運算子鏈

現代的程式語言有許多後綴運算子：函式呼叫 `()`、陣列索引 `[]`、屬性存取 `.`、遞增 `++` 等。在剖析主運算式後，需要一個迴圈來處理這些後綴運算子。

```python
def parse_primary(self):
    # ... 解析主運算式（變數、字面值、括號等）

    # 後綴運算子鏈
    while True:
        t = self.peek()
        if t.type == 'LPAREN':
            # 函式呼叫
            self.advance()
            args = self.parse_arguments()
            left = {'type': 'call', 'func': left, 'args': args}
        elif t.type == 'LBRACKET':
            # 陣列索引
            self.advance()
            idx = self.parse_expression()
            self.expect('RBRACKET')
            left = {'type': 'index', 'obj': left, 'index': idx}
        elif t.type == 'DOT':
            # 屬性/方法存取
            self.advance()
            name = self.expect('ID').value
            left = {'type': 'attr', 'obj': left, 'name': name}
        elif t.type in ('INCREMENT', 'DECREMENT'):
            # 後綴遞增/遞減
            op = self.advance().type
            # ...
        else:
            break
    return left
```

## 練習題

1. 請加入三元運算子 `? :` 的支援
2. 請實作 `switch` / `case` 陳述
3. 請處理運算子的結合性（左結合 vs 右結合）

## 本章重點

- 語法分析將 Token 序列轉換為 AST
- 遞迴下降剖析是最直觀的手寫剖析方法
- 運算子優先順序透過剖析函式的層級來實作
- 後綴運算子需要在剖析主運算式後用迴圈處理
- 良好的 AST 設計對後續的直譯或編譯至關重要
