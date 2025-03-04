import requests
import csv

BASE_URL = "https://www.koeln.de/apps/parken/json/current"
DATEN_FOLDER_PATH = "daten/"


def liegt_neue_messung_vor(timestamp):
    try:
        with open(DATEN_FOLDER_PATH + "letzte_messung.txt", "r") as f:
            return f.read() != timestamp
    except IOError:
        return True


def update_letzte_messung(timestamp):
    try:
        with open(DATEN_FOLDER_PATH + "letzte_messung.txt", "w") as f:
            f.write(timestamp)
    except IOError:
        return True


def persistiere_daten(data, append=True):
    mode = "a" if append else "w"
    slug = data["slug"]

    freie_parkplaetze = data["free"]
    kapazitaet = data["capacity"]
    timestamp = data["timestamp"]

    with open(DATEN_FOLDER_PATH + slug + ".csv", mode=mode) as f:
        writer = csv.writer(f, quotechar='"', quoting=csv.QUOTE_MINIMAL)

        if not append:
            writer.writerow(
                ["Zeitpunkt der Messung", "Freie Parkplaetze", "Gesamtkapazitaet"]
            )

        writer.writerow([timestamp, freie_parkplaetze, kapazitaet])


def hole_daten(append=True):
    res = requests.get(BASE_URL)
    res_json = res.json()
    timestamp = res_json["PH01"]["timestamp"]

    if liegt_neue_messung_vor(timestamp):
        for parkhaus in res_json:
            persistiere_daten(res_json[parkhaus], append)

        update_letzte_messung(timestamp)


if __name__ == "__main__":
    hole_daten()
