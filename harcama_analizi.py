from database import baglanti_kur


def en_cok_harcama_kategorisi(kullanici_id):

    baglanti = baglanti_kur()
    cursor = baglanti.cursor()

    print("\n--- HARCAMA KATEGORİ ANALİZİ ---")

    yil = input("Yıl: ")
    ay = input("Ay: ")

    if not yil.isdigit() or not ay.isdigit():
        print("Yıl ve ay sayısal olmalıdır!")
        baglanti.close()
        return

    yil = int(yil)
    ay = int(ay)

    if yil < 2000 or yil > 9999:
        print("Geçersiz yıl!")
        baglanti.close()
        return

    if ay < 1 or ay > 12:
        print("Ay 1 ile 12 arasında olmalıdır!")
        baglanti.close()
        return

    cursor.execute("""
        SELECT
            K.KategoriAdi,
            SUM(I.Tutar) AS ToplamHarcama
        FROM Islemler I
        INNER JOIN Kategoriler K
        ON I.KategoriID = K.KategoriID
        WHERE K.Tur = 'Gider'
        AND YEAR(I.Tarih) = ?
        AND MONTH(I.Tarih) = ?
        AND I.KullaniciID = ?
        GROUP BY K.KategoriAdi
        ORDER BY SUM(I.Tutar) DESC
    """, (yil, ay, kullanici_id))

    sonuclar = cursor.fetchall()

    if len(sonuclar) == 0:
        print("Bu ay için gider kaydı bulunamadı!")
    else:
        print("\n--- KATEGORİLERE GÖRE HARCAMALAR ---")

        for kategori in sonuclar:
            print(kategori[0], ":", float(kategori[1]), "TL")

        print("\nEn çok harcama yapılan kategori:")
        print(sonuclar[0][0], "-", float(sonuclar[0][1]), "TL")

    baglanti.close()