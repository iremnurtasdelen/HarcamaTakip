from database import baglanti_kur


# KATEGORİ EKLEME
def kategori_ekle(kullanici_id):

    baglanti = baglanti_kur()
    cursor = baglanti.cursor()

    print("\n--- KATEGORİ EKLE ---")
    print("1- Gelir Kategorisi")
    print("2- Gider Kategorisi")

    secim = input("Kategori türünü seçiniz: ")

    if secim == "1":
        tur = "Gelir"

    elif secim == "2":
        tur = "Gider"

    else:
        print("Geçersiz seçim!")
        baglanti.close()
        return

    kategori_adi = input("Kategori adı: ")

    if kategori_adi.strip() == "":
        print("Kategori adı boş bırakılamaz!")
        baglanti.close()
        return

    cursor.execute("""
        SELECT COUNT(*)
        FROM Kategoriler
        WHERE KategoriAdi = ?
        AND Tur = ?
    """, (kategori_adi.strip(), tur))

    sayi = cursor.fetchone()[0]

    if sayi > 0:
        print("Bu kategori zaten mevcut!")
        baglanti.close()
        return

    cursor.execute("""
        INSERT INTO Kategoriler
        (KategoriAdi, Tur)
        VALUES (?, ?)
    """, (kategori_adi.strip(), tur))

    baglanti.commit()

    print("Kategori başarıyla eklendi!")

    baglanti.close()


# KATEGORİLERİ LİSTELEME
def kategorileri_listele(kullanici_id):

    baglanti = baglanti_kur()
    cursor = baglanti.cursor()

    cursor.execute("""
        SELECT KategoriID, KategoriAdi, Tur
        FROM Kategoriler
        ORDER BY KategoriID
    """)

    kategoriler = cursor.fetchall()

    print("\n--- KATEGORİLER ---")

    if len(kategoriler) == 0:
        print("Henüz kategori bulunmuyor.")

    for kategori in kategoriler:
        print("--------------------")
        print("Kategori ID:", kategori[0])
        print("Kategori Adı:", kategori[1])
        print("Tür:", kategori[2])

    baglanti.close()


# KATEGORİ SİLME
def kategori_sil(kullanici_id):

    baglanti = baglanti_kur()
    cursor = baglanti.cursor()

    cursor.execute("""
        SELECT KategoriID, KategoriAdi, Tur
        FROM Kategoriler
        ORDER BY KategoriID
    """)

    kategoriler = cursor.fetchall()

    print("\n--- KATEGORİLER ---")

    if len(kategoriler) == 0:
        print("Henüz kategori bulunmuyor!")
        baglanti.close()
        return

    for kategori in kategoriler:
        print("--------------------")
        print("Kategori ID:", kategori[0])
        print("Kategori Adı:", kategori[1])
        print("Tür:", kategori[2])

    kategori_id = input("\nSilinecek kategori ID: ")

    if not kategori_id.isdigit():
        print("Kategori ID sayı olmalıdır!")
        baglanti.close()
        return

    kategori_id = int(kategori_id)

    cursor.execute("""
        SELECT COUNT(*)
        FROM Kategoriler
        WHERE KategoriID = ?
    """, (kategori_id,))

    kategori_sayisi = cursor.fetchone()[0]

    if kategori_sayisi == 0:
        print("Bu ID ile kategori bulunamadı!")
        baglanti.close()
        return

    cursor.execute("""
        SELECT COUNT(*)
        FROM Islemler
        WHERE KategoriID = ?
    """, (kategori_id,))

    islem_sayisi = cursor.fetchone()[0]

    if islem_sayisi > 0:
        print("Bu kategoriye ait işlemler bulunduğu için silinemez!")
        baglanti.close()
        return

    onay = input("Kategoriyi silmek istediğinize emin misiniz? (✓ / ✗): ").strip()

    if onay == "✓":

        cursor.execute("""
            DELETE FROM Kategoriler
            WHERE KategoriID = ?
        """, (kategori_id,))

        baglanti.commit()

        print("Kategori başarıyla silindi!")

    else:
        print("Silme işlemi iptal edildi.")

    baglanti.close()


# KATEGORİ GÜNCELLEME
def kategori_guncelle(kullanici_id):

    baglanti = baglanti_kur()
    cursor = baglanti.cursor()

    cursor.execute("""
        SELECT KategoriID, KategoriAdi, Tur
        FROM Kategoriler
        ORDER BY KategoriID
    """)

    kategoriler = cursor.fetchall()

    print("\n--- KATEGORİLER ---")

    if len(kategoriler) == 0:
        print("Güncellenecek kategori bulunamadı!")
        baglanti.close()
        return

    for kategori in kategoriler:
        print("--------------------")
        print("Kategori ID:", kategori[0])
        print("Kategori Adı:", kategori[1])
        print("Tür:", kategori[2])

    kategori_id = input("\nGüncellenecek kategori ID: ")

    if not kategori_id.isdigit():
        print("Kategori ID sayı olmalıdır!")
        baglanti.close()
        return

    kategori_id = int(kategori_id)

    cursor.execute("""
        SELECT Tur
        FROM Kategoriler
        WHERE KategoriID = ?
    """, (kategori_id,))

    kategori = cursor.fetchone()

    if kategori is None:
        print("Bu ID ile kategori bulunamadı!")
        baglanti.close()
        return

    yeni_ad = input("Yeni kategori adı: ")

    if yeni_ad.strip() == "":
        print("Kategori adı boş bırakılamaz!")
        baglanti.close()
        return

    tur = kategori[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM Kategoriler
        WHERE KategoriAdi = ?
        AND Tur = ?
        AND KategoriID != ?
    """, (yeni_ad.strip(), tur, kategori_id))

    sayi = cursor.fetchone()[0]

    if sayi > 0:
        print("Bu isimde bir kategori zaten mevcut!")
        baglanti.close()
        return

    cursor.execute("""
        UPDATE Kategoriler
        SET KategoriAdi = ?
        WHERE KategoriID = ?
    """, (yeni_ad.strip(), kategori_id))

    baglanti.commit()

    print("Kategori başarıyla güncellendi!")

    baglanti.close()