## Module file for add, sub, multi, and div functions

def add(x,y):
    
    try:
        float(x), float(y)
        return x + y
    except ValueError:
        print("Must be numeric")
        

def sub(x,y):

    try:
        float(x), float(y)
        return x - y
    except ValueError:
        print("Must be numeric")
        return None

def mult(x,y):
    
    try:
        float(x), float(y)
        return x * y
    except ValueError:
        print("Must be numeric")
        
def div(x,y):
    
    try:
        float(x), float(y)
        return x / y
    except ValueError:
        print("Must be numeric")
    except ZeroDivisionError:
        print("Can not divide by zero")
 