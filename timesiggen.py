from random import choice

f = open('timesig.txt', 'w')
f.write(f'{choice(range(80, 181))} {choice(range(57, 69))}')
f.close()