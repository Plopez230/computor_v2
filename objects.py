# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    objects.py                                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: plopez-b <plopez-b@student.42malaga.com    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/09/21 17:25:26 by plopez-b          #+#    #+#              #
#    Updated: 2024/09/23 03:09:32 by plopez-b         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import math
from copy import deepcopy


class MathError(Exception):
    pass


def join_sum_terms(terms):
    result = ""
    for term in terms:
        if not term.startswith("-") and result != "":
            result += " + "
        else:
            result += " "
        result += term
    return result.lstrip()


class TreeNode:

    def __init__(self):
        self.name = None
        self.is_function = False
        self.is_variable = False
        self.is_defined = True


class Complex(TreeNode):
    
    def __init__(self, real, imaginary):
        super().__init__()
        self.r = real
        self.i = imaginary

    def __eq__(self, other):
        if isinstance(other, Complex):
            return self.r == other.r and self.i == other.i
        return False
    
    def __lt__(self, other):
        if self.r < other.r:
            return True
        if self.r == other.r and self.i < other.i:
            return True
        return False

    def eval(self, value):
        if not value.is_variable:
            self.is_function = False
        return self
    
    def as_function(self):
        return Polynomial(t=[[Complex(0, 0), self]])

    def is_integer(self):
        return self.i == 0 and float(int(self.r)) == self.r

    def is_unsigned(self):
        return self.is_integer() and self.r >= 0

    def mod(self):
        return (self.r ** 2 + self.i ** 2) ** (1/2)
    
    def arg(self):
        alpha = math.atan(self.i / self.r)
        if self.r >= 0 and self.i >= 0:
            return alpha
        if self.r >= 0 and self.i < 0:
            return -alpha
        if self.r < 0 and self.i >= 0:
            return math.pi + alpha
        if self.r < 0 and self.i < 0:
            return math.pi - alpha

    def log(self):
        return Complex(
            math.log(self.mod()),
            self.arg()
        )

    def exp(self):
        return Complex(
            math.exp(self.r) * math.cos(self.i),
            math.exp(self.r) * math.sin(self.i)
        )
    
    def ceil(self):
        return Complex(
            math.ceil(self.r),
            math.ceil(self.i)
        )

    def __neg__(self):
        return Complex(-self.r, -self.i)

    def __add__(self, other):
        if isinstance(other, Complex):
            return Complex(self.r + other.r,
                           self.i + other.i)
        if isinstance(other, Function):
            return self.as_function() + other
        if isinstance(other, Matrix):
            return other + self

    def __sub__(self, other):
        if isinstance(other, Complex):
            return Complex(self.r - other.r,
                           self.i - other.i)
        if isinstance(other, Function):
            return self.as_function() - other
        if isinstance(other, Matrix):
            return -other + self
        
    def __mul__(self, other):
        if isinstance(other, Complex):
            return Complex(self.r * other.r - self.i * other.i,
                           self.r * other.i + self.i * other.r)
        if isinstance(other, Function):
            return self.as_function() * other
        if isinstance(other, Matrix):
            return other * self
        
    def __truediv__(self, other):
        if isinstance(other, Complex):
            return Complex((self.r * other.r + self.i * other.i)
                           / (other.r ** 2 + other.i ** 2),
                           (self.i * other.r - self.r * other.i)
                           / (other.r ** 2 + other.i ** 2))
        if isinstance(other, Function):
            return self.as_function() / other
        if isinstance(other, Matrix):
            return (self * (other / other)) / other
        
    def __pow__(self, other):
        if isinstance(other, Complex):
            return (other * self.log()).exp()
        if isinstance(other, Function):
            return self.as_function() ** other
        if isinstance(other, Matrix):
            return (self * (other / other)) ** other
        
    def __mod__(self, other):
        if isinstance(other, Complex):
            return self + other * (-self / other).ceil()
        if isinstance(other, Function):
            return self.as_function() % other
        if isinstance(other, Matrix):
            return (self * (other / other)) % other

    def mat_pow(self, other):
        type = other.__class__.__name__
        raise MathError(f"Invalid operation '^^' between Complex and {type}")
        
    def mat_mul(self, other):
        type = other.__class__.__name__
        raise MathError(f"Invalid operation '**' between Complex and {type}")
        
    def print_terms(self):
        terms = 0
        if self.r != 0:
            terms += 1
        if self.i != 0:
            terms += 1
        return max(terms, 1)
    
    def __repr__(self):
        terms = []
        if self.r != 0:
            t = ""
            if self.r < 0:
                t += "- "
            t += f"{abs(self.r)}"
            terms.append(t.lstrip())
        if self.i != 0:
            t = ""
            if self.i < 0:
                t += "- "
            if abs(self.i) != 1:
                t += f"{abs(self.i)} * "
            t += "i"
            terms.append(t.lstrip())
        return join_sum_terms(terms).lstrip()


