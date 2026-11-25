from database import baglanti_kur
from datetime import datetime


def islem_filtrele(kullanici_id):

    baglanti = baglanti_kur()
    cursor = baglanti.cursor()

    print("\n--- İŞLEM FİLTRELEME ---")
    print("1- Kategoriye Göre Filtrele")
    print("2- Tarih Aralığına Göre Filtrele")
    print("3- Gelir / Gider Türüne Göre Filtrele")
    print("4- Açıklamaya Göre Ara")

    secim = input("Seçiminiz: ")

    if secim == "1":

        kategori_id = input("Kategori ID: ")

        if not kategori_id.isdigit():
            print("Kategori ID sayı olmalıdır!")
            baglanti.close()
            return

        cursor.execute("""
            SELECT Islemler.IslemID, Islemler.Aciklama,
                   Islemler.Tutar, Islemler.Tarih,
                   Kategoriler.KategoriAdi, Kategoriler.Tur
            FROM Islemler
            INNER JOIN Kategoriler
            ON Islemler.KategoriID = Kategoriler.KategoriID
            WHERE Islemler.KategoriID = ?
            AND Islemler.KullaniciID = ?
        """, (int(kategori_id), kullanici_id))

    elif secim == "2":

        baslangic = input("Başlangıç tarihi (YYYY-AA-GG): ")
        bitis = input("Bitiş tarihi (YYYY-AA-GG): ")

        try:
            baslangic_tarih = datetime.strptime(
                baslangic, "%Y-%m-%d"
            )

            bitis_tarih = datetime.strptime(
                bitis, "%Y-%m-%d"
            )

        except ValueError:
            print("Geçersiz tarih formatı!")
            baglanti.close()
            return

        if baslangic_tarih > bitis_tarih:
            print("Başlangıç tarihi bitiş tarihinden sonra olamaz!")
            baglanti.close()
            return

        cursor.execute("""
            SELECT Islemler.IslemID, Islemler.Aciklama,
                   Islemler.Tutar, Islemler.Tarih,
                   Kategoriler.KategoriAdi, Kategoriler.Tur
            FROM Islemler
            INNER JOIN Kategoriler
            ON Islemler.KategoriID = Kategoriler.KategoriID
            WHERE Islemler.Tarih BETWEEN ? AND ?
            AND Islemler.KullaniciID = ?
        """, (baslangic, bitis, kullanici_id))

    elif secim == "3":

        print("\n1- Gelir")
        print("2- Gider")

        tur_secim = input("İşlem türünü seçiniz: ")

        if tur_secim == "1":
            tur = "Gelir"

        elif tur_secim == "2":
            tur = "Gider"

        else:
            print("Geçersiz seçim!")
            baglanti.close()
            return

        cursor.execute("""
            SELECT Islemler.IslemID, Islemler.Aciklama,
                   Islemler.Tutar, Islemler.Tarih,
                   Kategoriler.KategoriAdi, Kategoriler.Tur
            FROM Islemler
            INNER JOIN Kategoriler
            ON Islemler.KategoriID = Kategoriler.KategoriID
            WHERE Kategoriler.Tur = ?
            AND Islemler.KullaniciID = ?
        """, (tur, kullanici_id))

    elif secim == "4":

        aranan = input("Aranacak kelime: ")

        cursor.execute("""
            SELECT Islemler.IslemID, Islemler.Aciklama,
                   Islemler.Tutar, Islemler.Tarih,
                   Kategoriler.KategoriAdi, Kategoriler.Tur
            FROM Islemler
            INNER JOIN Kategoriler
            ON Islemler.KategoriID = Kategoriler.KategoriID
            WHERE Islemler.Aciklama LIKE ?
            AND Islemler.KullaniciID = ?
        """, ("%" + aranan + "%", kullanici_id))

    else:
        print("Geçersiz seçim!")
        baglanti.close()
        return

    islemler = cursor.fetchall()

    print("\n--- FİLTRELENEN İŞLEMLER ---")

    if len(islemler) == 0:
        print("Sonuç bulunamadı.")

    for islem in islemler:
        print("--------------------")
        print("İşlem ID:", islem[0])
        print("Açıklama:", islem[1])
        print("Tutar:", islem[2])
        print("Tarih:", islem[3])
        print("Kategori:", islem[4])
        print("Tür:", islem[5])

    baglanti.close()