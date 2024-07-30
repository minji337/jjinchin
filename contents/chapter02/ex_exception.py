try:
    result = 10 / 0
except ZeroDivisionError as ze:
    print(f"0으로 나눌 수 없습니다: {str(ze)}")
else:
    print(f"결과는 {result}입니다.")
finally:
    print("예외 처리가 완료되었습니다.")