class Matrix(TreeNode):

    def __init__(self, contents):
        super().__init__()
        self.c = contents
        self.check_shape()

    def as_function(self):
        return Function(self)

    def eval(self, value):
        if not value.is_variable:
            self.is_function = False
        contents = []
        for row in self.c:
            r = []
            for el in row:
                r.append(el.eval(value))
            contents.append(r)
        return Matrix(contents)
            
    def check_shape(self):
        self.cols = None
        for row in self.c:
            if self.cols == None:
                self.cols = len(row)
            if self.cols != len(row):
                raise MathError("Invalid shape")
    
    def check_elements(self):
        self.type = None
        for row in self.c:
            for el in row:
                type = el.__class__.__name__
                if self.type == None:
                    self.type = type
                if self.type != type:
                    raise MathError(f"Element {el} of invalid type {type}")

    def __neg__(self):
        elements = []
        for row in range(self.rows):
            r = []
            for col in range(self.cols):
                r.append(-self.c[row][col])
            elements.append(r)
        return Matrix(elements)
    
    def __add__(self, other):
        if isinstance(other, Complex):
            return Matrix([[el + other for el in row] for row in self.c])
        if isinstance(other, Function):
            return self.as_function() + other
        if isinstance(other, Matrix):
            if self.rows != other.rows or self.cols != other.cols:
                raise MathError("Matrices with different shapes")
            else:
                elements = []
                for row in range(self.rows):
                    r = []
                    for col in range(self.cols):
                        r.append(self.c[row][col] + other.c[row][col])
                    elements.append(r)
                return Matrix(elements)
        type = other.__class__.__name__
        raise MathError(f"Invalid operation '+' between Matrix and {type}")

    def __sub__(self, other):
        if isinstance(other, Complex):
            return Matrix([[el - other for el in row] for row in self.c])
        if isinstance(other, Function):
            return self.as_function() - other
        if isinstance(other, Matrix):
            if self.rows != other.rows or self.cols != other.cols:
                raise MathError("Matrices with different shapes")
            else:
                elements = []
                for row in range(self.rows):
                    r = []
                    for col in range(self.cols):
                        r.append(self.c[row][col] - other.c[row][col])
                    elements.append(r)
                return Matrix(elements)
        type = other.__class__.__name__
        raise MathError(f"Invalid operation '-' between Matrix and {type}")

    def __mul__(self, other):
        if isinstance(other, Complex):
            return Matrix([[el * other for el in row] for row in self.c])
        if isinstance(other, Function):
            return self.as_function() * other
        if isinstance(other, Matrix):
            if self.rows != other.rows or self.cols != other.cols:
                raise MathError("Matrices with different shapes")
            else:
                elements = []
                for row in range(self.rows):
                    r = []
                    for col in range(self.cols):
                        r.append(self.c[row][col] * other.c[row][col])
                    elements.append(r)
                return Matrix(elements)
        type = other.__class__.__name__
        raise MathError(f"Invalid operation '*' between Matrix and {type}")
        
    def mat_mul(self, other):
        if isinstance(other, Matrix):
            if self.rows != other.cols:
                raise MathError("Invalid shape")
            else:
                elements = [
                    [None for i in range(self.rows)] for a in range(other.cols)
                ]
                for row in range(self.rows):
                    for col in range(other.cols):
                        element = Complex(0, 0)
                        for i in range(self.cols):
                            element += self.c[row][i] * other.c[i][col]
                        elements[row][col] = element
                return Matrix(elements)
        type = other.__class__.__name__
        raise MathError(f"Invalid operation '**' between Matrix and {type}")

    def __truediv__(self, other):
        if isinstance(other, Complex):
            return Matrix([[el / other for el in row] for row in self.c])
        if isinstance(other, Function):
            return self.as_function() / other
        if isinstance(other, Matrix):
            if self.rows != other.rows or self.cols != other.cols:
                raise MathError("Matrices with different shapes")
            else:
                elements = []
                for row in range(self.rows):
                    r = []
                    for col in range(self.cols):
                        r.append(self.c[row][col] / other.c[row][col])
                    elements.append(r)
                return Matrix(elements)
        type = other.__class__.__name__
        raise MathError(f"Invalid operation '/' between Matrix and {type}")
        
    def __pow__(self, other):
        if isinstance(other, Complex):
            return Matrix([[el ** other for el in row] for row in self.c])
        if isinstance(other, Function):
            return self.as_function() ** other
        if isinstance(other, Matrix):
            if self.rows != other.rows or self.cols != other.cols:
                raise MathError("Matrices with different shapes")
            else:
                elements = []
                for row in range(self.rows):
                    r = []
                    for col in range(self.cols):
                        r.append(self.c[row][col] ** other.c[row][col])
                    elements.append(r)
                return Matrix(elements)
        type = other.__class__.__name__
        raise MathError(f"Invalid operation '^' between Matrix and {type}")
        
    def mat_pow(self, other):
        if isinstance(other, Complex) and other.is_unsigned():
            result = self
            for i in range(int(other.r) - 1):
                    result = result.mat_mul(self)
            return result
        raise MathError(f"Exponent must be positive integer")
        
    def __mod__(self, other):
        if isinstance(other, Complex):
            return Matrix([[el % other for el in row] for row in self.c])
        if isinstance(other, Function):
            return self.as_function() % other
        if isinstance(other, Matrix):
            if self.rows != other.rows or self.cols != other.cols:
                raise MathError("Matrices with different shapes")
            else:
                elements = []
                for row in range(self.rows):
                    r = []
                    for col in range(self.cols):
                        r.append(self.c[row][col] % other.c[row][col])
                    elements.append(r)
                return Matrix(elements)
        type = other.__class__.__name__
        raise MathError(f"Invalid operation '%' between Matrix and {type}")
        
    def __repr__(self):
        return str(self.c)


