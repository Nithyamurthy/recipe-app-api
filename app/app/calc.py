"""
Calculator functions
"""

def add(x,y):
    return x + y

def subtract(x,y):
    if x > y:
        return x - y
    elif x < y:
        return y - x
    else:
        return 0
