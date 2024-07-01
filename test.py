def NoUseFunc():
    return 0

a = 1 # a is integer
b = False # b is bool
b = a # assign integer to bool

''' Abstract Syntax Tree:
(module
    (function_definition
        name: (identifier)
        parameters: (parameters)
        body: (block (return_statement (integer))))
    (expression_statement
        (assignment
            left: (identifier)
            right: (integer)))
    (comment)
    (expression_statement
        (assignment
            left: (identifier)
            right: (false)))
            (comment)
    (expression_statement
        (assignment
            left: (identifier)
            right: (identifier)))
    (comment))
'''