class Function(TreeNode):

    def __init__(self, value = None):
        super().__init__()
        self.value = value

    def as_function(self):
        return self

    def __add__(self, other):
        if isinstance(self, Polynomial):
            if isinstance(other, Complex):
                other = Polynomial(t = [[Complex(0, 0), other]])
            if isinstance(other, Polynomial):
                return self.add(other)
        return Add(self, other.as_function())

    def __sub__(self, other):
        if isinstance(self, Polynomial):
            if isinstance(other, Complex):
                other = Polynomial(t = [[Complex(0, 0), other]])
            if isinstance(other, Polynomial):
                return self.sub(other)
        return Sub(self, other.as_function())

    def __mul__(self, other):
        if isinstance(self, Polynomial):
            if isinstance(other, Complex):
                other = Polynomial(t = [[Complex(0, 0), other]])
            if isinstance(other, Polynomial):
                return self.mul(other)
        return Mul(self, other.as_function())

    def __truediv__(self, other):
        if isinstance(self, Polynomial):
            if isinstance(other, Complex):
                other = Polynomial(t = [[Complex(0, 0), other]])
                return self.mul(other)
        return Div(self, other.as_function())

    def __pow__(self, other):
        if isinstance(self, Polynomial):
            if isinstance(other, Complex):
                if other.is_integer():
                    return self.pow(other)
        return Pow(self, other.as_function())

    def __mod__(self, other):
        return Mod(self, other.as_function())
    
    def eval(self, value):
        if not value.is_variable:
            self.is_function = False
        return self.value.eval(value)
    
    def __repr__(self):
        return str(self.value)
    
    def with_par(self, parent):
        if self.__class__.__name__ == "Function":
            if isinstance(self.value, Complex) \
                and self.value.i != 0:
                    return f"({str(self.value)})"
        classname = parent.__class__.__name__
        precedences = {
            "Add": [],
            "Sub": [],
            "Mod": ["Add", "Sub"],
            "Mul": ["Add", "Sub", "Mod"],
            "Div": ["Add", "Sub", "Mod"],
            "Pow": ["Add", "Sub", "Mod", "Mul", "Div"]
        }
        if self.__class__.__name__ in precedences[classname]:
            return f"({str(self)})"
        return str(self)


class Add(Function):

    def __init__(self, first, second):
        super().__init__()
        self.first = first
        self.second = second

    def eval(self, value):
        if not value.is_variable:
            self.is_function = False
        return self.first.eval(value) + self.second.eval(value)
    
    def __repr__(self):
        return f"{self.first.with_par(self)} + {self.second.with_par(self)}"


