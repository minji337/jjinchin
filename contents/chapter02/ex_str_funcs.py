# split는 문자열을 지정된 구분자에 따라 분리하는 함수입니다.
text = "김민지 and 고비"
result = text.split(" and ")
print(f"split: {result}")
# replace는 문자열의 일부(또는 전부)를 다른 문자열로 교체하는 함수입니다.
result = text.replace("and", "그리고")
print(f"replace: {result}")
