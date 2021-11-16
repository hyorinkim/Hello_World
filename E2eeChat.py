import socket
import threading
import base64
from datetime import datetime
#바이트스트림 아스키코드로 바꾸기 위해 인코딩 디코딩
from Cryptodome import Random
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad,unpad

BLOK_SIZE=16
#블록크기 128bit = 16바이트
# Key 길이가 256bit = 32바이트
#IV는 128bit =16바이트
RecieveKey=None#전달받은 키 보관
RecieveIv=None#전달받은 IV 보관

ChgFail=False#키 전송과정 문제로 실패인지 확인
ChgDuplicate=False#키가 중복되서 실패인지 확인

#키교환 시점에서 랜덤한 키와 랜덤 IV를 생성
class E2eeChat:
    def __init__(self,key,iv):
        #iv=bytes([0x00]*16)#Initial vector 0으로 초기화 후 16바이트 할당
        #iv = Random.new().read(BLOK_SIZE)#랜덤한 iv생성
        #key = key.encode('utf-8')
        #iv = iv.encode('utf-8')
        self.crypto=AES.new(key,AES.MODE_CBC,iv)


    def encrypt(self,data):
        #암호화 메세지 16의 배수여야한다.
         enc = self.crypto.encrypt(pad(data,BLOK_SIZE))#블록 사이즈에 맞게 빈공간을 채워주는 pad함수 사용
        #다음에 encrypt 암호화 수행
         enc=str(base64.b64encode(enc),encoding="utf-8")#스트링타입으로 변환
         #print("암호환 것: "+enc)#암호화 되었는지 확인함
         return enc

    def decrypt(self, enc):
        #복호화 메세지 16의 배수여야한다.

        dec = base64.b64decode(enc.encode("utf-8"))#암호화한 문장을 base64로 decode시킴
        dec = self.crypto.decrypt(dec)
        # print("복호화 한것: ")
        # print(dec.decode("utf-8"))#복호화 잘 되는지 확인
        return unpad(dec, BLOK_SIZE).decode("utf-8")#원래 문장의 크기로 되돌림 unpad






# 서버 연결정보; 자체 서버 실행시 변경 가능
SERVER_HOST = "homework.islab.work"
SERVER_PORT = 8080

connectSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connectSocket.connect((SERVER_HOST, SERVER_PORT))

def socket_read():#메세지 받는함수
    while True:
        readbuff = connectSocket.recv(2048)

        if len(readbuff) == 0:
            continue

        recv_payload = readbuff.decode('utf-8')
        parse_payload(recv_payload)

def socket_send():#메세지 보내는 함수
    global  User1#암호화와 복호화 하기 위한 객체 선언
    while True:
        str = input("3EPROTO CONNECT or KEYXCHG ").split(" ")

        if str[1]=="CONNECT" or str[1]=="DISCONNECT":
            st=str[0]+" "+str[1]+"\n"
            st+=input("Credential : name ") #상대방에게 내가 누구인지를 알리는 코드 즉 서버에 로그인 하는 코드
        
        elif str[1]=="KEYXCHGOK": #전달한 클라이언트1는 키가 제대로 전달 되었는지 확인할 수 있도록 전달받은 클라리언트2가 KEYXCHGOK메소드를 보내준다.
            st = str[0] + " " + str[1] + "\n"
            st += input("Algo: ")
            st += "\n"
            st += input("From:")
            st += "\n"
            st += input("To: ")
            st += "\n"
        elif str[1]== "KEYXCHG": #두클라이언트는 키를 교환해야지 메세지를 주고 받을 수 있다.키를 전달해준 클라이언트1과는 정해진 Algo방법으로 암호화 복호화한다.
            st=str[0]+" "+str[1]+"\n"
            st+=input("Algo: ")
            st+="\n"
            st+=input("From:")
            st+="\n"
            st+=input("To: ")
            st+="\n"+"\n"
            Body_Key=input("Body: ")#여기에 평문을 입력받는데 상대클라이언트한테는
            Body_iv=input("Iv: ")

            # 키랑 Iv를 입력 받는 경우
            st+=Body_Key+"\n"+Body_iv
            Body_Key=Body_Key.encode('utf-8')
            Body_iv=Body_iv.encode('utf-8')
            User1=E2eeChat(Body_Key,Body_iv)#키와 IV로 암호화 하는 객체 생성

        elif str[1] == "KEYXCHGRST":#키를 바꾸고 싶을 때
            st=str[0]+" "+str[1]+"\n"
            st+=input()+"\n"#Algo
            st+=input()+"\n"#from
            st+=input()#to
            st+="\n"+"\n"
            st+=input()#key
            st+="\n"
            st+=input()#iv
        elif str[1]=="KEYXCHGFAIL":#키전송이 FAIl임을 알려줄 때
            st = str[0] + " " + str[1] + "\n"
            st += input("Algo: ")
            st += "\n"
            st += input("From:")
            st += "\n"
            st += input("To: ")
            st += "\n"
            if ChgFail:#키가 없을 때
                st+="Miss key"
            if ChgDuplicate:#키가 중복 되었을 때
                st+"Duplicated Key Exchange Request"
        elif str[1] == "MSGSEND":#메세지를 보낼 때
            st = str[0]+" "+str[1]+"\n"#3EPROTO MSGEND
            st += input()+"\n"#From
            st += input()+"\n"#To
            st += input()#Nonce
            st+="\n"+"\n"
            msg=input()#message
            # 클라이언트1은 MSGSEND 메소드를 사용한다. 바디에 암호화된 메세지를 넣어서 전송한다.
            st+=User1.encrypt(msg.encode('utf-8'))#암호화해서 보내기

        send_bytes = st.encode('utf-8')
        connectSocket.sendall(send_bytes)#전송
        
