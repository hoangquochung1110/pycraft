from .expr import ExprVisitor, Binary, Grouping, Literal, Expr, Unary
from .tokenclass import TokenType


class Interpreter(ExprVisitor):

    def visit_literal_expr(self, expr: Literal):
        return expr.value

    def visit_grouping_expr(self, expr: Grouping):
        return self.evaluate(expr.expression)

    def visit_unary_expr(self, expr: Unary):
        right = self.evaluate(expr.right)

        match expr.operator.type:
            case TokenType.MINUS:
                return -right
            case TokenType.BANG:
                return not self._is_truthy(right)
        return None

    def visit_binary_expr(self, expr: Binary):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        match expr.operator.type:
            case TokenType.MINUS: return float(left) - float(right)
            case TokenType.SLASH: return float(left) / float(right)
            case TokenType.STAR: return float(left) * float(right)
            case TokenType.PLUS:
                if isinstance(left, float) and isinstance(right, float):
                    return left + right
                if isinstance(left, str) and isinstance(right, str):
                    return left + right
            case TokenType.GREATER: return float(left) > float(right)
            case TokenType.GREATER_EQUAL: return float(left) >= float(right)
            case TokenType.LESS: return float(left) < float(right)
            case TokenType.LESS_EQUAL: return float(left) <= float(right)
            case TokenType.BANG_EQUAL: return not self._is_equal(left, right)
            case TokenType.EQUAL_EQUAL: return self._is_equal(left, right)

    def evaluate(self, expr: Expr):
        """Helper method to send the expr back

        into interpreter's visitor implementation."""
        return expr.accept(self)

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
