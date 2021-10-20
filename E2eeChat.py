import socket
import threading
import base64
#바이트스트림 아스키코드로 바꾸기 위해 인코딩 디코딩
from Cryptodome import Random
from Cryptodome.Cipher import AES

BLOK_SIZE=16
#16바이트 = 128bit

def __init__(self,key):
    iv=bytes([0x00]*16)#Initial vector 0으로 초기화 후 16바이트 할당
    self.crypto=AES.new(key,AES.MODE_CBC,iv)

def encrypt(self,data):
    #암호화 메세지 16의 배수여야한다.
     enc=self.crypto.encrypt(data)
     return enc

def decrypt(self, enc):
    #복호화 메세지 16의 배수여야한다.
    dec= self.crypto.decrypt(enc)
    return dec






# 서버 연결정보; 자체 서버 실행시 변경 가능
SERVER_HOST = "homework.islab.work"
SERVER_PORT = 8080

connectSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connectSocket.connect((SERVER_HOST, SERVER_PORT))

def socket_read():
    while True:
        readbuff = connectSocket.recv(2048)

        if len(readbuff) == 0:
            continue

        recv_payload = readbuff.decode('utf-8')
        parse_payload(recv_payload)

def socket_send():
    while True:
        #상대방에게 내가 누구인지를 알리는 코드 즉 서버에 로그인 하는 코드
        #두클라이언트는 키를 교환해야지 메세지를 주고 받을 수 있다.키를 전달해준 클라이언트1과는 정해진 Algo방법으로 암호화 복호화한다.
        # 키를 전달받은 클라이언트2는 RELAYOK 를 받고 IV와 키를 받았으니까 배열에다가 저장해둔다.
        #BASE64알고리즘 사요앻서 키와 IV를 바꿀것
        #그리고 전달한 클라이언트1는 키가 제대로 전달 되었는지 확인할 수 있도록 전달받은 클라리언트2가 KEYXCHGOK메소드를 보내준다.
        #그래서 해당키와 알고리즘 방식으로 메세지를 교환할 것이다. NONCE는 메세지를 구분하기위한 난수 랜덤하게 아무거이나 사용해라?
        # 클라이언트1은 MSGSEND 메소드를 사용한다. 바디에 암호화된 메세지를 넣어서 전송한다.
        # 클라이언트1은 MESGSENDOK라는 것을 서버로 부터 받는다.
        #클라이언트2는 MSGRECV를 받았고 암호화된 메세지를 받을 것이다.
        str = input("Preamble: CONNECT or KEYXCHG ").split(" ")
        if str[1]=="CONNECT" or str[1]=="DISCONNECT":
            st=str[0]+" "+str[1]+"\n"
            st+=input("Credential : name ")
        elif str[1]== "KEYXCHG":
            st=str[0]+" "+str[1]+"\n"
            st+="Algo: "
            st+=input("Algo: ")
            st+="\n"
            st+="From: "
            st+=input("From:")
            st+="\n"
            st+="To: "
            st+=input("To: ")
            st+="\n"+"\n"
            Body_Key_IV=input("Body: ")#여기에 평문을 입력받는데 상대클라이언트한테는
            # 암호화된 문장이 전달되어야함
            body_bytes=Body_Key_IV.encode()

        #str+="\n"
        #str+=input("CONNECT-> Credential: or KEYXCHG-> Algo: ,From:, To:, Key")

        # str=[]
        # for _ in range():
        #     str.append(input())
        #3EPROTO
        #Algo: AES-256-CBC
        #From: CNU-InfoSecUser
        #TO: CNU-InfoSecUser2
        #
        send_bytes = st.encode('utf-8')
        print(send_bytes)# 어떻게 나오지?
        connectSocket.sendall(send_bytes)
#예쁜 UI?를 해야된다고? 터미널 창으로 해도 된당!!
def parse_payload(payload):
    # 수신된 페이로드를 여기서 처리; 필요할 경우 추가 함수 정의 가능
    print(payload)
    pass

reading_thread = threading.Thread(target=socket_read)
sending_thread = threading.Thread(target=socket_send)

reading_thread.start()
sending_thread.start()

reading_thread.join()
sending_thread.join()