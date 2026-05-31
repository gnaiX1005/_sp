# 第五章：進階語言功能

## 5.1 陣列與索引

陣列是程式語言中最基本的複合資料型態。我們可以將陣列實作為 Python 的 list。

### 陣列字面值

```python
def parse_array_lit(self):
    self.expect('LBRACKET')
    elements = []
    if self.peek().type != 'RBRACKET':
        elements.append(self.parse_expression())
        while self.peek().type == 'COMMA':
            self.advance()
            elements.append(self.parse_expression())
    self.expect('RBRACKET')
    return {'type': 'array', 'elements': elements}
```

### 陣列索引

```python
# AST 節點
{'type': 'index', 'obj': <array_expr>, 'index': <index_expr>}

# 執行
elif ntype == 'index':
    obj = self.eval(node['obj'], scope)
    idx = self.eval(node['index'], scope)
    return obj[idx]
```

### 陣列索引賦值

```python
# arr[0] = 42
{'type': 'assign', 'target': {'type': 'index', ...}, 'value': {'type': 'lit', 'value': 42}}

# 執行
elif ntype == 'assign':
    val = self.eval(node['value'], scope)
    target = node['target']
    if target['type'] == 'id':
        scope[target['name']] = val
    elif target['type'] == 'index':
        obj = self.eval(target['obj'], scope)
        idx = self.eval(target['index'], scope)
        obj[idx] = val
```

## 5.2 類別與物件

物件導向程式設計（OOP）是現代程式語言的重要特性。我們可以在直譯器中加入類別系統。

### 類別定義

```python
class Point {
    func init(x, y) {
        self.x = x;
        self.y = y;
    }
    func show() {
        print(self.x, self.y);
    }
}
```

### 類別的資料結構

```python
class ClassDef:
    def __init__(self, name, methods):
        self.name = name
        self.methods = methods  # name -> UserFunction

class Instance:
    def __init__(self, klass):
        self._class = klass
        self._data = {}         # 實例屬性
```

### 實例化 (new)

```python
def execute_new(self, node, scope):
    class_name = node['class_name']
    klass = self.classes[class_name]
    inst = Instance(klass)
    args = [self.eval(a, scope) for a in node['args']]
    if 'init' in klass.methods:
        klass.methods['init'].call_with_self(inst, args)
    return inst
```

### 方法呼叫

```python
def execute_method_call(self, obj, method_name, args):
    if isinstance(obj, Instance):
        meth = obj._class.methods[method_name]
        return meth.call_with_self(obj, args)
```

## 5.3 複合賦值運算子

複合賦值運算子（`+=`, `-=`, `*=`, `/=", `%=`）讓程式碼更簡潔。

```python
# x += 5 等同於 x = x + 5
elif self.peek().type in ('ASSIGN', 'PLUSEQ', 'MINUSEQ', ...):
    op = self.advance().type
    val = self.parse_expression()
    if op == 'ASSIGN':
        return {'type': 'assign', 'target': expr, 'value': val}
    else:
        op_map = {'PLUSEQ': '+', 'MINUSEQ': '-', ...}
        return {
            'type': 'assign',
            'target': expr,
            'value': {
                'type': 'binop',
                'op': op_map[op],
                'left': expr,      # 注意：這裡 expr 會被評估兩次
                'right': val
            }
        }
```

## 5.4 範圍與迭代

範圍運算子 `..` 可以建立一個可迭代的範圍值，支援 for-in 迴圈。

### Range 值

```python
class RangeValue:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __iter__(self):
        i = self.start
        if self.start <= self.end:
            while i < self.end:
                yield i
                i += 1
        else:
            while i > self.end:
                yield i
                i -= 1
```

### for-in 直譯

```python
elif stype == 'for_in':
    iterable = self.eval(stmt['iterable'], self.global_scope)
    for val in iterable:
        self.global_scope[stmt['var']] = val
        for s in stmt['body']:
            r = self.execute(s)
            if isinstance(r, dict):
                if r['type'] == 'return': return r
                if r['type'] == 'break': break
```

## 5.5 字串處理

字串操作是語言實用性的關鍵。我們可以提供如 `split` 和 `join` 的內建函式。

```python
def builtin_split(self, s, sep=' '):
    if isinstance(s, str):
        return s.split(sep)
    raise RuntimeError("split requires a string")

def builtin_join(self, arr, sep=' '):
    return sep.join(str(x) for x in arr)
```

## 5.6 更多內建函式

實用的內建函式能大幅提升語言的可用性：

| 類別 | 函式 | 用途 |
|------|------|------|
| I/O | `print` | 輸出 |
| I/O | `input` | 輸入 |
| 型態轉換 | `int`, `float`, `str` | 型態轉換 |
| 數學 | `abs`, `sqrt`, `floor`, `ceil` | 數學計算 |
| 陣列 | `len`, `push`, `pop` | 陣列操作 |
| 字串 | `split`, `join` | 字串處理 |
| 檔案 | `fopen`, `fgets`, `fputs`, `fclose` | 檔案 I/O |
| 其他 | `exit`, `time`, `random` | 工具函式 |

## 練習題

1. 請加入多維陣列的支援
2. 請實作類別繼承（class inheritance）
3. 請加入 `map` / `filter` / `reduce` 等高階函式

## 本章重點

- 陣列透過 Python list 實作，支援索引讀寫
- 類別系統包含 ClassDef（類別定義）和 Instance（實例）
- 方法呼叫需要將 self 綁定到實例
- 複合賦值運算子簡化常見的賦值模式
- 範圍運算子與 for-in 提供更簡潔的迭代方式
- 豐富的內建函式讓語言更實用
