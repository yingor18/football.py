import streamlit as st
import random

st.set_page_config(page_title="足球生涯模擬器 Deluxe", page_icon="⚽", layout="wide")

# 1. 初始化資料結構
if "player" not in st.session_state:
    st.session_state.player = {
        "name": "Ho Yin",
        "age": 17,
        "club": "自由球員",
        "wage": 500,           # 週薪 ($)
        "money": 2000,         # 存款 ($)
        "trainer": False,      # 是否聘請私人體能教練
        "house": "標準公寓",    # 住處
        "shooting": 65,
        "passing": 60,
        "dribbling": 62,
        "stamina": 70,
        "energy": 100,
        "matches": 0,
        "goals": 0,
        "assists": 0,
        "season": 1,
        "week": 1,
        "points": 0,           # 聯賽積分
        "logs": ["你的職業足球生涯正式開啟！"]
    }

player = st.session_state.player

def get_ovr(p):
    return int(p['shooting'] * 0.35 + p['passing'] * 0.3 + p['dribbling'] * 0.25 + p['stamina'] * 0.1)

# 2. 側邊欄（球員狀態與面板）
st.sidebar.title("👤 球員檔案")
st.sidebar.write(f"**姓名**：{player['name']} ({player['age']} 歲)")
st.sidebar.write(f"**效力球會**：{player['club']}")
st.sidebar.write(f"**週薪**：${player['wage']:,}")
st.sidebar.write(f"**存款**：${player['money']:,}")
st.sidebar.caption(f"第 {player['season']} 賽季 | 第 {player['week']}/38 週")

st.sidebar.progress(player['energy'] / 100, text=f"體力：{player['energy']}/100")

st.sidebar.subheader(f"📊 綜合能力值 (OVR): {get_ovr(player)}")
c1, c2 = st.sidebar.columns(2)
c1.metric("🎯 射門", player['shooting'])
c2.metric("🅰️ 傳球", player['passing'])
c3, c4 = st.sidebar.columns(2)
c3.metric("⚡ 盤帶", player['dribbling'])
c4.metric("💪 體能", player['stamina'])

st.title("⚽ 足球生涯模擬器 Deluxe")
st.caption("目標：從自由球員一路踢進豪門球會，拿下金球獎！")

# 3. 頁籤分頁
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🏟️ 比賽與賽季", 
    "🏋️ 訓練中心", 
    "💼 轉會市場", 
    "🏡 資產與生活", 
    "📜 生涯履歷"
])

# --- TAB 1: 比賽與賽季 ---
with tab1:
    st.header(f"第 {player['season']} 賽季 - 聯賽戰況")
    
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        st.subheader("📊 賽季數據")
        st.write(f"目前聯賽積分：**{player['points']} 分**")
        st.write(f"聯賽進球：**{player['goals']} 球**")
        st.write(f"聯賽助攻：**{player['assists']} 次**")
    
    with col_m2:
        st.subheader("⚽ 下一場比賽")
        cost = 15 if player['trainer'] else 20
        st.caption(f"體力消耗：{cost}（私人教練降低消耗）" if player['trainer'] else f"體力消耗：{cost}")
        
        if player['energy'] < cost:
            st.error("⚠️ 體力不足，請先去【訓練中心】選擇補充休息！")
        else:
            if st.button("▶️ 開始本週比賽", type="primary"):
                # 扣體力與給週薪
                player['energy'] -= cost
                player['money'] += player['wage']
                player['week'] += 1
                player['matches'] += 1
                
                # 模擬賽果
                ovr = get_ovr(player)
                team_score = random.randint(0, 3) + (1 if ovr > 70 else 0)
                opp_score = random.randint(0, 3)
                
                if team_score > opp_score:
                    player['points'] += 3
                elif team_score == opp_score:
                    player['points'] += 1
                    
                # 個人表現
                p_goal = 1 if random.random() < (player['shooting'] / 160) else 0
                p_assist = 1 if random.random() < (player['passing'] / 180) else 0
                player['goals'] += p_goal
                player['assists'] += p_assist
                
                log_text = f"第 {player['week']-1} 週：{player['club']} {team_score}-{opp_score} 對手。"
                if p_goal: log_text += " ⚽ 取得進球！"
                if p_assist: log_text += " 🅰️ 送出助攻！"
                player['logs'].insert(0, log_text)
                
                # 突發事件觸發 (15% 機率)
                if random.random() < 0.15:
                    event = random.choice([
                        ("📰 賽後新聞", "你獲選為全場最佳球員 (MVP)！士氣大振！"),
                        ("⚠️ 場外新聞", "賽前被拍到出入夜店，領隊對你發出口頭警告！"),
                        ("💬 記者會", "你在採訪中展現高情商發言，球迷支持度大幅上升！")
                    ])
                    player['logs'].insert(0, f"【{event[0]}】{event[1]}")
                
                # 結算賽季 (38週結束)
                if player['week'] > 38:
                    player['season'] += 1
                    player['week'] = 1
                    player['age'] += 1
                    st.balloons()
                    st.success(f"🎉 賽季結束！你在第 {player['season']-1} 賽季帶領球隊拿下 {player['points']} 分！")
                    player['points'] = 0
                else:
                    st.rerun()

