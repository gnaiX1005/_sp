# EasyLang3 -- 延伸自 EasyLang

使用 AI (OpenCode + BigPickle) 從 EasyLang (HW2) 延伸擴充的教學用程式語言直譯器。

## 新增功能

### 1. 範圍運算子 (`..`) 與 for-in 迴圈

```python
for i in 0..10 {
    print(i);
}

arr = [1, 2, 3];
for x in arr {
    print(x);
}
```

### 2. 複合賦值運算子

```python
x = 10;
x += 5;     // x = 15
x -= 3;     // x = 12
x *= 2;     // x = 24
x /= 4;     // x = 6
y = 17;
y %= 5;     // y = 2
```

### 3. 遞增/遞減運算子 (`++`, `--`)

```python
n = 0;
n++;
print(n);   // 1
n--;
print(n);   // 0
```

### 4. 類別系統 (`class`, `new`, `self`)

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

p = new Point(3, 4);
p.show();   // 3 4
```

### 5. 檔案 I/O

```
fh = fopen("test.txt", "w");
fputs(fh, "Hello");
fclose(fh);

fh = fopen("test.txt", "r");
line = fgets(fh);
fclose(fh);
```

### 6. 字串處理

```
parts = split("a,b,c", ",");
s = join(["x", "y"], "|");
```

### 7. 新增內建函式

| 函式 | 說明 |
|------|------|
| `fopen(path, mode)` | 開啟檔案 |
| `fgets(fh)` | 讀取一行 |
| `fputs(fh, str)` | 寫入字串 |
| `fclose(fh)` | 關閉檔案 |
| `split(str, sep)` | 分割字串 |
| `join(arr, sep)` | 合併陣列為字串 |
| `range(start, end)` | 建立範圍 |

## 執行方式

```bash
python3 interpreter.py program.easy
```

## 與 EasyLang (HW2) 相容

所有原本 EasyLang 的語法與範例皆可正常執行。
