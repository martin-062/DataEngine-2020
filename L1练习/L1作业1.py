# -*- coding: utf-8 -*-
"""
Created on Sun Jun 14 18:13:30 2020

@author: MaJun4
"""


print(sum(range(0,101,2)))

sum = 0
for i in range(0,101,2):
    sum = sum + i
print(sum)

sum = 0
i = 0
while i<= 100:
    sum = sum + i
    i+=2
print(sum)