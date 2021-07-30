sayi = int(input("kaçlar tablosu yapýlacagini giriniz: "))

       
print("Girdiginiz Sayinin Tablosu: ", sayi)

for l in range(1, 11):
    print(sayi,"x",l,"=",sayi * l)