import time
import requests
top_html = '''
<!DOCTYPE html>
<html>
    <head>
        <title>Crypto currency report</title>
        <meta charset="utf-8">
    </head>
    <body>
        <table border="1">
        <caption>Mayor Transactions (24 Hours)</caption>
            <tr>
                <th>Market</th>
                <th>Date</th>
                <th>Quantity</th>
                <th>Value</th>
                <th>Type of transaction</th>
                <th>Cost</th>
            </tr>
'''

bottom_html ='''
        </table>
    </body>
</html>
'''
text = top_html
actual_time = ((int(time.time()))-30*60)*1000 #marca de tiempo actual menos 30 minutos en milisegundos
yesterday_time = (int(time.time())- 60 * 60 * 24)*1000 #marca de tiempo 24 horas antes en milisegundos
url = 'https://www.buda.com/api/v2/markets'
response = requests.get(url)
for entity in response.json()["markets"]:
    market_id = entity["id"]
    print(market_id)
    url = f'https://www.buda.com/api/v2/markets/{market_id}/trades'
    max_value = 0
    requested_time = yesterday_time
    while (requested_time>=yesterday_time and requested_time<actual_time):
        try:
            response = requests.get(url, params={
                'timestamp': requested_time, 
                'limit': 100,
                })
            for item in response.json()['trades']['entries']:
                transaction = float(item[1])*float(item[2])
                if transaction > max_value:
                    max_value= transaction
                    order = item
        except:
            time.sleep(3)
            requested_time-= 30*60*1000
        requested_time+= 30*60*1000
    print(time.ctime(float(order[0])/1000))
    print("quantity: "+str(order[1]))
    print("price:  "+str(order[2]))
    print(order[3])
    print("trasaction value:  "+ str(float(order[1])*float(order[2])))
    print("......................................................................")
    date = time.ctime(float(order[0])/1000)
    quantity = str(order[1]) + " " + market_id[0:3]
    price = str(order[2]) + " " +market_id[4:7]
    buyOrSell = str(order[3])
    cost = str(float(order[1]) * float(order[2])) + " " + market_id[4:7]
    market_html= f'''
                <tr>
                    <td>{market_id}</td>
                    <td>{date}</td>
                    <td>{quantity}</td>
                    <td>{price}</td>
                    <td>{buyOrSell}</td>
                    <td>{cost}</td>
                </tr>
                '''
    text += market_html
text += bottom_html
file = open("report.html","w")
file.write(text)
file.close()
