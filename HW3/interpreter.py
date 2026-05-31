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
    'PLUSEQ': 'PLUSEQ', 'MINUSEQ': 'MINUSEQ', 'STAREQ': 'STAREQ', 'SLASHEQ': 'SLASHEQ', 'PERCENTEQ': 'PERCENTEQ',
    'INCREMENT': 'INCREMENT', 'DECREMENT': 'DECREMENT',
    'EQ': 'EQ', 'NE': 'NE', 'LT': 'LT', 'GT': 'GT', 'LE': 'LE', 'GE': 'GE',
    'ASSIGN': 'ASSIGN', 'LPAREN': 'LPAREN', 'RPAREN': 'RPAREN',
    'LBRACKET': 'LBRACKET', 'RBRACKET': 'RBRACKET', 'LBRACE': 'LBRACE', 'RBRACE': 'RBRACE',
    'COMMA': 'COMMA', 'SEMI': 'SEMI', 'DOT': 'DOT', 'DOTS': 'DOTS',
    'AND': 'AND', 'OR': 'OR', 'NOT': 'NOT',
    'IF': 'IF', 'ELSE': 'ELSE', 'WHILE': 'WHILE', 'FOR': 'FOR',
    'IN': 'IN',
    'RETURN': 'RETURN', 'BREAK': 'BREAK', 'CONTINUE': 'CONTINUE',
    'FUNC': 'FUNC', 'CLASS': 'CLASS', 'NEW': 'NEW', 'SELF': 'SELF',
    'EOF': 'EOF'
}

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.line = 1
        self.col = 1
        self.tokens = []
        self.keywords = {
            'if', 'else', 'while', 'for', 'return', 'break', 'continue',
            'func', 'and', 'or', 'not', 'true', 'false', 'null',
            'class', 'new', 'self', 'in'
        }

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
                if self.pos + 1 < len(self.text) and self.text[self.pos + 1] == '.':
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
            elif ch == '+':
                self.advance()
                if self.peek() == '=': self.advance(); self.tokens.append(Token('PLUSEQ', '+=', self.line, start_col))
                elif self.peek() == '+': self.advance(); self.tokens.append(Token('INCREMENT', '++', self.line, start_col))
                else: self.tokens.append(Token('PLUS', '+', self.line, start_col))
            elif ch == '-':
                self.advance()
                if self.peek() == '=': self.advance(); self.tokens.append(Token('MINUSEQ', '-=', self.line, start_col))
                elif self.peek() == '-': self.advance(); self.tokens.append(Token('DECREMENT', '--', self.line, start_col))
                else: self.tokens.append(Token('MINUS', '-', self.line, start_col))
            elif ch == '*':
                self.advance()
                if self.peek() == '=': self.advance(); self.tokens.append(Token('STAREQ', '*=', self.line, start_col))
                else: self.tokens.append(Token('STAR', '*', self.line, start_col))
            elif ch == '/':
                self.advance()
                if self.peek() == '=': self.advance(); self.tokens.append(Token('SLASHEQ', '/=', self.line, start_col))
                else: self.tokens.append(Token('SLASH', '/', self.line, start_col))
            elif ch == '%':
                self.advance()
                if self.peek() == '=': self.advance(); self.tokens.append(Token('PERCENTEQ', '%=', self.line, start_col))
                else: self.tokens.append(Token('PERCENT', '%', self.line, start_col))
            elif ch == '(': self.advance(); self.tokens.append(Token('LPAREN', '(', self.line, start_col))
            elif ch == ')': self.advance(); self.tokens.append(Token('RPAREN', ')', self.line, start_col))
            elif ch == '[': self.advance(); self.tokens.append(Token('LBRACKET', '[', self.line, start_col))
            elif ch == ']': self.advance(); self.tokens.append(Token('RBRACKET', ']', self.line, start_col))
            elif ch == '{': self.advance(); self.tokens.append(Token('LBRACE', '{', self.line, start_col))
            elif ch == '}': self.advance(); self.tokens.append(Token('RBRACE', '}', self.line, start_col))
            elif ch == ',': self.advance(); self.tokens.append(Token('COMMA', ',', self.line, start_col))
            elif ch == ';': self.advance(); self.tokens.append(Token('SEMI', ';', self.line, start_col))
            elif ch == '.':
                self.advance()
                if self.peek() == '.':
                    self.advance()
                    self.tokens.append(Token('DOTS', '..', self.line, start_col))
                else:
                    self.tokens.append(Token('DOT', '.', self.line, start_col))
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
            stmts.append(self.parse_func_def() or self.parse_class_def() or self.parse_statement())
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

    def parse_class_def(self):
        if self.peek().type == 'CLASS':
            self.advance()
            name = self.expect('ID').value
            self.expect('LBRACE')
            methods = []
            while self.peek().type != 'RBRACE':
                fd = self.parse_func_def()
                if fd:
                    methods.append(fd)
                else:
                    raise SyntaxError(f"Expected method definition in class at {self.peek().line}:{self.peek().col}")
            self.expect('RBRACE')
            return {'type': 'class_def', 'name': name, 'methods': methods}
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
        elif t.type == 'LBRACE':
            return {'type': 'block', 'stmts': self.parse_block_from_brace()}
        else:
            expr = self.parse_expression()
            if self.peek().type in ('ASSIGN', 'PLUSEQ', 'MINUSEQ', 'STAREQ', 'SLASHEQ', 'PERCENTEQ'):
                op = self.advance().type
                val = self.parse_expression()
                self.expect('SEMI')
                if op == 'ASSIGN':
                    return {'type': 'assign', 'target': expr, 'value': val}
                op_map = {'PLUSEQ': '+', 'MINUSEQ': '-', 'STAREQ': '*', 'SLASHEQ': '/', 'PERCENTEQ': '%'}
                return {'type': 'assign', 'target': expr, 'value': {'type': 'binop', 'op': op_map[op], 'left': expr, 'right': val}}
            elif self.peek().type in ('INCREMENT', 'DECREMENT'):
                op = self.advance().type
                self.expect('SEMI')
                inc_op = '+' if op == 'INCREMENT' else '-'
                return {'type': 'assign', 'target': expr, 'value': {'type': 'binop', 'op': inc_op, 'left': expr, 'right': {'type': 'lit', 'value': 1}}}
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
        if self.peek().type == 'ID' and self.pos + 1 < len(self.tokens) and self.tokens[self.pos + 1].type == 'IN':
            var_name = self.expect('ID').value
            self.expect('IN')
            iterable = self.parse_expression()
            body = self.parse_block()
            return {'type': 'for_in', 'var': var_name, 'iterable': iterable, 'body': body}
        else:
            self.expect('LPAREN')
            init = None
            if self.peek().type != 'SEMI':
                init = self.parse_expression()
                if self.peek().type == 'ASSIGN':
                    self.advance()
                    init = {'type': 'assign', 'target': init, 'value': self.parse_expression()}
                elif self.peek().type in ('PLUSEQ', 'MINUSEQ', 'STAREQ', 'SLASHEQ', 'PERCENTEQ'):
                    op = self.advance().type
                    val = self.parse_expression()
                    op_map = {'PLUSEQ': '+', 'MINUSEQ': '-', 'STAREQ': '*', 'SLASHEQ': '/', 'PERCENTEQ': '%'}
                    init = {'type': 'assign', 'target': init, 'value': {'type': 'binop', 'op': op_map[op], 'left': init, 'right': val}}
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
                elif self.peek().type in ('PLUSEQ', 'MINUSEQ', 'STAREQ', 'SLASHEQ', 'PERCENTEQ'):
                    op = self.advance().type
                    val = self.parse_expression()
                    op_map = {'PLUSEQ': '+', 'MINUSEQ': '-', 'STAREQ': '*', 'SLASHEQ': '/', 'PERCENTEQ': '%'}
                    update = {'type': 'assign', 'target': update, 'value': {'type': 'binop', 'op': op_map[op], 'left': update, 'right': val}}
                elif self.peek().type in ('INCREMENT', 'DECREMENT'):
                    op = self.advance().type
                    inc_op = '+' if op == 'INCREMENT' else '-'
                    update = {'type': 'assign', 'target': update, 'value': {'type': 'binop', 'op': inc_op, 'left': update, 'right': {'type': 'lit', 'value': 1}}}
            self.expect('RPAREN')
            body = self.parse_block()
            return {'type': 'for', 'init': init, 'cond': cond, 'update': update, 'body': body}

    def parse_block_from_brace(self):
        self.expect('LBRACE')
        stmts = []
        while self.peek().type != 'RBRACE':
            stmts.append(self.parse_statement())
        self.expect('RBRACE')
        return stmts

    def parse_expression(self):
        return self.parse_range()

    def parse_range(self):
        left = self.parse_or()
        if self.peek().type == 'DOTS':
            self.advance()
            right = self.parse_or()
            left = {'type': 'range', 'start': left, 'end': right}
        return left

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
            left = {'type': 'lit', 'value': t.value}
        elif t.type == 'STRING':
            self.advance()
            left = {'type': 'lit', 'value': t.value}
        elif t.type in ('TRUE', 'FALSE'):
            self.advance()
            left = {'type': 'lit', 'value': t.value}
        elif t.type == 'NULL':
            self.advance()
            left = {'type': 'lit', 'value': None}
        elif t.type == 'SELF':
            self.advance()
            left = {'type': 'id', 'name': 'self'}
        elif t.type == 'ID':
            self.advance()
            left = {'type': 'id', 'name': t.value}
        elif t.type == 'LPAREN':
            self.advance()
            left = self.parse_expression()
            self.expect('RPAREN')
        elif t.type == 'LBRACKET':
            self.advance()
            elems = []
            if self.peek().type != 'RBRACKET':
                elems.append(self.parse_expression())
                while self.peek().type == 'COMMA':
                    self.advance()
                    elems.append(self.parse_expression())
            self.expect('RBRACKET')
            left = {'type': 'array', 'elements': elems}
        elif t.type == 'NEW':
            self.advance()
            class_name = self.expect('ID').value
            self.expect('LPAREN')
            args = []
            if self.peek().type != 'RPAREN':
                args.append(self.parse_expression())
                while self.peek().type == 'COMMA':
                    self.advance()
                    args.append(self.parse_expression())
            self.expect('RPAREN')
            left = {'type': 'new', 'class_name': class_name, 'args': args}
        else:
            raise SyntaxError(f"Unexpected token {t.type} at {t.line}:{t.col}")

        while True:
            t = self.peek()
            if t.type == 'LPAREN':
                self.advance()
                args = []
                if self.peek().type != 'RPAREN':
                    args.append(self.parse_expression())
                    while self.peek().type == 'COMMA':
                        self.advance()
                        args.append(self.parse_expression())
                self.expect('RPAREN')
                left = {'type': 'call', 'func': left, 'args': args}
            elif t.type == 'LBRACKET':
                self.advance()
                idx = self.parse_expression()
                self.expect('RBRACKET')
                left = {'type': 'index', 'obj': left, 'index': idx}
            elif t.type == 'DOT':
                self.advance()
                name = self.expect('ID').value
                left = {'type': 'attr', 'obj': left, 'name': name}
            elif t.type in ('INCREMENT', 'DECREMENT'):
                self.advance()
                if left.get('type') != 'id':
                    raise SyntaxError("Can only increment/decrement a variable")
                op = '+' if t.type == 'INCREMENT' else '-'
                left = {'type': 'assign_expr', 'target': left, 'value': {'type': 'binop', 'op': op, 'left': left, 'right': {'type': 'lit', 'value': 1}}}
            else:
                break
        return left


