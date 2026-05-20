#!/usr/bin/env python3
import sys
import os
import math
import random as rand_module

class Token:
    def __init__(self, type, value, line, col):
        self.type = type
        self.value = value
        self.line = line
        self.col = col

    def __repr__(self):
        return f"Token({self.type}, {self.value!r}, {self.line}:{self.col})"

TOKENS = {
    'INT': 'INT', 'FLOAT': 'FLOAT', 'STRING': 'STRING', 'ID': 'ID',
    'TRUE': 'TRUE', 'FALSE': 'FALSE', 'NULL': 'NULL',
    'PLUS': 'PLUS', 'MINUS': 'MINUS', 'STAR': 'STAR', 'SLASH': 'SLASH', 'PERCENT': 'PERCENT',
    'EQ': 'EQ', 'NE': 'NE', 'LT': 'LT', 'GT': 'GT', 'LE': 'LE', 'GE': 'GE',
    'ASSIGN': 'ASSIGN', 'LPAREN': 'LPAREN', 'RPAREN': 'RPAREN',
    'LBRACKET': 'LBRACKET', 'RBRACKET': 'RBRACKET', 'LBRACE': 'LBRACE', 'RBRACE': 'RBRACE',
    'COMMA': 'COMMA', 'SEMI': 'SEMI', 'DOT': 'DOT',
    'AND': 'AND', 'OR': 'OR', 'NOT': 'NOT',
    'IF': 'IF', 'ELSE': 'ELSE', 'WHILE': 'WHILE', 'FOR': 'FOR',
    'RETURN': 'RETURN', 'BREAK': 'BREAK', 'CONTINUE': 'CONTINUE',
    'FUNC': 'FUNC',
    'EOF': 'EOF'
}

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.line = 1
        self.col = 1
        self.tokens = []
        self.keywords = {'if', 'else', 'while', 'for', 'return', 'break', 'continue', 'func', 'and', 'or', 'not', 'true', 'false', 'null'}

    def peek(self):
        if self.pos < len(self.text):
            return self.text[self.pos]
        return '\0'

    def advance(self):
        ch = self.text[self.pos]
        self.pos += 1
        if ch == '\n':
            self.line += 1
            self.col = 1
        else:
            self.col += 1
        return ch

    def skip_whitespace(self):
        while self.pos < len(self.text) and self.text[self.pos] in ' \t\r\n':
            self.advance()

    def skip_comment(self):
        if self.peek() == '/' and self.pos + 1 < len(self.text) and self.text[self.pos + 1] == '/':
            while self.pos < len(self.text) and self.text[self.pos] != '\n':
                self.advance()
        elif self.peek() == '/' and self.pos + 1 < len(self.text) and self.text[self.pos + 1] == '*':
            self.advance()
            self.advance()
            while self.pos < len(self.text):
                if self.text[self.pos] == '*' and self.pos + 1 < len(self.text) and self.text[self.pos + 1] == '/':
                    self.advance()
                    self.advance()
                    break
                self.advance()

    def read_number(self):
        start_col = self.col
        num_str = ''
        has_dot = False
        while self.pos < len(self.text) and (self.text[self.pos].isdigit() or self.text[self.pos] == '.'):
            if self.text[self.pos] == '.':
                if has_dot:
                    break
                has_dot = True
            num_str += self.text[self.pos]
            self.advance()
        if has_dot:
            return Token('FLOAT', float(num_str), self.line, start_col)
        return Token('INT', int(num_str), self.line, start_col)

    def read_string(self):
        start_col = self.col
        self.advance()
        s = ''
        while self.pos < len(self.text) and self.text[self.pos] != '"':
            if self.text[self.pos] == '\\' and self.pos + 1 < len(self.text):
                self.advance()
                ch = self.text[self.pos]
                if ch == 'n': s += '\n'
                elif ch == 't': s += '\t'
                elif ch == '"': s += '"'
                elif ch == '\\': s += '\\'
                else: s += ch
            else:
                s += self.text[self.pos]
            self.advance()
        if self.pos < len(self.text):
            self.advance()
        return Token('STRING', s, self.line, start_col)

    def read_id(self):
        start_col = self.col
        s = ''
        while self.pos < len(self.text) and (self.text[self.pos].isalnum() or self.text[self.pos] == '_'):
            s += self.text[self.pos]
            self.advance()
        if s in self.keywords:
            if s == 'true': return Token('TRUE', True, self.line, start_col)
            if s == 'false': return Token('FALSE', False, self.line, start_col)
            if s == 'null': return Token('NULL', None, self.line, start_col)
            return Token(s.upper(), s, self.line, start_col)
        return Token('ID', s, self.line, start_col)

    def tokenize(self):
        while self.pos < len(self.text):
            self.skip_whitespace()
            if self.pos >= len(self.text):
                break
            if self.text[self.pos] == '/' and self.pos + 1 < len(self.text) and (self.text[self.pos + 1] == '/' or self.text[self.pos + 1] == '*'):
                self.skip_comment()
                continue
            ch = self.text[self.pos]
            start_col = self.col
            if ch.isdigit() or (ch == '.' and self.pos + 1 < len(self.text) and self.text[self.pos + 1].isdigit()):
                self.tokens.append(self.read_number())
            elif ch == '"':
                self.tokens.append(self.read_string())
            elif ch.isalpha() or ch == '_':
                self.tokens.append(self.read_id())
            elif ch == '+': self.advance(); self.tokens.append(Token('PLUS', '+', self.line, start_col))
            elif ch == '-': self.advance(); self.tokens.append(Token('MINUS', '-', self.line, start_col))
            elif ch == '*': self.advance(); self.tokens.append(Token('STAR', '*', self.line, start_col))
            elif ch == '/': self.advance(); self.tokens.append(Token('SLASH', '/', self.line, start_col))
            elif ch == '%': self.advance(); self.tokens.append(Token('PERCENT', '%', self.line, start_col))
            elif ch == '(': self.advance(); self.tokens.append(Token('LPAREN', '(', self.line, start_col))
            elif ch == ')': self.advance(); self.tokens.append(Token('RPAREN', ')', self.line, start_col))
            elif ch == '[': self.advance(); self.tokens.append(Token('LBRACKET', '[', self.line, start_col))
            elif ch == ']': self.advance(); self.tokens.append(Token('RBRACKET', ']', self.line, start_col))
            elif ch == '{': self.advance(); self.tokens.append(Token('LBRACE', '{', self.line, start_col))
            elif ch == '}': self.advance(); self.tokens.append(Token('RBRACE', '}', self.line, start_col))
            elif ch == ',': self.advance(); self.tokens.append(Token('COMMA', ',', self.line, start_col))
            elif ch == ';': self.advance(); self.tokens.append(Token('SEMI', ';', self.line, start_col))
            elif ch == '.' and self.pos + 1 < len(self.text) and self.text[self.pos + 1].isalpha():
                self.advance()
                return self.tokens.append(Token('DOT', '.', self.line, start_col))
            elif ch == '=':
                self.advance()
                if self.peek() == '=': self.advance(); self.tokens.append(Token('EQ', '==', self.line, start_col))
                else: self.tokens.append(Token('ASSIGN', '=', self.line, start_col))
            elif ch == '!':
                self.advance()
                if self.peek() == '=': self.advance(); self.tokens.append(Token('NE', '!=', self.line, start_col))
                else: raise SyntaxError(f"Unexpected '!' at {self.line}:{self.col}")
            elif ch == '<':
                self.advance()
                if self.peek() == '=': self.advance(); self.tokens.append(Token('LE', '<=', self.line, start_col))
                else: self.tokens.append(Token('LT', '<', self.line, start_col))
            elif ch == '>':
                self.advance()
                if self.peek() == '=': self.advance(); self.tokens.append(Token('GE', '>=', self.line, start_col))
                else: self.tokens.append(Token('GT', '>', self.line, start_col))
            elif ch == '&' and self.pos + 1 < len(self.text) and self.text[self.pos + 1] == '&':
                self.advance(); self.advance(); self.tokens.append(Token('AND', 'and', self.line, start_col))
            elif ch == '|' and self.pos + 1 < len(self.text) and self.text[self.pos + 1] == '|':
                self.advance(); self.advance(); self.tokens.append(Token('OR', 'or', self.line, start_col))
            else:
                raise SyntaxError(f"Unexpected character '{ch}' at {self.line}:{self.col}")
        self.tokens.append(Token('EOF', None, self.line, self.col))
        return self.tokens

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return self.tokens[-1]

    def advance(self):
        t = self.tokens[self.pos]
        self.pos += 1
        return t

    def expect(self, token_type):
        t = self.peek()
        if t.type != token_type:
            raise SyntaxError(f"Expected {token_type}, got {t.type} at {t.line}:{t.col}")
        return self.advance()

    def parse(self):
        stmts = []
        while self.peek().type != 'EOF':
            stmts.append(self.parse_func_def() or self.parse_statement())
        return stmts

    def parse_func_def(self):
        if self.peek().type == 'FUNC':
            self.advance()
            name = self.expect('ID').value
            self.expect('LPAREN')
            params = []
            if self.peek().type == 'ID':
                params.append(self.advance().value)
                while self.peek().type == 'COMMA':
                    self.advance()
                    params.append(self.expect('ID').value)
            self.expect('RPAREN')
            body = self.parse_block()
            return {'type': 'func_def', 'name': name, 'params': params, 'body': body}
        return None

    def parse_block(self):
        self.expect('LBRACE')
        stmts = []
        while self.peek().type != 'RBRACE':
            stmts.append(self.parse_statement())
        self.expect('RBRACE')
        return stmts

    def parse_statement(self):
        t = self.peek()
        if t.type == 'IF':
            return self.parse_if()
        elif t.type == 'WHILE':
            return self.parse_while()
        elif t.type == 'FOR':
            return self.parse_for()
        elif t.type == 'RETURN':
            self.advance()
            val = None
            if self.peek().type not in ('SEMI', 'RBRACE'):
                val = self.parse_expression()
            return {'type': 'return', 'value': val}
        elif t.type == 'BREAK':
            self.advance()
            return {'type': 'break'}
        elif t.type == 'CONTINUE':
            self.advance()
            return {'type': 'continue'}
        elif t.type == 'SEMI':
            self.advance()
            return None
        else:
            expr = self.parse_expression()
            if self.peek().type == 'ASSIGN':
                self.advance()
                val = self.parse_expression()
                self.expect('SEMI')
                return {'type': 'assign', 'target': expr, 'value': val}
            else:
                self.expect('SEMI')
                return {'type': 'expr_stmt', 'expr': expr}

    def parse_if(self):
        self.advance()
        self.expect('LPAREN')
        cond = self.parse_expression()
        self.expect('RPAREN')
        then = self.parse_block()
        else_b = None
        if self.peek().type == 'ELSE':
            self.advance()
            else_b = self.parse_block()
        return {'type': 'if', 'cond': cond, 'then': then, 'else': else_b}

    def parse_while(self):
        self.advance()
        self.expect('LPAREN')
        cond = self.parse_expression()
        self.expect('RPAREN')
        body = self.parse_block()
        return {'type': 'while', 'cond': cond, 'body': body}

    def parse_for(self):
        self.advance()
        self.expect('LPAREN')
        init = None
        if self.peek().type != 'SEMI':
            init = self.parse_expression()
            if self.peek().type == 'ASSIGN':
                self.advance()
                init = {'type': 'assign', 'target': init, 'value': self.parse_expression()}
            self.expect('SEMI')
        else:
            self.advance()
        cond = self.parse_expression() if self.peek().type != 'SEMI' else None
        self.expect('SEMI')
        update = None
        if self.peek().type != 'RPAREN':
            update = self.parse_expression()
            if self.peek().type == 'ASSIGN':
                self.advance()
                update = {'type': 'assign', 'target': update, 'value': self.parse_expression()}
        self.expect('RPAREN')
        body = self.parse_block()
        return {'type': 'for', 'init': init, 'cond': cond, 'update': update, 'body': body}

    def parse_expression(self):
        return self.parse_or()

    def parse_or(self):
        left = self.parse_and()
        while self.peek().type == 'OR':
            self.advance()
            right = self.parse_and()
            left = {'type': 'binop', 'op': 'or', 'left': left, 'right': right}
        return left

    def parse_and(self):
        left = self.parse_compare()
        while self.peek().type == 'AND':
            self.advance()
            right = self.parse_compare()
            left = {'type': 'binop', 'op': 'and', 'left': left, 'right': right}
        return left

    def parse_compare(self):
        left = self.parse_add()
        while self.peek().type in ('EQ', 'NE', 'LT', 'GT', 'LE', 'GE'):
            op = self.advance().value
            right = self.parse_add()
            left = {'type': 'binop', 'op': op, 'left': left, 'right': right}
        return left

    def parse_add(self):
        left = self.parse_term()
        while self.peek().type in ('PLUS', 'MINUS'):
            op = self.advance().value
            right = self.parse_term()
            left = {'type': 'binop', 'op': op, 'left': left, 'right': right}
        return left

    def parse_term(self):
        left = self.parse_unary()
        while self.peek().type in ('STAR', 'SLASH', 'PERCENT'):
            op = self.advance().value
            right = self.parse_unary()
            left = {'type': 'binop', 'op': op, 'left': left, 'right': right}
        return left

    def parse_unary(self):
        if self.peek().type == 'MINUS':
            self.advance()
            return {'type': 'unary', 'op': '-', 'operand': self.parse_unary()}
        elif self.peek().type == 'NOT':
            self.advance()
            return {'type': 'unary', 'op': 'not', 'operand': self.parse_unary()}
        return self.parse_primary()

    def parse_primary(self):
        t = self.peek()
        if t.type in ('INT', 'FLOAT'):
            self.advance()
            return {'type': 'lit', 'value': t.value}
        elif t.type == 'STRING':
            self.advance()
            return {'type': 'lit', 'value': t.value}
        elif t.type in ('TRUE', 'FALSE'):
            self.advance()
            return {'type': 'lit', 'value': t.value}
        elif t.type == 'NULL':
            self.advance()
            return {'type': 'lit', 'value': None}
        elif t.type == 'ID':
            self.advance()
            name = t.value
            if self.peek().type == 'LPAREN':
                self.advance()
                args = []
                if self.peek().type != 'RPAREN':
                    args.append(self.parse_expression())
                    while self.peek().type == 'COMMA':
                        self.advance()
                        args.append(self.parse_expression())
                self.expect('RPAREN')
                return {'type': 'call', 'name': name, 'args': args}
            elif self.peek().type == 'LBRACKET':
                self.advance()
                idx = self.parse_expression()
                self.expect('RBRACKET')
                return {'type': 'index', 'obj': {'type': 'id', 'name': name}, 'index': idx}
            return {'type': 'id', 'name': name}
        elif t.type == 'LPAREN':
            self.advance()
            e = self.parse_expression()
            self.expect('RPAREN')
            return e
        elif t.type == 'LBRACKET':
            self.advance()
            elems = []
            if self.peek().type != 'RBRACKET':
                elems.append(self.parse_expression())
                while self.peek().type == 'COMMA':
                    self.advance()
                    elems.append(self.parse_expression())
            self.expect('RBRACKET')
            return {'type': 'array', 'elements': elems}
        raise SyntaxError(f"Unexpected token {t.type} at {t.line}:{t.col}")

