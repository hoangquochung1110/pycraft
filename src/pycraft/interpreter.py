from typing import Iterable

from . import stmt
from .environment import Environment
from .error_handler import ErrorHandler
from .exception import BreakException, LoxRuntimeError
from .expr import (
    Assign,
    Binary,
    Call,
    Expr,
    ExprVisitor,
    Grouping,
    Literal,
    Logical,
    Unary,
    VariableExpr,
)
from .lox_callable import LoxCallable
from .stmt import Block, Print, Stmt, StmtExpression, StmtVisitor, Var
from .tokenclass import TokenType


class Interpreter(ExprVisitor, StmtVisitor[None]):

    def __init__(self, error_handler: ErrorHandler):
        self.error_handler = error_handler
        self._environment = Environment()

    def interpret(self, statements: Iterable[Stmt]):
        try:
            for stmt in statements:
                self._execute(stmt)
        except LoxRuntimeError as error:
            self.error_handler.runtime_error(error=error)

    def visit_literal_expr(self, expr: Literal):
        return expr.value

    def visit_logical_expr(self, expr: Logical):
        left = self.evaluate(expr.left)

        if expr.operator.type == TokenType.OR:
            if self._is_truthy(left):
                return left
        else:
            if not self._is_truthy(left):
                return left

        return self.evaluate(expr.right)

    def visit_grouping_expr(self, expr: Grouping):
        return self.evaluate(expr.expression)

    def visit_unary_expr(self, expr: Unary):
        right = self.evaluate(expr.right)

        match expr.operator.type:
            case TokenType.MINUS:
                self._check_number_operand(expr.operator, right)
                return -right
            case TokenType.BANG:
                return not self._is_truthy(right)
        return None

    def visit_variable_expr(self, expr: VariableExpr):
        return self._environment.get(expr.name)

    def visit_binary_expr(self, expr: Binary):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        match expr.operator.type:
            case TokenType.MINUS:
                self._check_number_operands(expr.operator, left, right)
                return float(left) - float(right)
            case TokenType.SLASH:
                self._check_number_operands(expr.operator, left, right)
                return float(left) / float(right)
            case TokenType.STAR:
                self._check_number_operands(expr.operator, left, right)
                return float(left) * float(right)
            case TokenType.PLUS:
                if isinstance(left, float) and isinstance(right, float):
                    return left + right
                if isinstance(left, str) and isinstance(right, str):
                    return left + right
                if isinstance(left, str) or isinstance(right, str):
                    return self._stringify(left) + self._stringify(right)
                raise RuntimeError(
                    expr.operator,
                    "Operands must be two numbers or two strings.",
                )
            case TokenType.GREATER:
                self._check_number_operands(expr.operator, left, right)
                return float(left) > float(right)
            case TokenType.GREATER_EQUAL:
                self._check_number_operands(expr.operator, left, right)
                return float(left) >= float(right)
            case TokenType.LESS:
                self._check_number_operands(expr.operator, left, right)
                return float(left) < float(right)
            case TokenType.LESS_EQUAL:
                self._check_number_operands(expr.operator, left, right)
                return float(left) <= float(right)
            case TokenType.BANG_EQUAL: return not self._is_equal(left, right)
            case TokenType.EQUAL_EQUAL: return self._is_equal(left, right)

    def visit_call_expr(self, expr: Call):
        callee = self.evaluate(expr.callee)

        arguments = []
        for argument in expr.arguments:
            arguments.append(self.evaluate(argument))

        if not isinstance(callee, LoxCallable):
            raise LoxRuntimeError(expr.paren, "Can only call functions and classes.")

        function: LoxCallable = callee
        return function(self, arguments)

    def evaluate(self, expr: Expr):
        """Helper method to send the expr back

        into interpreter's visitor implementation."""
        return expr.accept(self)

    def _execute(self, stmt: Stmt):
        stmt.accept(self)

    def visit_block_stmt(self, stmt: "Block") -> None:
        self.execute_block(stmt.statements, Environment(self._environment))
        return None

    def execute_block(self, statements: Iterable[Stmt], environment: Environment):
        # to keep the interpreter simple, we inelegantly change
        # and restore environment for each block
        previous: Environment = self._environment
        try:
            self._environment = environment
            for statement in statements:
                self._execute(statement)
        finally:
            self._environment = previous

    def visit_expression_stmt(self, stmt: StmtExpression) -> None:
        self.evaluate(stmt.expression)
        return None

    def visit_if_stmt(self, stmt: "stmt.If") -> None:
        if self._is_truthy(self.evaluate(stmt.condition)):
            self._execute(stmt.then_branch)
        elif stmt.else_branch is not None:
            self._execute(stmt.then_branch)
        return None

    def visit_print_stmt(self, stmt: Print) -> None:
        value = self.evaluate(stmt.expression)
        print(self._stringify(value))
        return None

    def visit_var_stmt(self, stmt: Var) -> None:
        # sets a variable to nil if it isn’t explicitly initialized
        value = None
        if stmt.initializer is not None:
            value = self.evaluate(stmt.initializer)

        self._environment.define(stmt.name.lexeme, value)
        return None

    def visit_while_stmt(self, stmt: stmt.While) -> None:
        while self._is_truthy(self.evaluate(stmt.condition)):
            try:
                self.evaluate(stmt.body)
            except BreakException:
                break
        return

    def visit_break_stmt(self, stmt: stmt.Break) -> None:
        raise BreakException()

    def visit_assign_expr(self, expr: Assign):
        value = self.evaluate(expr.value)
        self._environment.assign(expr.name, value)
        return value

    def _is_truthy(self, obj) -> bool:
        """Lox follows Ruby's simple rule: false and nil are falsey,

        and everything else is truthy.
        """
        if obj is None:
            return False
        if isinstance(obj, bool):
            return obj
        return True

    def _is_equal(self, a, b) -> bool:
        if a is None and b is None:
            return True
        if a is None:
            return False
        return a == b

    def _stringify(self, obj) -> str:
        if obj is None:
            return "nil"
        if isinstance(obj, float):
            text = str(obj)
            if text.endswith(".0"):
                text = text[:-2]
            return text
        return str(obj)

    def _check_number_operand(self, operator, operand):
        if isinstance(operand, float):
            return
        raise LoxRuntimeError(
            operator, "Operand must be a number.",
        )

    def _check_number_operands(self, operator, left, right):
        if isinstance(left, float) and isinstance(right, float):
            return
        raise LoxRuntimeError(
            operator, "Operands must be numbers.",
        )
