from database import baglanti_kur
from butce_kontrol import butce_kontrol
import math


def islem_duzenle(kullanici_id):

    baglanti = baglanti_kur()
    cursor = baglanti.cursor()

    cursor.execute("""
        SELECT I.IslemID, I.Aciklama,
               I.Tutar, I.Tarih,
               K.KategoriAdi, K.Tur,
               I.KategoriID
        FROM Islemler I
        INNER JOIN Kategoriler K
        ON I.KategoriID = K.KategoriID
        WHERE I.KullaniciID = ?
        ORDER BY I.IslemID
    """, (kullanici_id,))

    islemler = cursor.fetchall()

    print("\n--- KAYITLI İŞLEMLER ---")

    if len(islemler) == 0:
        print("Henüz kayıtlı işleminiz bulunmuyor.")
        baglanti.close()
        return

    for islem in islemler:
        print("--------------------")
        print("İşlem ID:", islem[0])
        print("Açıklama:", islem[1])
        print("Tutar:", islem[2])
        print("Tarih:", islem[3])
        print("Kategori:", islem[4])

    print("\n1- İşlem Sil")
    print("2- İşlem Güncelle")

    secim = input("Seçiminiz: ")

    if secim == "1":

        islem_id = input("Silinecek işlem ID: ")

        if not islem_id.isdigit():
            print("İşlem ID sayı olmalıdır!")
            baglanti.close()
            return

        cursor.execute("""
            SELECT KategoriID, Tarih, Tur
            FROM Islemler
            INNER JOIN Kategoriler
            ON Islemler.KategoriID = Kategoriler.KategoriID
            WHERE IslemID = ? AND KullaniciID = ?
        """, (int(islem_id), kullanici_id))

        eski_islem = cursor.fetchone()

        if eski_islem is None:
            print("Bu ID ile işlem bulunamadı.")
            baglanti.close()
            return

        onay = input("Silmek istediğinize emin misiniz? (✓ / ✗): ")

        if onay == "✓":

            cursor.execute("""
                DELETE FROM Islemler
                WHERE IslemID = ? AND KullaniciID = ?
            """, (int(islem_id), kullanici_id))

            baglanti.commit()

            print("İşlem başarıyla silindi!")

            if eski_islem[2] == "Gider":
                baglanti.close()
                butce_kontrol(eski_islem[0], str(eski_islem[1])[:10], kullanici_id)
                return

        else:
            print("Silme işlemi iptal edildi.")

    elif secim == "2":

        islem_id = input("Güncellenecek işlem ID: ")

        if not islem_id.isdigit():
            print("İşlem ID sayı olmalıdır!")
            baglanti.close()
            return

        cursor.execute("""
    SELECT Islemler.KategoriID, Islemler.Tarih, Kategoriler.Tur
    FROM Islemler
    INNER JOIN Kategoriler
    ON Islemler.KategoriID = Kategoriler.KategoriID
    WHERE Islemler.IslemID = ?
    AND Islemler.KullaniciID = ?
""", (int(islem_id), kullanici_id))

        eski_islem = cursor.fetchone()

        if eski_islem is None:
            print("Bu ID ile işlem bulunamadı.")
            baglanti.close()
            return

        yeni_tutar = input("Yeni tutar: ")

        try:
            yeni_tutar = float(yeni_tutar.replace(",", "."))
        except ValueError:
            print("Tutar sayısal olmalıdır!")
            baglanti.close()
            return

        if not math.isfinite(yeni_tutar) or yeni_tutar <= 0:
           print("Geçerli bir tutar giriniz!")
           baglanti.close()
           return

        yeni_aciklama = input("Yeni açıklama: ").strip()

        if yeni_aciklama == "":
            print("Açıklama boş bırakılamaz!")
            baglanti.close()
            return

        cursor.execute("""
            UPDATE Islemler
            SET Tutar = ?, Aciklama = ?
            WHERE IslemID = ? AND KullaniciID = ?
        """, (yeni_tutar, yeni_aciklama, int(islem_id), kullanici_id))

        baglanti.commit()

        print("İşlem başarıyla güncellendi!")

        if eski_islem[2] == "Gider":
            baglanti.close()
            butce_kontrol(eski_islem[0], str(eski_islem[1])[:10], kullanici_id)
            return

    else:
        print("Geçersiz seçim!")

    baglanti.close()