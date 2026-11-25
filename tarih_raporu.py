from database import baglanti_kur
from datetime import datetime


def tarih_araligi_raporu(kullanici_id):

    baglanti = baglanti_kur()
    cursor = baglanti.cursor()

    print("\n--- TARİH ARALIĞI GELİR GİDER RAPORU ---")

    baslangic = input("Başlangıç tarihi (YYYY-AA-GG): ")
    bitis = input("Bitiş tarihi (YYYY-AA-GG): ")

    try:
        baslangic_tarih = datetime.strptime(baslangic, "%Y-%m-%d")
        bitis_tarih = datetime.strptime(bitis, "%Y-%m-%d")

    except ValueError:
        print("Tarih formatı hatalı!")
        baglanti.close()
        return

    if baslangic_tarih > bitis_tarih:
        print("Başlangıç tarihi bitiş tarihinden sonra olamaz!")
        baglanti.close()
        return

    cursor.execute("""
        SELECT
            I.Tarih,
            K.KategoriAdi,
            K.Tur,
            I.Aciklama,
            I.Tutar
        FROM Islemler I
        INNER JOIN Kategoriler K
        ON I.KategoriID = K.KategoriID
        WHERE I.Tarih >= ?
        AND I.Tarih < DATEADD(DAY, 1, ?)
        AND I.KullaniciID = ?
        ORDER BY I.Tarih ASC
    """, (baslangic, bitis, kullanici_id))

    sonuclar = cursor.fetchall()

    toplam_gelir = 0
    toplam_gider = 0

    if len(sonuclar) == 0:
        print("\nBu tarih aralığında işlem bulunamadı!")

    else:
        print("\n--- İŞLEM DETAYLARI ---")

        for sonuc in sonuclar:
            print("\nTarih:", sonuc[0])
            print("Kategori:", sonuc[1])
            print("Tür:", sonuc[2])
            print("Açıklama:", sonuc[3])
            print("Tutar:", float(sonuc[4]), "TL")

            if sonuc[2] == "Gelir":
                toplam_gelir += float(sonuc[4])

            elif sonuc[2] == "Gider":
                toplam_gider += float(sonuc[4])

    print("\n--- RAPOR SONUCU ---")
    print("Başlangıç:", baslangic)
    print("Bitiş:", bitis)
    print("Toplam gelir:", toplam_gelir, "TL")
    print("Toplam gider:", toplam_gider, "TL")
    print("Net bakiye:", toplam_gelir - toplam_gider, "TL")

    baglanti.close()