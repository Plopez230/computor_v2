# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    symbols.py                                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: plopez-b <plopez-b@student.42malaga.com    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/09/23 04:32:33 by plopez-b          #+#    #+#              #
#    Updated: 2024/09/24 03:40:01 by plopez-b         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from objects import *


class SymbolTable:

    def __init__(self):
        self.variables = {}
        self.variable_name = None
        self.function_name = None
        self.assignment_read = False

    def assign(self, name, value):
        self.variables[name] = value

    def new_line(self):
        self.variable_name = None
        self.function_name = None
        self.assignment_read = False

    def assignment(self):
        self.assignment_read = True

    def variable(self, name):
        if self.assignment_read:
            return self._value_or_variable(name)
        return self._value_or_declare(name)

    def function(self, name):
        if self.assignment_read:
            return self._function_or_error(name)
        return self._function_or_declare(name)

    def is_defined(self, v):
        if not v.is_defined:
            raise SyntaxError(f"Undefined symbol: {v.name}")

    def can_assign(self, o):
        if not o.is_function and not o.is_variable:
            raise SyntaxError("Can't assign value to expression")
    
    def _new_variable(self, name):
        set_variable(name)
        value = Polynomial([[Complex(1, 0), Complex(1, 0)]])
        value.name = name
        value.is_variable = True
        value.is_defined = False
        return value
    
    def _existing_variable(self, name):
        value = self.variables[name]
        value.name = name
        value.is_variable = True
        return value
        
    def _new_function(self, name):
        value = Complex(0, 0)
        value.name = name
        value.is_function = True
        value.is_defined = False
        return value
    
    def _existing_function(self, name):
        value = self.variables[name]
        value.name = name
        value.is_function = True
        return value

    def _value_or_variable(self, name):
        if name in self.variables:
            return self._existing_variable(name)
        if name == self.variable_name:
            return self._new_variable(name)
        raise SyntaxError(f"Undefined symbol: {name}")

    def _value_or_declare(self, name):
        if name in self.variables:
            return self._existing_variable(name)
        if not self.variable_name or self.variable_name == name:
            self.variable_name = name
            return self._new_variable(name)
        raise SyntaxError(f"Undefined symbol: {name}")

    def _function_or_error(self, name):
        if name in self.variables:
            return self._existing_function(name)
        raise SyntaxError(f"Undefined symbol: {name}")
        
    def _function_or_declare(self, name):
        if name in self.variables:
            return self._existing_function(name)
        if not self.function_name:
            self.function_name = name
            return self._new_function(name)
        
    def __repr__(self):
        result = ""
        for symbol in self.variables.keys():
            value = self.variables[symbol]
            if isinstance(value, Function):
                result += "Function "
            if isinstance(value, Complex):
                result += "Complex  "
            if isinstance(value, Matrix):
                result += "Matrix   "
            result += f"{symbol} : {value}"
            result += "\n"
        return result


symbol_table = SymbolTable()
