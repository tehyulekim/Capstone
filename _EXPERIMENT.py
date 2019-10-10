""r"""
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






x = ["1.2.3.4", "1.2.3.3", "1.2.2.9"]

y= sorted(x)
print(y)









# https://stackoverflow.com/questions/20844019/filter-latest-items-in-a-list

from itertools import groupby
recs1 = [{'data': '1', 'version': '8'},
        {'data': '1', 'version': '2'},
        {'data': '2', 'version': '2'},
   {'data': '1', 'version': '3'}]

recs = sorted(recs1, key=lambda x: x['data'])
print("recs = " + str(recs))

filtered_recs = []
for key, group_iter in groupby(recs, lambda rec: rec['data']):
    recent_rec = max(group_iter, key = lambda rec: rec['version'])
    filtered_recs.append(recent_rec)

print(filtered_recs)



"""
