def func():
    print("func 입니다")
    
def main():
    print("main 함수가 여러 가지 작업을 수행 중에 있습니다.")
    func()
    
print(f"__name__은 {__name__}입니다.") 
    
if __name__ == "__main__":
    print("main으로 실행되었습니다.") 
    main()