class Sub(Function):

    def __init__(self, first, second):
        super().__init__()
        self.first = first
        self.second = second

    def eval(self, value):
        if not value.is_variable:
            self.is_function = False
        return self.first.eval(value) + self.second.eval(value)
    
    def __repr__(self):
        return f"{self.first.with_par(self)} - {self.second.with_par(self)}"


class Mul(Function):

    def __init__(self, first, second):
        super().__init__()
        self.first = first
        self.second = second

    def eval(self, value):
        if not value.is_variable:
            self.is_function = False
        return self.first.eval(value) * self.second.eval(value)
    
    def __repr__(self):
        return f"{self.first.with_par(self)} * {self.second.with_par(self)}"


class Div(Function):

    def __init__(self, first, second):
        super().__init__()
        self.first = first
        self.second = second

    def eval(self, value):
        if not value.is_variable:
            self.is_function = False
        return self.first.eval(value) / self.second.eval(value)
    
    def __repr__(self):
        return f"{self.first.with_par(self)} / {self.second.with_par(self)}"


class Pow(Function):

    def __init__(self, first, second):
        super().__init__()
        self.first = first
        self.second = second

    def eval(self, value):
        if not value.is_variable:
            self.is_function = False
        return self.first.eval(value) ** self.second.eval(value)
    
    def __repr__(self):
        return f"{self.first.with_par(self)} ^ {self.second.with_par(self)}"


class Mod(Function):

    def __init__(self, first, second):
        super().__init__()
        self.first = first
        self.second = second

    def eval(self, value):
        if not value.is_variable:
            self.is_function = False
        return self.first.eval(value) % self.second.eval(value)
    
    def __repr__(self):
        return f"({self.first.with_par(self)}) % ({self.second.with_par(self)})"


class Polynomial(Function):

    def __init__(self, t = None):
        super().__init__()
        self.t = t or []
        self.remove_zeros()

    def _get_term(self, terms, _exp):
        for term in terms:
            if term[0] == _exp:
                return term
        return None
    
    def remove_zeros(self):
        terms = []
        for term in self.t:
            if term[0] != Complex(0, 0) or term[1] != Complex(0, 0):
                terms.append(term)
        self.t = terms

    def add(self, pol):
        terms = deepcopy(self.t)
        for term in pol.t:
            t = self._get_term(terms, term[0])
            if not t:
                terms.append(term)
            else:
                t[1] = t[1] + term[1]
        return Polynomial(t = terms)

    def sub(self, pol):
        terms = deepcopy(self.t)
        for term in pol.t:
            t = self._get_term(terms, term[0])
            if not t:
                terms.append([term[0], -term[1]])
            else:
                t[1] = t[1] - term[1]
        return Polynomial(t = terms)
        
    def mul(self, pol):
        res = Polynomial(t=[])
        for t1 in self.t:
            for t2 in pol.t:
                res += Polynomial([[t1[0] + t2[0], t1[1] * t2[1]]])
        return res
        
    def div(self, pol):
        terms = []
        for t1 in self.t:
            for t2 in pol.t:
                terms.append([t1[0] - t2[0], t1[1] / t2[1]])
        return Polynomial(t = terms)
    
    def pow(self, complex):
        res = self
        i = int(complex.r)
        for x in range(i - 1):
            res = self.mul(res)
        return res
    
    def can_compose(self):
        if len(self.t) > 1:
            return True
        if len(self.t) == 1 and self.t[0][0] != Complex(0, 0):
            return True
        return False

    def eval(self, value):
        if not value.is_variable:
            self.is_function = False
        if isinstance(value, Function) and not self.can_compose():
            return self
        result = None
        for term in self.t:
            if not result:
                t = term[1] * value ** term[0]
                result = t
            else:
                t = term[1] * value ** term[0]
                result += t
        return result
    
    def _repr_term(self, term):
        c = term[1]
        e = term[0]
        r = []
        if c != Complex(1, 0):
            if (c.print_terms() > 1):
                r.append(f"({c})")
            else:
                r.append(f"{c}")
        if e != Complex(1, 0) and e != Complex(0, 0):
            if (e.print_terms() > 1):
                r.append(f"x^({e})")
            else:
                r.append(f"x^{e}")
        elif e != Complex(0, 0):
            r.append("x")
        if not r:
            r = ["1.0"]
        return " * ".join(r)

    def __repr__(self):
        sorted = deepcopy(self.t)
        sorted.sort(key=lambda x: -x[0])
        terms = [self._repr_term(term) for term in sorted]
        return join_sum_terms(terms)
    
    def with_par(self, parent):
        s = str(self)
        if " " in s:
            return f"({s})"
        return s
    