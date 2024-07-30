# 단리 이자 계산기(days : 일수, rate : 이율, amount: 원금)
def calculate_simple_interest(days, rate, amount):
    print("입력값 ", days, rate, amount)
    return amount * days / 365 * rate

simple_interest = calculate_simple_interest(100, 0.04, 1000000)
print("이자1:", simple_interest)

simple_interest = calculate_simple_interest(200, 0.03, 5000000)
print("이자2:", simple_interest)
