import json
import logging
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler
from telegram.constants import ParseMode
import random  
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from datetime import datetime
from flask import Flask
from threading import Thread
import os

app = Flask('')

@app.route('/')
def home():
    I_am_alive = "Bot çalışıyor ve aktif!"
    return I_am_alive

def run():
    # Render, Koyeb veya benzeri platformlar port atar, 
    # yerelde test ediyorsan 8080 kullanabilirsin
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# Botunu başlatmadan önce bu fonksiyonu çağır
if __name__ == "__main__":
    keep_alive()
    # Buradan sonra kendi bot başlatma kodunu (örneğin bot.infinity_polling()) yazabilirsin
TOKEN = "8421173302:AAEOZ7zgbj9fAIDa2ItXABGZKO3es-jMU_s"
DATA_FILE = 'roller.json'

ATANAN_ROLLER = {}  # Aktif roller: { user_id: "role_name emoji" }
OLEN_ROLLER = {}    # Ölen/Çıkarılan roller: { user_id: "role_name emoji" }
SON_LISTE_MESAJI = {}  
TBD_ESLESMELERI = {} 
HATE_ESLESMELERI = {}
GRUP_UYELERI = {} # { chat_id: [user_id1, user_id2, ...] }
GUNUN_ASKLARI = {}
UNO_KATILIMCILAR = {} # { chat_id: [user_id1, user_id2... ] }

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

ROL_EMOJILERI = {
    "TUGBA": "🎄🎄🎄",
    "TARIKAT AVCISI": "💂", 
    "YANCI": "💋", 
    "KORUYUCU MELEK": "👼", 
    "KM": "👼", 
    "DEDEKTIK": "🕵", 
    "GOZCU": "👳", 
    "OTACI": "🍃", 
    "MUHTAR": "🎖", 
    "SILAHSOR": "🔫", 
    "PRENS": "👑", 
    "CIFTCI": "👨‍🌾", 
    "BARISCIL": "☮️", 
    "DEMIRCI": "⚒", 
    "CIGIRTKAN": "📰", 
    "UYUTUCU": "💤", 
    "SIFACI": "🌟", 
    "KORSAN": "🏴‍☠", 
    "GOZCU CIRAGI": "🙇", 
    "KAHIN": "🌀", 
    "TILKI": "🦊", 
    "AVCI": "🎯", 
    "YASLI BILGE": "👵🏻", 
    "YB": "👵🏻", 
    "SARHOS": "🍻", 
    "MASON": "👷", 
    "SEYIRCI": "👁👁", 
    "HAYALET": "👻", 
    "SASI": "👀", 
    "UYURGEZER": "😴", 
    "ATEIST": "👦", 
    "ODUNCU": "🪓", 
    "FIRINCI": "🥖", 
    "BECERIKSIZ": "🤕", 
    "KUTUPHANECI": "📚", 
    "KURDUMSU": "👱🌚", 
    "EROS": "🏹", 
    "COMAR": "🃏", 
    "KOYLU": "👱", 
    "KAPICI": "🏘", 
    "BILEYICI": "👨🏻‍🦳", 
    "DELI": "🤪", 
    "EL HEREJE": "🦹‍♂️", 
    "YABANI COCUK": "👶", 
    "HAIN": "🖕", 
    "LANETLI": "😾", 
    "KURTADAM": "🐺", 
    "ALFA KURT": "⚡️", 
    "LYCAN": "🐺🌝", 
    "YAVRU KURT": "🐶", 
    "BEYAZ KURT": "🐺❄️", 
    "KUDUZ KURT": "🐺🤢", 
    "HIZLI KURT": "🐺💨", 
    "AC KURT": "🐺🍖", 
    "YASLI KURT": "🐲", 
    "FALCI": "🔮", 
    "TAKLITCI": "❌", 
    "IBLIS": "👺", 
    "SURVIVOR": "⛺️", 
    "SERI KATIL": "🔪", 
    "KUNDAKCI": "🔥", 
    "CIFT-GIDEN": "🎭", 
    "CG": "🎭", 
    "UNUTKAN": "🤔", 
    "TARIKATCI": "👤"
}
DIZI_KARAKTERLERI = [
    "Şerif Furtuna",
    "Esme Furtuna",
    "Eleni",
    "Adil Koçari",
    "Fadime Koçari",
    "Çakır",
    "Behçet",
    "Emine",
    "Sevcan",
    "Oruç Furtuna",
    "İso Furtuna",
    "Şirun Furtuna",
    "Amirum Dayı",
    "Akça Kız",
    "Gezep",
    "Bedriye",
    "Batum Hıdır",
    "Mikail",
    "Eyüphan",
    "Melina Miryano",
    "Boncuk",
    "Zarife",
    "Hicran",
    "İlve",
    "Atakan"
]
MOOD_LISTESI = [
    "mutlu",
    "yorgun",
    "hüzünlü",
    "durgun",
    "enerjik",
    "sinirli",
    "sakin",
    "heyecanlı",
    "çılgın",
    "delirmiş",
    "aptal",
    "salak",
    "güzel",
    "kırgın",
    "gerizekalı",
    "gözükara",
    "dahi",
    "neşeli"
    
    ]
