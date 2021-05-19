from urllib.parse import urlencode
from urllib.request import Request, urlopen

url = "https://careers.byteworks.com.ng/bwc/api/v1/public/test/submit" # Set destination URL here
answers = ['11', '8', '9', '4', '312', 'A', 'Yes', '128', 'I dont know', '8', 'B', 'I dont know', '225', 'I dont know',
           '2', '95', '17', 'I dont know' '32', 'A']

PARAMS = {
    "firstName": "Olayinka",
    "lastName": "Akeju",
    "email": "akejuolayinka016@gmail.com",
    "answers": answers,
    }

request = Request(url, urlencode(PARAMS).encode())
json = urlopen(request).read().decode()
print(json)