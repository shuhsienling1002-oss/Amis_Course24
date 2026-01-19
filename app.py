import streamlit as st
import time
import random
from io import BytesIO

# --- 1. 核心相容性修復 ---
def safe_rerun():
    """自動判斷並執行重整"""
    try:
        st.rerun()
    except AttributeError:
        try:
            st.experimental_rerun()
        except:
            st.stop()

def safe_play_audio(text):
    """語音播放安全模式"""
    try:
        from gtts import gTTS
        # 使用印尼語 (id) 發音
        tts = gTTS(text=text, lang='id')
        fp = BytesIO()
        tts.write_to_fp(fp)
        st.audio(fp, format='audio/mp3')
    except Exception as e:
        st.caption(f"🔇 (語音生成暫時無法使用)")

# --- 0. 系統配置 ---
st.set_page_config(page_title="Unit 24: O Romi'ad", page_icon="⏰", layout="centered")

# --- CSS 美化 (晨曦時間色調) ---
st.markdown("""
    <style>
    body { font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; }
    .source-tag { font-size: 12px; color: #aaa; text-align: right; font-style: italic; }
    
    /* 單字卡 */
    .word-card {
        background: linear-gradient(135deg, #E3F2FD 0%, #ffffff 100%);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
        margin-bottom: 15px;
        border-bottom: 4px solid #2196F3;
    }
    .emoji-icon { font-size: 48px; margin-bottom: 10px; }
    .amis-text { font-size: 22px; font-weight: bold; color: #1565C0; }
    .chinese-text { font-size: 16px; color: #7f8c8d; }
    
    /* 句子框 */
    .sentence-box {
        background-color: #E1F5FE;
        border-left: 5px solid #4FC3F7;
        padding: 15px;
        margin: 10px 0;
        border-radius: 0 10px 10px 0;
    }

    /* 按鈕 */
    .stButton>button {
        width: 100%; border-radius: 12px; font-size: 20px; font-weight: 600;
        background-color: #BBDEFB; color: #0D47A1; border: 2px solid #2196F3; padding: 12px;
    }
    .stButton>button:hover { background-color: #90CAF9; border-color: #1976D2; }
    .stProgress > div > div > div > div { background-color: #2196F3; }
    </style>
""", unsafe_allow_html=True)

# --- 2. 資料庫 (Unit 24: 14個單字 - 句子提取核心詞) ---
vocab_data = [
    {"amis": "Romi'ad", "chi": "日子 / 天氣", "icon": "📅", "source": "Row 252"},
    {"amis": "Dafak", "chi": "清晨 / 早上", "icon": "🌅", "source": "Row 1758"},
    {"amis": "Minanam", "chi": "學習", "icon": "📖", "source": "Row 1758"},
    {"amis": "Toki", "chi": "時間 / 鐘錶", "icon": "⏰", "source": "Row 676"},
    {"amis": "Dadaya", "chi": "晚上", "icon": "🌃", "source": "Row 416"},
    {"amis": "Romadiw", "chi": "唱歌", "icon": "🎤", "source": "Row 416"},
    {"amis": "Matini", "chi": "現在 / 此刻", "icon": "⌚", "source": "Row 1583"},
    {"amis": "Lomowad", "chi": "起床", "icon": "🛌", "source": "Row 1583"},
    {"amis": "Lahok", "chi": "中午 / 午餐", "icon": "🍱", "source": "Row 240"},
    {"amis": "Miheca", "chi": "年 / 歲", "icon": "🎂", "source": "Row 410"},
    {"amis": "Mahemek", "chi": "勤勞 / 以...為榮", "icon": "💪", "source": "Row 410"},
    {"amis": "Anini", "chi": "今天 / 現在", "icon": "👇", "source": "Row 1758"},
    {"amis": "Nacila", "chi": "昨天", "icon": "⏪", "source": "Row 1815"},
    {"amis": "Anocila", "chi": "明天", "icon": "⏩", "source": "Row 4610"},
]