UFC_LISTESI = ["Jon Jones", "Islam Makhachev", "Alex Pereira", "Israel Adesanya", "Max Holloway"," Sean O'Malley",
                "Dustin Poirier", "Charles Oliveira", "Alexander Volkanovski", "Ilia Topuria", "Khamzat Chimaev", 
                "Merab Dvalishvili", "Tom Aspinall", "Belal Muhammad","Dricus du Plessis", "Kamaru Usman", "Leon Edwards", "Justin Gaethje", 
                "Michael Chandler", "Paddy Pimblett", "Bo Nickal", "Shavkat Rakhmonov", "Colby Covington", "Robert Whittaker", "Gilbert Burns", 
                "Sean Strickland", "Petr Yan", "Brandon Moreno", "Alexandre Pantoja", "Aljamain Sterling", "Cory Sandhagen", "Umar Nurmagomedov", 
                "Brian Ortega", "Yair Rodriguez", "Beneil Dariush", "Arman Tsarukyan", "Michael Morales", "Kevin Holland", "Jiri Prochazka", 
                "Jamahal Hill", "Magomed Ankalaev", "Ciryl Gane", "Serghei Pavlovich", "Derrick Lewis", "Rose Namajunas", "Valentina Shevchenko", 
                "Zhang Weili", "Julianna Pena", "Kayla Harrison", "İbo Aslan", "Conor Mcgregor" ,"Khabib Nurmagomedov"]
SORU_FILE = 'sorular.json'
# Tek bir ortak soru havuzu
DOGRULUK_SORULARI = []
CESARET_SORULARI = []

