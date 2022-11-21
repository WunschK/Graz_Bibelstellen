# This is the Code for retrieving and analysing bible quotes in the Augsburger Interim

import requests as r
import bs4 as bs
import pandas as pd
from pprint import pprint
import csv

#Die Buch-Kürzel des alten Testaments
AT = ["Gn", "Ex", "Lv", "Nm", "Dt", "Ios", "Idc", "Rt", "1Sm", "2Sm", "3Rg", "4Rg", "1Par", "2Par", "Esr", "Neh", "Tb",
      "Idt", "Est", "1Mcc"
    , "2Mcc", "3Mcc", "4Mcc", "Iob", "Ps", "Prv", "Ecl", "Ct", "Sap", "Sir", "Is", "Ier", "Lam", "Bar", "Ez", "Dn",
      "Os", "Ioel", "Am", "Abd"
    , "Ion", "Mi", "Na", "Hab", "So", "Agg", "Za", "Mal"]

#Der Text der heruntergeladen werden soll
URL = 'https://exist.ulb.tu-darmstadt.de/2/r/edoc/resource/pa000008-0129'

#Initial download of XML-file and saving it to the drive
#response =r.get(URL)
#open('interim.xml', 'wb').write(response.content)

with open('interim.xml', 'r') as f:
    file = f.read()

soup = bs.BeautifulSoup(file, 'lxml')
#Die Anzahl aller refs mit cref
Refs = soup.find_all(attrs={'cref':True})
print(len(Refs))
#soup für notes mit ref, die cref haben.
suppy = soup.select('note:has(>ref[cref])')

#tests to identify which part we need. this is commented in and out a lot for testing
#test2 = suppy[5].find('ref').get('cref').split("_")[0]
#print(f"{test2}" )


#von soup.select zu at_stellen und nt_stellen
list_all =[suppy[i].find('ref') for i in range(len(suppy))]
list_at = [ref for ref in list_all if ref.get('cref').split('_')[0] in AT]
list_nt = [ref for ref in list_all if ref.get('cref').split('_')[0] not in AT]


# Liste für Vergleich
at_stellen = [ref for ref in Refs if ref['cref'].split('_')[0] in AT]
nt_stellen = [ref for ref in Refs if ref['cref'].split('_')[0] not in AT]



# Ziel: Ein pd.DataFrame der wie folgt ausschaut
#          kuerzel atnt       stelle zitat
# 0     Gn_1,26-27   at   Gen 1,26f.  None
# 1      Sir_15,14   at    Sir 15,14  None
# 2        Rm_5,12   nt     Röm 5,12  None
# 3      Eph_2,1-3   nt    Eph 2,1-3  None
# 4       Gal_5,17   nt     Gal 5,17  None




#Probe-Sachen
with open(f'interim2.xml', 'r') as f:
    file = f.read()
soup = bs.BeautifulSoup(file, 'lxml')
Refs = soup.select('ref[cRef]')

# Eine leere Liste wird erstellt und mit den Bibelstellen gefüllt. Hierbei wird sortiert, ob sie im Alten Testament stehen oder nicht.
# Ein zweites Auswahlkriterium ist die Frage, ob direkt vor dem Eltern-ELement des <ref type='biblical'> ein <q> steht, und somit ein direktes Zitat vorliegt.
data = []
for ref in Refs:
    if ref.get('cref').split('_')[0] in AT:
        if ref.parent.find_previous_sibling() == ref.parent.find_previous_sibling('q'):
            data.append((ref.get('cref') , 'at', ref.getText() , ref.parent.find_previous_sibling('q').get_text(' ',strip=True)))
        else:
            data.append((ref.get('cref'), 'at', ref.getText(), 'not a direct quote'))
    else:
        if ref.parent.find_previous_sibling() == ref.parent.find_previous_sibling('q'):
            data.append((ref.get('cref') , 'nt', ref.getText() , ref.parent.find_previous_sibling('q').get_text(' ',strip=True)))
        else:
            data.append((ref.get('cref'), 'nt', ref.getText(), 'not a direct quote'))
print(data[0])
print(data[282])
print(len(data))
# der eigentliche Dataframe wird gesetzt
df_data = pd.DataFrame(data)
# der Header wird gesetzt.
df_data.columns = ['kuerzel', 'atnt', 'stelle', 'zitat']



stellen = []
for i in range (0, len(df_data)):
    #if df_data['zitat'][i] != 'not a direct quote':
    stellen.append(df_data['stelle'][i])


# Hier wird eine Liste der wörtlichen Zitate erstellt
qs = []
for ref in Refs:
    if ref.parent.find_previous_sibling() == ref.parent.find_previous_sibling("q"):
        qs.append(ref.parent.find_previous_sibling("q").get_text(" ", strip=True))


# Zählen der Gesamtlänge des zitierten Textes; one Leerzeilen und Zeilenumbrüche
quote_len = 0
for i in range(len(qs)):
    quote_len +=len(qs[i].replace(" ","").replace("\n", ""))
    i+=1



ges = bs.BeautifulSoup(file, 'lxml')

ges_soup = ges.select('div')
total_len=0
for i in range(len(ges_soup)):
    total_len += len(ges_soup[i].getText().replace(" ", "").replace("n", ""))
print(f"Anzahl an erfassten Bibelstellen: {len(Refs)}")
print(f"wörtliche Zitate: {len(qs)}")
print("Gesamtlänge:" + str(total_len))
print("Zitatlänge :"+str(quote_len))
print("Prozentualer Anteil: " +(str(percent_calc(quote_len, total_len))))

