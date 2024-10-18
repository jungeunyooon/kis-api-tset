import websockets
import json
import requests
import os
import asyncio
import time

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from base64 import b64decode

clearConsole = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')

def stockhoka(data):
    recvvalue = data.split('^')  # 수신데이터를 split '^'

    print("유가증권 단축 종목코드 [" + recvvalue[0] + "]")
    print("영업시간 [" + recvvalue[1] + "]" + "시간구분코드 [" + recvvalue[2] + "]")
    print("======================================")
    print("매도호가10 [%s]    잔량10 [%s]" % (recvvalue[12], recvvalue[32]))
    print("매도호가09 [%s]    잔량09 [%s]" % (recvvalue[11], recvvalue[31]))
    print("매도호가08 [%s]    잔량08 [%s]" % (recvvalue[10], recvvalue[30]))
    print("매도호가07 [%s]    잔량07 [%s]" % (recvvalue[9], recvvalue[29]))
    print("매도호가06 [%s]    잔량06 [%s]" % (recvvalue[8], recvvalue[28]))
    print("매도호가05 [%s]    잔량05 [%s]" % (recvvalue[7], recvvalue[27]))
    print("매도호가04 [%s]    잔량04 [%s]" % (recvvalue[6], recvvalue[26]))
    print("매도호가03 [%s]    잔량03 [%s]" % (recvvalue[5], recvvalue[25]))
    print("매도호가02 [%s]    잔량02 [%s]" % (recvvalue[4], recvvalue[24]))
    print("매도호가01 [%s]    잔량01 [%s]" % (recvvalue[3], recvvalue[23]))
    print("--------------------------------------")
    print("매수호가01 [%s]    잔량01 [%s]" % (recvvalue[13], recvvalue[33]))
    print("매수호가02 [%s]    잔량02 [%s]" % (recvvalue[14], recvvalue[34]))
    print("매수호가03 [%s]    잔량03 [%s]" % (recvvalue[15], recvvalue[35]))
    print("매수호가04 [%s]    잔량04 [%s]" % (recvvalue[16], recvvalue[36]))
    print("매수호가05 [%s]    잔량05 [%s]" % (recvvalue[17], recvvalue[37]))
    print("매수호가06 [%s]    잔량06 [%s]" % (recvvalue[18], recvvalue[38]))
    print("매수호가07 [%s]    잔량07 [%s]" % (recvvalue[19], recvvalue[39]))
    print("매수호가08 [%s]    잔량08 [%s]" % (recvvalue[20], recvvalue[40]))
    print("매수호가09 [%s]    잔량09 [%s]" % (recvvalue[21], recvvalue[41]))
    print("매수호가10 [%s]    잔량10 [%s]" % (recvvalue[22], recvvalue[42]))
    print("======================================")
    print("총매도호가 잔량        [%s]" % (recvvalue[43]))
    print("총매도호가 잔량 증감   [%s]" % (recvvalue[54]))
    print("총매수호가 잔량        [%s]" % (recvvalue[44]))
    print("총매수호가 잔량 증감   [%s]" % (recvvalue[55]))
    print("시간외 총매도호가 잔량 [%s]" % (recvvalue[45]))
    print("시간외 총매수호가 증감 [%s]" % (recvvalue[46]))
    print("시간외 총매도호가 잔량 [%s]" % (recvvalue[56]))
    print("시간외 총매수호가 증감 [%s]" % (recvvalue[57]))
    print("예상 체결가            [%s]" % (recvvalue[47]))
    print("예상 체결량            [%s]" % (recvvalue[48]))
    print("예상 거래량            [%s]" % (recvvalue[49]))
    print("예상체결 대비          [%s]" % (recvvalue[50]))
    print("부호                   [%s]" % (recvvalue[51]))
    print("예상체결 전일대비율    [%s]" % (recvvalue[52]))
    print("누적거래량             [%s]" % (recvvalue[53]))
    print("주식매매 구분코드      [%s]" % (recvvalue[58]))

