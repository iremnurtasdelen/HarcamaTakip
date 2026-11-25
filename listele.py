from database import baglanti_kur


def islemleri_listele(kullanici_id):

    baglanti = baglanti_kur()

    cursor = baglanti.cursor()

    cursor.execute("""
    SELECT
        Islemler.IslemID,
        Islemler.Aciklama,
        Islemler.Tutar,
        Islemler.Tarih,
        Kategoriler.KategoriAdi,
        Kategoriler.Tur
    FROM Islemler
    INNER JOIN Kategoriler
    ON Islemler.KategoriID = Kategoriler.KategoriID
    WHERE Islemler.KullaniciID = ?
    ORDER BY Islemler.Tarih DESC
""", (kullanici_id,))

    islemler = cursor.fetchall()

    print("\n--- GELİR VE GİDER LİSTESİ ---")

    for islem in islemler:

        print("-----------------------------")
        print("İşlem ID:", islem[0])
        print("Açıklama:", islem[1])
        print("Tutar:", islem[2], "TL")
        print("Tarih:", islem[3])
        print("Kategori:", islem[4])
        print("Tür:", islem[5])

    baglanti.close()


