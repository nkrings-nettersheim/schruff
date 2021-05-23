import csv
import sqlite3

con = sqlite3.connect('db.sqlite3')

with open("days.csv") as csvdatei:
    csv_reader_object = csv.reader(csvdatei, delimiter=';')

    zeilennummer = 0
    cur = con.cursor()
    for row in csv_reader_object:

        if zeilennummer == 0:
            print(f'Spaltennamen sind: {", ".join(row)}')
        else:
            datum = row[0].split('.')
            day = "20" + str(datum[2]) + "-" + str(datum[1]) + "-" + str(datum[0])
            print(day)

            sql = f"INSERT INTO order_order_days (order_day, reibekuchen, spiessbraten) " \
                  f"VALUES ('{day}', '{row[1]}', '{row[2]}')"
            cur.execute(sql)
            con.commit()
        zeilennummer += 1

    print(f'Anzahl Datensätze: {zeilennummer-1}')


con.close()

print("Fertig!")
