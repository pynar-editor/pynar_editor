"""A?a??daki ?ekilde kullan?c?n?n girdi?i bir de?ere g?re ?arp?m tablosu olu?turan program? kodlay?n?z. "6" de?eri ?RNEK olarak verilmi?tir. Kullan?c? hangi say?s? girerse o say? i?in ?arp?m tablosu olu?turulacakt?r.

D?ng? kullan?lmayan cevaplar s?f?r alacakt?r. D?ng? de?i?keni olarak ilk ad?n?z?n ilk harfini kullan?n?z. ilk Ad?n?z?n ilk harfi ?,?,?,? ise bunun yerine o,s,c,u harflerini kullan?n?z. Bu kurala dikkat etmeyen ba?kas?ndan kopya ?ekmi? olarak i?lem g?recektir. (s?rekli taray?c?ya d?n yapmamak i?in bunu thonnye kopyalam??t?m)"""

"""o=o?uzhan k=kahraman k burada ?arp?m manas?na geliyor hocam ?arp?m=1 yerine k=1 olarak tan?mlad?m.? """

#bu program girdi?imiz say?y?, bizlere 0,1,...,10 a kadar say?larla ?arp?m?n? vermek i?in tasarlanm??t?r
o=int(input("Carpim tablosuna hos geldiniz. Tablosunu gormek istediginiz sayiyi, rakami giriniz: "))
k=1
print("carpim tablosu karsinizda")
for k in range(0,11):
? ? print(o*k)