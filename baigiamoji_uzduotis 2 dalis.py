
# Nuskaitom faila 'saldainiai.txt ir susimetam duomenis į sąrašą 'saldainiai''

import sqlite3
import seaborn as sns
from matplotlib import pyplot as plt
import numpy as np

saldainiai = []
with open('saldainiai.txt', encoding="utf8") as failas:
    for eilute in failas:
        eilute = eilute.rstrip('\n')
        isskaidyta = eilute.split(',')
        saldainis = [
            isskaidyta[0],
            isskaidyta[1],
            float(isskaidyta[2]),
            int(isskaidyta[3])
        ]
        saldainiai.append(tuple(saldainis))

for saldainis in saldainiai:
    print(saldainis)

# Sukuriam 'saldainiai.db', sukuriam lentele saldainiai ir uzpildom duomenimis

conn = sqlite3.connect("saldainiai.db")
c = conn.cursor()

with conn:
    c.execute("CREATE TABLE IF NOT EXISTS saldainiai\
               (pavadinimas text, skonis text, kaina float, kiekis integer)")

# c.executemany('INSERT OR REPLACE INTO saldainiai (pavadinimas, skonis, kaina, kiekis) VALUES (?, ?, ?, ?)', saldainiai)


# Susivedam naujo stulpelio pavadinima ir tipą, pvz 'suma', float. Užpildom jį kainos ir kieko sandaugos reiksmemis

# st_pavad = input('Nurodykite stulpelio kuri norite itraukti pavadinima: ')
# tipas = input(f'Nurodykite kokio tipo informacija bus talpinama stulpelyje {st_pavad} pvz. integer,float,text: ')
# c.execute(f"""ALTER TABLE saldainiai ADD COLUMN {st_pavad} '{tipas}'""")

sarasas = c.execute("SELECT * From saldainiai").fetchall()
# for saldainis in sarasas:
#     kiekis = saldainis[2] * saldainis[3]
#     c.execute(f"UPDATE saldainiai set suma = {kiekis} where pavadinimas = '{saldainis[0]}'")
# print(sarasas)

# print()

# Duomenų filtracija pagal tipą, t. y. skonį

# ieskomas = input(f'Įveskite ieksoma skoni: ')
# # print(name)
# paieskos_rez = c.execute(f"SELECT * From saldainiai where skonis LIKE '%{ieskomas}%'").fetchall()
# # print(paieskos_rez)
# if len(paieskos_rez):
#     print(f'Visų saldainių sąrašas, kurių skonis - {ieskomas} pateikiamas apačioje:')
#     for i in paieskos_rez:
#         print(i)
# else:
#     print('Duomenu nerasta')


# Duomenų trinimas pagal ivesto saldainio pavadinimą

# istrintas = input('Kokį saldainį norėtumėte pašalinti iš sąrašo, įveskite tikslų pavadinimą:')
# c.execute(f"DELETE from saldainiai WHERE pavadinimas='{istrintas}'")
# atsakymas = c.execute("SELECT * From saldainiai").fetchall()
# #
# for ats in atsakymas:
#     print(ats)


# Susidedam duomenis grafikams į atskirus sąrašus

visi_skoniai = []

for i in sarasas:
    visi_skoniai.append(i[1])

kiekiai = []
print(visi_skoniai)
skoniai = list(set(visi_skoniai))
for skonis in skoniai:
    kiekis = visi_skoniai.count(skonis)
    kiekiai.append(kiekis)
print(skoniai)
print(kiekiai)
print(len(skoniai), len(kiekiai))

# Grafikai, pagal skonio populiarumą saraše

# Grafikai
np.random.seed(19680801)
fig, ax = plt.subplots()
fig1, ax1 = plt.subplots()

# Grafikas Nr.1
ax.barh(skoniai, kiekiai, align='center')
ax.invert_yaxis()
ax.set_ylabel('Skoniai')
ax.set_xlabel('Kiekis')
ax.set_title('Populiariausi saldainių skoniai ir jų kiekiai sąraše')

# Grafikas Nr.2
ax1.pie(kiekiai, labels = skoniai)
ax1.set_title('Skoniai, ir jų dalys bendrame "krepšyje"')


plt.show()
conn.commit()
conn.close()