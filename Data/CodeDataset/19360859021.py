? ? dongu_kontrol=f;
? ? while(dongu_kontrol!=*):
? ? F=input("?arp?m tablosunu olu?turmak istedi?iniz say?y? giriniz // Program? kapamak i?in * giriniz")

? ? dongu_kontrol=F;
? ? if(dongu_kontrol == *):
? ? continue
? ? sonuc=0
? ? for X in range(0,10):
? ? sonuc=int(F)*int(X)
? ? print(f"{F}*{X}={sonuc}")