# --- 句子庫 (7句: 嚴格源自 CSV 並移除連字號) ---
sentences = [
    {"amis": "Minanam to sowal no Pangcah anini a dafak.", "chi": "今天清晨學阿美族語。", "icon": "📖", "source": "Row 1758"},
    {"amis": "Romadiw koni a kaying i dadaya.", "chi": "這位小姐昨晚在唱歌。", "icon": "🎤", "source": "Row 416"},
    {"amis": "Lomowad ko wawa i matini.", "chi": "小孩現在起床。", "icon": "🛌", "source": "Row 1583"},
    {"amis": "Pina ko toki a maomah kami?", "chi": "我們幾點做農活(勞動)？", "icon": "🌾", "source": "Row 676"},
    {"amis": "Caay kalahok kako i tini.", "chi": "我沒有在這裡吃午餐。", "icon": "🍱", "source": "Row 240"},
    {"amis": "Mahemek ko ina ni Panay to mihecaheca.", "chi": "Panay的媽媽每年都很勤勞。", "icon": "💪", "source": "Row 410"},
    {"amis": "Fangcal ko romi'ad.", "chi": "天氣(日子)好。", "icon": "☀️", "source": "Row 252"},
]

# --- 3. 隨機題庫 (Synced) ---
raw_quiz_pool = [
    {
        "q": "Minanam to sowal no Pangcah anini a dafak.",
        "audio": "Minanam to sowal no Pangcah anini a dafak",
        "options": ["今天清晨學阿美語", "今天晚上唱歌", "今天中午吃飯"],
        "ans": "今天清晨學阿美語",
        "hint": "Minanam (學習), Dafak (清晨) (Row 1758)"
    },
    {
        "q": "Romadiw koni a kaying i dadaya.",
        "audio": "Romadiw koni a kaying i dadaya",
        "options": ["這位小姐昨晚在唱歌", "這位小姐在睡覺", "這位小姐在工作"],
        "ans": "這位小姐昨晚在唱歌",
        "hint": "Romadiw (唱歌), Dadaya (晚上) (Row 416)"
    },
    {
        "q": "單字測驗：Lomowad",
        "audio": "Lomowad",
        "options": ["起床", "睡覺", "坐下"],
        "ans": "起床",
        "hint": "Row 1583: Lomowad ko wawa (小孩起床)"
    },
    {
        "q": "單字測驗：Matini",
        "audio": "Matini",
        "options": ["現在/此刻", "昨天", "明天"],
        "ans": "現在/此刻",
        "hint": "Row 1583: ...i matini (在此刻)"
    },
    {
        "q": "Caay kalahok kako i tini.",
        "audio": "Caay kalahok kako i tini",
        "options": ["我沒有在這裡吃午餐", "我沒有在這裡睡覺", "我沒有在這裡工作"],
        "ans": "我沒有在這裡吃午餐",
        "hint": "Lahok (中午/午餐) (Row 240)"
    },
    {
        "q": "單字測驗：Mahemek",
        "audio": "Mahemek",
        "options": ["勤勞/榮耀", "生氣", "懶惰"],
        "ans": "勤勞/榮耀",
        "hint": "Row 410: ...to mihecaheca (每年都很...)"
    },
    {
        "q": "單字測驗：Toki",
        "audio": "Toki",
        "options": ["時間/鐘錶", "錢", "書"],
        "ans": "時間/鐘錶",
        "hint": "Pina ko toki? (幾點?) (Row 676)"
    },
    {
        "q": "單字測驗：Miheca",
        "audio": "Miheca",
        "options": ["年/歲", "月", "日"],
        "ans": "年/歲",
        "hint": "計算時間的單位 (Row 410)"
    }
]

# --- 4. 狀態初始化 (洗牌邏輯) ---
if 'init' not in st.session_state:
    st.session_state.score = 0
    st.session_state.current_q_idx = 0
    st.session_state.quiz_id = str(random.randint(1000, 9999))
    
    # 抽題與洗牌
    selected_questions = random.sample(raw_quiz_pool, 3)
    final_questions = []
    for q in selected_questions:
        q_copy = q.copy()
        shuffled_opts = random.sample(q['options'], len(q['options']))
        q_copy['shuffled_options'] = shuffled_opts
        final_questions.append(q_copy)
        
    st.session_state.quiz_questions = final_questions
    st.session_state.init = True

