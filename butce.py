from database import baglanti_kur
import math



def butce_ekle(kullanici_id):

    baglanti = baglanti_kur()
    cursor = baglanti.cursor()

    print("\n--- BÜTÇE EKLEME ---")

    print("\nGider Kategorileri:")

    cursor.execute("""
    SELECT KategoriID, KategoriAdi
    FROM Kategoriler
    WHERE Tur = 'Gider'
""")

    kategoriler = cursor.fetchall()

    if len(kategoriler) == 0:
        print("Gider kategorisi bulunamadı!")
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
        print("Geçersiz kategori!")
        baglanti.close()
        return

    yil = input("Yıl: ")

    if not yil.isdigit():
        print("Yıl sayısal olmalıdır!")
        baglanti.close()
        return

    yil = int(yil)

    if yil < 2000 or yil > 9999:
        print("Geçersiz yıl!")
        baglanti.close()
        return

    ay = input("Ay: ")

    if not ay.isdigit():
        print("Ay sayısal olmalıdır!")
        baglanti.close()
        return

    ay = int(ay)

    if ay < 1 or ay > 12:
        print("Ay 1 ile 12 arasında olmalıdır!")
        baglanti.close()
        return

    butce_tutari = input("Bütçe tutarı: ")

    try:
        butce_tutari = float(butce_tutari.replace(",", "."))

    except ValueError:
        print("Geçerli bir tutar giriniz!")
        baglanti.close()
        return

    if not math.isfinite(butce_tutari) or butce_tutari <= 0:
        print("Bütçe tutarı sıfırdan büyük olmalıdır!")
        baglanti.close()
        return

    cursor.execute("""
        SELECT COUNT(*)
        FROM Butceler
        WHERE KategoriID = ?
        AND Yil = ?
        AND Ay = ?
        AND KullaniciID = ?
    """, (kategori_id, yil, ay, kullanici_id))

    kontrol = cursor.fetchone()

    if kontrol[0] > 0:
        print("Bu kategori için bu aya ait bütçe zaten mevcut!")
        baglanti.close()
        return

    cursor.execute("""
        INSERT INTO Butceler
        (KategoriID, Yil, Ay, ButceTutari, KullaniciID)
        VALUES (?, ?, ?, ?, ?)
    """, (kategori_id, yil, ay, butce_tutari, kullanici_id))

    baglanti.commit()

    print("\nBütçe başarıyla eklendi!")

    baglanti.close()



def butceleri_listele(kullanici_id):

    baglanti = baglanti_kur()
    cursor = baglanti.cursor()

    print("\n--- BÜTÇELERİ LİSTELE ---")

    cursor.execute("""
        SELECT B.ButceID, K.KategoriAdi, B.Yil, B.Ay, B.ButceTutari
        FROM Butceler B
        INNER JOIN Kategoriler K
        ON B.KategoriID = K.KategoriID
        WHERE B.KullaniciID = ?
        ORDER BY B.Yil DESC, B.Ay DESC
    """, (kullanici_id,))

    butceler = cursor.fetchall()

    if len(butceler) == 0:
        print("Henüz belirlenmiş bir bütçe bulunmuyor!")

    else:
        for butce in butceler:
            print("\nBütçe ID:", butce[0])
            print("Kategori:", butce[1])
            print("Yıl:", butce[2])
            print("Ay:", butce[3])
            print("Bütçe Tutarı:", butce[4], "TL")

    baglanti.close()



def butce_guncelle(kullanici_id):

    baglanti = baglanti_kur()
    cursor = baglanti.cursor()

    print("\n--- BÜTÇE GÜNCELLEME ---")

    cursor.execute("""
        SELECT B.ButceID, K.KategoriAdi, B.Yil, B.Ay, B.ButceTutari
        FROM Butceler B
        INNER JOIN Kategoriler K
        ON B.KategoriID = K.KategoriID
        WHERE B.KullaniciID = ?
    """, (kullanici_id,))

    butceler = cursor.fetchall()

    if len(butceler) == 0:
        print("Güncellenecek bütçe bulunamadı!")
        baglanti.close()
        return

    for butce in butceler:
        print("\nBütçe ID:", butce[0])
        print("Kategori:", butce[1])
        print("Yıl:", butce[2])
        print("Ay:", butce[3])
        print("Tutar:", butce[4], "TL")

    butce_id = input("\nGüncellenecek bütçenin ID numarası: ")

    if not butce_id.isdigit():
        print("Bütçe ID sayı olmalıdır!")
        baglanti.close()
        return

    butce_id = int(butce_id)

    butce_var = False

    for butce in butceler:
        if butce[0] == butce_id:
            butce_var = True

    if not butce_var:
        print("Geçersiz bütçe ID!")
        baglanti.close()
        return

    yeni_tutar = input("Yeni bütçe tutarı: ")

    try:
        yeni_tutar = float(yeni_tutar.replace(",", "."))

    except ValueError:
        print("Geçerli bir tutar giriniz!")
        baglanti.close()
        return

    if not math.isfinite(yeni_tutar) or yeni_tutar <= 0:
        print("Bütçe tutarı sıfırdan büyük olmalıdır!")
        baglanti.close()
        return

    cursor.execute("""
        UPDATE Butceler
        SET ButceTutari = ?
        WHERE ButceID = ?
        AND KullaniciID = ?
    """, (yeni_tutar, butce_id, kullanici_id))

    baglanti.commit()

    print("\nBütçe başarıyla güncellendi!")

    baglanti.close()



def butce_sil(kullanici_id):

    baglanti = baglanti_kur()
    cursor = baglanti.cursor()

    print("\n--- BÜTÇE SİLME ---")

    cursor.execute("""
        SELECT B.ButceID, K.KategoriAdi, B.Yil, B.Ay, B.ButceTutari
        FROM Butceler B
        INNER JOIN Kategoriler K
        ON B.KategoriID = K.KategoriID
        WHERE B.KullaniciID = ?
    """, (kullanici_id,))

    butceler = cursor.fetchall()

    if len(butceler) == 0:
        print("Silinecek bütçe bulunamadı!")
        baglanti.close()
        return

    for butce in butceler:
        print("\nBütçe ID:", butce[0])
        print("Kategori:", butce[1])
        print("Yıl:", butce[2])
        print("Ay:", butce[3])
        print("Tutar:", butce[4], "TL")

    butce_id = input("\nSilinecek bütçenin ID numarası: ")

    if not butce_id.isdigit():
        print("Bütçe ID sayı olmalıdır!")
        baglanti.close()
        return

    butce_id = int(butce_id)

    butce_var = False

    for butce in butceler:
        if butce[0] == butce_id:
            butce_var = True

    if not butce_var:
        print("Geçersiz bütçe ID!")
        baglanti.close()
        return

    onay = input("Bu bütçeyi silmek istediğinize emin misiniz? (✓ / ✗): ").strip()

    if onay == "✓":

        cursor.execute("""
            DELETE FROM Butceler
            WHERE ButceID = ?
            AND KullaniciID = ?
        """, (butce_id, kullanici_id))

        baglanti.commit()

        print("Bütçe başarıyla silindi!")

    else:
        print("Bütçe silme işlemi iptal edildi!")

    baglanti.close()