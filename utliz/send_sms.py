import requests
import urllib


def send_sms(number,message):
    url = 'http://smsc.xwireless.net/API/WebSMS/Http/v1.0a/index.php'
    username = 'info@serveconsulting.com'
    password = 'Sasegbon14A'
    message = urllib.parse.quote_plus(message)
    sender = 'CLANNIT'
    format = 'text'
    route = 29
    id = 1
    context = {'username':username,'password':password,'sender':sender,'to':number,'message':message,'reqid':id,
               'format':format,'route_id':route}
    try:
        sms_send = requests.post(url, data=context)
    except:
        pass