# --- TAB 2: 訓練中心 ---
with tab2:
    st.header("🏋️ 每日特訓")
    st.write("訓練消耗 15 體力，提升 1 點指定屬性：")
    
    t1, t2, t3, t4 = st.columns(4)
    with t1:
        if st.button("🎯 射門特訓"):
            if player['energy'] >= 15:
                player['energy'] -= 15
                player['shooting'] += 1
                player['logs'].insert(0, "🏋️ 進行了射門特訓，射門 +1")
                st.rerun()
            else: st.error("體力不足！")
            
    with t2:
        if st.button("🅰️ 傳球特訓"):
            if player['energy'] >= 15:
                player['energy'] -= 15
                player['passing'] += 1
                player['logs'].insert(0, "🏋️ 進行了傳球特訓，傳球 +1")
                st.rerun()
            else: st.error("體力不足！")

    with t3:
        if st.button("⚡ 盤帶特訓"):
            if player['energy'] >= 15:
                player['energy'] -= 15
                player['dribbling'] += 1
                player['logs'].insert(0, "🏋️ 進行了盤帶特訓，盤帶 +1")
                st.rerun()
            else: st.error("體力不足！")

    with t4:
        if st.button("😴 補充休息"):
            player['energy'] = min(100, player['energy'] + 45)
            player['logs'].insert(0, "😴 經過充分休息，體力恢復了 45")
            st.rerun()

# --- TAB 3: 轉會市場 ---
with tab3:
    st.header("💼 球會邀約與轉會")
    ovr = get_ovr(player)
    
    offers = []
    if ovr < 65:
        offers = [("港超聯球會", 800), ("日職乙球會", 1500)]
    elif ovr < 75:
        offers = [("日職聯球會", 3500), ("葡超球會", 8000), ("英冠球會", 12000)]
    elif ovr < 85:
        offers = [("葡萄牙體育", 35000), ("波圖", 40000), ("熱刺", 60000)]
    else:
        offers = [("皇家馬德里", 150000), ("曼城", 160000), ("拜仁慕尼黑", 140000)]
        
    st.write(f"根據你目前的綜合能力值 (**OVR: {ovr}**)，以下球會對你感興趣：")
    
    for club_name, wage_offer in offers:
        col_o1, col_o2 = st.columns([3, 1])
        col_o1.write(f"⚽ **{club_name}** | 開出週薪：**${wage_offer:,}**")
        if col_o2.button(f"加盟 {club_name}", key=club_name):
            player['club'] = club_name
            player['wage'] = wage_offer
            player['logs'].insert(0, f"✍️ 官宣！你正式加盟 {club_name}，週薪提升至 ${wage_offer:,}！")
            st.success(f"成功加盟 {club_name}！")
            st.rerun()

# --- TAB 4: 資產與生活 ---
with tab4:
    st.header("🏡 個人資產與生活")
    
    col_a1, col_a2 = st.columns(2)
    with col_a1:
        st.subheader("🏋️ 團隊團隊")
        if player['trainer']:
            st.success("✅ 已聘請私人體能教練（每場比賽體力消耗 -5）")
        else:
            st.write("聘請私人體能教練 ($10,000)")
            if st.button("聘請體能教練"):
                if player['money'] >= 10000:
                    player['money'] -= 10000
                    player['trainer'] = True
                    player['logs'].insert(0, "💼 聘請了私人體能教練！")
                    st.rerun()
                else: st.error("存款不足！")

    with col_a2:
        st.subheader("🏠 居住環境")
        st.write(f"目前住處：**{player['house']}**")
        if player['house'] == "標準公寓":
            if st.button("購買豪華別墅 ($100,000)"):
                if player['money'] >= 100000:
                    player['money'] -= 100000
                    player['house'] = "豪華別墅"
                    player['stamina'] += 5
                    player['logs'].insert(0, "🏡 搬進了豪華別墅，體能上限 +5！")
                    st.rerun()
                else: st.error("存款不足！")

# --- TAB 5: 生涯履歷 ---
with tab5:
    st.header("📜 生涯日誌")
    st.write(f"總出場數：{player['matches']} | 總進球：{player['goals']} | 總助攻：{player['assists']}")
    st.divider()
    for log in player['logs']:
        st.write(f"- {log}")
