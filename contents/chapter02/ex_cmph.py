# 0 ~ 9까지 중에서 짝수 선별
even_numbers = [v for v in range(10) if v % 2 == 0]
print("even_numbers:",even_numbers)

# 과일별 색깔의 길이 작성
fruits = {"apple": "red", "banana": "yellow", "grape": "purple"}
fruit_color_length = {fruit: len(color) for fruit, color in fruits.items()}
print("fruit_color_length:",fruit_color_length)
