fruits = {'수박': '박과의 여름과일', '사과': '사과나무의 열매', '딸기': '나무딸기속 식물'}
print('모든 과일:', fruits['수박'], fruits['사과'], fruits['딸기'])

fruits['포도'] = '덩굴성 자줏빛 과일'
del fruits['수박']

# fruits에 담긴 Key들을 가져와 fruits_keys에 담는다
fruits_keys = fruits.keys()

# list(...) 함수를 통해 fruits_keys의 데이터를 리스트 데이터 형식으로 변경한다.
fruits_keys_list = list(fruits_keys) 


# fruits에 담긴 Value들을 가져와 fruits_values에 담는다.
fruits_values = fruits.values()

# list(...;) 함수를 통해 fruits_values의 데이터를 리스트 데이터 형식으로 변경한다.
fruits_values_list = list(fruits_values) 

print("fruits_keys_list: ", fruits_keys_list)
print("fruits_values_list: ", fruits_values_list)
