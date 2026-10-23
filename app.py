import io
import os
import socket
import pandas as pd
import qrcode
import streamlit as st

# Sayfa Yapılandırması (Geniş Mod)
st.set_page_config(
    page_title="YİÜ Dijital Ekran Bağımlılığı & Persona Analizörü",
    layout="wide",
    page_icon="📱",
)

# ==========================================
# 💾 HATA KORUMALI CSV VERİ TABANI SİSTEMİ
# ==========================================
DOSYA_ADI = "kampus_verileri.csv"
SUTUNLAR = ["fakulte", "bolum", "ekran_suresi", "gece_suresi", "panik_seviyesi"]


# 1. Veriyi CSV Dosyasına Kaydetme
def veriyi_kaydet(yeni_veri):
    df_yeni = pd.DataFrame([yeni_veri])
    if not os.path.isfile(DOSYA_ADI):
        df_yeni.to_csv(DOSYA_ADI, index=False, encoding="utf-8-sig")
    else:
        df_yeni.to_csv(
            DOSYA_ADI, mode="a", header=False, index=False, encoding="utf-8-sig"
        )


# 2. Verileri Okuma (Eksik/Hatalı Sütun Korumalı)
def verileri_oku():
    if os.path.isfile(DOSYA_ADI):
        try:
            df = pd.read_csv(DOSYA_ADI, encoding="utf-8-sig")
            # Gerekli sütunlar eksikse güvenli boş DataFrame döndür
            for sutun in SUTUNLAR:
                if sutun not in df.columns:
                    return pd.DataFrame(columns=SUTUNLAR)
            return df
        except Exception:
            return pd.DataFrame(columns=SUTUNLAR)
    else:
        return pd.DataFrame(columns=SUTUNLAR)


# Local IP adresini otomatik tespit eden fonksiyon
def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


# YÜKSEK İHTİSAS ÜNİVERSİTESİ AKADEMİK VE İDARİ YAPISI
yiu_akademik_yapisi = {
    "Tıp Fakültesi": ["Tıp (Türkçe)", "Tıp (İngilizce)"],
    "Sağlık Bilimleri Fakültesi": [
        "Beslenme ve Diyetetik",
        "Dil ve Konuşma Terapisi",
        "Ebelik",
        "Ergoterapi",
        "Fizyoterapi ve Rehabilitasyon",
        "Hemşirelik",
        "Sağlık Yönetimi",
    ],
    "Spor Bilimleri Fakültesi": ["Antrenörlük Eğitimi", "Spor Yöneticiliği"],
    "Sağlık Hizmetleri Meslek Yüksekokulu": [
        "Ameliyathane Hizmetleri",
        "Anestezi",
        "Biyomedikal Cihaz Teknolojisi",
        "Elektronörofizyoloji",
        "Fizyoterapi",
        "İlk ve Acil Yardım",
        "Optisyenlik",
        "Tele-Sağlık Teknikerliği",
        "Tıbbi Dokümantasyon ve Sekreterlik",
        "Tıbbi Laboratuvar Teknikleri",
        "Tıbbi Tanıtım ve Pazarlama",
        "Tıbbi Veri İşleme Teknikerliği",
    ],
    "Meslek Yüksekokulu": [
        "Bilgisayar Programcılığı",
        "Eczane Hizmetleri",
        "Elektrik",
        "Grafik Tasarımı",
    ],
    "Akademik & İdari Personel": [
        "Akademisyen / Öğretim Üyesi",
        "Araştırma Görevlisi",
        "İdari Personel",
        "Diğer Kampüs Çalışanı",
    ],
}

# --- EKRAN DÜZENİ (Sol: %75 | Sağ: %25) ---
col_main, col_qr = st.columns([3, 1])

