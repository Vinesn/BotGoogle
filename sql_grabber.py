import pymssql
import os

symbolIn = ''
user = ''
password = ''
host = ''
db = ''


def DaneAsortymentu(Select, From, host, user, password, db, Where=None, Symbol=None):
    conn = pymssql.connect(host=host, user=user, password=password, database=db)
    cursor = conn.cursor(as_dict=True)

    if Where and Symbol:
        strquery_towar = f"SELECT {Select} FROM {From} WHERE {Where} = %s"
        cursor.execute(strquery_towar, (Symbol,))
    else:
        strquery_towar = f"SELECT {Select} FROM {From}"
        cursor.execute(strquery_towar)

    rows = cursor.fetchall()
    
    conn.close()

    return rows

def save_image(image_data, file_path):
    with open(file_path, 'wb') as file:
        file.write(image_data)

def InfoGrabber(host, user, password, db, symbol):
    all_items = DaneAsortymentu("*", "ModelDanychContainer.Asortymenty", host, user, password, db)
    Obiekt_Id = DaneAsortymentu("*", "ModelDanychContainer.MediaDokumentElementy_MediaDokumentElement_Asortyment", host, user, password, db)

    media_map = {}
    poprawneId = {}
    for item in Obiekt_Id:
        MediaDokument_Id = DaneAsortymentu("MediaDokument_Id", "ModelDanychContainer.MediaDokumentElementy", host, user, password, db, "Id", item['Id'])
        if MediaDokument_Id:
            uuid_str = str(MediaDokument_Id[0]['MediaDokument_Id'])
            zdjecie = DaneAsortymentu("Dane", "ModelDanychContainer.ZawartosciDokumentow", host, user, password, db, "DokumentDane_Id", uuid_str)
            if zdjecie:
                media_map[item['Obiekt_Id']] = zdjecie[0]['Dane']
                poprawneId[item['Obiekt_Id']] = item['Obiekt_Id']

    items_details = []
    
    for item in all_items:
        if item['Symbol'] == symbol:
            nazwa = DaneAsortymentu("Nazwa", "ModelDanychContainer.Asortymenty", host, user, password, db, "Id", item['Id'])
            cena_brutto = DaneAsortymentu("CenaBrutto", "ModelDanychContainer.PozycjeCennika", host, user, password, db, "Id", item['Id'])
            opis = DaneAsortymentu("Opis", "ModelDanychContainer.Asortymenty", host, user, password, db, "Id", item['Id'])
            kategoria = DaneAsortymentu("Nazwa", "ModelDanychContainer.GrupyAsortymentu", host, user, password, db, "Id", item['Grupa_Id'])
            
            item_detail = {
                'ID': item['Id'],
                'Nazwa': nazwa[0]['Nazwa'],
                'CenaBrutto': round(cena_brutto[0]['CenaBrutto'], 2),
                'Opis': opis[0]['Opis'],
                'Kategoria': kategoria[0]['Nazwa'],
                'Zdjecie': "BRAK WYMAGANEGO PARAMETRU: Zdjęcie"
            }

            if item['Id'] in poprawneId:
                if not os.path.exists(r"C:\images"):
                    os.makedirs(r"C:\images")
                image_file_path = rf"C:\images\{item['Id']}.jpg"
                save_image(media_map[item['Id']], image_file_path)
                item_detail['Zdjecie'] = image_file_path

            items_details.append(item_detail)

    return items_details


