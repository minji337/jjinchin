def func2():
    try:
        print(10 / 0)
    except ZeroDivisionError as ze:
        print(f"0으로 나눌 수 없습니다.")
        raise ze

def func1():
    try:
        func2()
    except ZeroDivisionError:
        print(f"func2에서 예외가 발생했습니다.")

func1()
