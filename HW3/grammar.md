# EasyLang3 語法規格 (EBNF)

## 詞彙結構

```
letter       ::= "a".."z" | "A".."Z" | "_"
digit        ::= "0".."9"
identifier   ::= letter { letter | digit }
integer      ::= ["-"] digit { digit }
float        ::= ["-"] digit { digit } "." digit { digit }
string       ::= '"' { any_char - '"' } '"'
boolean      ::= "true" | "false"
null         ::= "null"
comment      ::= "//" { any_char - newline } | "/*" { any_char } "*/"
whitespace   ::= " " | "\t" | "\n" | "\r"
```

## 運算子詞彙

```
"+"  "-"  "*"  "/"  "%"
"+=" "-=" "*=" "/=" "%="
"++" "--" ".."
"==" "!=" "<" ">" "<=" ">="
"="  "("  ")"  "["  "]"  "{"  "}"
","  ";"  "."
"&&" "||" "!"
```

## 保留字

```
if else while for return break continue
func and or not true false null
class new self in
```

## 程式結構

```
program          ::= { function | class_def | statement } EOF
function         ::= "func" identifier "(" [ param_list ] ")" block
class_def        ::= "class" identifier "{" { function } "}"
param_list       ::= identifier { "," identifier }
block            ::= "{" { statement } "}"
statement        ::= if_stmt
                   | while_stmt
                   | for_stmt
                   | return_stmt
                   | break_stmt
                   | continue_stmt
                   | compound_assign ";"
                   | inc_dec_stmt ";"
                   | expr_stmt ";"

if_stmt          ::= "if" "(" expression ")" block [ "else" block ]
while_stmt       ::= "while" "(" expression ")" block
for_stmt         ::= "for" "(" [ assignment ] ";" expression ";" [ assignment ] ")" block
                   | "for" identifier "in" expression block

return_stmt      ::= "return" [ expression ] ";"
break_stmt       ::= "break" ";"
continue_stmt    ::= "continue" ";"

expr_stmt        ::= assignment | expression
assignment       ::= identifier "=" expression
                   | identifier "[" expression "]" "=" expression
                   | expression "." identifier "=" expression
compound_assign  ::= expression ("+=" | "-=" | "*=" | "/=" | "%=") expression
inc_dec_stmt     ::= expression ("++" | "--")

expression       ::= range
range            ::= or_expr { ".." or_expr }
or_expr          ::= and_expr { "or" and_expr }
and_expr         ::= comparison { "and" comparison }
comparison       ::= term { ("==" | "!=" | "<" | ">" | "<=" | ">=") term }
term             ::= factor { ("+" | "-") factor }
factor           ::= unary { ("*" | "/" | "%") unary }
unary            ::= ("-" | "not") unary | postfix
postfix          ::= primary { "(" [ arg_list ] ")" | "[" expression "]" | "." identifier | "++" | "--" }
primary          ::= integer | float | string | boolean | null
                   | "self"
                   | identifier
                   | "(" expression ")"
                   | array_lit
                   | new_expr

new_expr         ::= "new" identifier "(" [ arg_list ] ")"
array_lit        ::= "[" [ expression { "," expression } ] "]"
arg_list         ::= expression { "," expression }
```

## 運算子優先順序

| 優先序 | 運算子 | 結合性 |
|--------|--------|--------|
| 1 (最高) | `()`, `[]`, `.`, `++`, `--` (後置) | 左到右 |
| 2 | `-` (一元), `not` | 右到左 |
| 3 | `*`, `/`, `%` | 左到右 |
| 4 | `+`, `-` | 左到右 |
| 5 | `==`, `!=`, `<`, `>`, `<=`, `>=` | 左到右 |
| 6 | `and` | 左到右 |
| 7 (最低) | `or` | 左到右 |
| 8 | `..` (range) | 左到右 |

## 新增功能 (vs EasyLang)

1. **範圍運算子 `..`**：產生可迭代的 range 值，例如 `1..10`
2. **for-in 迴圈**：`for i in 0..10 { ... }` 或 `for x in array { ... }`
3. **複合賦值**：`+=`, `-=`, `*=`, `/=", `%=`
4. **遞增/遞減**：後置 `++`, `--`
5. **類別系統**：`class`, `new`, `self` 關鍵字，支援方法與屬性
6. **方法呼叫**：`obj.method(args)` 語法
7. **檔案 I/O**：`fopen`, `fgets`, `fputs`, `fclose`
8. **字串處理**：`split`, `join` 內建函式
9. **`range()` 函式**：`range(start, end)` 建立範圍

## 註解

```
// 單行註解
/* 多行
   註解 */
```
