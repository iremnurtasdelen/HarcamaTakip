from datetime import datetime
from database import baglanti_kur
from butce_kontrol import butce_kontrol
import math


def gelir_gider_ekle(kullanici_id):

    baglanti = baglanti_kur()
    cursor = baglanti.cursor()

    print("\n1- Gelir Ekle")
    print("2- Gider Ekle")

    secim = input("İşlem seçiniz: ")

    if secim == "1":
        tur = "Gelir"

    elif secim == "2":
        tur = "Gider"

    else:
        print("Geçersiz seçim!")
        baglanti.close()
        return

    print("\nKategoriler:")

    cursor.execute(
    """SELECT KategoriID, KategoriAdi
    FROM Kategoriler
    WHERE Tur = ?""",
    (tur,)
)
    kategoriler = cursor.fetchall()

    if len(kategoriler) == 0:
        print("Bu işlem türüne ait kategori bulunamadı!")
        baglanti.close()
        return

    for kategori in kategoriler:
        print(kategori[0], "-", kategori[1])

    kategori_id = input("\nKategori numarası: ")

    if not kategori_id.isdigit():
        print("Kategori numarası sayı olmalıdır!")
        baglanti.close()
        return

    kategori_id = int(kategori_id)

    kategori_var = False

    for kategori in kategoriler:

        if kategori[0] == kategori_id:
            kategori_var = True

    if not kategori_var:
        print("Geçersiz kategori numarası!")
        baglanti.close()
        return

    tutar = input("Tutar: ")

    try:
        tutar = float(tutar.replace(",", "."))

    except ValueError:
        print("Tutar sayısal bir değer olmalıdır!")
        baglanti.close()
        return

    if not math.isfinite(tutar) or tutar <= 0:
        print("Geçerli bir tutar giriniz!")
        baglanti.close()
        return

    aciklama = input("Açıklama: ").strip()

    if aciklama == "":
        print("Açıklama boş bırakılamaz!")
        baglanti.close()
        return

    tarih = input("Tarih (YYYY-AA-GG): ").strip()

    if tarih == "":
        print("Tarih boş bırakılamaz!")
        baglanti.close()
        return

    try:
        datetime.strptime(tarih, "%Y-%m-%d")

    except ValueError:
        print("Geçersiz tarih! YYYY-AA-GG formatını kullanın.")
        baglanti.close()
        return

    cursor.execute(
        """INSERT INTO Islemler
        (Aciklama, Tutar, Tarih, KategoriID, KullaniciID)
        VALUES (?, ?, ?, ?, ?)""",
        (aciklama, tutar, tarih, kategori_id, kullanici_id)
    )

    baglanti.commit()

    print("\nİşlem başarıyla kaydedildi!")

    baglanti.close()

    if tur == "Gider":
        butce_kontrol(kategori_id, tarih, kullanici_id)