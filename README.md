# Pynar Türkçe Kod Editörü
Tübitak bünyesinde geliştirilen PyNar projesi, Python programlama için Türkçe derleme ortamı sunmayı amaçlamaktadır.

PyNar, programlamanın temellerini Python diliyle öğretmek için oluşturulmuş bir editördür. Editörü kullananlar içerisinde bulunan Chatbot ile iletişime geçebilecek, Hata ve uyarı mesajlarını Türkçe olarak alacak dolayısıyla gelecekte iyi birer programcı olabilmek için gerekeli güven ve motivasyona sahip olacaklardır.

Kullanıcılar Uygulama içerisinde gerekli Python Kod Örneklerini sürükle bırak yöntemi ile seçip çalıştırabilecek, Yeni Kodlar oluşturabilecek, Online ortamda kodlarını saklayabilecek, Hazır Kod dökümanları indirip yükleyebileceklerdir.

# Kurulum
# 1.Windows 10

Öncelikle bilgisayarınızda Python kurulu olmalıdır. Bu github reposundan zip olarak indirebilirsiniz:

İlk adım olaran indirdiğiniz zip dosyayı istediğiniz bir klasöre açınız(extract edin). Komut satırından ilgili klasöre girin.

Program için gerekli paketlerin kurulumu:

    pip install -r requirements.txt
    
![req](https://user-images.githubusercontent.com/30179132/99789976-7c61a580-2b34-11eb-9cae-7a85278219bd.PNG)

# Programı Çalıştırma
Programı çalıştırabilmek için indirdiğiniz dosyada ana dizin içerisinde komut satırını (CMD) başlatıp aşağıdaki işlemleri yapabilirsiniz:
    
    1) Windows -> Komut İstemi 
    2) cd proje_yolu
    3) python main.py
    
![Ekran Alıntısı](https://user-images.githubusercontent.com/30179132/103465502-28f69000-4d4d-11eb-998f-ee9d7be8d41d.PNG)

# 2.TÜBİTAK PARDUS 19 ve üstü

Aşağıdaki paketleri kurunuz

    sudo apt-get update
    sudo apt-get install -y python3-pyqt5 python3-pyqt5.qtsql python3-pyqt5.qsci vulture python3-pycodestyle python3-pyqt5.qtwebengine python3-natsort python3-tk python3-pip python3-unidecode
    pip3 install emoji

Programı indirdiğiniz klasöre girerek

    python3 main.py

komutu ile çalıştırınız. Editör açıldıktan sonra ayarlar bölümünden Komutlar seçenek bölümünde "Pardus" seçiniz.



# Özellikler
 * syntax highlighting
 * python yorumlayıcı başlatma 
 * terminal penceresi başlatma
 * kaynak kod analizi
 * dosya kaydetme / dosya açma 
 * dosya yazdırma

# Programın ekran görüntüsü:
![image](https://user-images.githubusercontent.com/30179132/112771996-18e20a00-9037-11eb-8832-7a828d10b3db.png)
