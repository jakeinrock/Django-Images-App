thumb_size1 = 400
thumb_size2 = 600

th1 = True
t1 = 'hej'
th2 = True
t2 = 'pa'
sizes = {}

if th1 is True:
    sizes[t1] = thumb_size1
if th2 is True:
    sizes[t2] = thumb_size2

print(sizes)

for k, v in sizes.items():
    print('wartosc k', k, 'wartosc v', v)