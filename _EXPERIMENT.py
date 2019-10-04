""r"""

"""

x = {
    '1': {
        '2': {
            "3": 33,
            "4": 44
        }
    },
    '1.2': [
        1,2,3,4
    ]


}

x.get('1')
print("x.get('1') = " + str(x.get('1')))

y=x['1']['2']
print("y = " + str(y))

for k in x:
    print(k)