class RangeValue:
    def __init__(self, start, end):
        self.start = start
        self.end = end
    def __iter__(self):
        i = self.start
        step = 1 if self.start <= self.end else -1
        if step > 0:
            while i < self.end:
                yield i
                i += step
        else:
            while i > self.end:
                yield i
                i += step
    def __repr__(self):
        return f"Range({self.start}..{self.end})"


class Instance:
    def __init__(self, klass):
        self._class = klass
        self._data = {}
    def __repr__(self):
        return f"<Instance of {self._class.name}>"


class ClassDef:
    def __init__(self, name, methods):
        self.name = name
        self.methods = methods


class UserFunction:
    def __init__(self, name, params, body, interp):
        self.name = name
        self.params = params
        self.body = body
        self.interp = interp
    def __repr__(self):
        return f"<Function {self.name}>"
    def call(self, args):
        return self._exec_in_scope(dict(self.interp.global_scope), args)
    def call_with_self(self, self_obj, args):
        scope = dict(self.interp.global_scope)
        scope['self'] = self_obj
        return self._exec_in_scope(scope, args)
    def _exec_in_scope(self, scope, args):
        for i, p in enumerate(self.params):
            scope[p] = args[i] if i < len(args) else None
        prev = self.interp.global_scope
        self.interp.global_scope = scope
        result = None
        for stmt in self.body:
            result = self.interp.execute(stmt)
            if isinstance(result, dict) and result.get('type') == 'return':
                result = result['value']
                break
            if isinstance(result, dict) and result.get('type') in ('break', 'continue'):
                break
        self.interp.global_scope = prev
        return result


