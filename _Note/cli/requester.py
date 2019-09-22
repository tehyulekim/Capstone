""r"""
https://2.python-requests.org/en/master/user/quickstart/




sending dict to json.
dict > json > dict





https://2.python-requests.org/en/master/user/quickstart/#more-complicated-post-requests

url = 'https://api.github.com/some/endpoint'
payload = {'some': 'data'}
r = requests.post(url, json=payload)


"""
import requests
import json

r = requests.get('http://127.0.0.1:5000/r')

print("r.text = ", r.text)
print("r.url = ", r.url)
print("r.status_code = ", r.status_code)
print("r.headers = ", r.headers)
print("r.encoding = ", r.encoding)


# r2 = requests.post('http://127.0.0.1:5000/r', data={'key': 'value'})
r2 = requests.post('http://127.0.0.1:5000/r', data="{'key': 'value'}")
print("r2.text = ", r2.text)

#  https://2.python-requests.org/en/master/user/quickstart/#json-response-content
r3 = requests.get('http://127.0.0.1:5000/c')
print("r3.text = ", r3.text)
print("r3.json() = ", r3.json())
x = r3.json()  # converts received data json string to dict
print("x = ", x)
print("type(x) = ", type(x))
