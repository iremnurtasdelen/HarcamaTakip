from database import baglanti_kur
import hashlib
import secrets



def sifre_hashle(sifre):

    tuz = secrets.token_hex(16)

    hash_degeri = hashlib.pbkdf2_hmac(
        'sha256',
        sifre.encode(),
        bytes.fromhex(tuz),
        100000
    ).hex()

    return tuz + ":" + hash_degeri



def kullanici_kayit():

    baglanti = baglanti_kur()
    cursor = baglanti.cursor()

    print("\n--- KULLANICI KAYIT ---")

    ad_soyad = input("Ad Soyad: ").strip()
    kullanici_adi = input("Kullanıcı Adı: ").strip()
    sifre = input("Şifre: ")

    if not ad_soyad or not kullanici_adi or not sifre:
        print("Hata: Boş alan bırakılamaz!")
        baglanti.close()
        return

    cursor.execute("""
        SELECT KullaniciID, Sifre FROM Kullanici
        WHERE KullaniciAdi = ?
    """, (kullanici_adi,))

    if cursor.fetchone():
        print("Bu kullanıcı adı zaten kullanılıyor!")
        baglanti.close()
        return

    sifre = sifre_hashle(sifre)

    cursor.execute("""
        INSERT INTO Kullanici (AdSoyad, KullaniciAdi, Sifre)
        VALUES (?, ?, ?)
    """, (ad_soyad, kullanici_adi, sifre))

    baglanti.commit()

    print("Kullanıcı kaydı başarılı!")

    baglanti.close()



def sifre_kontrol(sifre, kayitli_sifre):

    tuz, hash_degeri = kayitli_sifre.split(":")

    yeni_hash = hashlib.pbkdf2_hmac(
        'sha256',
        sifre.encode(),
        bytes.fromhex(tuz),
        100000
    ).hex()

    return yeni_hash == hash_degeri



def kullanici_giris():

    baglanti = baglanti_kur()
    cursor = baglanti.cursor()

    print("\n--- KULLANICI GİRİŞ ---")

    kullanici_adi = input("Kullanıcı Adı: ").strip()
    sifre = input("Şifre: ")

    if not kullanici_adi or not sifre:
        print("Hata: Boş alan bırakılamaz!")
        baglanti.close()
        return False

    cursor.execute("""
        SELECT KullaniciID, Sifre FROM Kullanici
        WHERE KullaniciAdi = ?
    """, (kullanici_adi,))

    sonuc = cursor.fetchone()

    if sonuc is None:
        print("Kullanıcı bulunamadı!")
        baglanti.close()
        return False

    if sifre_kontrol(sifre, sonuc[1]):
        print("Giriş başarılı!")
        kullanici_id = sonuc[0]
        baglanti.close()
        return kullanici_id

    else:
        print("Şifre hatalı!")
        baglanti.close()
        return False