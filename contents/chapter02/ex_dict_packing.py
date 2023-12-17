def func2(x, y):
    print("func2:", x + y)

def func1(**kwargs):
    print("type(kwargs):", type(kwargs), kwargs)
    print("func1:", kwargs['x'] + kwargs['y'])
    func2(**kwargs) 

func1(x=10, y=20)
