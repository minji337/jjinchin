def func(a, b=20):
    return a + b

print(func(10)) #30 출력
print(func(a=10)) #30 출력
print(func(b=10)) #TypeError: func() missing 1 required positional argument: 'a'
