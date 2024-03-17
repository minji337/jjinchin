def add(a, b):
    return a + b
def subtract(a, b):
    return a - b
def multiply(a, b):
    return a * b
def devide(a, b):
    return a / b

calc_dict = {"add": add, "multiply": multiply, "subtract": subtract, "devide": devide}
def func(func_name, a, b):
    return calc_dict[func_name](a, b)

print("add", func("add", 20, 2))
print("subtract", func("subtract", 20, 2))
print("multiply", func("multiply", 20, 2))
print("divide", func("divide", 20, 2))