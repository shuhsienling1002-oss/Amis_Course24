import streamlit as st
import random
import os
import time

# --- 🛠️ 0. 系統配置 ---
st.set_page_config(
    page_title="Riko' - 阿美語服飾教室",
    page_icon="👕",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 🎨 1. CSS 美化 (主題：阿美族服飾紅/熱情紅) ---
st.markdown("""
    <style>
    body { font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; }
    
    /* 主色調：阿美紅 (#C62828) 與 織布白 */
    h1 { color: #C62828; text-align: center; margin-bottom: 0px; }
    .subtitle { text-align: center; color: #5D4037; margin-top: 5px; font-size: 18px; }
    .author-tag { text-align: center; color: #8D6E63; font-weight: bold; margin-bottom: 30px; font-size: 16px; }
    
    /* 單字卡 (暖色系漸層) */
    .word-card {
        background: linear-gradient(135deg, #FFEBEE 0%, #ffffff 100%);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
        margin-bottom: 15px;
        border-bottom: 4px solid #C62828; /* 紅色底線 */
        transition: transform 0.2s;
    }
    .word-card:hover { transform: translateY(-5px); }
    .emoji-icon { font-size: 48px; margin-bottom: 10px; }
    .amis-text { font-size: 24px; font-weight: bold; color: #B71C1C; margin-bottom: 5px; }
    .chinese-text { font-size: 16px; color: #5D4037; }
    .source-tag { font-size: 12px; color: #A1887F; text-align: right; font-style: italic; margin-top: 10px;}
    
    /* 句子框 (米色背景) */
    .sentence-box {
        background-color: #FFF3E0;
        border-left: 5px solid #FF9800;
        padding: 15px;
        margin: 10px 0;
        border-radius: 0 10px 10px 0;
    }
    .sent-amis { font-size: 20px; color: #E65100; font-weight: bold; }
    .sent-chi { font-size: 16px; color: #4E342E; margin-top: 5px; }

    /* 按鈕樣式 (暖色風格) */
    .stButton>button {
        width: 100%; 
        border-radius: 12px; 
        font-size: 18px; 
        font-weight: 600;
        background-color: #FFCDD2; 
        color: #B71C1C; 
        border: 2px solid #EF9A9A; 
        padding: 10px;
    }
    .stButton>button:hover { 
        background-color: #EF5350; 
        border-color: #E53935; 
        color: #fff;
    }
    
    /* 進度條顏色 */
    .stProgress > div > div > div > div { background-color: #C62828; }
    </style>
""", unsafe_allow_html=True)

# --- 📂 2. Data Layer (數據層 - Riko' 系列) ---
VOCAB_DATA = [
    {"amis": "Riko'", "chi": "衣服", "icon": "👕", "source": "核心單字", "audio": "riko.m4a"},
    {"amis": "Makapahay", "chi": "漂亮的", "icon": "✨", "source": "形容詞", "audio": "makapahay.m4a"},
    {"amis": "Kifetolay", "chi": "厚的", "icon": "🧥", "source": "形容詞", "audio": "kifetolay.m4a"},
    {"amis": "Kamoto'ay", "chi": "短的", "icon": "🩳", "source": "形容詞", "audio": "kamotoay.m4a"},
    {"amis": "Sakalikoda", "chi": "用來豐年舞祭的", "icon": "💃", "source": "用途", "audio": "sakalikoda.m4a"},
    {"amis": "Kaolahan", "chi": "喜歡的", "icon": "❤️", "source": "感受", "audio": "kaolahan.m4a"},
]

SENTENCE_DATA = [
    {"amis": "Makapahay kora riko'.", "chi": "那件衣服很漂亮。", "icon": "✨", "audio": "sent_01.m4a"},
    {"amis": "O kifetolay konini a riko'.", "chi": "這一件衣服是厚的。", "icon": "🧥", "audio": "sent_02.m4a"},
    {"amis": "O kamoto'ay kora a riko'.", "chi": "那件衣服是短的。", "icon": "🩳", "audio": "sent_03.m4a"},
    {"amis": "O riko' no 'Amis koni.", "chi": "這件衣服是阿美族服飾。", "icon": "👘", "audio": "sent_04.m4a"},
    {"amis": "O sakalikoda a riko' konini.", "chi": "這件衣服是豐年舞穿的。", "icon": "💃", "audio": "sent_05.m4a"},
    {"amis": "Kaolahan ako koni a riko'.", "chi": "這件衣服是我喜歡的。", "icon": "❤️", "audio": "sent_06.m4a"},
]

# --- ⚙️ 3. Service Layer (核心邏輯) ---

def safe_rerun():
    try:
        st.rerun()
    except AttributeError:
        try:
            st.experimental_rerun()
        except:
            st.stop()

class ResourceManager:
    """資源管理器：智慧路徑搜尋"""
    
    @staticmethod
    def find_audio_path(filename: str):
        """在多個可能的位置尋找檔案"""
        candidates = [
            f"Teacher_Course23/audio/{filename}",  # 主要路徑
            f"audio/{filename}",                   # 備用路徑
            filename                               # 根目錄
        ]
        
        for path in candidates:
            if os.path.exists(path):
                return path
        return None

    @staticmethod
    def play_audio(filename: str):
        found_path = ResourceManager.find_audio_path(filename)
        
        if found_path:
            try:
                with open(found_path, "rb") as f:
                    audio_bytes = f.read()
                st.audio(audio_bytes, format='audio/mp4')
            except Exception as e:
                st.error(f"播放錯誤: {e}")
        else:
            st.warning(f"⚠️ 找不到檔案: {filename}")
            with st.expander("🔧 為什麼沒聲音？"):
                st.write(f"系統找不到: {filename}")
                st.write("請確認檔案是否上傳至 Teacher_Course23/audio/")

class QuizEngine:
    @staticmethod
    def generate_quiz(num_questions=4):
        pool = VOCAB_DATA.copy()
        if len(pool) < 4: return []
        
        selected_targets = random.sample(pool, num_questions)
        quiz_set = []
        
        for target in selected_targets:
            answer = target['amis']
            distractors = [w['amis'] for w in pool if w['amis'] != answer]
            wrong_options = random.sample(distractors, 2)
            options = wrong_options + [answer]
            random.shuffle(options)
            
            quiz_set.append({
                "q": f"「{target['chi']}」的阿美語怎麼說？",
                "audio": target['audio'],
                "options": options,
                "ans": answer,
                "hint": f"提示：{target['source']} - {target['icon']}"
            })
        return quiz_set

# --- 📱 4. Presentation Layer (UI 介面) ---

def main():
    # 標題區 (阿美族服飾主題)
    st.markdown("<h1 style='text-align: center;'>👕 Riko' 阿美語服飾篇</h1>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>阿美語生活教室 | 主題：衣著與形容詞</div>", unsafe_allow_html=True)
    st.markdown("<div class='author-tag'>講師：高春美 | 教材提供者：高春美</div>", unsafe_allow_html=True)

    # 初始化 Session State
    if 'init' not in st.session_state:
        st.session_state.score = 0
        st.session_state.current_q_idx = 0
        st.session_state.quiz_questions = QuizEngine.generate_quiz()
        st.session_state.init = True

    tab1, tab2 = st.tabs(["📖 學習單字與句型", "🎲 隨機挑戰"])

    # === Tab 1: 學習模式 ===
    with tab1:
        st.subheader("📝 核心單字 (Vocabulary)")
        col1, col2 = st.columns(2)
        for i, word in enumerate(VOCAB_DATA):
            with (col1 if i % 2 == 0 else col2):
                st.markdown(f"""
                <div class="word-card">
                    <div class="emoji-icon">{word['icon']}</div>
                    <div class="amis-text">{word['amis']}</div>
                    <div class="chinese-text">{word['chi']}</div>
                    <div class="source-tag">{word['source']}</div>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"🔊 播放", key=f"btn_vocab_{i}"):
                    ResourceManager.play_audio(word['audio'])

        st.markdown("---")
        st.subheader("🗣️ 實用句型 (Sentences)")
        for i, sent in enumerate(SENTENCE_DATA):
            st.markdown(f"""
            <div class="sentence-box">
                <div class="sent-amis">{sent['icon']} {sent['amis']}</div>
                <div class="sent-chi">{sent['chi']}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"▶️ 朗讀句子", key=f"btn_sent_{i}"):
                ResourceManager.play_audio(sent['audio'])

    # === Tab 2: 測驗模式 ===
    with tab2:
        st.subheader("🧠 隨機測驗")
        
        questions = st.session_state.quiz_questions
        current_idx = st.session_state.current_q_idx
        
        if current_idx < len(questions):
            q_data = questions[current_idx]
            progress = current_idx / len(questions)
            st.progress(progress)
            
            st.markdown(f"### Q{current_idx + 1}: {q_data['q']}")
            
            if st.button("🔊 聽聽看", key=f"quiz_audio_{current_idx}"):
                ResourceManager.play_audio(q_data['audio'])
            
            cols = st.columns(len(q_data['options']))
            if f"answered_{current_idx}" not in st.session_state:
                for idx, opt in enumerate(q_data['options']):
                    if cols[idx].button(opt, key=f"opt_{current_idx}_{idx}"):
                        if opt == q_data['ans']:
                            st.success(f"🎉 正確！ {q_data['ans']}")
                            st.session_state.score += 25
                        else:
                            st.error(f"❌ 答錯了，正確答案是：{q_data['ans']}")
                            st.info(q_data['hint'])
                        
                        st.session_state[f"answered_{current_idx}"] = True
                        time.sleep(1.5)
                        st.session_state.current_q_idx += 1
                        safe_rerun()
            else:
                st.info("載入下一題中...")
        else:
            st.progress(1.0)
            st.balloons()
            final_score = st.session_state.score
            st.markdown(f"""
            <div style="text-align: center; padding: 30px; background-color: #FFEBEE; border-radius: 20px; border: 2px solid #C62828;">
                <h2 style="color: #B71C1C;">測驗完成！</h2>
                <h1 style="font-size: 60px; color: #C62828;">{final_score} 分</h1>
                <p>Makapahay kiso! (你很棒！)</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("🔄 再玩一次"):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                safe_rerun()

    # --- 🔍 除錯工具 ---
    with st.sidebar:
        st.header("🔧 開發者工具")
        st.write("路徑檢查 (Teacher_Course23)：")
        try:
            files = os.listdir(".")
            if "Teacher_Course23" in files:
                st.success("✅ 找到 Teacher_Course23")
                if os.path.exists("Teacher_Course23/audio"):
                    audio_files = os.listdir("Teacher_Course23/audio")
                    st.write(f"📂 audio 內有 {len(audio_files)} 個檔案")
                    st.code("\n".join(audio_files[:5]))
            else:
                st.warning("⚠️ 沒找到 Teacher_Course23")
        except Exception as e:
            st.error(f"讀取錯誤: {e}")

if __name__ == "__main__":
    main()
