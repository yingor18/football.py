import streamlit as st
import random
import plotly.graph_objects as go

st.set_page_config(page_title="綠茵傳奇 Pro - 職業足球生涯", page_icon="⚽", layout="wide")

# 1. 初始化遊戲狀態
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
        "coach_trust": 65,
        "fans_love": 50,
        "matches": 0,
        "goals": 0,
        "assists": 0,
        "season": 1,
        "week": 1,
        "points": 15,
        "has_trainer": False,
        "house": "無 (租房)",
        "rival_goals": 12, # 聯賽神射手競爭對手進球數
        "social_tweets": [
            "球迷A: 橫濱水手新星 Ho Yin 備受期待！",
            "媒體: 本賽季神射手之爭異常激烈。"
        ],
        "current_event": None,
        "logs": ["17 歲正式簽約，開啟職業足球生涯！"]
    }

p = st.session_state.player

def get_ovr(player):
    return int(player['shooting'] * 0.35 + player['passing'] * 0.3 + player['dribbling'] * 0.25 + player['stamina'] * 0.1)

ovr = get_ovr(p)

# --- 側邊欄：FIFA 風格球員卡與雷達圖 ---
st.sidebar.title("⚽ 球員檔案")
st.sidebar.markdown(f"### 👤 **{p['name']}** (OVR: **{ovr}**)")
st.sidebar.caption(f"效力：**{p['club']}** | 年齡：{p['age']} 歲")

# 能力雷達圖
fig = go.Figure(data=go.Scatterpolar(
  r=[p['shooting'], p['passing'], p['dribbling'], p['stamina']],
  theta=['射門', '傳球', '盤帶', '體能'],
  fill='toself',
  line_color='#00CC96'
))
fig.update_layout(
  polar=dict(radialaxis=dict(visible=True, range=[40, 100])),
  showlegend=False, margin=dict(l=20, r=20, t=20, b=20), height=200
)
st.sidebar.plotly_chart(fig, use_container_width=True)

st.sidebar.metric("💰 週薪", f"${p['wage']:,}")
st.sidebar.metric("💵 存款", f"${p['money']:,}")
st.sidebar.divider()
st.sidebar.progress(p['energy'] / 100, text=f"⚡ 體力：{p['energy']}/100")
st.sidebar.progress(p['coach_trust'] / 100, text=f"🧢 教練信任度：{p['coach_trust']}%")
st.sidebar.progress(p['fans_love'] / 100, text=f"❤️ 球迷支持度：{p['fans_love']}%")

# --- 主介面 ---
st.title("⚽ 綠茵傳奇 Pro - 職業足球生涯")

# 1. 社交媒體與新聞
st.markdown("### 📱 社交媒體與媒體動態")
c_tw1, c_tw2 = st.columns(2)
c_tw1.info(f"💬 {p['social_tweets'][0]}")
c_tw2.info(f"💬 {p['social_tweets'][1]}")

st.divider()

# 2. 突發事件觸發 (如有)
if p['current_event']:
    st.warning(f"🚨 **突發事件：{p['current_event']['title']}**")
    st.write(p['current_event']['desc'])
    col_e1, col_e2 = st.columns(2)
    if col_e1.button(p['current_event']['opt1_text']):
        p['current_event']['opt1_effect']()
        p['current_event'] = None
        st.rerun()
    if col_e2.button(p['current_event']['opt2_text']):
        p['current_event']['opt2_effect']()
        p['current_event'] = None
        st.rerun()
    st.divider()

# 3. 日程與核心操作
st.markdown(f"## 🗓️ 第 {p['season']} 賽季 - 第 {p['week']}/38 週")

col_act1, col_act2, col_act3 = st.columns(3)

