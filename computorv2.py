# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    computorv2.py                                      :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: plopez-b <plopez-b@student.42malaga.com    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/09/24 04:34:24 by plopez-b          #+#    #+#              #
#    Updated: 2024/09/24 05:13:19 by plopez-b         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from exceptions import *
from symbols import symbol_table
from yacc import parser

while True:
    try:
        print ("\033[1;34m", end="")
        s = input('> ')
        print ("\033[0m", end="")
    except EOFError:
        break
    if not s: continue
    try:
        symbol_table.new_line()
        result = parser.parse(s)
        print(f"\033[1;32m{result}\033[0m")
    except SyntaxError as e:
        print (f"\033[1;31m{e}\033[0m")
    except MathError as e:
        print (f"\033[1;31mMath error: {e}\033[0m")
    except ZeroDivisionError as e:
        print (f"\033[1;31mDivision by 0\033[0m")
