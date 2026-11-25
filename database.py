import pyodbc

def baglanti_kur():

    baglanti = pyodbc.connect(
        "DRIVER={***};"
        "SERVER=***;"
        "DATABASE=***;"
        "Trusted_Connection=***;"
    )

    return baglanti