class Interpreter:
    def __init__(self):
        self.global_scope = {}
        self.functions = {}
        self.builtins = {
            'print': self.builtin_print,
            'input': self.builtin_input,
            'len': self.builtin_len,
            'push': self.builtin_push,
            'pop': self.builtin_pop,
            'exit': self.builtin_exit,
            'time': self.builtin_time,
            'random': self.builtin_random,
            'int': self.builtin_int,
            'str': self.builtin_str,
            'float': self.builtin_float,
            'abs': self.builtin_abs,
            'sqrt': self.builtin_sqrt,
            'floor': self.builtin_floor,
            'ceil': self.builtin_ceil,
        }

    def eval(self, node, scope):
        if node is None:
            return None
        ntype = node['type']
        if ntype == 'lit':
            return node['value']
        elif ntype == 'id':
            if node['name'] in scope:
                return scope[node['name']]
            raise NameError(f"Undefined variable: {node['name']}")
        elif ntype == 'assign':
            val = self.eval(node['value'], scope)
            target = node['target']
            if target['type'] == 'id':
                scope[target['name']] = val
            elif target['type'] == 'index':
                obj = self.eval(target['obj'], scope)
                idx = self.eval(target['index'], scope)
                obj[idx] = val
            return val
        elif ntype == 'binop':
            left = self.eval(node['left'], scope)
            right = self.eval(node['right'], scope)
            op = node['op']
            if op == '+':
                if isinstance(left, str) or isinstance(right, str):
                    return str(left) + str(right)
                return left + right
            elif op == '-': return left - right
            elif op == '*': return left * right
            elif op == '/':
                if isinstance(left, float) or isinstance(right, float):
                    return float(left) / float(right)
                return int(left / right)
            elif op == '%': return left % right
            elif op == '==': return left == right
            elif op == '!=': return left != right
            elif op == '<': return left < right
            elif op == '>': return left > right
            elif op == '<=': return left <= right
            elif op == '>=': return left >= right
            elif op == 'and': return bool(left) and bool(right)
            elif op == 'or': return bool(left) or bool(right)
        elif ntype == 'unary':
            operand = self.eval(node['operand'], scope)
            if node['op'] == '-': return -operand
            elif node['op'] == 'not': return not operand
        elif ntype == 'call':
            name = node['name']
            args = [self.eval(a, scope) for a in node['args']]
            if name in self.builtins:
                return self.builtins[name](*args)
            if name not in self.functions:
                raise NameError(f"Undefined function: {name}")
            func = self.functions[name]
            new_scope = dict(self.global_scope)
            for i, p in enumerate(func['params']):
                new_scope[p] = args[i] if i < len(args) else None
            prev_scope = self.global_scope
            self.global_scope = new_scope
            result = None
            for stmt in func['body']:
                result = self.execute(stmt)
                if isinstance(result, dict) and result.get('type') == 'return':
                    result = result['value']
                    break
                if isinstance(result, dict) and result.get('type') in ('break', 'continue'):
                    break
            self.global_scope = prev_scope
            return result
        elif ntype == 'array':
            return [self.eval(e, scope) for e in node['elements']]
        elif ntype == 'index':
            obj = self.eval(node['obj'], scope)
            idx = self.eval(node['index'], scope)
            return obj[idx]
        elif ntype == 'expr_stmt':
            return self.eval(node['expr'], scope)
        return None

    def execute(self, stmt):
        if stmt is None:
            return None
        stype = stmt['type']
        if stype == 'func_def':
            self.functions[stmt['name']] = stmt
            return None
        elif stype == 'return':
            return {'type': 'return', 'value': self.eval(stmt['value'], self.global_scope) if stmt['value'] else None}
        elif stype == 'break':
            return {'type': 'break'}
        elif stype == 'continue':
            return {'type': 'continue'}
        elif stype == 'if':
            if self.is_truthy(self.eval(stmt['cond'], self.global_scope)):
                for s in stmt['then']:
                    r = self.execute(s)
                    if isinstance(r, dict) and r['type'] in ('return', 'break', 'continue'):
                        return r
            elif stmt['else']:
                for s in stmt['else']:
                    r = self.execute(s)
                    if isinstance(r, dict) and r['type'] in ('return', 'break', 'continue'):
                        return r
        elif stype == 'while':
            while self.is_truthy(self.eval(stmt['cond'], self.global_scope)):
                exited_early = False
                for s in stmt['body']:
                    r = self.execute(s)
                    if isinstance(r, dict):
                        if r['type'] == 'return': return r
                        if r['type'] == 'break': 
                            exited_early = True
                            break
                        if r['type'] == 'continue':
                            exited_early = True
                            break
                if not exited_early:
                    continue
                break
        elif stype == 'for':
            scope = self.global_scope
            if stmt['init']:
                self.eval(stmt['init'], scope)
            while stmt['cond'] is None or self.is_truthy(self.eval(stmt['cond'], scope)):
                for s in stmt['body']:
                    r = self.execute(s)
                    if isinstance(r, dict):
                        if r['type'] == 'return': return r
                        if r['type'] == 'break': break
                else:
                    if stmt['update']:
                        self.eval(stmt['update'], scope)
                    continue
                break
                if stmt['update']:
                    self.eval(stmt['update'], scope)
        elif stype == 'assign':
            self.eval(stmt, self.global_scope)
        elif stype == 'expr_stmt':
            self.eval(stmt['expr'], self.global_scope)
        return None

    def is_truthy(self, v):
        if v is None or v is False:
            return False
        if isinstance(v, (int, float)) and v == 0:
            return False
        return True

    def builtin_print(self, *args):
        end = '\n'
        if len(args) > 0 and isinstance(args[-1], dict) and args[-1].get('_print_end'):
            end = args[-1]['_print_end']
            args = args[:-1]
        print(*args, end=end)
        return None

    def builtin_input(self, prompt=''):
        return input(str(prompt))

    def builtin_len(self, arr):
        if isinstance(arr, (list, str)):
            return len(arr)
        return 0

    def builtin_push(self, arr, val):
        if isinstance(arr, list):
            arr.append(val)
        return None

    def builtin_pop(self, arr):
        if isinstance(arr, list) and len(arr) > 0:
            return arr.pop()
        return None

    def builtin_exit(self, code=0):
        sys.exit(int(code) if code else 0)

    def builtin_time(self):
        import time
        return int(time.time())

    def builtin_random(self):
        return rand_module.randint(0, 2147483647)

    def builtin_int(self, x):
        if isinstance(x, float):
            return int(x)
        if isinstance(x, str):
            return int(x)
        return int(x) if x else 0

    def builtin_float(self, x):
        if isinstance(x, str):
            return float(x)
        return float(x) if x else 0.0

    def builtin_str(self, x):
        return str(x)

    def builtin_abs(self, x):
        return abs(x)

    def builtin_sqrt(self, x):
        return math.sqrt(x)

    def builtin_floor(self, x):
        return math.floor(x)

    def builtin_ceil(self, x):
        return math.ceil(x)

    def run(self, ast):
        for stmt in ast:
            self.execute(stmt)

def main():
    if len(sys.argv) < 2:
        print("Usage: python interpreter.py <program.easy>", file=sys.stderr)
        sys.exit(1)
    filename = sys.argv[1]
    if not os.path.exists(filename):
        print(f"Error: File '{filename}' not found", file=sys.stderr)
        sys.exit(1)
    with open(filename, 'r', encoding='utf-8') as f:
        source = f.read()
    try:
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        interpreter = Interpreter()
        interpreter.run(ast)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()