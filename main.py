from flask import Flask, render_template, request
import sqlite3

conn = sqlite3.connect('sonuclar.db')
cursor = conn.cursor()
app = Flask(__name__)

#Sorular ve cevaplar
sorular = {
    1: {
        "soru": "Aşağıdakilerden hangisi işletim sistemi değildir?",
        "cevaplar": ["Windows", "MacOS", "Linux", "BIOS"],
        "dogru_cevap": "BIOS"
    },
    2: {
        "soru": "Aşağıdaki metodlardan hangisi karakter yada metinsel ifadeler için kullanılır?",
        "cevaplar": ["int", "string", "double", "var"],
        "dogru_cevap": "string"
    },
    3: {
        "soru": "Aşağıdaki oyunlardan hangisinde bloklar, hayatta kalma ve çoklu oyunculuk içerikleri bulunur?",
        "cevaplar": ["Grand Theft Auto 5", "Call of Duty", "Need for Speed", "Minecraft"],
        "dogru_cevap": "Minecraft"
    },
    4: {
        "soru": "Aşağıdaki Disney Pixar filmlerinden hangisi 2024 yılınde gişe ve izlenme rekoru kırdı?",
        "cevaplar": ["Cars", "Toy Story 4", "Insıde Out 2", "Moana"],
        "dogru_cevap": "Insıde Out 2"
    },
    5: {
        "soru": "Aşağıdaki kelimelerden hangisi 'Medya Oynatıcı' anlamına gelir?",
        "cevaplar": ["Music List", "Media Player", "Hide File", "Word Document"],
        "dogru_cevap": "Media Player"
    },
}

def get_db_connection():
    conn = sqlite3.connect('sonuclar.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def quiz():
    return render_template('index.html', sorular=sorular)

@app.route('/', methods=['POST','GET'])
def cevap():
    #puan belirleme
    puan = 0
    for soru_id, soru in sorular.items():
        secilen_cevap = request.form.get(f'soru{soru_id}')#Cevap kontolü
        if secilen_cevap == soru['dogru_cevap']:
            puan += 20
    ogrenci = request.form['text']
    print(ogrenci +" "+ str(puan))
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO sonuc(ogrenci, notlar) VALUES (?, ?)", (ogrenci, puan))
        conn.commit()
        print("Veritabanına Kaydedildi.")
        return render_template('index.html', sorular=sorular, puan=puan, ogrenci=ogrenci)
    except sqlite3.Error as e:
        return render_template('hata.html', hata=str(e))
       
    
@app.route('/info')
def info():
    return render_template('info.html')

if __name__ == '__main__':
    conn.close()
    app.run(debug=True)