def parse_payload(payload):
    global RecieveKey #받은 키
    global RecieveIv #받은 IV
    global ChgDuplicate #키 교환시 키가 이미 있을때 중복되었을 때
    global ChgFail #키 교환시 키가 잘못왔을때 키가 없을때
    # 수신된 페이로드를 여기서 처리; 필요할 경우 추가 함수 정의 가능
    segment1=payload.split("\n")
    segment2=segment1[0].split(" ")
    # print(segment1)#전달받은 payload 확인용
    if segment2[1]=="KEYXCHG":
        #키가 중복인지 체크하기
        if RecieveKey is not None:  # 키가 이미 있어요
            print("키 이미 받았다. KEYXCHGFAIL 전송하라.")
            ChgDuplicate=True
            #직접 입력으로 KEYFAIL을 보내기 때문에 socket_send함수내에 구현됨
            return


        print("key 받았다.")
        RecieveKey = segment1[6].encode('utf-8')
        RecieveIv = segment1[7].encode('utf-8')
        #받은 키와 IV를 저장해두는 부분
        
        # print("CHG RecieveKey:")
        # print(RecieveKey)
        # print("CHG RecieveIv:")
        # print(RecieveIv) #받은 키와IV 확인하는 부분

        #키를 받았는데 그 키 값이 잘 못 되었는지 확인하는 부분
        if RecieveKey == "" or RecieveKey is None:  # keyxchg fail일때
            print("키가 잘못 됐다. KEYXCHGFAIL전송하라.")
            ChgFail=True
            # 직접 입력으로 KEYFAIL을 보내기 때문에 socket_send함수내에 구현됨
            return

        return #KEYOK일때 # 직접 입력으로 KEYOK를 보내기 때문에 socket_send함수내에 구현됨
    elif segment2[1]=="KEYXCHGRST":
        print("키바꾸기 성공")
        RecieveKey = segment1[6].encode('utf-8')
        RecieveIv = segment1[7].encode('utf-8')
        #재전송받은 KEY와 IV값으로 교체한다. 

        return #KEYOK보내야함 # 직접 입력으로 KEYOK를 보내기 때문에 socket_send함수내에 구현됨

    if segment2[1]=="MSGRECV":#메세지를 받았을 때
        receiver = E2eeChat(RecieveKey,RecieveIv)#받아서 저장해둔 키와 IV로 복호화할 수 있는 객체를 생성
        encmsg=segment1[5]#받은 메세지
        # print("받은 메세지")
        # print(encmsg)#메세지가 암호화 되어있는지 확인해봄
        decmsg=receiver.decrypt(encmsg)
        payload=payload.replace(encmsg,decmsg)#메세지를 받는 클라이언트에겐 복호화된 메세지로 보여야하니까지 payload에 메세지 부분을 복호화 된것으로 바꿔줌


    print(payload)
    pass

reading_thread = threading.Thread(target=socket_read)
sending_thread = threading.Thread(target=socket_send)

reading_thread.start()
sending_thread.start()

reading_thread.join()
sending_thread.join()