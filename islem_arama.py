from database import baglanti_kur


def islem_ara(kullanici_id):

    baglanti = baglanti_kur()
    cursor = baglanti.cursor()

    print("\n--- İŞLEM ARAMA ---")
    print("1- Kategori adına göre ara")
    print("2- Açıklamaya göre ara")
    print("3- İşlem türüne göre ara")

    secim = input("\nArama türünü seçiniz: ")

    if secim == "1":
        aranan = input("Kategori adı: ")

        cursor.execute("""
            SELECT I.Tarih, K.KategoriAdi, K.Tur, I.Aciklama, I.Tutar
            FROM Islemler I
            INNER JOIN Kategoriler K
            ON I.KategoriID = K.KategoriID
            WHERE K.KategoriAdi LIKE ?
            AND I.KullaniciID = ?
            ORDER BY I.Tarih DESC
        """, ('%' + aranan + '%', kullanici_id))

    elif secim == "2":
        aranan = input("Açıklama: ")

        cursor.execute("""
            SELECT I.Tarih, K.KategoriAdi, K.Tur, I.Aciklama, I.Tutar
            FROM Islemler I
            INNER JOIN Kategoriler K
            ON I.KategoriID = K.KategoriID
            WHERE I.Aciklama LIKE ?
            AND I.KullaniciID = ?
            ORDER BY I.Tarih DESC
        """, ('%' + aranan + '%', kullanici_id))

    elif secim == "3":
        aranan = input("Gelir veya Gider: ").strip().capitalize()

        if aranan not in ["Gelir", "Gider"]:
            print("Geçersiz işlem türü!")
            baglanti.close()
            return

        cursor.execute("""
            SELECT I.Tarih, K.KategoriAdi, K.Tur, I.Aciklama, I.Tutar
            FROM Islemler I
            INNER JOIN Kategoriler K
            ON I.KategoriID = K.KategoriID
            WHERE K.Tur = ?
            AND I.KullaniciID = ?
            ORDER BY I.Tarih DESC
        """, (aranan, kullanici_id))

    else:
        print("Geçersiz seçim!")
        baglanti.close()
        return

    sonuclar = cursor.fetchall()

    if len(sonuclar) == 0:
        print("\nArama sonucunda işlem bulunamadı!")

    else:
        print("\n--- ARAMA SONUÇLARI ---")

        for sonuc in sonuclar:
            print("\nTarih:", sonuc[0])
            print("Kategori:", sonuc[1])
            print("Tür:", sonuc[2])
            print("Açıklama:", sonuc[3])
            print("Tutar:", float(sonuc[4]), "TL")

    baglanti.close()