import streamlit as st
import librosa
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os, base64
import matplotlib.font_manager as fm
import arabic_reshaper
from bidi.algorithm import get_display

# ----------------------------------------
# إعداد الصفحة
# ----------------------------------------
st.set_page_config(page_title="Music Comparator", layout="wide")

# ----------------------------------------
# إعداد خط عربي للرسم البياني
# ----------------------------------------
font_path = "/Users/abdulaziz/Desktop/Amiri-Regular1.ttf"
if os.path.exists(font_path):
    arabic_font = fm.FontProperties(fname=font_path)
else:
    arabic_font = fm.FontProperties(family="Arial")

def fix_arabic(text):
    return get_display(arabic_reshaper.reshape(text))

# ----------------------------------------
# الخلفية مع النصوص أقصى اليسار (الوصف مزحوف يمين)
# ----------------------------------------
def set_parallax(image_file):
    if os.path.exists(image_file):
        with open(image_file, "rb") as f:
            encoded = base64.b64encode(f.read()).decode()
        st.markdown(
            f"""
            <style>
            body {{
                margin: 0;
                padding: 0;
                background: black;
            }}
            .hero {{
                background-image: url("data:image/jpg;base64,{encoded}");
                height: 100vh;
                background-attachment: fixed;
                background-position: center;
                background-repeat: no-repeat;
                background-size: cover;
                position: relative;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: flex-start;  /* أقصى اليسار */
                color: white;
                text-align: left;
                padding-left: 0;   /* بدون مسافة */
            }}
            .hero::after {{
                content: "";
                position: absolute;
                bottom: 0;
                left: 0;
                width: 100%;
                height: 40%;
                background: linear-gradient(to bottom, rgba(0,0,0,0) 0%, rgba(0,0,0,1) 100%);
            }}
            header[data-testid="stHeader"] {{
                background: transparent;
                height: 0rem;
            }}
            div.block-container {{
                padding-top: 0rem !important;
                margin-top: 0rem !important;
            }}
            .glass {{
                background: rgba(0, 0, 0, 0.5);
                border-radius: 15px;
                padding: 20px;
                margin-bottom: 20px;
            }}
            h1.title-text {{
                font-size: 3.5em;
                margin-bottom: 0;
            }}
            p.desc-text {{
                font-size: 1.3em;
                color: #dddddd;
                margin-left: 40px; /* تزحيف الوصف لليمين */
            }}
            </style>
            <div class="hero">
                <h1 class="title-text">🎶 Music Comparator</h1>
                <p class="desc-text">قارن بين مقطعين موسيقيين باستخدام الذكاء الاصطناعي</p>
            </div>
            """,
            unsafe_allow_html=True
        )

set_parallax("fairuz.jpg")

# ----------------------------------------
# واجهة رفع الملفات
# ----------------------------------------
st.markdown('<div class="glass">', unsafe_allow_html=True)
file1 = st.file_uploader("📂 اختر الملف الصوتي الأول", type=["mp3", "wav", "ogg"])
file2 = st.file_uploader("📂 اختر الملف الصوتي الثاني", type=["mp3", "wav", "ogg"])
st.markdown('</div>', unsafe_allow_html=True)

# ----------------------------------------
# استخراج الخصائص
# ----------------------------------------
def extract_features(file):
    y, sr = librosa.load(file, duration=60)
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    spectral_centroid = np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))
    spectral_bandwidth = np.mean(librosa.feature.spectral_bandwidth(y=y, sr=sr))
    rolloff = np.mean(librosa.feature.spectral_rolloff(y=y, sr=sr))
    zero_crossing = np.mean(librosa.feature.zero_crossing_rate(y))
    rms = np.mean(librosa.feature.rms(y=y))

    return {
        "🎵 السرعة (Tempo - BPM)": round(float(tempo), 2),
        "🎼 الحدة (Spectral Centroid)": round(float(spectral_centroid), 2),
        "📊 عرض النغمة (Bandwidth)": round(float(spectral_bandwidth), 2),
        "🎤 ميل الصوت (Rolloff)": round(float(rolloff), 2),
        "🔀 تغيرات الصوت (Zero Crossing Rate)": round(float(zero_crossing), 4),
        "🔊 القوة (Loudness)": round(float(rms), 4),
    }

