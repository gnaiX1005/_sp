# EasyLang3

使用 AI (OpenCode + BigPickle) 從 EasyLang 延伸擴充的教學用程式語言直譯器。

## 語言特性

- **動態型別**：直譯器自動判定型別
- **強型態**：型態在執行前確定
- **直譯器**：遞迴下降剖析 + 樹狀走訪直譯
- **支援函式**：自訂函式、遞迴、多參數、回傳值
- **陣列**：動態陣列，支援索引存取、巢狀結構
- **類別導向**：class / new / self，支援方法與屬性
- **檔案 I/O**：檔案讀寫操作

## 資料型態

| 型態 | 說明 | 範例 |
|------|------|------|
| int | 整數 | `42`, `-5` |
| float | 浮點數 | `3.14`, `-0.5` |
| string | 字串 | `"Hello"` |
| bool | 布林值 | `true`, `false` |
| array | 陣列 | `[1, 2, 3]` |
| range | 範圍 | `0..10` |
| object | 物件 | `new Point(3, 4)` |
| null | 空值 | `null` |

## 運算子

### 算術
| 運算子 | 說明 | 範例 |
|--------|------|------|
| `+` | 加法 / 字串串接 | `a + b` |
| `-` | 減法 | `a - b` |
| `*` | 乘法 | `a * b` |
| `/` | 除法（整數除回傳整數） | `a / b` |
| `%` | 取餘數 | `a % b` |

### 比較
| 運算子 | 範例 |
|--------|------|
| `==` `!=` | `a == b` |
| `<` `>` `<=` `>=` | `a < b` |

### 邏輯
| 運算子 | 範例 |
|--------|------|
| `and` | `a and b` |
| `or` | `a or b` |
| `not` | `not a` |

### 賦值
| 運算子 | 範例 | 等價於 |
|--------|------|--------|
| `=` | `x = 10` | — |
| `+=` | `x += 5` | `x = x + 5` |
| `-=` | `x -= 5` | `x = x - 5` |
| `*=` | `x *= 5` | `x = x * 5` |
| `/=` | `x /= 5` | `x = x / 5` |
| `%=` | `x %= 5` | `x = x % 5` |

### 遞增/遞減
| 運算子 | 範例 |
|--------|------|
| `++`（後置） | `i++` |
| `--`（後置） | `i--` |

### 其他
| 運算子 | 說明 | 範例 |
|--------|------|------|
| `..` | 範圍 | `0..10` |
| `.` | 屬性/方法存取 | `obj.x` `obj.method()` |
| `[]` | 陣列索引 | `arr[0]` |
| `()` | 函式/方法呼叫 | `foo()` |

## 流程控制

### if / else
```
if (x > 0) {
    print("positive");
} else {
    print("non-positive");
}
```

### while
```
i = 0;
while (i < 10) {
    print(i);
    i = i + 1;
}
```

### for (C-style)
```
for (i = 0; i < 10; i++) {
    print(i);
}
```

### for-in（迭代範圍或陣列）
```
for i in 0..10 {
    print(i);
}

arr = [10, 20, 30];
for val in arr {
    print(val);
}
```

## 函式

```
func add(a, b) {
    return a + b;
}

func factorial(n) {
    if (n <= 1) {
        return 1;
    }
    return n * factorial(n - 1);
}

print(add(3, 4));
print("5! =", factorial(5));
```

## 陣列

```
arr = [1, 2, 3, 4, 5];
print(arr[0]);      // 1
arr[0] = 99;
push(arr, 6);       // [1,2,3,4,5,6]
val = pop(arr);     // val = 6
print(len(arr));    // 5
```

## 類別

```
class Point {
    func init(x, y) {
        self.x = x;
        self.y = y;
    }
    func show() {
        print(self.x, self.y);
    }
    func distance(other) {
        dx = self.x - other.x;
        dy = self.y - other.y;
        return sqrt(dx * dx + dy * dy);
    }
}

p1 = new Point(0, 0);
p2 = new Point(3, 4);
p1.show();
print(p1.distance(p2));   // 5.0
```

## 內建函式

### 基本 I/O
| 函式 | 說明 | 範例 |
|------|------|------|
| `print(...)` | 輸出訊息 | `print("Hello", x)` |
| `input(prompt)` | 取得使用者輸入 | `name = input("Name: ")` |

### 型態轉換
| 函式 | 說明 | 範例 |
|------|------|------|
| `int(x)` | 轉整數 | `int("42")` → `42` |
| `float(x)` | 轉浮點數 | `float("3.14")` → `3.14` |
| `str(x)` | 轉字串 | `str(42)` → `"42"` |

### 數學
| 函式 | 說明 | 範例 |
|------|------|------|
| `abs(x)` | 絕對值 | `abs(-5)` → `5` |
| `sqrt(x)` | 平方根 | `sqrt(9)` → `3` |
| `floor(x)` | 無條件捨去 | `floor(3.9)` → `3` |
| `ceil(x)` | 無條件進位 | `ceil(3.1)` → `4` |
| `random()` | 隨機整數 | `random()` |

### 陣列操作
| 函式 | 說明 | 範例 |
|------|------|------|
| `len(arr)` | 取得長度 | `len([1,2,3])` → `3` |
| `push(arr, val)` | 加入元素 | `push(arr, 4)` |
| `pop(arr)` | 移除最後元素 | `pop(arr)` → `4` |

### 字串處理
| 函式 | 說明 | 範例 |
|------|------|------|
| `split(s, sep)` | 分割字串 | `split("a,b", ",")` → `["a","b"]` |
| `join(arr, sep)` | 合併陣列 | `join(["a","b"], ",")` → `"a,b"` |

### 檔案 I/O
| 函式 | 說明 | 範例 |
|------|------|------|
| `fopen(path, mode)` | 開啟檔案 | `fh = fopen("test.txt", "r")` |
| `fgets(fh)` | 讀取一行（EOF 回傳 null） | `line = fgets(fh)` |
| `fputs(fh, str)` | 寫入字串 | `fputs(fh, "Hello")` |
| `fclose(fh)` | 關閉檔案 | `fclose(fh)` |

### 其他
| 函式 | 說明 | 範例 |
|------|------|------|
| `exit(code)` | 結束程式 | `exit(0)` |
| `time()` | 目前時間戳（秒） | `time()` |
| `range(start, end)` | 建立範圍 | `range(1, 11)` |

## 註解

```
// 單行註解
/* 多行
   註解 */
```

## 執行方式

```bash
python3 interpreter.py program.easy
```

## 範例程式

所有範例位於 `examples/` 目錄：

| 檔案 | 說明 |
|------|------|
| `range.easy` | for-in 與範圍運算子 |
| `compound.easy` | 複合賦值與遞增減 |
| `class.easy` | 類別系統（Point, Counter, BankAccount） |
| `file.easy` | 檔案 I/O、字串 split/join |
