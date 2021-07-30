while True:
    try:
        sayý=int(input("Çarpým taplosu oluþturmak istediðiniz sayýyý giriniz: "))

        for i in range(11):
            çarpým=sayý*i
            print("{} x {} = {}".format(sayý,i,çarpým))
           
    except ValueError:
        print("Lütfen sayý giriniz...")