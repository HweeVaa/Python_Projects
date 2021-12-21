import RPi.GPIO as GPIO
import Adafruit_DHT as dht
import time

GPIO.setwarnings (False)

GPIO.setmode(GPIO.BCM)
DHT = 17
pin = 4
led = 13

GPIO.setup(23,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(led,GPIO.OUT)
GPIO.setup(pin,GPIO.IN)

h,t = dht.read_retry(dht.DHT22, DHT)#온습도 감지
Humi = [round(h,2)]#습도저장 배열

b=0#진동이벤트
c=0#소리이벤트
i=0#메인이벤트(습도, 안개)
d=0#비 이벤트
try:
    while True:
        f = open("Humi_vib.xlsx","a")#데이터 시트 호출
        #wtime = datetime.datetime.now()#데이터 시트에 시간정보 저장
        #1) 상황인식에 도움을 줄 수 있는 센서를 선정하고 네트워크를 연결한다.
        #2) 각 센서들은 상황과 관련한 물리적 화학적 감지결과를 보고한다. 
        h,t = dht.read_retry(dht.DHT22, DHT)#습도 센서
        result = GPIO.input(23)#진동 센서
        soundlevel = GPIO.input(pin)#소리 센서
        #3) 호스트에서 이벤트를 탐색한다. 
        if h>=85 and d == 0:#습도 85이상, 비 이벤트 x -> 메인 이벤트 시작
            i+=1#메인이벤트 시작
            Humi.append(round(h,2))#습도 배열에 습도 데이터 저장, 85 이상의 습도데이터만 배열에 저장된다
            #4) 이벤트가 감지된 센서 데이터가 있을 때, 다른 센서 데이터에서도 이벤트가 발생하였는지 여부를 탐색한다.
            if result == 1:#진동감지
                print("진동 감지")
                b+=1#진동 이벤트 시작
                if soundlevel == 1:#진동이 감지되면 소리유무를 판단한다
                    print("소리 감지")
                    c+=1#소리 이벤트 시작
                else:
                    print("소리 없음")
                    c=0#소리 이벤트 초기화
            else:
                print("진동 없음")
                b=0#진동 이벤트 초기화
                c=0#소리 이벤트 초기화
        #5) 이벤트가 감지된 센서 데이터의 이벤트가 감소 양상을 보일 때, 해당 센서의 이벤트 데이터를 접수하지 않는다.
        #13) 각 센서의 이벤트 데이터가 감소 양상으로 접어 든 후 이벤트 보고 중단되는 센서가 이벤트 보고를 다시 재개하지 않을 때, 데이트 스트림 분석을 중단한다. 
        #14) 남은 센서의 이벤트 보고가 중단될 때, 스트림에 대한 접수 및 저장을 중단한다. 
        elif h<85:#습도 85 미만 -> 메인 이벤트 종료
            GPIO.output(led,False)
            X = "습도 : {},습도부족,-> 안개X\n".format(round(h,2))
            f.writelines(X)#데이터 시트에 저장
            Humi = []#습도 배열 초기화
            i=0#메인 이벤트 초기화
            b=0#진동 이벤트 초기화
            c=0#소리 이벤트 초기화
            d=0#비 이벤트 초기화
            print(X)

        print(round(h,2))
        print(Humi)
        print(b)
        print(c)
        #6) 다른 센서 데이터에서 이벤트가 발생하지 않을 때, 이벤트가 감지된 센서 데이터의 이벤트 변화 양상을 관찰한다.
        if i>=5 and d == 0:#85 이상의 습도가 5번 이상 감지되면 메인 이벤트 시작
            if Humi[i-5] >= 85 and Humi[i-4] >= 85 and Humi[i-3] >= 85 and Humi[i-2] >= 85 and Humi[i-1] >= 85:#배열의 모든 원소가 85 이상이면 시작,
                #7) 이벤트 발생 센서 데이터의 이벤트가 증가 양상을 보일 때, 계속 다른 센서 데이터의 이벤트 발생을 탐색한다.
                #8) 다른 센서 데이터의 이벤트 발생이 감지되었을 때, 이 때부터 각 센서 데이터의 데이터들을 접수하고 저장하기 시작한다. 
                #9) 각 센서 데이터가 이벤트 지속되는 것을 확인하며 일정한 시간 간격으로 분할하며 분석한다. 
                if b<=2:#진동이벤트가 없으면 안개라고 판단한다      
                    P = "습도 : {}, 진동OFF,-> 안개\n".format(Humi[i-1])
                    f.writelines(P)
                    print(P)
                    GPIO.output(led,True)
                elif b>=3 and c<=2:#진동이벤트가 3 이상이라면 비라고 판단한다
                    GPIO.output(led,False)
                    Q = "습도 : {}, 진동ON 소리OFF,-> 우천 가능\n".format(Humi[i-1])
                    f.writelines(Q)
                    print(Q)
                    d = 1#비 이벤트 시작
                elif b>=3 and c>=3:#진동이벤트와 소리이벤트 모두 3 이상이라면 확실한 비라고 판단한다
                    GPIO.output(led,False)
                    R = "습도 : {}, 진동ON 소리ON,-> 우천 확실\n".format(Humi[i-1])
                    f.writelines(R)
                    print(R)
                    d = 1#비 이벤트 시작

                    #10) 각 센서 데이터의 이벤트의 변화가 감소양상으로 가는지 탐색한다.
                    #11) 각 센서 데이터의 이벤트 중에서 중단되는 것이 있는지 탐색한다. 
                    #11) 감소양상으로 접어 든 이후 이벤트가 중단되는 센서 데이터가 있을 경우 다시 이벤트가 발생하는지 탐색한다. 
                    #12) 이벤트가 중단된 센서 데이터에서 다시 이벤트가 발생하여 지속 하면 9)~11)과정을 지속한다. 
        
        elif i < 5 and h >= 85:#메인 이벤트 판단, 습도가 85 이상이 5번 이상 유지되면 메인이벤트 시작
            GPIO.output(led,False)
            X = "습도 : {},,-> 안개의심\n".format(round(h,2))
            f.writelines(X)
            print(X)

        if d==1:#우천 후 이벤트
            GPIO.output(led,False)
            Z = "습도 : {},,->우천후\n".format(round(h,2))
            f.writelines(Z)
            print(Z)
        time.sleep(2)#2초마다 데이터를 받는다.

except KeyboardInterrupt:
    exit(0)