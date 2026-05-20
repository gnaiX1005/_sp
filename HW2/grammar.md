# EasyLang 語法規格 (EBNF)

## 詞彙結構

```
letter     ::= "a".."z" | "A".."Z" | "_"
digit      ::= "0".."9"
identifier ::= letter { letter | digit }
integer    ::= ["-"] digit { digit }
float      ::= ["-"] digit { digit } "." digit { digit }
string     ::= '"' { any_char - '"' } '"'
boolean    ::= "true" | "false"
null       ::= "null"
comment    ::= "//" { any_char - newline } | "/*" { any_char } "*/"
whitespace ::= " " | "\t" | "\n" | "\r"
```

## 程式結構

```
program        ::= { function | statement } EOF
function       ::= "func" identifier "(" [ param_list ] ")" block
param_list     ::= identifier { "," identifier }
block          ::= "{" { statement } "}"
statement      ::= if_stmt
                 | while_stmt
                 | for_stmt
                 | return_stmt
                 | break_stmt
                 | continue_stmt
                 | expr_stmt ";"

if_stmt        ::= "if" "(" expression ")" block [ "else" block ]
while_stmt     ::= "while" "(" expression ")" block
for_stmt       ::= "for" "(" [ assignment ] ";" expression ";" [ assignment ] ")" block

return_stmt    ::= "return" [ expression ] ";"
break_stmt     ::= "break" ";"
continue_stmt  ::= "continue" ";"

expr_stmt      ::= assignment | expression
assignment     ::= identifier "=" expression
                 | identifier "[" expression "]" "=" expression

expression     ::= logic_or
logic_or       ::= logic_and { "or" logic_and }
logic_and      ::= comparison { "and" comparison }
comparison     ::= term { ("==" | "!=" | "<" | ">" | "<=" | ">=") term }
term           ::= factor { ("+" | "-") factor }
factor         ::= unary { ("*" | "/" | "%") unary }
unary          ::= ("-" | "not") unary | primary
primary        ::= integer | float | string | boolean | null
                 | identifier [ "(" [ arg_list ] ")" | "[" expression "]" ]
                 | "(" expression ")"
                 | array_lit

array_lit       ::= "[" [ expression { "," expression } ] "]"
arg_list       ::= expression { "," expression }
```

## 運算子優先順序

| 優先序 | 運算子 | 結合性 |
|--------|--------|--------|
| 1 (最高) | `-` (一元), `not` | 右到左 |
| 2 | `*`, `/`, `%` | 左到右 |
| 3 | `+`, `-` | 左到右 |
| 4 | `==`, `!=`, `<`, `>`, `<=`, `>=` | 左到右 |
| 5 | `and` | 左到右 |
| 6 (最低) | `or` | 左到右 |

## 註解

```
// 單行註解
/* 多行
   註解 */
```

## 保留字

```
if else while for return break continue
func and or not true false null
```

## 語法圖要點

1. 每個 statement 以分號 `;` 結尾（block 內的最後一個 statement 可省略）
2. function 內可以巢狀定義（在 p0 风格中允許）
3. array 可以用 `[val1, val2, ...]` 建立
4. 所有變數在首次賦值時建立，無需宣告