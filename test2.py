import yfinance as yf

# 원하는 주식 티커 입력 (예: 삼성전자 '005930.KS')
ticker = '005930.KS'
LG ='066570.KS'
stock = yf.Ticker(LG)

# 과거 데이터 수집 (시작 날짜와 종료 날짜 설정)
# data = stock.history(start="2024-10-01", end="2024-10-18")
data = stock.history(period='1y')  # 최신 1일 데이터 가져오기
# 고가, 저가, 시가, 종가, 거래량 출력
# print(data[['Open', 'High', 'Low', 'Close', 'Volume']])