class Interpreter:
    def __init__(self):
        self.global_scope = {}
        self.functions = {}
        self.classes = {}
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
            'fopen': self.builtin_fopen,
            'fgets': self.builtin_fgets,
            'fputs': self.builtin_fputs,
            'fclose': self.builtin_fclose,
            'split': self.builtin_split,
            'join': self.builtin_join,
            'range': self.builtin_range,
        }

    def eval(self, node, scope):
        if node is None:
            return None
        ntype = node['type']
        if ntype == 'lit':
            return node['value']
        elif ntype == 'id':
            name = node['name']
            if name in scope:
                return scope[name]
            if name in self.functions:
                return self.functions[name]
            if name in self.builtins:
                return self.builtins[name]
            raise NameError(f"Undefined variable: {name}")
        elif ntype == 'assign':
            val = self.eval(node['value'], scope)
            target = node['target']
            if target['type'] == 'id':
                scope[target['name']] = val
            elif target['type'] == 'index':
                obj = self.eval(target['obj'], scope)
                idx = self.eval(target['index'], scope)
                obj[idx] = val
            elif target['type'] == 'attr':
                obj = self.eval(target['obj'], scope)
                if isinstance(obj, Instance):
                    obj._data[target['name']] = val
                else:
                    raise RuntimeError("Cannot set attribute on non-object")
            return val
        elif ntype == 'assign_expr':
            val = self.eval(node['value'], scope)
            target = node['target']
            if target['type'] == 'id':
                old = self.eval(target, scope)
                scope[target['name']] = val
                return old
            raise RuntimeError("Cannot assign to non-variable")
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
            func_expr = node['func']
            if func_expr['type'] == 'attr':
                obj = self.eval(func_expr['obj'], scope)
                method_name = func_expr['name']
                if isinstance(obj, Instance):
                    if method_name in obj._class.methods:
                        meth = obj._class.methods[method_name]
                        args = [self.eval(a, scope) for a in node['args']]
                        return meth.call_with_self(obj, args)
                    raise NameError(f"Method '{method_name}' not found on {obj._class.name}")
                raise RuntimeError("Cannot call method on non-object")
            func = self.eval(func_expr, scope)
            args = [self.eval(a, scope) for a in node['args']]
            if isinstance(func, UserFunction):
                return func.call(args)
            if callable(func):
                return func(*args)
            raise RuntimeError(f"Not callable: {func}")
        elif ntype == 'array':
            return [self.eval(e, scope) for e in node['elements']]
        elif ntype == 'index':
            obj = self.eval(node['obj'], scope)
            idx = self.eval(node['index'], scope)
            return obj[idx]
        elif ntype == 'attr':
            obj = self.eval(node['obj'], scope)
            name = node['name']
            if isinstance(obj, Instance):
                if name in obj._data:
                    return obj._data[name]
                raise NameError(f"No attribute '{name}' on {obj._class.name}")
            raise RuntimeError(f"Cannot access attribute on non-object")
        elif ntype == 'range':
            start = self.eval(node['start'], scope)
            end = self.eval(node['end'], scope)
            return RangeValue(int(start), int(end))
        elif ntype == 'new':
            class_name = node['class_name']
            if class_name not in self.classes:
                raise NameError(f"Undefined class: {class_name}")
            klass = self.classes[class_name]
            inst = Instance(klass)
            args = [self.eval(a, scope) for a in node['args']]
            if 'init' in klass.methods:
                klass.methods['init'].call_with_self(inst, args)
            return inst
        elif ntype == 'expr_stmt':
            return self.eval(node['expr'], scope)
        return None

    def execute(self, stmt):
        if stmt is None:
            return None
        stype = stmt['type']
        if stype == 'func_def':
            func = UserFunction(stmt['name'], stmt['params'], stmt['body'], self)
            self.functions[stmt['name']] = func
            return None
        elif stype == 'class_def':
            methods = {}
            for m in stmt['methods']:
                func = UserFunction(m['name'], m['params'], m['body'], self)
                methods[m['name']] = func
            klass = ClassDef(stmt['name'], methods)
            self.classes[stmt['name']] = klass
            return None
        elif stype == 'return':
            return {'type': 'return', 'value': self.eval(stmt['value'], self.global_scope) if stmt['value'] else None}
        elif stype == 'break':
            return {'type': 'break'}
        elif stype == 'continue':
            return {'type': 'continue'}
        elif stype == 'block':
            for s in stmt['stmts']:
                r = self.execute(s)
                if isinstance(r, dict) and r['type'] in ('return', 'break', 'continue'):
                    return r
            return None
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
        elif stype == 'for_in':
            iterable = self.eval(stmt['iterable'], self.global_scope)
            for val in iterable:
                self.global_scope[stmt['var']] = val
                for s in stmt['body']:
                    r = self.execute(s)
                    if isinstance(r, dict):
                        if r['type'] == 'return': return r
                        if r['type'] == 'break': break
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
        print(*args)
        return None

    def builtin_input(self, prompt=''):
        return input(str(prompt))

    def builtin_len(self, arr):
        if isinstance(arr, (list, str, RangeValue)):
            return len(list(arr)) if isinstance(arr, RangeValue) else len(arr)
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

    def builtin_fopen(self, path, mode='r'):
        try:
            return open(path, mode)
        except Exception as e:
            raise RuntimeError(f"Cannot open file '{path}': {e}")

    def builtin_fgets(self, fh):
        if hasattr(fh, 'readline'):
            line = fh.readline()
            return line if line else None
        raise RuntimeError("fgets requires a file handle")

    def builtin_fputs(self, fh, s):
        if hasattr(fh, 'write'):
            fh.write(str(s))
            return None
        raise RuntimeError("fputs requires a file handle")

    def builtin_fclose(self, fh):
        if hasattr(fh, 'close'):
            fh.close()
            return None
        raise RuntimeError("fclose requires a file handle")

    def builtin_split(self, s, sep=' '):
        if isinstance(s, str):
            return s.split(sep)
        raise RuntimeError("split requires a string")

    def builtin_join(self, arr, sep=' '):
        return sep.join(str(x) for x in arr)

    def builtin_range(self, start, end):
        return RangeValue(int(start), int(end))

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
