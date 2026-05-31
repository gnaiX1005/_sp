# 第六章：虛擬機與中間碼

## 6.1 什麼是虛擬機

虛擬機（Virtual Machine, VM）是一種軟體模擬的執行環境。它能執行特定的指令集，通常用來執行編譯器產生的中間碼（Intermediate Representation, IR）。

常見的虛擬機包含：

- **JVM (Java Virtual Machine)**：執行 Java 位元組碼
- **CPython VM**：執行 Python 位元組碼
- **LLVM IR**：LLVM 的中間表示法
- **WebAssembly**：瀏覽器中的虛擬機

## 6.2 堆疊機 vs 暫存機

### 堆疊機 (Stack Machine)

堆疊機使用堆疊來儲存運算元和結果。大部分指令從堆疊頂端取值，並將結果推回堆疊。

```python
# 計算 3 + 4 * 2
PUSH 3       # 3 進堆疊
PUSH 4       # 4 進堆疊
PUSH 2       # 2 進堆疊
MUL          # 彈出 4, 2 → 計算 4*2=8 → 8 進堆疊
ADD          # 彈出 3, 8 → 計算 3+8=11 → 11 進堆疊
```

堆疊機的優點是：
- 實作簡單
- 指令較短（不需要指定暫存器）
- 適合直譯執行

### 暫存機 (Register Machine)

暫存機使用暫存器來儲存運算元，指令必須指定來源和目的暫存器。

```assembly
LOAD R1, 3     # R1 = 3
LOAD R2, 4     # R2 = 4
LOAD R3, 2     # R3 = 2
MUL  R2, R3    # R2 = R2 * R3
ADD  R1, R2    # R1 = R1 + R2
```

暫存機的優點是：
- 更接近真實硬體
- 最佳化空間更大
- 執行效率更高

## 6.3 四元組 (Quadruple)

四元組是一種常見的中間碼格式，每個指令包含四個欄位：

```
(op, arg1, arg2, result)
```

例如 `a = b + c * 2` 可以轉換為：

```
(*, c, 2, t1)    # t1 = c * 2
(+, b, t1, t2)   # t2 = b + t1
(=, t2, -, a)    # a = t2
```

### 四元組虛擬機實作

```python
class VM:
    def __init__(self, quadruples):
        self.quadruples = quadruples
        self.stack = []
        self.memory = {}

    def run(self):
        pc = 0  # 程式計數器
        while pc < len(self.quadruples):
            op, arg1, arg2, result = self.quadruples[pc]
            if op == 'PUSH':
                self.stack.append(self.get_value(arg1))
            elif op == 'ADD':
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a + b)
            elif op == 'MUL':
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a * b)
            elif op == 'JMP':
                pc = result
                continue
            elif op == 'JMP_F':
                cond = self.stack.pop()
                if not cond:
                    pc = result
                    continue
            pc += 1
```

## 6.4 LLVM IR 簡介

LLVM IR 是 LLVM 編譯器基礎架構使用的中間表示法。它具有以下特性：

### SSA 形式

LLVM IR 使用 SSA（Static Single Assignment）形式，每個變數只能被賦值一次。

```llvm
define i32 @factorial(i32 %n) {
entry:
    %cmp = icmp sle i32 %n, 1
    br i1 %cmp, label %then, label %else

then:
    ret i32 1

else:
    %sub = sub i32 %n, 1
    %rec = call i32 @factorial(i32 %sub)
    %result = mul i32 %n, %rec
    ret i32 %result
}
```

### LLVM IR 指令

| 指令類別 | 範例 | 說明 |
|---------|------|------|
| 算術 | `add i32 %a, %b` | 整數加法 |
| 比較 | `icmp slt i32 %a, %b` | 有號小於比較 |
| 分支 | `br i1 %cond, label %t, label %f` | 條件分支 |
| 函式呼叫 | `call i32 @foo(i32 %arg)` | 呼叫函式 |
| 回傳 | `ret i32 %val` | 回傳值 |
| 載入 | `load i32, i32* %ptr` | 從記憶體載入 |
| 儲存 | `store i32 %val, i32* %ptr` | 存入記憶體 |

## 6.5 RISC-V 虛擬機

RISC-V 是一個精簡指令集架構（RISC）。我們可以實作簡化的 RISC-V 虛擬機來執行編譯後的程式。

### RV0 虛擬機

```c
typedef struct {
    int regs[32];     // 32 個暫存器
    int pc;           // 程式計數器
    int *memory;      // 記憶體
    int mem_size;     // 記憶體大小
} CPU;

void execute(CPU *cpu, Instruction *code, int len) {
    while (cpu->pc < len) {
        Instruction inst = code[cpu->pc];
        switch (inst.opcode) {
            case ADD:
                cpu->regs[inst.rd] = cpu->regs[inst.rs1] + cpu->regs[inst.rs2];
                cpu->pc++;
                break;
            case ADDI:
                cpu->regs[inst.rd] = cpu->regs[inst.rs1] + inst.imm;
                cpu->pc++;
                break;
            case BEQ:
                if (cpu->regs[inst.rs1] == cpu->regs[inst.rs2])
                    cpu->pc += inst.imm;
                else
                    cpu->pc++;
                break;
            // ... 其他指令
        }
    }
}
```

### RISC-V 指令格式

RISC-V 指令有六種基本格式：

```
R-type:  [funct7][rs2][rs1][funct3][rd][opcode]
I-type:  [imm][rs1][funct3][rd][opcode]
S-type:  [imm][rs2][rs1][funct3][imm][opcode]
B-type:  [imm][rs2][rs1][funct3][imm][opcode]
U-type:  [imm][rd][opcode]
J-type:  [imm][rd][opcode]
```

## 6.6 從原始碼到執行的完整流程

```
原始碼 (.c / .py)
    ↓ 詞法分析
Token 序列
    ↓ 語法分析
AST
    ↓ 中間碼生成
四元組 / LLVM IR
    ↓ 組譯 / 編譯
目的檔 (.o)
    ↓ 連結
可執行檔
    ↓ 載入
虛擬機執行
```

## 練習題

1. 請為你的四元組 VM 加入陣列操作指令
2. 請實作一個簡單的暫存機虛擬機
3. 請比較堆疊機和暫存機在執行同一程式時的性能差異

## 本章重點

- 虛擬機是一種軟體模擬的執行環境
- 堆疊機實作簡單但效率較低
- 暫存機更接近真實硬體，效率更高
- 四元組是常見的中間碼格式
- LLVM IR 使用 SSA 形式，支援豐富的最佳化
- RISC-V 是精簡指令集架構，適合用於教學
