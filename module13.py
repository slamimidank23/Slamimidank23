a = int(input("Введите количество билетов:"))
s = 0
for person in range(a,):
    b = int(input('Введите возраст:'))
    if b < 18:
        s += 0
    elif 18 <= b <=25:
        s += 990
    elif b > 25:
        s += 1390
if a > 3:
    s = s - (s*0.1)
    print("Сумма билетов включая скидку",s)