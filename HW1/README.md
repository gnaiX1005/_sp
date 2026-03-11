### 1. 編譯你的編譯器

首先，將你的 `hw1.c` 編譯成一個可執行檔（我們取名為 `my_compiler`）：

```bash
gcc hw1.c -o my_compiler

```

### 2. 確認測試檔內容

請確保你的 `test.c` 內容是簡化的語法（不要包含 `int` 或 `func main`），例如：

```c
i = 0;
sum = 0;
while (i < 10) {
    sum = sum + i;
    i = i + 1;
}

```

### 3. 用「你的編譯器」去跑 `test.c`

這是最重要的一步，執行你剛剛做出來的 `my_compiler`：

```bash
./my_compiler test.c

```

---

### 💡 如果你一定要讓 `test.c` 也能被 GCC 編譯

如果你希望 `test.c` 既能被你的編譯器跑，也能被 GCC 跑，那你必須把 `test.c` 改寫成標準的 C 語言格式（加入 `int main()` 和變數宣告）：

**修改後的 `test.c`：**

```c
#include <stdio.h>

int main() {
    int i = 0;
    int sum = 0;
    while (i < 10) {
        sum = sum + i;
        i = i + 1;
    }
    printf("sum = %d\n", sum); // 這是為了讓 GCC 跑完有輸出
    return 0;
}

```

**但是請注意：**
如果你的 `test.c` 改成上面這樣，你的 `my_compiler` 可能會因為不認得 `int` 這個字而噴錯。所以最好的做法還是：

* **用 GCC 編譯 `hw1.c**`。
* **用 `my_compiler` 跑簡化版的 `test.c**`。

你現在輸入 `./my_compiler test.c` 應該就能看到 `sum = 45` 了，試試看？
