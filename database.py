import pyodbc

def baglanti_kur():

    baglanti = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=.\\SQLEXPRESS;"
        "DATABASE=HarcamaTakipDB;"
        "Trusted_Connection=yes;"
    )

    return baglanti