# ==========================================
# 📍 SOL TARAF: EKRAN BAĞIMLILIĞI ANALİZİ
# ==========================================
with col_main:
    st.title("📊 İstatistik & Veri Topluluğu")
    st.markdown("### 📱 YİÜ Dijital Ekran Bağımlılığı & Persona Analizörü")
    st.caption(
        "Verilerinizi girin, 5 saniyede kişiselleştirilmiş nörolojik"
        " analizinizi ve canlı kampüs verilerini görün!"
    )

    st.write("")

    # --- VERİ GİRİŞ PANELİ ---
    with st.expander("📝 Veri Giriş Paneli", expanded=True):

        col_f1, col_f2 = st.columns(2)
        with col_f1:
            secilen_fakulte = st.selectbox(
                "Fakülteniz / Yüksekokulunuz / Biriminiz:",
                list(yiu_akademik_yapisi.keys()),
            )
        with col_f2:
            secilen_bolum = st.selectbox(
                "Bölümünüz / Programınız / Unvanınız:",
                yiu_akademik_yapisi[secilen_fakulte],
            )

        st.markdown("---")
        st.markdown("##### 🔍 Dijital Alışkanlık Soruları")

        col_s1, col_s2 = st.columns(2)

        with col_s1:
            ekran_suresi = st.slider(
                "Günlük ortalama ekran süren (saat):", 0, 18, 7
            )
            gece_suresi = st.slider(
                "Gece yatakta ekrana bakma süren (dakika):", 0, 180, 45
            )
            sabah_bakis = st.slider(
                "Sabah gözünü açar açmaz ekrana bakma süren (dakika):", 0, 60, 10
            )
            dijital_tur = st.selectbox(
                "En çok vakit harcadığın içerik türü:",
                [
                    "Shorts / Reels / TikTok (Kısa Videolar)",
                    "Mobil / Bilgisayar Oyunları",
                    "Sosyal Medya & Chat (WhatsApp, Instagram)",
                    "Dizi / Film / YouTube",
                ],
            )

        with col_s2:
            panik_seviyesi = st.slider(
                "Şarjın %15'in altına düştüğündeki panik seviyen (1-10):",
                1,
                10,
                7,
            )
            odak_suresi = st.slider(
                "Ders/İş çalışırken telefona bakma aralığın (dakikada bir):",
                5,
                120,
                20,
            )
            bildirim_kontrol = st.slider(
                "Günde nedensiz / bildirimsiz ekran açma sayısı:", 0, 120, 40
            )
            hayali_titresim = st.radio(
                "Cebinde telefon çalmadığı halde titreşim hissettiğin oluyor"
                " mu? (Phantom Vibe)",
                ["Sık Sık Oluyor", "Bazen Oluyor", "Hiç Olmadı"],
                horizontal=True,
            )

        st.write("")
        analiz_et = st.button(
            "🔴 EKRAN BAĞIMLILIĞIMI ANALİZ ET", use_container_width=True
        )

    # ==========================================
    # 🎯 DİNAMİK SONUÇ EKRANI
    # ==========================================
    if analiz_et:
        yeni_kayit = {
            "fakulte": secilen_fakulte,
            "bolum": secilen_bolum,
            "ekran_suresi": ekran_suresi,
            "gece_suresi": gece_suresi,
            "panik_seviyesi": panik_seviyesi,
        }
        veriyi_kaydet(yeni_kayit)

        st.success(
            f"✅ **{secilen_fakulte} - {secilen_bolum}** veriniz veritabanına"
            " başarıyla kaydedildi!"
        )

        raw_score = (
            (ekran_suresi * 4)
            + (gece_suresi / 2)
            + (sabah_bakis * 0.8)
            + (panik_seviyesi * 3)
            + ((120 - odak_suresi) * 0.2)
            + (bildirim_kontrol * 0.3)
        )
        score = min(int(raw_score), 100)

        st.markdown("## 📋 Analiz Raporu & Dijital Karne")
        st.write(f"**Genel Dijital Bağımlılık Endeksi:** **%{score}**")
        st.progress(score / 100)

        if score >= 80:
            persona_title = "🚨 DİJİTAL ZOMBİ (Kritik Seviye Bağımlı)"
            persona_desc = (
                "Gerçek dünyadan kopuş başlamış! Mavi ışık maruziyetiniz tavan"
                " yapmış durumda."
            )
            card_type = st.error
        elif score >= 60:
            persona_title = "📲 DOOMSCROLLER (Şiddetli Akış Bağımlısı)"
            persona_desc = (
                "Sürekli ekran kaydırma döngüsündesiniz. Beyniniz hızlı"
                " dopamin arıyor."
            )
            card_type = st.warning
        elif score >= 40:
            persona_title = "🔋 PHANTOM VIBE SENDROMLU (Orta Seviye Bağımlı)"
            persona_desc = (
                "Telefonunuzla duygusal bağ kurmuşsunuz, ancak kontrolü ele"
                " alabilirsiniz."
            )
            card_type = st.info
        else:
            persona_title = "🌿 DİJİTAL ZEN ÜSTADI (Dengeli Kullanıcı)"
            persona_desc = (
                "Tebrikler! Teknoloji sizi değil, siz teknolojiyi"
                " yönetiyorsunuz."
            )
            card_type = st.success

        card_type(f"### {persona_title}\n\n**Özet:** {persona_desc}")
        st.write("")

        m1, m2, m3, m4 = st.columns(4)
        yillik_gun = round((ekran_suresi * 365) / 24, 1)
        m1.metric("Yılda Ekranda Geçen Süre", f"{yillik_gun} Gün", "Ömründen")
        mavi_isik = min(int((ekran_suresi / 16) * 100), 100)
        m2.metric("Mavi Işık Maruziyeti", f"%{mavi_isik}", "Göz Yorgunluğu")
        odak_kaybi = round((120 - odak_suresi) / 10, 1)
        m3.metric("Odaklanma Süresi Kaybı", f"%{min(odak_kaybi*10, 90)}", "Verim Kaybı")
        melatonin = (
            "Kritik Düşük" if gece_suresi > 30 else "Normal Seviyede"
        )
        m4.metric("Uyku Kalitesi Etkisi", melatonin, f"-{gece_suresi} dk")

        st.markdown("---")

        st.markdown("### 💊 Tıbbi & Nörolojik Reçete (Kişiye Özel)")

        neuro_items = []
        detox_items = []

        if "Shorts" in dijital_tur:
            neuro_items.append(
                "**Dopamin Uyarımı:** Kısa videolar (Reels/TikTok) beyninizin"
                " odaklanma yeteneğini zayıflatıyor."
            )
            detox_items.append(
                "**15 Saniye Kuralı:** Kaydırmalı video uygulamalarına günlük"
                " süre sınırı koyun."
            )
        elif "Oyun" in dijital_tur:
            neuro_items.append(
                "**Adrenalin Deşarjı:** Mobil/PC oyunları sempatik sinir"
                " sistemini sürekli tetikte tutuyor."
            )
            detox_items.append(
                "**Mola Rutini:** Her 30 dakikalık oyun seansı sonrası uzaktaki"
                " bir noktaya odaklanın."
            )
        elif "Sosyal Medya" in dijital_tur:
            neuro_items.append(
                "**FOMO & Bekleme Kaygısı:** Sürekli mesaj/bildirim kontrolü"
                " zihinsel yorgunluk oluşturuyor."
            )
            detox_items.append(
                "**Sessiz Mod:** Sosyal medya uygulamalarının tüm anlık"
                " bildirimlerini kapatın."
            )
        else:
            neuro_items.append(
                "**Pasif Bilişsel Yük:** Uzun süreli dizi/YouTube takibi"
                " algısal zindeliği yavaşlatıyor."
            )
            detox_items.append(
                "**Otomatik Oynatmayı Kapatın:** Dizi platformlarında otomatik"
                " sonraki bölüme geçişi devreden çıkarın."
            )

        if hayali_titresim in ["Sık Sık Oluyor", "Bazen Oluyor"]:
            neuro_items.append(
                "**Phantom Vibe Sendromu:** Cebinizde hayali titreşim"
                " hissetmeniz, somatosensoriyel korteksinizin hassaslaştığını"
                " gösterir."
            )
            detox_items.append(
                "**Fiziksel Mesafe:** Çalışırken telefonu cebinizde değil,"
                " masanın uzağında tutun."
            )

        if gece_suresi >= 30:
            neuro_items.append(
                "**Melatonin Baskılanması:** Gece ekrana bakmak melatonin"
                " salgısını durdurur."
            )
            detox_items.append(
                "**Gece Yasağı:** Yatak odasına girmeden 30 dakika önce tüm"
                " ekranları kapatın."
            )

        col_r1, col_r2 = st.columns(2)
        with col_r1:
            st.info(
                "**🧠 Nörolojik Etki Değerlendirmesi:**\n\n"
                + "\n\n".join([f"* {item}" for item in neuro_items])
            )
        with col_r2:
            st.warning(
                "**⚡ Acil Uygulamalı Detoks Adımları:**\n\n"
                + "\n\n".join([f"{i+1}. {item}" for i, item in enumerate(detox_items)])
            )

    st.write("---")

    # ==========================================
    # 📊 GERÇEK ZAMANLI KAMPÜS VERİ PANOSU
    # ==========================================
    st.subheader("📊 Canlı Kampüs Veri Panosu")

    df_canli = verileri_oku()
    toplam_katilimci = len(df_canli)

    if toplam_katilimci == 0:
        st.info(
            "💡 **Henüz kaydedilmiş veri bulunmuyor.** Yukarıdaki panelden form"
            " doldurup 'EKRAN BAĞIMLILIĞIMI ANALİZ ET' butonuna basarak ilk"
            " veriyi siz ekleyin!"
        )
    else:
        ort_ekran = round(df_canli["ekran_suresi"].mean(), 1)
        ort_panik = round(df_canli["panik_seviyesi"].mean(), 1)
        ort_gece = round(df_canli["gece_suresi"].mean(), 1)

        cp1, cp2, cp3, cp4 = st.columns(4)
        cp1.metric("Toplam Katılımcı", f"{toplam_katilimci} Kişi")
        cp2.metric("Kampüs Ort. Ekran Süresi", f"{ort_ekran} Saat/Gün")
        cp3.metric("Ortalama Şarj Paniği", f"{ort_panik} / 10")
        cp4.metric("Gece Ekran Ortalaması", f"{ort_gece} Dakika")

        st.write("")
        st.markdown(
            "##### 🏫 Katılan Birimlere Göre Gerçek Ekran Süreleri"
            " (Saat/Gün)"
        )

        fakulte_ortalamalari = (
            df_canli.groupby("fakulte")["ekran_suresi"].mean().reset_index()
        )
        fakulte_ortalamalari.columns = [
            "Fakülte / Yüksekokul / Birim",
            "Ortalama Ekran Süresi (Saat)",
        ]

        st.bar_chart(
            data=fakulte_ortalamalari,
            x="Fakülte / Yüksekokul / Birim",
            y="Ortalama Ekran Süresi (Saat)",
            color="#FF4B4B",
        )


# ==========================================
# 📱 SAĞ TARAF: TELEFONLA ERİŞİM QR KODU
# ==========================================
with col_qr:
    st.markdown("### 📱 Telefonla Katıl")

    # Canlı İnternet Adresi
    target_url = "https://yiu-ekran-bagimliligi.streamlit.app"

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=2,
    )
    qr.add_data(target_url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    byte_im = buf.getvalue()

    st.image(byte_im, use_container_width=True)
    st.info(
        f"Kameranızla QR kodu taratarak doğrudan katılabilirsiniz:\n\n`{target_url}`"
    )
