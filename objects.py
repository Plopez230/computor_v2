# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    objects.py                                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: plopez-b <plopez-b@student.42malaga.com    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/09/21 17:25:26 by plopez-b          #+#    #+#              #
#    Updated: 2024/09/21 18:22:27 by plopez-b         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import math

class Complex:
    
    def __init__(self, real, imaginary):
        self.r = real
        self.i = imaginary

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

    def __sub__(self, other):
        if isinstance(other, Complex):
            return Complex(self.r - other.r,
                           self.i - other.i)
        
    def __mul__(self, other):
        if isinstance(other, Complex):
            return Complex(self.r * other.r - self.i * other.i,
                           self.r * other.i + self.i * other.r)
        
    def __truediv__(self, other):
        if isinstance(other, Complex):
            return Complex((self.r * other.r + self.i * other.i)
                           / (other.r ** 2 + other.i ** 2),
                           (self.i * other.r - self.r * other.i)
                           / (other.r ** 2 + other.i ** 2))
        
    def __pow__(self, other):
        if isinstance(other, Complex):
            return (other * self.log()).exp()
        
    def __mod__(self, other):
        if isinstance(other, Complex):
            return self + other * (-self / other).ceil()

    def __repr__(self):
        if self.i != 0 and self.r != 0:
            return f"{self.r} + {self.i} * i"
        if self.i != 0:
            return f"{self.i} * i"
        if self.r != 0:
            return f"{self.r}"
        else:
            return f"{self.r}"
