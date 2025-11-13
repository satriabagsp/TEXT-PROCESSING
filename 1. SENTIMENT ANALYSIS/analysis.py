from tqdm import tqdm
from sentistrength_id.sentistrength_id import sentistrength
from koneksi_database import connectDB, set_var

# Untuk mengelompokkan sentimen berita dan sentimen kutipan
def sentiment():
    mydb, mycursor = connectDB()

    # config
    config = dict()
    config["negation"] = True
    config["booster"] = True
    config["ungkapan"] = True
    config["consecutive"] = True
    config["repeated"] = True
    config["emoticon"] = True
    config["question"] = True
    config["exclamation"] = True
    config["punctuation"] = True
    senti = sentistrength(config)

    # Membuka daftar berita yang telah diolah NER
    sql_berita = """ SELECT `id`, `konten_berita`, `kutipan`, `sub_indikator` FROM `temp_output` """
    mycursor.execute(sql_berita)
    berita = mycursor.fetchall()

    # Mengolah sentimen berita satu per satu
    for row in tqdm(berita):
        id = row[0]
        konten = row[1]
        kutipan = row[2]

        senti_konten = senti.main(konten)
        # sk_pos = senti_konten['max_positive']
        # sk_neg = senti_konten['max_negative']
        # skor_sk = int(sk_pos) + int(sk_neg)
        # sk = str(skor_sk)
        sk = senti_konten['kelas']


        senti_quote = senti.main(kutipan)
        # sq_pos = senti_quote['max_positive']
        # sq_neg = senti_quote['max_negative']
        # skor_sq = int(sq_pos) + int(sq_neg)
        # sq = str(skor_sq)
        sq = senti_quote['kelas']

        # input to db
        set_var('sentimen_berita', sk, id)
        set_var('sentimen_kutipan', sq, id)