def stockspurchase(data_cnt, data):
    print("============================================")
    menulist = "유가증권단축종목코드|주식체결시간|주식현재가|전일대비부호|전일대비|전일대비율|가중평균주식가격|주식시가|주식최고가|주식최저가|매도호가1|매수호가1|체결거래량|누적거래량|누적거래대금|매도체결건수|매수체결건수|순매수체결건수|체결강도|총매도수량|총매수수량|체결구분|매수비율|전일거래량대비등락율|시가시간|시가대비구분|시가대비|최고가시간|고가대비구분|고가대비|최저가시간|저가대비구분|저가대비|영업일자|신장운영구분코드|거래정지여부|매도호가잔량|매수호가잔량|총매도호가잔량|총매수호가잔량|거래량회전율|전일동시간누적거래량|전일동시간누적거래량비율|시간구분코드|임의종료구분코드|정적VI발동기준가"
    menustr = menulist.split('|')
    pValue = data.split('^')
    i = 0
    for cnt in range(data_cnt):     # 넘겨받은 체결데이터 개수만큼 print 한다
        print("### [%d / %d]"%(cnt+1, data_cnt))
        for menu in menustr:
            print("%-13s[%s]" % (menu, pValue[i]))
            i += 1

def stocksigningnotice(data, key, iv):
    menulist = "고객ID|계좌번호|주문번호|원주문번호|매도매수구분|정정구분|주문종류|주문조건|주식단축종목코드|체결수량|체결단가|주식체결시간|거부여부|체결여부|접수여부|지점번호|주문수량|계좌명|체결종목명|신용구분|신용대출일자|체결종목명40|주문가격"
    menustr1 = menulist.split('|')

    # AES256 처리 단계
    aes_dec_str = aes_cbc_base64_dec(key, iv, data)
    pValue = aes_dec_str.split('^')

    i = 0
    for menu in menustr1:
        print("%s  [%s]" % (menu, pValue[i]))
        i += 1

def aes_cbc_base64_dec(key, iv, cipher_text):
    """
    :param key:  str type AES256 secret key value
    :param iv: str type AES256 Initialize Vector
    :param cipher_text: Base64 encoded AES256 str
    :return: Base64-AES256 decoded str
    """
    cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC, iv.encode('utf-8'))
    return bytes.decode(unpad(cipher.decrypt(b64decode(cipher_text)), AES.block_size))

def get_approval(key, secret):
    """웹소켓 접속키 발급"""
    url = 'https://openapi.koreainvestment.com:9443'
    headers = {"content-type": "application/json"}
    body = {"grant_type": "client_credentials",
            "appkey": key,
            "secretkey": secret}
    PATH = "oauth2/Approval"
    URL = f"{url}/{PATH}"
    res = requests.post(URL, headers=headers, data=json.dumps(body))
    approval_key = res.json()["approval_key"]
    return approval_key

# TPS 측정을 위한 변수 초기화
message_count = 0
start_time = time.time()