# 【動作 1：比賽系統】
with col_act1:
    st.subheader("🏟️ 進行聯賽")
    st.write("對手：**聯賽強敵**")
    
    if st.button("🔥 正式開賽", type="primary", use_container_width=True):
        if p['energy'] >= 20:
            p['energy'] -= (15 if p['has_trainer'] else 22)
            p['matches'] += 1
            p['money'] += p['wage']
            
            # 隨機競爭對手進球
            if random.random() < 0.4:
                p['rival_goals'] += 1
                
            # 觸發賽事關鍵決策
            success_shoot = random.randint(1, 100) < p['shooting']
            success_pass = random.randint(1, 100) < p['passing']
            
            m_g, m_a = 0, 0
            if success_shoot: m_g += 1
            if success_pass: m_a += 1
            
            p['goals'] += m_g
            p['assists'] += m_a
            
            # 生成賽後社交媒體動態
            if m_g + m_a >= 1:
                p['coach_trust'] = min(100, p['coach_trust'] + 6)
                p['fans_love'] = min(100, p['fans_love'] + 8)
                p['social_tweets'] = [
                    f"球迷X: {p['name']} 表現太猛了！帶領球隊拿到勝仗！",
                    f"體育頭條: {p['name']} 在比賽中展現強大支配力。"
                ]
            else:
                p['coach_trust'] = max(0, p['coach_trust'] - 4)
                p['social_tweets'] = [
                    f"球迷Y: {p['name']} 今天狀態一般，需要加油了。",
                    f"記者: {p['club']} 本場缺乏進攻火力的支援。"
                ]
                
            # 15% 機率觸發賽後突發事件
            if random.random() < 0.2:
                p['current_event'] = {
                    "title": "賽後採訪",
                    "desc": "記者問：「你覺得球隊今天的表現如何？是不是教練戰術有問題？」",
                    "opt1_text": "🛡️ 支持教練戰術 (教練信任 +10)",
                    "opt1_effect": lambda: p.update({"coach_trust": min(100, p['coach_trust']+10)}),
                    "opt2_text": "🔥 暗示戰術太保守 (球迷支持 +10, 教練信任 -10)",
                    "opt2_effect": lambda: p.update({"coach_trust": max(0, p['coach_trust']-10), "fans_love": min(100, p['fans_love']+10)})
                }

            p['week'] += 1
            if p['week'] > 38:
                p['season'] += 1; p['week'] = 1; p['age'] += 1; p['rival_goals'] = random.randint(10, 15)
                st.balloons()
            st.rerun()
        else:
            st.error("體力不足！請先休養。")

# 【動作 2：訓練系統】
with col_act2:
    st.subheader("🏋️ 自主特訓")
    t_choice = st.selectbox("特訓項目", ["🎯 射門特訓", "🅰️ 傳球特訓", "⚡ 盤帶特訓", "💪 體能特訓"])
    if st.button("💪 開始訓練 (消耗 15 體力)", use_container_width=True):
        if p['energy'] >= 15:
            p['energy'] -= 15
            if "射門" in t_choice: p['shooting'] += 1
            elif "傳球" in t_choice: p['passing'] += 1
            elif "盤帶" in t_choice: p['dribbling'] += 1
            elif "體能" in t_choice: p['stamina'] += 1
            st.success("能力提升成功！")
            st.rerun()
        else: st.error("體力不足！")

# 【動作 3：休養與生活】
with col_act3:
    st.subheader("🛌 休養與度假")
    st.write("進行休養快速恢復狀態。")
    if st.button("☕ 充分休養一週 (體力 +50)", use_container_width=True):
        p['energy'] = min(100, p['energy'] + 50)
        p['week'] += 1
        p['money'] += p['wage']
        if p['week'] > 38:
            p['season'] += 1; p['week'] = 1; p['age'] += 1
        st.rerun()

st.divider()

# 4. 下方：聯賽競爭榜與資產商店
col_bot1, col_bot2 = st.columns(2)

with col_bot1:
    st.subheader("🏆 聯賽神射手排行榜 (Top Scorers)")
    st.table([
        {"排名": "1", "球員": "哈蘭德 (曼城)", "進球數": p['rival_goals']},
        {"排名": "2", "球員": f"{p['name']} ({p['club']})", "進球數": p['goals']},
        {"排名": "3", "球員": "姆巴佩 (皇家馬德里)", "進球數": max(0, p['rival_goals'] - 2)}
    ])

with col_bot2:
    st.subheader("🛍️ 個人資產與服務商店")
    
    if not p['has_trainer']:
        if st.button("💼 聘請私人體能教練 ($8,000) - 減少比賽體力消耗"):
            if p['money'] >= 8000:
                p['money'] -= 8000; p['has_trainer'] = True
                st.success("成功聘請私人教練！"); st.rerun()
            else: st.error("存款不足！")
    else:
        st.success("✅ 已擁有私人體能教練")

    if p['house'] == "無 (租房)":
        if st.button("🏡 購買豪華別墅 ($80,000) - 球迷支持度 +15"):
            if p['money'] >= 80000:
                p['money'] -= 80000; p['house'] = "豪華別墅"; p['fans_love'] = min(100, p['fans_love'] + 15)
                st.success("成功購買豪華別墅！"); st.rerun()
            else: st.error("存款不足！")
    else:
        st.success(f"🏡 現有住處：{p['house']}")
