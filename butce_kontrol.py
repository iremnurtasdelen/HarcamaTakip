from database import baglanti_kur
from datetime import datetime


def butce_kontrol(kategori_id, tarih, kullanici_id):

    baglanti = baglanti_kur()
    cursor = baglanti.cursor()

    tarih = datetime.strptime(tarih, "%Y-%m-%d")

    yil = tarih.year
    ay = tarih.month

    cursor.execute("""
        SELECT ButceTutari
        FROM Butceler
        WHERE KategoriID = ?
        AND Yil = ?
        AND Ay = ?
        AND KullaniciID = ?
    """, (kategori_id, yil, ay, kullanici_id))

    sonuc = cursor.fetchone()

    if sonuc is None:
        print("\nBu kategori için bütçe tanımlanmamış!")
        baglanti.close()
        return

    butce = float(sonuc[0])

    cursor.execute("""
        SELECT SUM(Tutar)
        FROM Islemler
        WHERE KategoriID = ?
        AND YEAR(Tarih) = ?
        AND MONTH(Tarih) = ?
        AND KullaniciID = ?
    """, (kategori_id, yil, ay, kullanici_id))

    harcama = cursor.fetchone()[0]

    if harcama is None:
        harcama = 0
    else:
        harcama = float(harcama)

    oran = (harcama / butce) * 100

    print("\n--- BÜTÇE DURUMU ---")
    print("Bütçe:", butce, "TL")
    print("Harcanan:", harcama, "TL")
    print("Kullanım oranı:", round(oran, 2), "%")

    if oran >= 100:
        if harcama > butce:
            print("UYARI! Bütçenizi aştınız!")
            print("Aşım miktarı:", harcama - butce, "TL")
        else:
            print("Bütçenizin tamamını kullandınız!")

    elif oran >= 80:
        print("DİKKAT! Bütçenizin %80'ini kullandınız!")

    elif oran >= 50:
        print("Bilgi: Bütçenizin %50'sini kullandınız!")

    else:
        print("Bütçeniz normal seviyede.")

    baglanti.close()