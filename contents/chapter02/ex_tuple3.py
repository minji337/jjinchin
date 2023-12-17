def calculate(a, b):
    sum_result = a + b
    product_result = a * b
    return sum_result, product_result  # 튜플 패킹

# 언패킹하여 각 결과에 할당
sum_value, product_value = calculate(3, 4)
print("sum_value:", sum_value)
print("product_value:", product_value)
