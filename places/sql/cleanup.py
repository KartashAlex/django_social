#!/usr/bin/env python

import re

f1 = open('country0.sql', 'r')
data = f1.read()
f1.close()

data = re.sub(
    'INSERT INTO .*? VALUES \(\'(\d+)\', \'.*?\',\'.*?\',\'.*?\',\'(.+?)\'\);', 
    'INSERT INTO places_country (id, name) VALUES (\'\\1\', \'\\2\');',
    data)
    

f1 = open('country.sql', 'w')
f1.write(data)
f1.close()

f1 = open('city0.sql', 'r')
data = f1.read()
f1.close()

data = re.sub(
    'INSERT INTO .*? VALUES \(\'(\d+)\', \'(\d+)\',\'(.+?)\',\'.*?\'\);', 
    'INSERT INTO places_city (id, country_id, name) VALUES (\'\\1\', \'\\2\', \'\\3\');',
    data)
    

f1 = open('city.sql', 'w')
f1.write(data)
f1.close()
