from collections import deque
from random import SystemRandom
from pprint import pprint


cryptorand = SystemRandom()

r1keys = deque('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ ')
r1values = deque('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ ')

cryptorand.shuffle(r1keys)
cryptorand.shuffle(r1values)

R1 = dict(zip(r1keys, r1values))

pprint(R1)

r1values.rotate(1)

R1 = dict(zip(r1keys, r1values))

print('\n')
pprint(R1)


'''
keys = [1, 2, 3]
values = [4, 5, 6]

d = dict(zip(keys, values))

print(d)
'''



import secrets
foo = ['a', 'b', 'c', 'd', 'e']
print(secrets.choice(foo))



from random import shuffle
x = [i for i in range(10)]
shuffle(x)
print(x)


from random import SystemRandom
cryptorand = SystemRandom()
x = [i for i in range(10)]
cryptorand.shuffle(x)
print(x)
