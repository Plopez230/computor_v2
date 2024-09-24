# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    lex.py                                             :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: plopez-b <plopez-b@student.42malaga.com    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/09/21 02:27:59 by plopez-b          #+#    #+#              #
#    Updated: 2024/09/24 05:03:14 by plopez-b         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import ply.lex as lex
from exceptions import *

# List of token names.   This is always required
tokens = (
    # OPERATIONS
    'PLUS',
    'MINUS',
    'TIMES',
    'TIMESMATRIX',
    'DIVIDE',
    'POWER',
    'POWERMATRIX',
    'MODULUS',
    'ASSIGNMENT',
    # PARENTHESIS
    'LPAREN',
    'RPAREN',
    'LBRACK',
    'RBRACK',
    # PUNCTUATION
    'SEMICOLON',
    'COMMA',
    'QUESTION',
    # LITERALS
    'RATIONAL',
    'IDENTIFIER',
    # RESERVED WORDS
    'IMAGINARY',
    'SYMBOLS',
)

# Reserved words 
reserved = {
    'i' : 'IMAGINARY',
    'symbols': "SYMBOLS",
}

# Regular expression rules for simple tokens
t_PLUS          = r'\+'
t_MINUS         = r'-'
t_TIMES         = r'\*'
t_TIMESMATRIX   = r'\*\*'
t_DIVIDE        = r'/'
t_POWER         = r'\^'
t_POWERMATRIX   = r'\^\^'
t_MODULUS       = r'\%'
t_ASSIGNMENT    = r'\='
t_LPAREN        = r'\('
t_RPAREN        = r'\)'
t_LBRACK        = r'\['
t_RBRACK        = r'\]'
t_SEMICOLON     = r'\;'
t_COMMA         = r'\,'
t_QUESTION      = r'\?'

def t_RATIONAL(t):
    r'([0-9]+[.]?[0-9]*)|([0-9]*[.]?[0-9]+)'
    t.value = float(t.value)
    return t

def t_IDENTIFIER(t):
    r'[a-zA-Z]+'
    t.value = t.value.lower()
    t.type = reserved.get(t.value, 'IDENTIFIER')
    return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    c = t.value[0]
    raise SyntaxError(f"Illegal character: {c}")

# Build the lexer
lexer = lex.lex()