def sorulari_yukle():
    global DOGRULUK_SORULARI, CESARET_SORULARI
    try:
        with open(SORU_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            DOGRULUK_SORULARI = data.get('dogruluk', [])
            CESARET_SORULARI = data.get('cesaret', [])
    except:
        DOGRULUK_SORULARI = []
        CESARET_SORULARI = []

def sorulari_kaydet():
    try:
        data = {
            'dogruluk': DOGRULUK_SORULARI,
            'cesaret': CESARET_SORULARI
        }
        with open(SORU_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        logging.error(f"Soru kaydetme hatası: {e}")
# --- ÖZEL MESAJ SORGUSU VE EKLEME ---
async def soru_ekle_dm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type != "private":
        await update.message.reply_text("🔒 Soru eklemeyi sadece **bana özel mesaj atarak** yapabilirsin!", parse_mode=ParseMode.MARKDOWN)
        return

    if not context.args:
        await update.message.reply_text("⚠️ **Kullanım:** `/ekleD Soru metni` veya `/ekleC Görev metni`", parse_mode=ParseMode.MARKDOWN)
        return

    command = update.message.text.split()[0].lower()
    metin = " ".join(context.args)

    if "d" in command:
        DOGRULUK_SORULARI.append(metin)
        tur_adi = "Doğruluk"
    else:
        CESARET_SORULARI.append(metin)
        tur_adi = "Cesaret"

    sorulari_kaydet()
    await update.message.reply_text(f"✅ **{tur_adi}** sorusu havuza eklendi!\n\n`{metin}`", parse_mode=ParseMode.MARKDOWN)

# --- YÖNETİCİ: SORULARI GÖR ---
async def sorulari_gor(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        await update.message.reply_text("❌ Bu komutu sadece yöneticiler kullanabilir.")
        return

    msg = "📋 **TÜM SORU HAVUZU**\n\n"
    
    msg += "❓ **DOĞRULUK SORULARI:**\n"
    if DOGRULUK_SORULARI:
        for i, s in enumerate(DOGRULUK_SORULARI, 1):
            msg += f"`D{i}` - {s}\n"
    else:
        msg += "*(Henüz doğruluk sorusu yok)*\n"

    msg += "\n🔥 **CESARET GÖREVLERİ:**\n"
    if CESARET_SORULARI:
        for i, s in enumerate(CESARET_SORULARI, 1):
            msg += f"`C{i}` - {s}\n"
    else:
        msg += "*(Henüz cesaret görevi yok)*\n"

    msg += "\n🗑 *Silmek için:* `/sorusil D1` veya `/sorusil C2`"
    
    await update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)

# --- YÖNETİCİ: SORU SİL ---
async def soru_sil(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        await update.message.reply_text("❌ Bu komutu sadece yöneticiler kullanabilir.")
        return

    if not context.args:
        await update.message.reply_text("⚠️ Kullanım: `/sorusil D1` veya `/sorusil C2`", parse_mode=ParseMode.MARKDOWN)
        return

    kod = context.args[0].upper()
    
    try:
        tur = kod[0]
        indeks = int(kod[1:]) - 1

        if tur == 'D':
            if 0 <= indeks < len(DOGRULUK_SORULARI):
                silinen = DOGRULUK_SORULARI.pop(indeks)
                sorulari_kaydet()
                await update.message.reply_text(f"✅ **Doğruluk Sorusu Silindi:**\n`{silinen}`", parse_mode=ParseMode.MARKDOWN)
            else:
                await update.message.reply_text("❌ Geçersiz Doğruluk soru numarası!")
        elif tur == 'C':
            if 0 <= indeks < len(CESARET_SORULARI):
                silinen = CESARET_SORULARI.pop(indeks)
                sorulari_kaydet()
                await update.message.reply_text(f"✅ **Cesaret Görevi Silindi:**\n`{silinen}`", parse_mode=ParseMode.MARKDOWN)
            else:
                await update.message.reply_text("❌ Geçersiz Cesaret görev numarası!")
        else:
            await update.message.reply_text("⚠️ Kod `D` veya `C` ile başlamalıdır. (Örn: `D1`, `C3`)")
    except ValueError:
        await update.message.reply_text("⚠️ Hatalı format! Örnek kullanım: `/sorusil D1`")

# --- GRUPTA SORU ÇEKME KOMUTLARI ---
async def dogruluk_cek(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not DOGRULUK_SORULARI:
        await update.message.reply_text("❓ Havuzda hiç doğruluk sorusu yok! Bota özel mesajdan `/ekleD soru...` yazarak ekleyin.", parse_mode=ParseMode.MARKDOWN)
        return
    soru = random.choice(DOGRULUK_SORULARI)
    user = update.effective_user.first_name
    await update.message.reply_text(f"🎯 **DOĞRULUK**\n\n👤 **Soru Sorulan:** {user}\n\n❓ **Soru:** {soru}", parse_mode=ParseMode.MARKDOWN)

async def cesaret_cek(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not CESARET_SORULARI:
        await update.message.reply_text("🔥 Havuzda hiç cesaret görevi yok! Bota özel mesajdan `/ekleC görev...` yazarak ekleyin.", parse_mode=ParseMode.MARKDOWN)
        return
    gorev = random.choice(CESARET_SORULARI)
    user = update.effective_user.first_name
    await update.message.reply_text(f"🔥 **CESARET**\n\n👤 **Meydan Okunan:** {user}\n\n💥 **Görev:** {gorev}", parse_mode=ParseMode.MARKDOWN)
# Yardımcı fonksiyon: Rol adını formatlar (Büyük harf ve Türkçe karakterleri basitleştirir)
def format_role_name(role_name):
    """Gelen rol adını büyük harf yapar ve Türkçe karakterleri basitleştirerek eşleşmeyi garanti eder."""
    
    formatted = role_name.strip().upper()
    
    # Türkçe karakterleri İngilizce eşdeğerlerine çevirme
    mapping = {
        'İ': 'I', 'I': 'I', 'Ğ': 'G', 'Ü': 'U', 'Ş': 'S', 'Ö': 'O', 'Ç': 'C',
        'ı': 'I', 'ğ': 'G', 'ü': 'U', 'ş': 'S', 'ö': 'O', 'ç': 'C'
    }
    
    # Basitleştirme işlemini gerçekleştirme
    result = "".join(mapping.get(char, char) for char in formatted)
    
    return result

# Bu yardımcı fonksiyonu kullanıcıları "tanımak" için her komutun başına ekleyeceğiz
def uyi_kaydet(chat_id, user_id):
    if chat_id not in GRUP_UYELERI:
        GRUP_UYELERI[chat_id] = []
    if user_id not in GRUP_UYELERI[chat_id]:
        GRUP_UYELERI[chat_id].append(user_id)

def rolleri_yukle():
    global ATANAN_ROLLER, OLEN_ROLLER, TBD_ESLESMELERI, HATE_ESLESMELERI, GRUP_UYELERI
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # JSON'dan gelen string ID'leri tekrar sayıya (int) çeviriyoruz
            ATANAN_ROLLER = {int(k): v for k, v in data.get('aktif', {}).items()}
            OLEN_ROLLER = {int(k): v for k, v in data.get('olen', {}).items()}
            TBD_ESLESMELERI = {int(k): v for k, v in data.get('tbd', {}).items()}
            HATE_ESLESMELERI = {int(k): v for k, v in data.get('hate', {}).items()}
            GRUP_UYELERI = {int(k): v for k, v in data.get('uyeler', {}).items()} # <-- Bu satırı ekledik
    except (FileNotFoundError, json.JSONDecodeError):
        pass

def rolleri_kaydet():
    try:
        data_to_save = {
            'aktif': ATANAN_ROLLER,
            'olen': OLEN_ROLLER,
            'tbd': TBD_ESLESMELERI,
            'hate': HATE_ESLESMELERI,
            'uyeler': GRUP_UYELERI  # <-- Bu satırı ekledik
        }
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data_to_save, f, indent=4, ensure_ascii=False)
    except Exception as e:
        logging.error(f"Kaydetme hatası: {e}")

async def is_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Kullanıcının yönetici olup olmadığını kontrol eder."""
    if update.effective_chat.type == "private": return True
    member = await context.bot.get_chat_member(update.effective_chat.id, update.effective_user.id)
    return member.status in ['creator', 'administrator']

def get_group_data(dictionary, chat_id):
    """Sözlükte gruba ait bir alan yoksa oluşturur ve döndürür."""
    if chat_id not in dictionary:
        dictionary[chat_id] = {}
    return dictionary[chat_id]
       
async def rol_al(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    
    if not context.args:
        await update.message.reply_text("Kullanım: `/rol köylü`", parse_mode=ParseMode.MARKDOWN)
        return

    raw_role_name = " ".join(context.args)
    emoji = ROL_EMOJILERI.get(format_role_name(raw_role_name), "")
    role_to_save = f"{raw_role_name} {emoji}".strip()

    aktifler = get_group_data(ATANAN_ROLLER, chat_id)
    oluler = get_group_data(OLEN_ROLLER, chat_id)

    if user_id in oluler:
        oluler.pop(user_id)

    aktifler[user_id] = role_to_save
    uyi_kaydet(chat_id, user_id)
    rolleri_kaydet()
    
    await roller(update, context)

async def roller(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    aktifler = get_group_data(ATANAN_ROLLER, chat_id)

    if chat_id in SON_LISTE_MESAJI:
        try:
            await context.bot.delete_message(chat_id=chat_id, message_id=SON_LISTE_MESAJI[chat_id])
        except: pass

    if not aktifler:
        msg = await update.message.reply_text("Listede kimse kalmadı.")
        SON_LISTE_MESAJI[chat_id] = msg.message_id
        return

    liste_metni = "<b>🎊 Hayatta Kalan Rol Listesi:</b>\n\n"
    user_display_data = []
    for uid, role in aktifler.items():
        try:
            member = await context.bot.get_chat_member(chat_id, uid)
            name = member.user.first_name
        except: name = f"Bilinmeyen ({uid})"
        user_display_data.append(f" ⭐︎ <b>{name}</b>: <i>{role}</i>")

    liste_metni += "\n".join(user_display_data)
    new_msg = await update.message.reply_text(liste_metni, parse_mode=ParseMode.HTML)
    SON_LISTE_MESAJI[chat_id] = new_msg.message_id

async def sil(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if not update.message.reply_to_message:
        await update.message.reply_text("Silmek istediğiniz kişiyi alıntılayın.")
        return
    
    user_id_to_delete = update.message.reply_to_message.from_user.id
    aktifler = get_group_data(ATANAN_ROLLER, chat_id)
    oluler = get_group_data(OLEN_ROLLER, chat_id)

    if user_id_to_delete in aktifler:
        del aktifler[user_id_to_delete]
        if user_id_to_delete in oluler: del oluler[user_id_to_delete]
        rolleri_kaydet()
        await roller(update, context)
    else:
        await update.message.reply_text("Bu kişinin rolü bulunmamaktadır.")

async def temizle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    # Sadece bu grubun verisini temizle
    ATANAN_ROLLER[chat_id] = {}
    OLEN_ROLLER[chat_id] = {}
    rolleri_kaydet()
    await update.message.reply_text("🧹 Bu grubun listesi temizlendi.")

async def uno_anket(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        await update.message.reply_text("Sadece yöneticiler turnuva başlatabilir.")
        return
    chat_id = update.effective_chat.id
    UNO_KATILIMCILAR[chat_id] = []
    keyboard = [[InlineKeyboardButton("Katılıyorum ✅", callback_data="uno_katil")]]
    await update.message.reply_text(
        "🃏 <b>UNO TURNUVASI BAŞLIYOR!</b>\n\nKatılmak için butona basın.",
        reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.HTML
    )

async def uno_buton(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    chat_id = query.message.chat_id
    user_id = query.from_user.id
    user_full_name = query.from_user.first_name
    
    if chat_id not in UNO_KATILIMCILAR:
        UNO_KATILIMCILAR[chat_id] = []
        
    # Eğer kullanıcı zaten listedeyse sadece uyarı ver
    if user_id in UNO_KATILIMCILAR[chat_id]:
        await query.answer("Zaten turnuvaya kayıtlısın!", show_alert=True)
        return

    # Yeni kullanıcıyı ekle
    UNO_KATILIMCILAR[chat_id].append(user_id)
    uyi_kaydet(chat_id, user_id)
    
    # --- LİSTEYİ GÜNCELLEME KISMI ---
    katilimci_isimleri = []
    for uid in UNO_KATILIMCILAR[chat_id]:
        try:
            # Botun hafızasındaki isimleri çekmeye çalışıyoruz
            member = await context.bot.get_chat_member(chat_id, uid)
            katilimci_isimleri.append(f"• {member.user.first_name}")
        except:
            katilimci_isimleri.append(f"• Bilinmeyen Oyuncu")

    liste_str = "\n".join(katilimci_isimleri)
    kisi_sayisi = len(katilimci_isimleri)

    yeni_metin = (
        f"🃏 <b>UNO TURNUVASI BAŞLIYOR!</b>\n\n"
        f"Katılmak için aşağıdaki butona basın.\n\n"
        f"👥 <b>Katılımcı Sayısı:</b> {kisi_sayisi}\n"
        f"📝 <b>Liste:</b>\n{liste_str}\n\n"
        f"<i>Yönetici kura çekmek için /kura yazabilir.</i>"
    )

    # Mesajı butonla birlikte güncelle
    keyboard = [[InlineKeyboardButton("Katılıyorum ✅", callback_data="uno_katil")]]
    await query.edit_message_text(
        text=yeni_metin,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.HTML
    )
    
    await query.answer(f"Başarıyla katıldın {user_full_name}!")

async def uno_kura(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        await update.message.reply_text("Sadece yöneticiler kura çekebilir.")
        return
    chat_id = update.effective_chat.id
    ids = UNO_KATILIMCILAR.get(chat_id, [])
    if len(ids) < 2:
        await update.message.reply_text("⚠️ En az 2 katılımcı lazım.")
        return
    random.shuffle(ids)
    isimler = []
    for uid in ids:
        try:
            m = await context.bot.get_chat_member(chat_id, uid)
            isimler.append(m.user.first_name)
        except: isimler.append("Gizemli Oyuncu")
    
    metin = "⚔️ <b>UNO EŞLEŞMELERİ</b> ⚔️\n\n"
    while len(isimler) >= 2:
        metin += f"🔹 {isimler.pop()}  <b>VS</b>  {isimler.pop()}\n"
    if isimler: metin += f"🌟 {isimler[0]}  ➡️  <b>ÜST TURA GEÇTİ (BAY)</b>\n"
    
    UNO_KATILIMCILAR[chat_id] = [] # Listeyi temizle
    await update.message.reply_text(metin, parse_mode=ParseMode.HTML)

async def tbd_komutu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """/tbd komutu: Özel ID'lere kalıcı karakter atar; diğerlerine her zaman rastgele karakter verir."""
    
    user_id = update.effective_user.id
    user_name = update.effective_user.first_name 
    
    # 📌 Sadece kalıcı olmasını istediğimiz özel ID'ler ve karakterleri
    OZEL_ESLESMELER = {
        5589921248: "Gezep",
        5372260938: "Şerif Furtuna"
    }
    
    karakter_to_send = ""
    
    if user_id in OZEL_ESLESMELER:
        # 👑 Kullanıcı özel ID listesinde (Kalıcı Atama Mantığı)
        
        if user_id in TBD_ESLESMELERI:
            # Zaten atanmışsa: Kayıtlı karakteri kullan
            karakter_to_send = TBD_ESLESMELERI[user_id]
            
        else:
            # Atanmamışsa: Özel karakteri ata ve kaydet
            karakter_to_save = OZEL_ESLESMELER[user_id]
            TBD_ESLESMELERI[user_id] = karakter_to_save
            rolleri_kaydet()
            karakter_to_send = karakter_to_save
            
        # Özel mesajı gönder (Gezep ve Şerif Furtuna için)
        await update.message.reply_text(
            f"👑 {user_name}, sen <b>{karakter_to_send}</b>'sın!",
            parse_mode=ParseMode.HTML
        )
        
    else:
        # 💫 Kullanıcı özel ID listesinde değil (Her zaman rastgele mantık)
        
        # Her komut kullanımında yeni bir rastgele karakter seç
        random_karakter = random.choice(DIZI_KARAKTERLERI)
        karakter_to_send = random_karakter
        
        # Standart rastgele mesajı gönder
        await update.message.reply_text(
            f"💫 {user_name}, sen <b>{karakter_to_send}</b>'sın!",
            parse_mode=ParseMode.HTML
        )

async def mood_komutu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    user_name = update.effective_user.first_name 
    
    # 1. Rastgele Yüzdeyi Seçme (0'dan 100'e kadar)
    random_yuzde = random.randint(0, 100)
    
    # 2. Ruh Hali Listesinden Rastgele Bir Mood Seçme
    random_mood = random.choice(MOOD_LISTESI)
    
    # 3. Mesajı Hazırlama ve Gönderme
    await update.message.reply_text(
        f"{user_name} bugün kendini <i>%{random_yuzde} {random_mood}</i> hissediyor",
        parse_mode=ParseMode.HTML
    )

async def fav_komutu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    user_name = update.effective_user.first_name 
    
    # Kullanıcıyı ve grubu listeye kaydet (Bot bu kişiyi artık "tanıyor")
    uyi_kaydet(chat_id, user_id)
    
    uyeler = GRUP_UYELERI.get(chat_id, [])
    
    if len(uyeler) < 2:
        await update.message.reply_text("Henüz grupta yeterli kişi tanımıyorum. Biraz daha mesajlaşın! 😉")
        return

    # Kendisi hariç birini seçmeye çalışalım
    diger_uyeler = [u for u in uyeler if u != user_id]
    secilen_id = random.choice(diger_uyeler if diger_uyeler else uyeler)
    
    try:
        member = await context.bot.get_chat_member(chat_id, secilen_id)
        target_name = member.user.first_name
    except:
        target_name = "Gizemli Biri"

    await update.message.reply_text(
        f"💞 <b>{user_name}</b>'nin bu grupta en sevdiği kişi: <b>{target_name}</b> 💞",
        parse_mode=ParseMode.HTML
    )
async def ufc_komutu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    user_name = update.effective_user.first_name 
    
    random_ufc = random.choice(UFC_LISTESI)
    
    # 3. Mesajı Hazırlama ve Gönderme
    await update.message.reply_text(
        f"<b>{user_name}</b> bir UFC dövüşcüsü olsaydı<b> {random_ufc}</b> olurdu 🥊",
        parse_mode=ParseMode.HTML
    ) 

async def hate_komutu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    user_name = update.effective_user.first_name 
    
    uyi_kaydet(chat_id, user_id)
    uyeler = GRUP_UYELERI.get(chat_id, [])

    if len(uyeler) < 2:
        await update.message.reply_text("Nefret edecek kadar kimseyi tanımıyorum henüz... 🙄")
        return

    diger_uyeler = [u for u in uyeler if u != user_id]
    secilen_id = random.choice(diger_uyeler if diger_uyeler else uyeler)
    
    try:
        member = await context.bot.get_chat_member(chat_id, secilen_id)
        target_name = member.user.first_name
    except:
        target_name = "Biri"

    await update.message.reply_text(
        f"😠 <b>{user_name}</b>, şu an <b>{target_name}</b> kişisine acayip bilenmiş durumda! 😠",
        parse_mode=ParseMode.HTML
    )

async def slap_komutu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    # 1. Alıntı kontrolü
    if not update.message.reply_to_message:
        await update.message.reply_text("Lütfen bir mesajı alıntılayın")
        return
    
    # 2. İsimleri çekme
    # Tokat Atan (Komutu Kullanan)
    slapper_name = update.effective_user.first_name 
    
    # Tokat Yiyen (Alıntılanan)
    slapped_user = update.message.reply_to_message.from_user
    slapped_name = slapped_user.first_name
    
    # Kullanıcılar aynı mı?
    if update.effective_user.id == slapped_user.id:
        await update.message.reply_text(f"Ooo, <b>{slapper_name}</b> kendini tokatladı! İşte bu acıtır🤕", parse_mode=ParseMode.HTML)
        return
        
    # 3. Yanıtı Hazırlama ve Gönderme
    
    # Rastgele tokat ifadeleri ekleyebiliriz:
    slap_ifadeleri = [
        f"kişisine tokadı yapıştırdı!",
        f"kişisini gasp etti!",
        f"kişisini yere serdi!",
        f"kişisinin kahvesine tükürdü!",
        f"kişisinin saçına sakız yapıştırdı!",
        f"kişisine suikast girişiminde bulundu!",
        f"kişisinin ayağını gıdıkladı!",
        f"kişisinin elbisesini yırttı!",
        f"kişisinin hayat çizgisini kısalttı!",
        f"kişisine el bombası fırlattı!",
        f"kişisinin borç defterini kabarttı!",
        f"kişisinin selamını almadı!",
        f"kişisinin çorabını çaldı",
        f"kişisinin pastasını parmakladı!",
        f"kişisinin düğününü bastı!",
        f"kişisine yumruğu indirdi!",
        f"kişisiyle elim sende oynadı!",
        f"kişisinin çenesini çıkardı!",
        f"kişisinin travmalarını podcast yaptı!",
        f"kişisinin adını alemden sildi!",
        f"kişisine varoluşsal kriz yaşattı!",
        f"kişisinin gömleğine burnunu sildi",
        f"kişisinin içindeki boşluğa öküz gibi oturdu!",
        f"kişisinin dizisine dis attı!",
        f"kişisinin sakalına koli bandı yapıştırdı!",
        f"kişisine söz verip tutmadı!",
        f"kişisini sapanla avladı!",
        f"kişisinin başına düştü!",
        f"kişisinin gay olduğunu iddia etti!", 
        f"kişisinin yüzüne tükürdü!",
        f"kişisini kırmızı listeye ekledi!",
        f"kişisinin kulağına üfledi!",
        f"kişisine hakaret etti!",
        f"kişisine virüslü balon hediye etti!",
        f"kişisinin saçını düğümledi!",
        f"kişisini tekmeledi!",
        f"kişisini veterinere götürdü!",
        f"kişisinin ses telleriyle beste yaptı!",
        f"kişisinin doğum günü pastasından çıktı!",
        f"kişisinin kariyerini bitirdi!",
        f"kişisini çok fena ısırdı!",
        f"kişisini zombiye çevirdi!",
        f"kişisini Mars'a gönderdi!",
        f"kişisinin burnunu sıktı!",
        f"kişisiyle güreş tuttu!",
        f"kişisini denize attı!",
        f"kişisini 12 kg tüp gibi patlattı!",
        f"kişisini mangala oturttu!",
        f"kişisine tekme attı!",
        f"kişisinin saçlarını yoldu!",
        f"kişisine küfür eder gibi baktı!",
        f"kişisini çama oturttu!",
        f"kişisini timsahlara attı"
    ]
    random_slap_ifadesi = random.choice(slap_ifadeleri)
    
    cevap_metni = f"<b>{slapper_name}</b>, <b>{slapped_name}</b> {random_slap_ifadesi}"
    
    await update.message.reply_text(
        cevap_metni,
        parse_mode=ParseMode.HTML)

async def kiss_komutu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """/kiss komutu: Alıntı varsa o kişiyi, yoksa FAV_LISTESI'nden birini öper."""
    
    user_name = update.effective_user.first_name
    
    # 1. Alıntı var mı kontrol et
    if update.message.reply_to_message:
        target_name = update.message.reply_to_message.from_user.first_name
    else:
        # Alıntı yoksa listeden rastgele seç
        target_name = random.choice(FAV_LISTESI)

    # 2. Kendi kendini öpme kontrolü (Listedeki isimle kullanıcı ismi aynıysa)
    if user_name == target_name:
        await update.message.reply_text(
            f"<b>{user_name}</b>,  kendine kocaman bir öpücük kondurdu💋",
            parse_mode=ParseMode.HTML
        )
        return

    # 3. Rastgele Öpücük İfadesi
    kiss_ifadeleri = [
        "kişinin yanağına kocaman bir öpücük kondurdu💋",
        "kişiyi şap diye öptü",
        "kişiye beklenmedik bir anda sevgi dolu bir öpücük gönderdi. ❤️",
        "kişiye havadan bir öpücük fırlattı😚💨",
        "kişinin alnından öpüp helalimsin dedi.",
        "kişinin elini öptü.",
        "kişinin burnunu öptü🥹",
        "kişiye kocaman sarılıp kafasını öptü..",
        "kişinin gözlerinden öptü.",
        "kişinin saçlarını okşayıp öptü.",
        "kişinin ayağını öptü"

    ]
    secilen_ifade = random.choice(kiss_ifadeleri)

    # 4. Mesajı Gönder
    await update.message.reply_text(
        f"✨ <b>{user_name}</b>, <b>{target_name}</b> adlı {secilen_ifade}",
        parse_mode=ParseMode.HTML
    )

async def ship_komutu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    today = datetime.now().strftime("%Y-%m-%d") # Bugünün tarihi
    
    uyeler = GRUP_UYELERI.get(chat_id, [])
    
    # 1. Grupta yeterli kişi var mı kontrolü
    if len(uyeler) < 2:
        await update.message.reply_text("Günün çiftini seçebilmem için grupta en az 2 kişiyi tanımam lazım! Biraz mesajlaşın. 💕")
        return

    # 2. Bugün bu grupta seçim yapıldı mı kontrolü
    grup_ask_verisi = GUNUN_ASKLARI.get(chat_id)
    
    if grup_ask_verisi and grup_ask_verisi.get("tarih") == today:
        # Eğer bugün zaten seçilmişse, eski sonucu söyle
        await update.message.reply_text(
            f"💓 Bugünün şanslı çifti zaten seçildi: \n\n{grup_ask_verisi['cift']} \n\nYarın tekrar deneyin! 😉",
            parse_mode=ParseMode.HTML
        )
    else:
        # 3. Yeni çift seçme işlemi
        secilenler = random.sample(uyeler, 2) # Listeden rastgele 2 benzersiz kişi seç
        
        isimler = []
        for uid in secilenler:
            
            member = await context.bot.get_chat_member(chat_id, uid)
            isimler.append(member.user.first_name)
           
        
        cift_metni = f"<b>{isimler[0]}</b> ❤️ <b>{isimler[1]}</b>"
        
        # Veriyi kaydet (Hafızada tut)
        GUNUN_ASKLARI[chat_id] = {
            "tarih": today,
            "cift": cift_metni
        }
        
        # Dosyaya da kaydedelim ki bot kapanınca gitmesin (isteğe bağlı)
        # rolleri_kaydet() fonksiyonuna GUNUN_ASKLARI'nı da ekleyebilirsin.

        await update.message.reply_text(
            f"💘 <b>Günün Çifti Belirlendi!</b> 💘\n\nİşte bugün birbirine en çok yakışanlar:\n\n{cift_metni}\n\n✨ <i>Mutluluklar dileriz!</i>",
            parse_mode=ParseMode.HTML
        )
def main(): 
    keep_alive()   
    rolleri_yukle() 
    sorulari_yukle()
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("rol", rol_al)) 
    application.add_handler(CommandHandler("r", rol_al)) 
    application.add_handler(CommandHandler("roller", roller)) 
    application.add_handler(CommandHandler("sil", sil)) 
    application.add_handler(CommandHandler("temizle", temizle)) 
    application.add_handler(CommandHandler("tbd", tbd_komutu)) 
    application.add_handler(CommandHandler("mood", mood_komutu)) 
    application.add_handler(CommandHandler("fav", fav_komutu)) 
    application.add_handler(CommandHandler("hate", hate_komutu))    
    application.add_handler(CommandHandler("ufc", ufc_komutu))
    application.add_handler(CommandHandler("slap", slap_komutu))
    application.add_handler(CommandHandler("kiss", kiss_komutu))
    application.add_handler(CommandHandler("ship", ship_komutu))
    application.add_handler(CommandHandler(["ekled", "eklec"], soru_ekle_dm))
    application.add_handler(CommandHandler(["sorularigor", "sorulari_gor"], sorulari_gor))
    application.add_handler(CommandHandler("sorusil", soru_sil))
    application.add_handler(CommandHandler(["dogruluk", "d"], dogruluk_cek))
    application.add_handler(CommandHandler(["cesaret", "c"], cesaret_cek))
    application.add_handler(CommandHandler("uno", uno_anket))
    application.add_handler(CommandHandler("kura", uno_kura))
    application.add_handler(CallbackQueryHandler(uno_buton, pattern="^uno_katil$"))

    logging.info("Telegram Rol Botu çalışmaya başladı...")
    application.run_polling(poll_interval=1.0)
    
if __name__ == '__main__':
    keep_alive()
    main()
