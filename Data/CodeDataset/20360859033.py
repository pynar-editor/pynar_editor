sayi = int(input("Bir sayi giriniz: "))
print("Kaclar tablosu yapilacak?:", sayi)
for s in range(0,11):
    carpim = sayi * s
    print(str(sayi), "x", str(s), "=", carpim)