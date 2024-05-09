from datetime import datetime
from abc import ABC, abstractmethod

class Szoba(ABC):
    def __init__(self, szobaszam, ar):
        self.szobaszam = szobaszam
        self.ar = ar
        self.foglalt_datumok = []

    def foglal(self, datum):
        if datum not in self.foglalt_datumok:
            self.foglalt_datumok.append(datum)
            return True
        else:
            return False

class EgyagyasSzoba(Szoba):
    def __init__(self, szobaszam):
        super().__init__(szobaszam, 5000)

class KetagyasSzoba(Szoba):
    def __init__(self, szobaszam):
        super().__init__(szobaszam, 8000)

class Foglalás:
    def __init__(self, szoba, datum):
        self.szoba = szoba
        self.datum = datum

class Szalloda:
    def __init__(self, nev):
        self.nev = nev
        self.szobak = []
        self.foglalasok = []

    def add_szoba(self, szoba):
        self.szobak.append(szoba)

    def foglalas(self, szobaszam, datum):
        for szoba in self.szobak:
            if szoba.szobaszam == szobaszam:
                if szoba.foglal(datum):
                    foglalas = Foglalás(szoba, datum)
                    self.foglalasok.append(foglalas)
                    return foglalas.szoba.ar
                else:
                    return None
        return None

    def lemondas(self, foglalas):
        if foglalas in self.foglalasok:
            self.foglalasok.remove(foglalas)
            foglalas.szoba.foglalt_datumok.remove(foglalas.datum)
            return True
        else:
            return False

    def listaz_foglalasok(self):
        for foglalas in self.foglalasok:
            print(f"Szoba: {foglalas.szoba.szobaszam}, Dátum: {foglalas.datum}")

    def abc(self):
        self.foglalasok.sort(key=lambda x: x.datum)

# Teszt adatok
szalloda = Szalloda("Teszt Szalloda")
szalloda.add_szoba(EgyagyasSzoba("101"))
szalloda.add_szoba(KetagyasSzoba("102"))
szalloda.add_szoba(EgyagyasSzoba("103"))

szalloda.foglalas("101", datetime(2024, 5, 10))
szalloda.foglalas("101", datetime(2024, 5, 15))
szalloda.foglalas("102", datetime(2024, 5, 20))
szalloda.foglalas("103", datetime(2024, 5, 25))
szalloda.foglalas("102", datetime(2024, 5, 30))

# ABC rendezés
szalloda.abc()

# Felhasználói interfész
while True:
    print("\nVálassz egy műveletet:")
    print("1. Foglalás")
    print("2. Lemondás")
    print("3. Foglalások listázása")
    print("4. Kilépés")

    valasztas = input("Választás (1/2/3/4): ")

    if valasztas == "1":
        szobaszam = input("Kérlek add meg a szoba számát: ")
        while True:
            datum_str = input("Kérlek add meg a foglalás dátumát (YYYY-MM-DD): ")
            try:
                datum = datetime.strptime(datum_str, "%Y-%m-%d")
                if datum < datetime.now():
                    print("Hibás dátum! Kérlek adj meg egy jövőbeli dátumot.")
                else:
                    break
            except ValueError:
                print("Hibás dátumformátum! Kérlek használj YYYY-MM-DD formátumot.")
        ar = szalloda.foglalas(szobaszam, datum)
        if ar is not None:
            print(f"Sikeres foglalás! Ár: {ar}")
        else:
            print("Nem lehet erre a dátumra foglalni vagy a szoba már fog" )
    elif valasztas == "2":
        print("Kérlek add meg a lemondani kívánt foglalás adatait:")
        szobaszam = input("Szobaszám: ")
        while True:
            datum_str = input("Dátum (YYYY-MM-DD): ")
            try:
                datum = datetime.strptime(datum_str, "%Y-%m-%d")
                break
            except ValueError:
                print("Hibás dátumformátum! Kérlek használj YYYY-MM-DD formátumot.")
        lemondott = False
        for foglalas in szalloda.foglalasok:
            if foglalas.szoba.szobaszam == szobaszam and foglalas.datum == datum:
                if szalloda.lemondas(foglalas):
                    print("Sikeres lemondás!")
                    lemondott = True
                    break
        if not lemondott:
            print("Nincs ilyen foglalás.")

    elif valasztas == "3":
        print("Foglalások:")
        szalloda.listaz_foglalasok()

    elif valasztas == "4":
        print("Kilépés...")
        break

