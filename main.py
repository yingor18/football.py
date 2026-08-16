import streamlit as st
import random

# 設定網頁標題與圖示
st.set_page_config(page_title="足球生涯模擬器", page_icon="⚽", layout="centered")

st.title("⚽ 足球生涯模擬器")
st.caption("打造屬於你的傳奇球星生涯！")

# 1. 初始化球員數據 (保存在 session_state 中)
if "player" not in st.session_state:
    st.session_state.player = {
        "name": "Ho Yin",
        "age": 17,
        "club": "自由球員",
        "shooting": 65,
        "passing": 60,
        "dribbling": 62,
        "stamina": 70,
        "energy": 100,
        "matches": 0,
        "goals": 0,
        "assists": 0,
        "logs": ["你的職業足球生涯正式開始了！"]
    }

player = st.session_state.player

# 2. 側邊欄：顯示球員基本資料與面板
st.sidebar.header("👤 球員資訊")
st.sidebar.write(f"**姓名**：{player['name']}")
st.sidebar.write(f"**年齡**：{player['age']} 歲")
st.sidebar.write(f"**效力球隊**：{player['club']}")
st.sidebar.progress(player['energy'] / 100, text=f"體力：{player['energy']}/100")

# 能力值區塊
st.sidebar.subheader("📊 能力屬性")
col_s1, col_s2 = st.sidebar.columns(2)
col_s1.metric("射門", player['shooting'])
col_s2.metric("傳球", player['passing'])
col_s3, col_s4 = st.sidebar.columns(2)
col_s3.metric("盤帶", player['dribbling'])
col_s4.metric("體能", player['stamina'])

# 3. 主畫面：功能頁籤
tab1, tab2, tab3 = st.tabs(["🏟️ 進行比賽", "🏋️ 每日訓練", "📜 生涯日誌"])

with tab1:
    st.header("聯賽比賽")
    if player['energy'] < 20:
        st.warning("⚠️ 體力不足（低於 20），請先休息或進行輕度訓練！")
    else:
        if st.button("⚽ 參加本週比賽", type="primary"):
            player['energy'] -= 20
            player['matches'] += 1
            
            # 隨機模擬比賽結果
            team_score = random.randint(0, 4)
            opp_score = random.randint(0, 3)
            
            # 根據屬性計算個人表現
            scored = random.random() < (player['shooting'] / 150)
            assisted = random.random() < (player['passing'] / 180)
            
            p_goals = 1 if scored else 0
            p_assists = 1 if assisted else 0
            
            player['goals'] += p_goals
            player['assists'] += p_assists
            
            res_msg = f"第 {player['matches']} 場：比賽結束 {team_score}-{opp_score}。"
            if p_goals > 0:
                res_msg += " ⚽ 你取得了一個進球！"
            if p_assists > 0:
                res_msg += " 🅰️ 你送出了一次助攻！"
                
            player['logs'].insert(0, res_msg)
            st.success(res_msg)
            st.rerun()

    #生涯數據統計
    st.divider()
    st.subheader("📈 個人生涯數據")
    c1, c2, c3 = st.columns(3)
    c1.metric("出場數", player['matches'])
    c2.metric("總進球", player['goals'])
    c3.metric("總助攻", player['assists'])

with tab2:
    st.header("訓練中心")
    st.write("提升你的個人屬性（每次訓練消耗 15 體力）：")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🎯 射門特訓"):
            if player['energy'] >= 15:
                player['energy'] -= 15
                player['shooting'] += 1
                player['logs'].insert(0, "🏋️ 進行了射門特訓，射門 +1")
                st.rerun()
            else:
                st.error("體力不足！")
                
    with col2:
        if st.button("🎯 傳球特訓"):
            if player['energy'] >= 15:
                player['energy'] -= 15
                player['passing'] += 1
                player['logs'].insert(0, "🏋️ 進行了傳球特訓，傳球 +1")
                st.rerun()
            else:
                st.error("體力不足！")

    with col3:
        if st.button("😴 補充休息"):
            player['energy'] = min(100, player['energy'] + 40)
            player['logs'].insert(0, "😴 經過充分休息，體力恢復了 40")
            st.rerun()

with tab3:
    st.header("生涯日誌")
    for log in player['logs']:
        st.write(f"- {log}")
