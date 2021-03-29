require 'json'
require 'httpclient'
require 'time'


top_html =%{ 
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
}


bottom_html =%{
        </table>
    </body>
</html>
}



market_html= %{
                <tr>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                </tr>
    }



text = top_html
actual_time = (Time.now.to_i - 20 * 60) * 1000
yesterday_time = (Time.now.to_i - 60 * 60 * 24) * 1000
url = 'https://www.buda.com/api/v2/markets'
client = HTTPClient.new
begin
    response = JSON.parse(client.get_content(url))
rescue
    retry
end


for entity in response["markets"]
    market_id = entity["id"]
    puts(market_id)
    url = 'https://www.buda.com/api/v2/markets/%s/trades?timestamp=%s;limit=100'
    max_value = 0
    order = nil
    scape = false
    requested_time = actual_time 
    while (requested_time>=yesterday_time && requested_time<=actual_time && scape == false ) do
        begin
            response = JSON.parse(client.get_content(url%[market_id,requested_time]))
            for item in response['trades']['entries']
                if item[0].to_f < yesterday_time
                  scape = true
                  break
                end
                transaction = item[1].to_f * item[2].to_f
                if transaction > max_value && item[0].to_i>=yesterday_time && item[0].to_i<actual_time
                  max_value = transaction
                  order = item
                end
            end
            requested_time -= 20*60 * 1000
        rescue
            retry
        end
    end
    if order == nil
        empty = '-'
        text += market_html%[market_id,empty,empty,empty,empty,empty]
        next
    end
    puts(Time.at(order[0].to_f/1000))
    puts("quantity: " + order[1].to_s + " " + entity['base_currency'])
    puts("price: " + order[2].to_s + " " + entity['quote_currency'])
    puts(order[3])
    puts("trasaction value: "+ ((order[1].to_f) * (order[2].to_f) ).to_s + " " + entity['quote_currency'])
    puts("......................................................................")
    date = Time.at(order[0].to_f/1000)
    quantity = order[1].to_s + " " + entity['base_currency'] #market_id[0:3]
    price = order[2].to_s + " " + entity['quote_currency'] #market_id[4:7]
    buy_or_sell = order[3].to_s
    cost = ((order[1]).to_f * (order[2]).to_f).to_s + " " + entity['quote_currency']#market_id[4:7]
    text += market_html%[market_id,date,quantity,price,buy_or_sell,cost]
end
text += bottom_html
file = File.open("report.html","w")
file.puts text
file.close
#=end
