from islem import gelir_gider_ekle
from kategori import kategori_ekle, kategorileri_listele, kategori_sil, kategori_guncelle
from listele import islemleri_listele
from rapor import gelir_gider_raporu
from duzenle import islem_duzenle
from filtrele import islem_filtrele
from butce import butce_ekle, butceleri_listele, butce_guncelle, butce_sil
from butce_kontrol import butce_kontrol
from bakiye import bakiye_goruntule
from aylik_rapor import aylik_rapor
from harcama_analizi import en_cok_harcama_kategorisi
from tarih_raporu import tarih_araligi_raporu
from islem_arama import islem_ara
from giris import kullanici_kayit, kullanici_giris


print("\n--- BÜTÇE TAKİP UYGULAMASI ---")
print("1- Kullanıcı Kayıt")
print("2- Kullanıcı Giriş")
print("3- Çıkış")

kullanici_id = False

while True:

    secim = input("\nSeçiminiz: ").strip()

    if secim == "1":
        kullanici_kayit()

    elif secim == "2":
        kullanici_id = kullanici_giris()

        if kullanici_id is not False:
            break


while True:

    print("\n====== GELİR GİDER TAKİP UYGULAMASI ======")

    print("1- İşlem Ekle")
    print("2- Kategori Ekle")
    print("3- Kategorileri Listele")
    print("4- Kategori Sil")
    print("5- Kategori Güncelle")
    print("6- İşlemleri Listele")
    print("7- Gelir Gider Raporu")
    print("8- İşlem Güncelle / Sil")
    print("9- İşlem Filtrele")
    print("10- Bütçe Ekle")
    print("11- Bütçeleri Listele")
    print("12- Bütçe Güncelle")
    print("13- Bütçe Sil")
    print("14- Bütçe Kontrolü")
    print("15- Bakiye Görüntüle")
    print("16- Aylık Gelir Gider Raporu")
    print("17- En Çok Harcama Yapılan Kategori")
    print("18- Tarih Aralığı Raporu")
    print("19- İşlem Ara")
    print("20- Çıkış")
    

    secim = input("\nSeçiminizi yapınız: ").strip()

    if secim == "1":
        gelir_gider_ekle(kullanici_id)

    elif secim == "2":
       kategori_ekle(kullanici_id)

    elif secim == "3":
        kategorileri_listele(kullanici_id)

    elif secim == "4":
        kategori_sil(kullanici_id)

    elif secim == "5":
        kategori_guncelle(kullanici_id)

    elif secim == "6":
        islemleri_listele(kullanici_id)

    elif secim == "7":
         gelir_gider_raporu(kullanici_id)

    elif secim == "8":
        islem_duzenle(kullanici_id)

    elif secim == "9":
        islem_filtrele(kullanici_id)

    elif secim == "10":
         butce_ekle(kullanici_id)

    elif secim == "11":
         butceleri_listele(kullanici_id)


    elif secim == "12":
       butce_guncelle(kullanici_id)

    elif secim == "13":
       butce_sil(kullanici_id)

    elif secim == "14":

       kategori_id = input("Gider kategorisi ID: ")

       if not kategori_id.isdigit():
           print("Geçerli bir kategori ID giriniz!")

       else:
           tarih = input("Kontrol edilecek tarih (YYYY-AA-GG): ")

           if len(tarih) == 10 and tarih[4] == "-" and tarih[7] == "-":
               butce_kontrol(int(kategori_id), tarih, kullanici_id)

           else:
               print("Tarih formatı hatalı!")

    elif secim == "15":
       bakiye_goruntule(kullanici_id)

    elif secim == "16":
       aylik_rapor(kullanici_id)

    elif secim == "17":
        en_cok_harcama_kategorisi(kullanici_id)

    elif secim == "18":
        tarih_araligi_raporu(kullanici_id)

    elif secim == "19":
        islem_ara(kullanici_id)

    elif secim == "20":
        print("Uygulamadan çıkılıyor...")
        break

    else:
        print("Geçersiz seçim!")