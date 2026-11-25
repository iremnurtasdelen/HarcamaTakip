from database import baglanti_kur


def aylik_rapor(kullanici_id):

    baglanti = baglanti_kur()
    cursor = baglanti.cursor()

    print("\n--- AYLIK GELİR GİDER RAPORU ---")

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
            SUM(CASE WHEN K.Tur = 'Gelir' THEN I.Tutar ELSE 0 END),
            SUM(CASE WHEN K.Tur = 'Gider' THEN I.Tutar ELSE 0 END)
        FROM Islemler I
        INNER JOIN Kategoriler K
        ON I.KategoriID = K.KategoriID
        WHERE YEAR(I.Tarih) = ?
        AND MONTH(I.Tarih) = ?
        AND I.KullaniciID = ?
    """, (yil, ay, kullanici_id))

    sonuc = cursor.fetchone()

    toplam_gelir = float(sonuc[0] or 0)
    toplam_gider = float(sonuc[1] or 0)

    bakiye = toplam_gelir - toplam_gider

    print("\n========== AYLIK RAPOR ==========")
    print("Dönem:", ay, "/", yil)
    print("--------------------------------")
    print("Toplam Gelir:", toplam_gelir, "TL")
    print("Toplam Gider:", toplam_gider, "TL")
    print("--------------------------------")
    print("Net Bakiye:", bakiye, "TL")
    print("================================")

    baglanti.close()