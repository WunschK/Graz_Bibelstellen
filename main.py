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




