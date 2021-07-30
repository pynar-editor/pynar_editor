while True:
    try:
        s = int(input("Sayi giriniz:"))
        sayi = s
        for a in range (1,sayi+1): 
            for b in range (1,11):   
                carp = a*b
                if carp == a*b:
                  print(a,"x",b,":",carp)   
                  if b == 10:   
                        print("\n")
            break