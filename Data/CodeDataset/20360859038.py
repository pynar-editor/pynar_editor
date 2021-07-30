"""Aþaðýdaki þekilde kullanýcýnýn girdiði bir deðere göre çarpým tablosu oluþturan programý kodlayýnýz. "6" deðeri ÖRNEK olarak verilmiþtir. Kullanýcý hangi sayýsý girerse o sayý için çarpým tablosu oluþturulacaktýr.

Döngü kullanýlmayan cevaplar sýfýr alacaktýr. Döngü deðiþkeni olarak ilk adýnýzýn ilk harfini kullanýnýz. ilk Adýnýzýn ilk harfi ö,þ,ç,ü ise bunun yerine o,s,c,u harflerini kullanýnýz. Bu kurala dikkat etmeyen baþkasýndan kopya çekmiþ olarak iþlem görecektir. (sürekli tarayýcýya dön yapmamak için bunu thonnye kopyalamýþtým)"""

"""o=oðuzhan k=kahraman k burada çarpým manasýna geliyor hocam çarpým=1 yerine k=1 olarak tanýmladým.  """

#bu program girdiðimiz sayýyý, bizlere 0,1,...,10 a kadar sayýlarla çarpýmýný vermek için tasarlanmýþtýr
o=int(input("Carpim tablosuna hos geldiniz. Tablosunu gormek istediginiz sayiyi, rakami giriniz: "))
k=1
print("carpim tablosu karsinizda")
for k in range(0,11):
    print(o*k)