class Car:

    def __init__(self):
        self.speed = 0  # 초기 속도

    def accelerate(self, speed_increase):
        self.speed += speed_increase  # 속도 증가로 self.speed = self.speed + speed_increase와 동일
        print("가속 후 속도:", self.speed)

    def decelerate(self, speed_decrease):
        if self.speed >= speed_decrease:  # 감속할 속도가 현재 속도 이상인지 확인
            self.speed -= speed_decrease  # 속도 감소로 self.speed = self.speed - speed_decrease 동일
            print("감속 후 속도:", self.speed)
        else:
            self.stop()

    def stop(self):
        self.speed = 0
        print("자동차가 멈췄습니다.")

car = Car() 
car.accelerate(10)  # 시속 10킬로미터 가속
car.accelerate(20)  # 시속 20킬로미터 추가 가속
car.decelerate(20)  # 시속 20킬로미터 감속
car.decelerate(20)  # 시속 20킬로미터 추가 감속
