import streamlit as st
import random
import time

st.set_page_config(page_title="綠茵傳奇 Pro", page_icon="⚽", layout="wide")

# 1. 初始化資料
if "player" not in st.session_state:
    st.session_state.player = {
        "name": "Ho Yin",
        "age": 17,
        "club": "橫濱水手",
        "wage": 1500,
        "money": 5000,
        "shooting": 68,
        "passing": 65,
        "dribbling": 66,
        "stamina": 70,
        "energy": 100,
        "coach_trust": 65,   # 教練信任度
        "fans_love": 50,     # 球迷支持度
        "matches": 0,
        "goals": 0,
        "assists": 0,
        "season": 1,
        "week": 1,
        "points": 12,        # 球會積分
        "last_match_result": "尚未開始賽季",
        "social_tweets": [
            "球迷A: 聽講青訓營有個叫 Ho Yin 嘅新人好有天份！",
            "記者B: 橫濱水手今季能否保級，就睇新秀發揮了。"
        ],
        "logs": ["17 歲正式簽約，展開職業足球生涯！"]
    }

p = st.session_state.player

def get_ovr(player):
    return int(player['shooting'] * 0.35 + player['passing'] * 0.3 + player['dribbling'] * 0.25 + player['stamina'] * 0.1)

ovr = get_ovr(p)

# --- 側邊欄：球員簡介與狀態 ---
st.sidebar.title("⚽ 綠茵傳奇 Pro")
st.sidebar.markdown(f"### 👤 **{p['name']}** (OVR: {ovr})")
st.sidebar.caption(f"效力：**{p['club']}** | {p['age']} 歲")
st.sidebar.divider()

st.sidebar.metric("💰 週薪", f"${p['wage']:,}")
st.sidebar.metric("💵 存款", f"${p['money']:,}")

st.sidebar.divider()
st.sidebar.progress(p['energy'] / 100, text=f"⚡ 體力：{p['energy']}/100")
st.sidebar.progress(p['coach_trust'] / 100, text=f"🧢 教練信任：{p['coach_trust']}%")
st.sidebar.progress(p['fans_love'] / 100, text=f"❤️ 球迷支持：{p['fans_love']}%")

st.sidebar.divider()
st.sidebar.caption(f"第 {p['season']} 賽季 | 第 {p['week']}/38 週")

# --- 主介面 ---
st.title("⚽ 綠茵傳奇 - 職業球員主控台")

# 頂部：最新社交媒體動態 (X / Twitter)
st.markdown("### 📱 社交媒體與球迷反應 (X / Twitter)")
col_tw1, col_tw2 = st.columns(2)
col_tw1.info(f"💬 {p['social_tweets'][0]}")
col_tw2.info(f"💬 {p['social_tweets'][1]}")

st.divider()

# 中部：本週核心操作區 (無須切換 Tab，全部單頁搞定)
st.markdown(f"## 🗓️ 第 {p['week']} 週日程")

col_act1, col_act2, col_act3 = st.columns(3)

# 動作 1：進行比賽
with col_act1:
    st.subheader("🏟️ 進行本週聯賽")
    st.write(f"對手：**聯賽勁敵**")
    if p['coach_trust'] < 40:
        st.error("⚠️ 教練信任過低：本場只能後備上陣 (出場時間受限)")
    else:
        st.success("👕 狀態良好：正選上陣")
        
    if st.button("🔥 正式開賽 (消耗 20 體力)", type="primary", use_container_width=True):
        if p['energy'] >= 20:
            p['energy'] -= 20
            p['matches'] += 1
            p['money'] += p['wage']
            
            # 模擬比賽直播
            st.markdown("---")
            st.subheader("📡 現場比賽直播中...")
            
            # 比賽文字模擬
            m_goals = 0
            m_assists = 0
            events = []
            
            # 上半場
            if random.randint(1, 100) < p['shooting']:
                m_goals += 1
                events.append("⚽ 32' **GOAL！** 你在禁區外接應妙傳，一腳世界波打破僵局！")
            else:
                events.append("❌ 32' 你在禁區前起腳遠射，可惜球擦柱而出。")
                
            # 下半場
            if random.randint(1, 100) < p['passing']:
                m_assists += 1
                events.append("🅰️ 75' **ASSIST！** 你送出一記手術刀直塞，隊友輕鬆推射破門！")
            elif random.randint(1, 100) < p['dribbling']:
                m_goals += 1
                events.append("⚽ 88' **GOAL！** 你連過兩人後冷靜扣過門將，推射空門得手！")
            else:
                events.append("❌ 88' 你嘗試強行突破被對方後衛合力包抄破壞。")
            
            p['goals'] += m_goals
            p['assists'] += m_assists
            
            # 生成賽後新聞同球迷 Tweets
            if m_goals + m_assists >= 2:
                p['coach_trust'] = min(100, p['coach_trust'] + 10)
                p['fans_love'] = min(100, p['fans_love'] + 12)
                p['points'] += 3
                p['social_tweets'] = [
                    f"球迷X: {p['name']} 簡直係神！單場 {m_goals}球{m_assists}助攻，天秀！",
                    f"體育報: {p['name']} 支配全場，帶領球隊取得重要勝仗！"
                ]
            elif m_goals + m_assists == 1:
                p['coach_trust'] = min(100, p['coach_trust'] + 5)
                p['fans_love'] = min(100, p['fans_love'] + 5)
                p['points'] += 3
                p['social_tweets'] = [
                    f"球迷Y: {p['name']} 表現唔錯，關鍵時刻靠得住！",
                    f"體育報: 憑藉 {p['name']} 的關鍵發揮，球隊小勝對手。"
                ]
            else:
                p['coach_trust'] = max(0, p['coach_trust'] - 5)
                p['points'] += 1
                p['social_tweets'] = [
                    f"球迷Z: {p['name']} 今日沉寂咗，狀態麻麻喎...",
                    f"媒體: 鋒線乏力，{p['name']} 全場未獲太多機會。"
                ]
            
            p['week'] += 1
            if p['week'] > 38:
                p['season'] += 1
                p['week'] = 1
                p['age'] += 1
                p['points'] = 0
                st.balloons()
            
            st.rerun()
        else:
            st.error("體力不足！請先休息恢復。")