# --- 5. 主介面 ---
st.markdown("<h1 style='text-align: center; color: #1565C0;'>Unit 24: O Romi'ad</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666;'>時間與日子 (CSV Extracted)</p>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📚 詞彙與句型", "🎲 隨機挑戰"])

# === Tab 1: 學習模式 ===
with tab1:
    st.subheader("📝 核心單字 (從句子提取)")
    col1, col2 = st.columns(2)
    for i, word in enumerate(vocab_data):
        with (col1 if i % 2 == 0 else col2):
            st.markdown(f"""
            <div class="word-card">
                <div class="emoji-icon">{word['icon']}</div>
                <div class="amis-text">{word['amis']}</div>
                <div class="chinese-text">{word['chi']}</div>
                <div class="source-tag">src: {word['source']}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"🔊 聽發音", key=f"btn_vocab_{i}"):
                safe_play_audio(word['amis'])

    st.markdown("---")
    st.subheader("🗣️ 實用句型 (Data-Driven)")
    for i, s in enumerate(sentences):
        st.markdown(f"""
        <div class="sentence-box">
            <div style="font-size: 20px; font-weight: bold; color: #0D47A1;">{s['icon']} {s['amis']}</div>
            <div style="font-size: 16px; color: #555; margin-top: 5px;">{s['chi']}</div>
            <div class="source-tag">src: {s['source']}</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"▶️ 播放句型", key=f"btn_sent_{i}"):
            safe_play_audio(s['amis'])

# === Tab 2: 隨機挑戰模式 ===
with tab2:
    st.markdown("### 🎲 隨機評量")
    
    if st.session_state.current_q_idx < len(st.session_state.quiz_questions):
        q_data = st.session_state.quiz_questions[st.session_state.current_q_idx]
        
        st.progress((st.session_state.current_q_idx) / 3)
        st.markdown(f"**Question {st.session_state.current_q_idx + 1} / 3**")
        
        st.markdown(f"### {q_data['q']}")
        if q_data['audio']:
            if st.button("🎧 播放題目音檔", key=f"btn_audio_{st.session_state.current_q_idx}"):
                safe_play_audio(q_data['audio'])
        
        # 使用洗牌後的選項
        unique_key = f"q_{st.session_state.quiz_id}_{st.session_state.current_q_idx}"
        user_choice = st.radio("請選擇正確答案：", q_data['shuffled_options'], key=unique_key)
        
        if st.button("送出答案", key=f"btn_submit_{st.session_state.current_q_idx}"):
            if user_choice == q_data['ans']:
                st.balloons()
                st.success("🎉 答對了！")
                time.sleep(1)
                st.session_state.score += 100
                st.session_state.current_q_idx += 1
                safe_rerun()
            else:
                st.error(f"不對喔！提示：{q_data['hint']}")
                
    else:
        st.progress(1.0)
        st.markdown(f"""
        <div style='text-align: center; padding: 30px; background-color: #BBDEFB; border-radius: 20px; margin-top: 20px;'>
            <h1 style='color: #0D47A1;'>🏆 挑戰成功！</h1>
            <h3 style='color: #333;'>本次得分：{st.session_state.score}</h3>
            <p>你已經學會時間表達了！</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 再來一局 (重新抽題)", key="btn_restart"):
            st.session_state.score = 0
            st.session_state.current_q_idx = 0
            st.session_state.quiz_id = str(random.randint(1000, 9999))
            
            new_questions = random.sample(raw_quiz_pool, 3)
            final_qs = []
            for q in new_questions:
                q_copy = q.copy()
                shuffled_opts = random.sample(q['options'], len(q['options']))
                q_copy['shuffled_options'] = shuffled_opts
                final_qs.append(q_copy)
            
            st.session_state.quiz_questions = final_qs
            safe_rerun()
