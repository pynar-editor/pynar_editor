    dongu_kontrol=f;
    while(dongu_kontrol!=*):
    F=input("çarpým tablosunu oluþturmak istediðiniz sayýyý giriniz // Programý kapamak için * giriniz")

    dongu_kontrol=F;
    if(dongu_kontrol == *):
    continue
    sonuc=0
    for X in range(0,10):
    sonuc=int(F)*int(X)
    print(f"{F}*{X}={sonuc}")