async def connect():
    global message_count, start_time
    g_appkey = ''
    g_appsceret = ''
    stockcode = '005930'    # 테스트용 임시 종목 설정, 삼성전자
    htsid = 'angal231'    # 체결통보용 htsid 입력
    custtype = 'P'      # customer type, 개인:'P' 법인 'B'
    url = 'ws://ops.koreainvestment.com:31000' # 모의투자

    g_approval_key = get_approval(g_appkey, g_appsceret)
    print("approval_key [%s]" % (g_approval_key))

    async with websockets.connect(url, ping_interval=60) as websocket:
        while True:
            print("1.주식호가, 2.주식호가해제, 3.주식체결, 4.주식체결해제, 5.주식체결통보(고객), 6.주식체결통보해제(고객), 7.주식체결통보(모의), 8.주식체결통보해제(모의)")
            print("Input Command :")
            cmd = input()

            if not cmd.isdigit() or int(cmd) not in range(9):
                print("> Wrong Input Data", cmd)
                continue  

            if cmd == '0':
                print("Exit!!")
                break

            # 입력값에 따라 요청 처리
            if cmd == '1':  # 주식호가 등록
                tr_id = 'H0STASP0'
                tr_type = '1'
            elif cmd == '2':  # 주식호가 등록해제
                tr_id = 'H0STASP0'
                tr_type = '2'
            elif cmd == '3':  # 주식체결 등록
                tr_id = 'H0STCNT0'
                tr_type = '1'
            elif cmd == '4':  # 주식체결 등록해제
                tr_id = 'H0STCNT0'
                tr_type = '2'
            elif cmd == '5':  # 주식체결통보 등록(고객용)
                tr_id = 'H0STCNI0'
                tr_type = '1'
            elif cmd == '6':  # 주식체결통보 등록해제(고객용)
                tr_id = 'H0STCNI0'
                tr_type = '2'
            elif cmd == '7':  # 주식체결통보 등록(모의)
                tr_id = 'H0STCNI9'
                tr_type = '1'
            elif cmd == '8':  # 주식체결통보 등록해제(모의)
                tr_id = 'H0STCNI9'
                tr_type = '2'

            # 전송 데이터 설정
            if cmd in ['5', '6', '7', '8']:
                senddata = json.dumps({
                    "header": {
                        "approval_key": g_approval_key,
                        "custtype": custtype,
                        "tr_type": tr_type,
                        "content-type": "utf-8"
                    },
                    "body": {
                        "input": {
                            "tr_id": tr_id,
                            "tr_key": htsid
                        }
                    }
                })
            else:
                senddata = json.dumps({
                    "header": {
                        "approval_key": g_approval_key,
                        "custtype": custtype,
                        "tr_type": tr_type,
                        "content-type": "utf-8"
                    },
                    "body": {
                        "input": {
                            "tr_id": tr_id,
                            "tr_key": stockcode
                        }
                    }
                })

            print('Input Command is :', senddata)

            await websocket.send(senddata)

            # 실시간 데이터 수신 및 TPS 계산
            while True:
                data = await websocket.recv()
                print("Recev Command is :", data)

                message_count += 1
                current_time = time.time()

                # 1초마다 TPS를 계산 및 출력
                if current_time - start_time >= 1.0:
                    print(f"TPS (초당 처리량): {message_count}")
                    message_count = 0
                    start_time = current_time

                # 데이터 처리 로직
                if data[0] in ['0', '1']:  # 실시간 데이터일 경우
                    recvstr = data.split('|')
                    trid0 = recvstr[1]

                    if trid0 == "H0STASP0":  # 주식호가
                        print("#### 주식호가 ####")
                        stockhoka(recvstr[3])

                    elif trid0 == "H0STCNT0":  # 주식체결
                        print("#### 주식체결 ####")
                        data_cnt = int(recvstr[2])  # 체결데이터 개수
                        stockspurchase(data_cnt, recvstr[3])

                    elif trid0 in ["H0STCNI0", "H0STCNI9"]:  # 체결통보
                        print("#### 주식체결통보 ####")
                        stocksigningnotice(recvstr[3], aes_key, aes_iv)

                else:
                    jsonObject = json.loads(data)
                    trid = jsonObject["header"]["tr_id"]

                    if trid != "PINGPONG":
                        rt_cd = jsonObject["body"]["rt_cd"]
                        if rt_cd == '1':  # 에러 처리
                            print(f"### ERROR RETURN CODE [ {rt_cd} ] MSG [ {jsonObject['body']['msg1']} ]")
                            break
                        elif rt_cd == '0':  # 정상 처리
                            print(f"### RETURN CODE [ {rt_cd} ] MSG [ {jsonObject['body']['msg1']} ]")
                            if trid in ["H0STCNI0", "H0STCNI9"]:
                                aes_key = jsonObject["body"]["output"]["key"]
                                aes_iv = jsonObject["body"]["output"]["iv"]
                                print(f"### TRID [{trid}] KEY[{aes_key}] IV[{aes_iv}]")

                    elif trid == "PINGPONG":
                        print(f"### RECV [PINGPONG] [{data}]")
                        await websocket.pong(data)
                        print(f"### SEND [PINGPONG] [{data}]")

# 비동기로 서버에 접속
asyncio.run(connect())

