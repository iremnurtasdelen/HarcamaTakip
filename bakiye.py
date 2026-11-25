from database import baglanti_kur


def bakiye_goruntule(kullanici_id):

    baglanti = baglanti_kur()
    cursor = baglanti.cursor()

    print("\n--- BAKİYE DURUMU ---")

    cursor.execute("""
        SELECT
            SUM(CASE WHEN K.Tur = 'Gelir' THEN I.Tutar ELSE 0 END),
            SUM(CASE WHEN K.Tur = 'Gider' THEN I.Tutar ELSE 0 END)
        FROM Islemler I
        INNER JOIN Kategoriler K
        ON I.KategoriID = K.KategoriID
        WHERE I.KullaniciID = ?
    """, (kullanici_id,))

    sonuc = cursor.fetchone()

    toplam_gelir = float(sonuc[0] or 0)
    toplam_gider = float(sonuc[1] or 0)

    bakiye = toplam_gelir - toplam_gider

    print("\nToplam Gelir:", toplam_gelir, "TL")
    print("Toplam Gider:", toplam_gider, "TL")
    print("--------------------------")
    print("Mevcut Bakiye:", bakiye, "TL")

    baglanti.close()