# ----------------------------------------
# توليد تفسير فني مبسط
# ----------------------------------------
def generate_summary(f1, f2):
    summary = []

    if f1["🎵 السرعة (Tempo - BPM)"] > f2["🎵 السرعة (Tempo - BPM)"]:
        summary.append("🎵 المقطع الأول يتميز بسرعة إيقاع واضحة تزيد من قوته.")
    elif f1["🎵 السرعة (Tempo - BPM)"] < f2["🎵 السرعة (Tempo - BPM)"]:
        summary.append("🎵 المقطع الثاني يتميز بسرعة إيقاع واضحة تزيد من قوته.")
    else:
        summary.append("🎵 المقطعين متقاربين في سرعة الإيقاع.")

    if f1["🔊 القوة (Loudness)"] > f2["🔊 القوة (Loudness)"]:
        summary.append("🔊 المقطع الأول بصوت أعلى وأوضح يبرز بشكل جيد.")
    elif f1["🔊 القوة (Loudness)"] < f2["🔊 القوة (Loudness)"]:
        summary.append("🔊 المقطع الثاني بصوت أعلى وأوضح يبرز بشكل جيد.")
    else:
        summary.append("🔊 المقطعين بنفس مستوى القوة تقريبًا.")

    if f1["🎼 الحدة (Spectral Centroid)"] > f2["🎼 الحدة (Spectral Centroid)"]:
        summary.append("🎼 المقطع الأول بنغمة حادة وصوت واضح أكثر.")
    elif f1["🎼 الحدة (Spectral Centroid)"] < f2["🎼 الحدة (Spectral Centroid)"]:
        summary.append("🎼 المقطع الثاني يظهر بحدة صوتية تجعله أكثر وضوحًا.")
    else:
        summary.append("🎼 المقطعين متقاربين في درجة الحدة.")

    return "\n".join([f"- {s}" for s in summary])

# ----------------------------------------
# عند رفع ملفين
# ----------------------------------------
if file1 and file2:
    st.markdown('<div class="glass">', unsafe_allow_html=True)
    st.success("📊 جاري تحليل الملفات...")

    features1 = extract_features(file1)
    features2 = extract_features(file2)

    df = pd.DataFrame([features1, features2], index=["المقطع الأول", "المقطع الثاني"])
    st.subheader("📋 مقارنة الخصائص الموسيقية")
    st.table(df)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="glass">', unsafe_allow_html=True)
    st.subheader("📈 مقارنة رسومية")

    labels = list(features1.keys())
    values1 = list(features1.values())
    values2 = list(features2.values())
    x = np.arange(len(labels))
    width = 0.35

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(x - width/2, values1, width, label=fix_arabic("المقطع الأول"), color="#1f77b4")
    ax.bar(x + width/2, values2, width, label=fix_arabic("المقطع الثاني"), color="#ff7f0e")

    ax.set_xticks(x)
    ax.set_xticklabels([fix_arabic(lbl) for lbl in labels], fontproperties=arabic_font, fontsize=11, rotation=20, ha="right")

    ax.set_title(fix_arabic("📊 مقارنة الخصائص الموسيقية"), fontproperties=arabic_font, fontsize=14, pad=20)
    ax.legend(prop=arabic_font, loc="upper right", fontsize=12, frameon=True)

    st.pyplot(fig)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="glass">', unsafe_allow_html=True)
    st.subheader("📝 التفسير المبسط")
    st.markdown(generate_summary(features1, features2))
    st.markdown('</div>', unsafe_allow_html=True)

else:
    st.info("👆 الرجاء رفع ملفين صوتيين للمقارنة.")

