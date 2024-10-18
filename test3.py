import os
import json
import time
import requests
import pandas as pd

try:
    import websocket

except ImportError:
    print("websocket-client 설치중입니다.")
    os.system('python3 -m pip3 install websocket-client')

# 웹소켓 접속키 발급
def get_approval(key, secret):
    url = 'https://openapivts.koreainvestment.com:29443'  # 모의투자계좌
    headers = {"content-type": "application/json"}
    body = {"grant_type": "client_credentials",
            "appkey": key,
            "secretkey": secret}
    PATH = "oauth2/Approval"
    URL = f"{url}/{PATH}"
    time.sleep(0.05)
    res = requests.post(URL, headers=headers, data=json.dumps(body))
    approval_key = res.json()["approval_key"]
    return approval_key    

g_appkey = ''
g_appsecret = ''
g_approval_key = get_approval(g_appkey, g_appsecret)
    
h = {
    "appkey": g_appkey,
    "appsecret": g_appsecret
}
b = {
    "header": {
        "approval_key": g_approval_key,
        "custtype": "P",
        "tr_type": "1",
        "content-type": "utf-8"
    },
    "body": {
        "input": {
            "tr_id": "H0STCNT0",  # API명
            "tr_key": "373220"    # 종목번호
        }
    }
}

# Pandas DataFrame 이용
def pdbind(result):
    # 필요한 데이터만 추출하여 출력
    print('주식 시가', result[7]),
    print('주식 최고가', result[8]),
    print('주식 최저가', result[9]),
    print("주식 현재가:", result[2])
    print("전일 대비:", result[4])
    print("전일 대비율:", result[5])
    print("거래량:", result[12])
    print("누적 거래량:", result[13])

def on_message(ws, data):
    if data[0] in ['0', '1']:  # 시세 데이터가 아닌 경우
        d1 = data.split("|")
        if len(d1) >= 4:
            isEncrypt = d1[0]
            tr_id = d1[1]
            tr_cnt = d1[2]
            recvData = d1[3]
            result = recvData.split("^")
            pdbind(result)  # 필요한 데이터 출력
        else:
            print('Data Size Error=', len(d1))
    else:
        recv_dic = json.loads(data)
        tr_id = recv_dic['header']['tr_id']

        if tr_id == 'PINGPONG':
            ws.send(data, websocket.ABNF.OPCODE_PING)
        else:
            print('tr_id=', tr_id, '\nmsg=', data)

def on_error(ws, error):
    print('error=', error)

def on_close(ws, status_code, close_msg):
    print('on_close close_status_code=', status_code, " close_msg=", close_msg)

def on_open(ws):
    print('on_open send data=', json.dumps(b))
    ws.send(json.dumps(b), websocket.ABNF.OPCODE_TEXT)

# WebSocket 연결
ws = websocket.WebSocketApp("ws://ops.koreainvestment.com:31000",
                            on_open=on_open, on_message=on_message, on_error=on_error)

ws.run_forever()
