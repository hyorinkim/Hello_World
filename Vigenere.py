N = [input() for _ in range(6)]


def vigenere(plain, key):
    charList = list(plain)
    keylist = list(key)
    keyLen = len(key)
    jump = 0
    for ind, ch in enumerate(charList):
        keyChar = keylist[ind % keyLen]  # 평문의 각 문자에 맞는 키를 찾는 것
        if 'z' >= keyChar and keyChar >= 'a':
            jump = ord(keyChar) - 97  # key:a~z 0~25로 매핑

            # 평문에서 암호문으로 바꿀때 카이사르처럼 띄어쓸 양 찾기
            if chr(ord(charList[ind]) + jump) > 'z':
                charList[ind] = chr(ord(charList[ind]) + jump - 26)
            else:
                charList[ind] = chr(ord(charList[ind]) + jump)
        elif 'Z' >= keyChar and keyChar >= 'A':
            jump = ord(keyChar) - 65  # key:A~Z 0~25로 매핑
            # 평문에서 암호문으로 바꿀때 카이사르처럼 띄어쓸 양 찾기
            if chr(ord(charList[ind]) + jump) > 'Z':
                charList[ind] = chr(ord(charList[ind]) + jump - 26)
            else:
                charList[ind] = chr(ord(charList[ind]) + jump)
    encrypt = ""
    print(encrypt.join(charList))


for i in range(5):
    vigenere(N[i], N[5])