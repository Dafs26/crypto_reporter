import requests
market_id = "ltc-ars"
requestedTime = 1616994985000 
url = f'https://www.buda.com/api/v2/markets/{market_id}/trades'
response = requests.get(url, params={
'timestamp': requestedTime, 
'limit': 100,
})
response = response.json()
for item in  response['trades']['entries']:
    print (item)
    if item[1] == '1.282616402':
        print (item)
        print ("Este es!")
