# 第八章：組合語言與 RISC-V

## 8.1 什麼是組合語言

組合語言（Assembly Language）是機器碼的人類可讀表示法。每條組合語言指令對應一條機器碼指令，使用助憶碼（mnemonic）來代替二進位編碼。

### 從高階語言到組合語言

```c
// C 語言
int add(int a, int b) {
    return a + b;
}
```

```assembly
; RISC-V 組合語言
add:
    addi sp, sp, -16     ; 配置堆疊空間
    sd   a0, 8(sp)       ; 儲存 a
    sd   a1, 0(sp)       ; 儲存 b
    ld   a0, 8(sp)       ; 載入 a
    ld   a1, 0(sp)       ; 載入 b
    add  a0, a0, a1      ; a0 = a0 + a1
    addi sp, sp, 16      ; 釋放堆疊空間
    ret                   ; 回傳 (a0 為回傳值)
```

## 8.2 RISC-V 架構簡介

RISC-V 是一個開放的精簡指令集架構（RISC），由加州大學柏克萊分校開發。它的設計理念是精簡、模組化、可擴展。

### 暫存器

RISC-V 有 32 個通用暫存器，每個 32/64 位元：

| 暫存器 | ABI 名稱 | 用途 |
|--------|---------|------|
| x0 | zero | 恆為 0 |
| x1 | ra | 回傳位址 |
| x2 | sp | 堆疊指標 |
| x5-x7 | t0-t2 | 臨時暫存器 |
| x10-x17 | a0-a7 | 函式參數 / 回傳值 |
| x8-x9 | s0-s1 | 被呼叫者儲存 |
| x18-x27 | s2-s11 | 被呼叫者儲存 |
| x28-x31 | t3-t6 | 臨時暫存器 |

### 指令格式

RISC-V 有六種基本指令格式，所有指令都是 32 位元：

```
R-type (暫存器-暫存器):
31:25    24:20   19:15   14:12   11:7    6:0
funct7   rs2     rs1     funct3  rd      opcode

I-type (立即數):
31:20           19:15   14:12   11:7    6:0
imm[11:0]       rs1     funct3  rd      opcode

S-type (儲存):
31:25    24:20   19:15   14:12   11:7    6:0
imm[4:0] rs2     rs1     funct3  imm[11:5] opcode
```

## 8.3 常用 RISC-V 指令

### 算術指令

```assembly
add  rd, rs1, rs2    ; rd = rs1 + rs2
sub  rd, rs1, rs2    ; rd = rs1 - rs2
addi rd, rs1, imm    ; rd = rs1 + imm（立即數）
mul  rd, rs1, rs2    ; rd = rs1 * rs2
div  rd, rs1, rs2    ; rd = rs1 / rs2
rem  rd, rs1, rs2    ; rd = rs1 % rs2
```

### 邏輯指令

```assembly
and  rd, rs1, rs2    ; rd = rs1 & rs2
or   rd, rs1, rs2    ; rd = rs1 | rs2
xor  rd, rs1, rs2    ; rd = rs1 ^ rs2
slli rd, rs1, shamt  ; rd = rs1 << shamt（左移）
srli rd, rs1, shamt  ; rd = rs1 >> shamt（邏輯右移）
```

### 存取指令

```assembly
lb   rd, imm(rs1)    ; rd = 載入位元組（符號延伸）
lw   rd, imm(rs1)    ; rd = 載入字組 (32-bit)
ld   rd, imm(rs1)    ; rd = 載入雙字組 (64-bit)
sb   rs2, imm(rs1)   ; 儲存位元組
sw   rs2, imm(rs1)   ; 儲存字組
sd   rs2, imm(rs1)   ; 儲存雙字組
```

### 分支指令

```assembly
beq  rs1, rs2, label ; if (rs1 == rs2) goto label
bne  rs1, rs2, label ; if (rs1 != rs2) goto label
blt  rs1, rs2, label ; if (rs1 < rs2) goto label
bge  rs1, rs2, label ; if (rs1 >= rs2) goto label
jal  rd, label       ; rd = PC+4; goto label（跳躍並連結）
jalr rd, rs1, imm    ; rd = PC+4; goto rs1+imm
```

## 8.4 從 C 語言到組合語言

### 陣列存取

```c
int arr[4] = {1, 2, 3, 4};
int x = arr[2];
```

```assembly
la   t0, arr         ; t0 = arr 的位址
lw   a0, 8(t0)       ; a0 = arr[2]（每個 int 4 位元組）
```

### 函式呼叫慣例

RISC-V 的函式呼叫慣例（Calling Convention）：

```assembly
; 呼叫者 (caller):
addi sp, sp, -16     ; 分配堆疊空間
sd   a0, 0(sp)       ; 儲存參數
li   a0, 42          ; 設定參數
jal  func            ; 呼叫函式
ld   a0, 0(sp)       ; 恢復參數
addi sp, sp, 16      ; 釋放堆疊空間

; 被呼叫者 (callee):
func:
addi sp, sp, -32     ; 分配堆疊框架
sd   ra, 24(sp)      ; 儲存回傳位址
sd   s0, 16(sp)      ; 儲存 s0
addi s0, sp, 32      ; 設定框架指標
; ... 函式主體 ...
ld   ra, 24(sp)      ; 恢復回傳位址
ld   s0, 16(sp)      ; 恢復 s0
addi sp, sp, 32      ; 釋放堆疊框架
ret
```

## 8.5 組譯器實作

一個簡易的組譯器需要：

1. **第一趟**：收集所有標籤（label）的位址
2. **第二趟**：將指令轉換為機器碼

```python
class Assembler:
    def __init__(self):
        self.symbols = {}    # 標籤 -> 位址
        self.output = []     # 輸出的機器碼

    def pass1(self, lines):
        # 第一趟：收集標籤
        address = 0
        for line in lines:
            line = line.split('#')[0].strip()  # 去除註解
            if not line:
                continue
            if line.endswith(':'):  # 標籤
                label = line[:-1]
                self.symbols[label] = address
            else:
                address += 4  # 每條指令 4 位元組

    def pass2(self, lines):
        # 第二趟：產生機器碼
        for line in lines:
            line = line.split('#')[0].strip()
            if not line or line.endswith(':'):
                continue
            machine_code = self.assemble(line)
            self.output.append(machine_code)
```

## 8.6 組合語言的應用場景

雖然高階語言已經非常成熟，但組合語言在以下場景仍然不可或缺：

1. **開機程式**：系統啟動的第一段程式碼
2. **中斷處理**：需要精確控制暫存器
3. **效能關鍵**：某些特殊指令無法由編譯器產生
4. **逆向工程**：分析二進位程式
5. **嵌入式系統**：資源極度受限的環境

## 練習題

1. 請寫一個 RISC-V 組合語言程式計算費波那契數列
2. 請使用 objdump 觀察 C 程式編譯後的組合語言
3. 請實作一個支援 addi、lw、sw、beq 的簡易組譯器

## 本章重點

- 組合語言是機器碼的人類可讀表示法
- RISC-V 是開放的精簡指令集架構
- RISC-V 有 32 個通用暫存器和六種指令格式
- 函式呼叫慣例定義了參數傳遞和暫存器使用規則
- 組譯器需要兩趟掃描來處理標籤和產生機器碼
- 組合語言在系統啟動、中斷處理等場景仍不可或缺
