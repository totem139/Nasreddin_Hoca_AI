# 🧠 Nasreddin Hoca AI - İki Modlu Gelişmiş (Mod Değiştirilebilir)
# by Kaan

from openai import OpenAI
from dotenv import load_dotenv
import os, random
from flask import Flask, render_template, request, jsonify
import base64

# --------------------------
# API anahtarı
# --------------------------
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# --------------------------
# Hoca'nın karakteri
# --------------------------
normal_hoca_persona = """
Sen Nasreddin Hoca'nın karakterini temsil eden bir yapay zekâsın.
Anadolu bilgesinin ruhunu taşıyorsun: halktan biri, esprili, bilge ama sade bir insansın.
Cevaplarında mizah, bilgelik ve halk dili harmanlanır. Kendini hiçbir zaman üstün görmezsin;
insanlarla eşit seviyede konuşursun. Her yanıtında ya düşündüren bir nükte, ya da kısa bir öğüt olmalıdır.
Bazen fıkra tarzında örnekler verirsin, ama bunlar modern dünyaya da uyarlanabilir.
Gerektiğinde önceki konuşmaları hatırlayarak cevap ver.
Tarzın Nasreddin Hoca’nın klasik özelliklerini taşır:
1. Zeki ama saf görünümlüsün.
2. Nüktedan, düşündüren bir mizah anlayışın var.
3. Halk diliyle konuşursun ama kaba olmazsın.
4. Cevaplarında kısa ama anlamlı ifadeler kullanırsın.
5. Gerektiğinde soruyla cevap vererek karşı tarafı düşündürürsün.
6. Asla sinirlenmez, alay etmez, bilgelikle yönlendirirsin.
7. Modern konular hakkında konuşurken bile Nasreddin Hoca mantığını korursun.
Örnek üslup:
- 'Evladım, eşeğe ters binmek bazen doğruyu göstermek içindir.'
- 'Bazen maya tutmaz ama denemeden de yoğurt olmaz.'
- 'İnternetin hızına değil, aklın sabrına güven.'
"""

kuran_hoca_persona = """
Sen Kuran Hoca'sın. Kullanıcının sorularına Kur'an'daki bilgilerle cevap ver.
Sorulara sadece doğru ve güvenilir sure ve ayetlerden alıntılar kullanarak yanıt ver.
Gerektiğinde önceki konuşmaları hatırlayarak cevap ver.
"""

# --------------------------
# Basit Kur'an verisi
# --------------------------
kuran_data = {
    "Fatiha": [
        "1. Rahmân ve Rahîm olan Allah'ın adıyla",
        "2. Hamd, âlemlerin Rabbi Allah'a mahsustur",
        "3. Rahmân ve Rahîm olan Allah'a hamdolsun",
        "4. Din gününün sahibine hamdolsun",
        "5. Yalnız sana ibadet eder ve yalnız senden yardım dileriz",
        "6. Bizi doğru yola ilet",
        "7. Kendilerine nimet verdiklerinin yoluna ilet, gazaba uğrayanların ve sapmışların yoluna değil"
    ],
    "İhlas": [
        "1. De ki: O Allah bir tektir",
        "2. Allah Samed'dir",
        "3. Doğurmadı ve doğurulmadı",
        "4. O'nun dengi hiçbir şey değildir"
    ]
}

# --------------------------
# Geçmiş ve eğitim
# --------------------------
gecmis = []
normal_egitim = [
    {"role": "user", "content": "Arkadaşım bana küstü"},
    {"role": "assistant", "content": "Evladım, gönül bu, kırılır da barışır da. Önce sen bir selam ver, buz erir gider."}
]

# --------------------------
# Başlangıç mod ve persona
# --------------------------
aktif_persona = normal_hoca_persona
aktif_egitim = normal_egitim
secim = "1"

# --------------------------
# Flask app
# --------------------------
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    global gecmis, aktif_persona, aktif_egitim, secim

    user_input = request.json['message']

    # Mod değiştirme komutu
    if user_input.startswith("/mod"):
        sec = user_input.split()[1]
        if sec == "1":
            aktif_persona = normal_hoca_persona
            aktif_egitim = normal_egitim
            secim = "1"
            return jsonify({"reply": "Mod değiştirildi: Normal Nasreddin Hoca"})
        elif sec == "2":
            aktif_persona = kuran_hoca_persona
            aktif_egitim = []
            secim = "2"
            return jsonify({"reply": "Mod değiştirildi: Kur'an Hoca"})
        else:
            return jsonify({"reply": "Geçersiz mod numarası"})

    # Kur'an Hoca modu
    if secim == "2":
        sure_found = False
        for sure, ayetler in kuran_data.items():
            if sure.lower() in user_input.lower():
                return jsonify({"reply": "\n".join(ayetler)})
        if not sure_found:
            mesaj_icerigi = f"Kullanıcının sorusuna yanıt verirken sadece Kur'an'dan alıntı yap. Önceki konuşmaları hatırla: {gecmis}. Soru: {user_input}"
            messages = [
                {"role": "system", "content": aktif_persona},
                {"role": "user", "content": mesaj_icerigi}
            ]
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages
            )
            reply = response.choices[0].message.content
            gecmis.append({"role": "user", "content": user_input})
            gecmis.append({"role": "assistant", "content": reply})
            return jsonify({"reply": reply})

    # Normal Hoca modu
    else:
        cevap_tipi = random.choice(["ogut", "fikra"])
        if cevap_tipi == "fikra":
            user_input_mod = f"Kısa bir fıkra ile cevap ver: {user_input}"
        else:
            user_input_mod = f"Bilgece bir öğüt ver: {user_input}"

        messages = [
            {"role": "system", "content": aktif_persona},
            *aktif_egitim,
            *gecmis,
            {"role": "user", "content": user_input_mod}
        ]
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )
        reply = response.choices[0].message.content
        gecmis.append({"role": "user", "content": user_input_mod})
        gecmis.append({"role": "assistant", "content": reply})
        return jsonify({"reply": reply})


@app.route("/test")
def test():
    return "Flask çalışıyor!"

if __name__ == "__main__":
    app.run(debug=True)