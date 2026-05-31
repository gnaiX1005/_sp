# 第四章：直譯器實作

## 4.1 樹狀走訪直譯

樹狀走訪直譯（Tree-Walking Interpreter）是最直接的直譯方式：直接走訪 AST 的每個節點，在走訪的過程中執行對應的動作。

### 直譯器基本架構

```python
class Interpreter:
    def __init__(self):
        self.global_scope = {}
        self.functions = {}

    def eval(self, node, scope):
        if node is None:
            return None
        ntype = node['type']
        if ntype == 'lit':
            return node['value']
        elif ntype == 'id':
            return scope[node['name']]
        elif ntype == 'binop':
            left = self.eval(node['left'], scope)
            right = self.eval(node['right'], scope)
            if node['op'] == '+': return left + right
            if node['op'] == '-': return left - right
            if node['op'] == '*': return left * right
            if node['op'] == '/': return left / right
        elif ntype == 'call':
            func = self.functions[node['name']]
            args = [self.eval(a, scope) for a in node['args']]
            # 建立新作用域並執行函式
            ...
```

## 4.2 環境與作用域

作用域（Scope）決定了變數的可見範圍。最簡單的作用域實作方式是使用 Python 的 dict。

### 作用域鏈

```python
# 全域作用域
global_scope = {}

# 函式呼叫時建立新的區域作用域
def call_function(func, args):
    # 新作用域繼承全域變數
    new_scope = dict(global_scope)
    # 設定參數
    for i, param in enumerate(func['params']):
        new_scope[param] = args[i]
    # 在新作用域中執行
    prev = current_scope
    current_scope = new_scope
    result = execute_function_body(func)
    current_scope = prev
    return result
```

## 4.3 函式呼叫與遞迴

函式呼叫是直譯器中最複雜的部分之一。需要處理：

1. **參數傳遞**：將實際參數對應到形式參數
2. **作用域切換**：建立新的區域作用域
3. **回傳值**：處理 `return` 陳述
4. **遞迴支援**：確保每次呼叫都有獨立的作用域

### AST 節點表示

函式定義的 AST 節點：

```python
{
    'type': 'func_def',
    'name': 'factorial',
    'params': ['n'],
    'body': [
        {'type': 'if', 'cond': ..., 'then': [...], 'else': [...]},
        {'type': 'return', 'value': ...}
    ]
}
```

函式呼叫的 AST 節點：

```python
{
    'type': 'call',
    'func': {'type': 'id', 'name': 'factorial'},
    'args': [{'type': 'lit', 'value': 5}]
}
```

### 執行函式

```python
def execute_function(self, func, args):
    # 建立新作用域
    new_scope = dict(self.global_scope)
    # 綁定參數
    for i, p in enumerate(func['params']):
        new_scope[p] = args[i] if i < len(args) else None
    # 切換作用域
    prev_scope = self.global_scope
    self.global_scope = new_scope
    # 依序執行函式主體
    result = None
    for stmt in func['body']:
        result = self.execute(stmt)
        if isinstance(result, dict) and result.get('type') == 'return':
            result = result['value']
            break
    # 恢復作用域
    self.global_scope = prev_scope
    return result
```

## 4.4 流程控制

### if 陳述

```python
def execute_if(self, stmt):
    if self.is_truthy(self.eval(stmt['cond'], self.global_scope)):
        for s in stmt['then']:
            r = self.execute(s)
            if r and r['type'] in ('return', 'break', 'continue'):
                return r
    elif stmt['else']:
        for s in stmt['else']:
            r = self.execute(s)
            if r and r['type'] in ('return', 'break', 'continue'):
                return r
```

### while 迴圈

```python
def execute_while(self, stmt):
    while self.is_truthy(self.eval(stmt['cond'], self.global_scope)):
        for s in stmt['body']:
            r = self.execute(s)
            if isinstance(r, dict):
                if r['type'] == 'return': return r
                if r['type'] == 'break': break
                if r['type'] == 'continue': continue
```

## 4.5 內建函式

內建函式（Built-in Functions）是直譯器直接提供的功能，使用者不需要自行定義即可使用。

### 註冊內建函式

```python
class Interpreter:
    def __init__(self):
        self.builtins = {
            'print': self.builtin_print,
            'len': self.builtin_len,
            'push': self.builtin_push,
            'pop': self.builtin_pop,
        }

    def builtin_print(self, *args):
        print(*args)

    def builtin_len(self, arr):
        return len(arr)

    def builtin_push(self, arr, val):
        arr.append(val)

    def builtin_pop(self, arr):
        return arr.pop()
```

### 查詢順序

當直譯器看到一個函式呼叫時，需要依序查詢：

1. **區域/全域變數**：是否為使用者定義的變數
2. **使用者定義函式**：是否為自訂函式
3. **內建函式**：是否為直譯器提供的內建功能

```python
def resolve_name(self, name, scope):
    if name in scope:
        return scope[name]          # 變數
    if name in self.functions:
        return self.functions[name]  # 使用者函式
    if name in self.builtins:
        return self.builtins[name]   # 內建函式
    raise NameError(f"Undefined: {name}")
```

## 4.6 錯誤處理與除錯

### 語法錯誤

語法錯誤發生在詞法分析或語法分析階段，表示程式碼不符合語法規則。

```python
raise SyntaxError(f"Unexpected token {t.type} at {t.line}:{t.col}")
```

### 執行期錯誤

執行期錯誤發生在程式執行階段，例如參考未定義的變數、型態錯誤等。

```python
raise NameError(f"Undefined variable: {name}")
raise RuntimeError(f"Type error: cannot add {type(x)} and {type(y)}")
```

### 取得有意義的錯誤訊息

良好的錯誤訊息應包含：

- 錯誤類型（語法錯誤、名稱錯誤、型態錯誤）
- 錯誤位置（行號、列號）
- 錯誤說明（什麼地方出了問題）
- 建議修正方式

## 練習題

1. 請為直譯器加入除錯模式（顯示每個 AST 節點的執行過程）
2. 請實作 `try` / `catch` 例外處理
3. 請加入斷言 `assert` 陳述

## 本章重點

- 樹狀走訪直譯是最直觀的直譯方式
- 作用域使用 dict 實作，函式呼叫時建立新作用域
- 函式呼叫需要處理參數傳遞、作用域切換和回傳值
- 遞迴依靠每次呼叫建立獨立作用域來支援
- 內建函式提供語言的核心功能
- 良好的錯誤訊息對開發者體驗至關重要
