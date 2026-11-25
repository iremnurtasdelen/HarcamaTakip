from database import baglanti_kur


def gelir_gider_raporu(kullanici_id):
    baglanti = baglanti_kur()
    cursor = baglanti.cursor()

    print("\n--- RAPORLAMA ---")
    print("1- Genel Gelir Gider Raporu")
    print("2- Kategori Bazlı Rapor")
    print("3- Aylık Rapor")

    secim = input("Seçiminiz: ")

    if secim == "1":

        cursor.execute("""
    SELECT Kategoriler.Tur, SUM(Islemler.Tutar)
    FROM Islemler
    INNER JOIN Kategoriler
    ON Islemler.KategoriID = Kategoriler.KategoriID
    WHERE Islemler.KullaniciID = ?
    GROUP BY Kategoriler.Tur
""", (kullanici_id,))

        sonuclar = cursor.fetchall()

        toplam_gelir = 0
        toplam_gider = 0

        for sonuc in sonuclar:
            if sonuc[0] == "Gelir":
                toplam_gelir = sonuc[1]
            elif sonuc[0] == "Gider":
                toplam_gider = sonuc[1]

        bakiye = toplam_gelir - toplam_gider

        print("\n--- GENEL RAPOR ---")
        print("Toplam Gelir:", toplam_gelir)
        print("Toplam Gider:", toplam_gider)
        print("Kalan Bakiye:", bakiye)

    elif secim == "2":

        cursor.execute("""
    SELECT Kategoriler.KategoriAdi,
           Kategoriler.Tur,
           SUM(Islemler.Tutar)
    FROM Islemler
    INNER JOIN Kategoriler
    ON Islemler.KategoriID = Kategoriler.KategoriID
    WHERE Islemler.KullaniciID = ?
    GROUP BY Kategoriler.KategoriAdi, Kategoriler.Tur
    ORDER BY Kategoriler.Tur
""", (kullanici_id,))

        sonuclar = cursor.fetchall()

        print("\n--- KATEGORİ BAZLI RAPOR ---")

        if len(sonuclar) == 0:
            print("Henüz işlem bulunmuyor.")

        for sonuc in sonuclar:
            print("--------------------")
            print("Kategori:", sonuc[0])
            print("Tür:", sonuc[1])
            print("Toplam:", sonuc[2])

    elif secim == "3":

        yil = input("Yıl giriniz: ")
        ay = input("Ay giriniz (1-12): ")

        if not yil.isdigit() or not ay.isdigit():
            print("Yıl ve ay sayısal olmalıdır!")

        elif int(ay) < 1 or int(ay) > 12:
            print("Ay 1 ile 12 arasında olmalıdır!")

        else:
            cursor.execute("""
               SELECT Kategoriler.Tur, SUM(Islemler.Tutar)
               FROM Islemler
               INNER JOIN Kategoriler
               ON Islemler.KategoriID = Kategoriler.KategoriID
               WHERE YEAR(Islemler.Tarih) = ?
               AND MONTH(Islemler.Tarih) = ?
               AND Islemler.KullaniciID = ?
               GROUP BY Kategoriler.Tur
            """, (int(yil), int(ay), kullanici_id))

            sonuclar = cursor.fetchall()

            toplam_gelir = 0
            toplam_gider = 0

            for sonuc in sonuclar:
                if sonuc[0] == "Gelir":
                    toplam_gelir = sonuc[1]
                elif sonuc[0] == "Gider":
                    toplam_gider = sonuc[1]

            print("\n--- AYLIK RAPOR ---")
            print("Yıl:", yil)
            print("Ay:", ay)
            print("Toplam Gelir:", toplam_gelir)
            print("Toplam Gider:", toplam_gider)
            print("Kalan Bakiye:", toplam_gelir - toplam_gider)

    else:
        print("Geçersiz seçim!")

    baglanti.close()


