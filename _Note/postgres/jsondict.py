""r"""
json to dictionary

json.dumps != json.dump(file)
json.loads != json.load(file)


object -json.dumps-> JSON str
JSON str -json.loads-> object


https://www.w3schools.com/python/python_json.asp

dictionary = {"key1":"value1", "key2":"value2"}
print(dictionary["key1"])

d1 = {'k1': 'v1', 'k2': 'v2'}
d2 = {'1': '11', '2': '22'}
d3 = {'0': d1}

print("dict1 = ", d1['k1'])
print("d3['0'] = ", d3['0'])


a = dict(one=1, two=2, three=3)
b = {'one': 1, 'two': 2, 'three': 3}
c = dict(zip(['one', 'two', 'three'], [1, 2, 3]))
d = dict([('two', 2), ('one', 1), ('three', 3)])
e = dict({'three': 3, 'one': 1, 'two': 2})
a == b == c == d == e # True


x= [1,2,3]
print(type(x)) # <class 'list'>



https://docs.python.org/3.7/tutorial/datastructures.html#dictionaries
dict([('sape', 4139), ('guido', 4127), ('jack', 4098)])
{'sape': 4139, 'guido': 4127, 'jack': 4098}


d = json.dumps(['foo', {'bar': ('baz', None, 1.0, 2)}])
print(type(d)) # <class 'str'>
l = json.loads('["foo", {"bar":["baz", null, 1.0, 2]}]')
print(type(l)) # <class 'list'>


object -json.dump-> JSON
JSON -json.load-> object


https://www.w3schools.com/python/python_json.asp

import json

# some JSON:
x =  '{ "name":"John", "age":30, "city":"New York"}'

# parse x:
y = json.loads(x)

# the result is a Python dictionary:
print(y["age"])

"""
import json
x = json.dumps(
    {
        'k1': 'v1',
        'k2': 'v2'
    }
)
print(x)
y = json.loads(x)
print(y)

b = {'one': 1, 'two': 2, 'three': 3, 'four': 4}
print(json.dumps(b, indent=4, sort_keys=True))  # sort keys by alphabet

dictionary = {
    'key1"stnd"aei': "value1",
    "key2": "value2"
}
print(dictionary)
