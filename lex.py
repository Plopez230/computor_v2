# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    calclex.py                                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: plopez-b <plopez-b@student.42malaga.com    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/09/21 02:27:59 by plopez-b          #+#    #+#              #
#    Updated: 2024/09/21 02:50:22 by plopez-b         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import ply.lex as lex

# List of token names.   This is always required
tokens = (
    # OPERATIONS
    'PLUS',
    'MINUS',
    'TIMES',
    'TIMESMATRIX',
    'DIVIDE',
    'POWER',
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
    # LITERALS
    'RATIONAL',
    'IDENTIFIER',
    # RESERVED WORDS
    'IMAGINARY',
)

# Reserved words 
reserved = {
    'i' : 'IMAGINARY',
}

# Regular expression rules for simple tokens
t_PLUS          = r'\+'
t_MINUS         = r'-'
t_TIMES         = r'\*'
t_TIMESMATRIX   = r'\*\*'
t_DIVIDE        = r'/'
t_POWER         = r'\^'
t_MODULUS       = r'\%'
t_ASSIGNMENT    = r'\='
t_LPAREN        = r'\('
t_RPAREN        = r'\)'
t_LBRACK        = r'\['
t_RBRACK        = r'\]'
t_SEMICOLON     = r'\;'
t_COMMA         = r'\,'

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
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()


# Test it out
data = ''' =
3 + [4 * .10]
  + -20 *2 i I+ hola * ** / ^ %
'''

# Give the lexer some input
lexer.input(data)

# Tokenize
while True:
    tok = lexer.token()
    if not tok: 
        break      # No more input
    print(tok)