# 動作 2：自主訓練
with col_act2:
    st.subheader("🏋️ 自主加練")
    train_option = st.selectbox("選擇特訓項目", ["🎯 射門 (加強得分)", "🅰️ 傳球 (加強助攻)", "⚡ 盤帶 (加強突破)", "💪 體能 (提升體力上限)"])
    
    if st.button("💪 開始自主特訓 (消耗 15 體力)", use_container_width=True):
        if p['energy'] >= 15:
            p['energy'] -= 15
            if "射門" in train_option: p['shooting'] += 1
            elif "傳球" in train_option: p['passing'] += 1
            elif "盤帶" in train_option: p['dribbling'] += 1
            elif "體能" in train_option: p['stamina'] += 1
            st.success("訓練完成，能力值升級！")
            st.rerun()
        else:
            st.error("體力不足！")

# 動作 3：休息與恢復
with col_act3:
    st.subheader("🛌 理療休養")
    st.write("進行水療與物理治療，快速恢復體力。")
    if st.button("☕ 休養一週 (體力 +50)", use_container_width=True):
        p['energy'] = min(100, p['energy'] + 50)
        p['week'] += 1
        p['money'] += p['wage']
        p['social_tweets'] = [
            f"球迷: {p['name']} 本週獲准休假養精蓄銳。",
            f"新聞: {p['club']} 安排核心球員進行輪休復原。"
        ]
        if p['week'] > 38:
            p['season'] += 1; p['week'] = 1; p['age'] += 1; p['points'] = 0
        st.rerun()

st.divider()

# 底部：聯賽情報與轉會動態
col_bot1, col_bot2 = st.columns(2)

with col_bot1:
    st.subheader("📊 聯賽形勢與個人數據")
    st.write(f"目前球隊聯賽積分：**{p['points']} 分**")
    m1, m2, m3 = st.columns(3)
    m1.metric("出場數", f"{p['matches']} 場")
    m2.metric("進球數", f"{p['goals']} 球")
    m3.metric("助攻數", f"{p['assists']} 次")

with col_bot2:
    st.subheader("💼 經理人轉會快訊")
    offers = [
        ("葡超 - 葡萄牙體育 (Sporting CP)", 73, 12000),
        ("西甲 - 皇家馬德里", 82, 85000),
        ("英超 - 曼城", 85, 95000)
    ]
    
    available_offer = False
    for club_name, req_ovr, wage in offers:
        if ovr >= req_ovr:
            available_offer = True
            st.write(f"✨ **{club_name}** 向你發出邀請！(週薪：${wage:,})")
            if st.button(f"✍️ 加盟 {club_name}", key=club_name):
                p['club'] = club_name
                p['wage'] = wage
                p['social_tweets'] = [
                    f"【重磅官宣】{p['name']} 以天價加盟 {club_name}！",
                    f"球迷: 歡迎 {p['name']} 來到新球會！"
                ]
                st.success(f"成功加盟 {club_name}！")
                st.rerun()
    if not available_offer:
        st.caption("目前你的 OVR 尚未達到豪門門檻，繼續表現吸引關注吧！")
