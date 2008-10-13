#!/usr/bin/env python

import re

f1 = open('country0.sql', 'r')
data = f1.read()
f1.close()

data1 = re.sub(
    'INSERT INTO .*? VALUES \(\'(\d+)\', \'.*?\',\'.*?\',\'.*?\',\'(.+?)\'\);', 
    '{"pk":\\1, "model":"places.country", "fields": {}},\
     {"pk": null, "model":"places.countrytranslation", "fields": {"master": \\1, "name":\"\\2\", "language_id": 1}},',
    data)
data1 = re.sub('--.*', '', data1)

f1 = open('city0.sql', 'r')
data = f1.read()
f1.close()

data2 = re.sub(
    'INSERT INTO .*? VALUES \(\'(\d+)\', \'(\d+)\',\'(.+?)\',\'.*?\'\);', 
    '{"pk":\\1, "model":"places.city", "fields": {"country":\\2}},\
     {"pk": null, "model":"places.citytranslation", "fields": {"master": \\1, "name":\"\\3\", "language_id": 1}},',
    data)
data2 = re.sub('--.*', '', data2)

data0 = data1 + data2
data00 = []
i = 1
for d in data0.split('\n'):
    if d.strip() != '':
        data00 += [re.sub('null', str(i), d)]
        i += 1

f1 = open('places.json', 'w')
f1.write('[')
f1.write('\n'.join(data00)[:-1])
f1.write(']')
f1.close()
