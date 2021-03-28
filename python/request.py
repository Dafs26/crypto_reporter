import time
import requests
actualTime = ((int(time.time()))-30*60)*1000 #marca de tiempo actual menos 30 minutos en milisegundos
yesterdayTime = (int(time.time())- 60 * 60 * 24)*1000 #marca de tiempo 24 horas antes en milisegundos
url = 'https://www.buda.com/api/v2/markets'
response = requests.get(url)
for entity in response.json()["markets"]:
    market_id = entity["id"]
    print(market_id)
    url = f'https://www.buda.com/api/v2/markets/{market_id}/trades'
    maxValue = 0
    requestedTime = yesterdayTime
    while (requestedTime>=yesterdayTime and requestedTime<actualTime):
        try:
            response = requests.get(url, params={
                'timestamp': requestedTime, 
                'limit': 100,
                })
            for item in response.json()['trades']['entries']:
                transaction = float(item[1])*float(item[2])
                if transaction > maxValue:
                    maxValue = transaction
                    order = item
        except:
            time.sleep(3)
            requestedTime -= 30*60*1000
        requestedTime+= 30*60*1000
    print(time.ctime(float(order[0])/1000))
    print("cantidad: "+str(order[1])
    print("precio:  "+str(order[2]))
    print(order[3])
    print("transaccion total:  "+ str(float(order[1])*float(order[2])))
    print("......................................................................")
