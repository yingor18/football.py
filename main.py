import streamlit as st
import random
import plotly.graph_objects as go

st.set_page_config(page_title="足球生涯模擬器 Pro", page_icon="⚽", layout="wide")

# 1. 初始化資料結構
if "player" not in st.session_state:
    st.session_state.player = {
        "name": "Ho Yin",
        "number": 10,
        "age": 17,
        "club": "自由球員",
        "wage": 500,
        "money": 2000,
        "trainer": False,
        "house": "標準公寓",
        "shooting": 68,
        "passing": 65,
        "dribbling": 66,
        "stamina": 70,
        "energy": 100,
        "matches": 0,
        "goals": 0,
        "assists": 0,
        "season": 1,
        "week": 1,
        "points": 0,
        "transfer_requested": False,
        "logs": ["你的職業足球生涯正式開啟！"]
    }

player = st.session_state.player

def get_ovr(p):
    return int(p['shooting'] * 0.35 + p['passing'] * 0.3 + p['dribbling'] * 0.25 + p['stamina'] * 0.1)

# 2. 側邊欄：球員資料與能力值雷達圖
st.sidebar.title("👤 球員檔案")
player['name'] = st.sidebar.text_input("球員姓名", value=player['name'])
player['number'] = st.sidebar.number_input("球衣號碼", min_value=1, max_value=99, value=player['number'])

st.sidebar.markdown(f"**效力球會**：{player['club']}")
st.sidebar.markdown(f"**年齡**：{player['age']} 歲 | **週薪**：${player['wage']:,}")
st.sidebar.markdown(f"**存款**：${player['money']:,}")
st.sidebar.caption(f"第 {player['season']} 賽季 | 第 {player['week']}/38 週")

st.sidebar.progress(player['energy'] / 100, text=f"體力：{player['energy']}/100")

# Plotly 能力雷達圖
ovr_val = get_ovr(player)
st.sidebar.subheader(f"📊 綜合能力 (OVR): {ovr_val}")

fig = go.Figure(data=go.Scatterpolar(
  r=[player['shooting'], player['passing'], player['dribbling'], player['stamina']],
  theta=['射門', '傳球', '盤帶', '體能'],
  fill='toself',
  line_color='#1f77b4'
))
fig.update_layout(
  polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
  showlegend=False,
  margin=dict(l=20, r=20, t=20, b=20),
  height=200
)
st.sidebar.plotly_chart(fig, use_container_width=True)

st.title("⚽ 足球生涯模擬器 Pro")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🏟️ 進行比賽", 
    "💼 轉會市場", 
    "🏋️ 訓練中心", 
    "🏡 個人資產", 
    "📜 生涯履歷"
])

# --- TAB 1: 進行比賽 (含關鍵時刻決策) ---
with tab1:
    st.header(f"第 {player['season']} 賽季 - 第 {player['week']} 週比賽")
    
    cost = 15 if player['trainer'] else 20
    if player['energy'] < cost:
        st.error("⚠️ 體力不足，請先至【訓練中心】休息！")
    else:
        st.subheader("⚽ 比賽關鍵決策")
        st.write("第 80 分鐘，比數平手！你在禁區前沿拿到球，對方後衛正在逼近：")
        
        col_act1, col_act2, col_act3 = st.columns(3)
        choice = None
        if col_act1.button("🚀 選擇：大力遠射 (考驗射門)"): choice = "shoot"
        if col_act2.button("👟 選擇：直塞助攻 (考驗傳球)"): choice = "pass"
        if col_act3.button("⚡ 選擇：強行盤帶突破 (考驗盤帶)"): choice = "dribble"
        
        if choice:
            player['energy'] -= cost
            player['money'] += player['wage']
            player['week'] += 1
            player['matches'] += 1
            
            # 根據決策與能力計算成功率
            success = False
            msg = ""
            if choice == "shoot":
                chance = player['shooting'] / 110
                if random.random() < chance:
                    success = True
                    player['goals'] += 1
                    msg = f"⚽ 絕殺！{player['name']} 在禁區外敲出一記世界波直接轟入球門死角！"
                else:
                    msg = "❌ 遠射力道太勁偏出立柱！"
            elif choice == "pass":
                chance = player['passing'] / 110
                if random.random() < chance:
                    success = True
                    player['assists'] += 1
                    msg = f"🅰️ 妙傳！{player['name']} 送出一記手術刀般的直塞，隊友輕鬆推射入網！"
                else:
                    msg = "❌ 傳球被對方中後衛截獲！"
            elif choice == "dribble":
                chance = player['dribbling'] / 110
                if random.random() < chance:
                    success = True
                    player['goals'] += 1
                    msg = f"⚽ 精彩連過兩人！{player['name']} 晃過門將把球推入空門！"
                else:
                    msg = "❌ 盤帶試圖過人時被對方破壞！"
            
            player['points'] += (3 if success else 1)
            player['logs'].insert(0, f"第 {player['week']-1} 週：{msg}")
            
            if success:
                st.balloons()
                st.success(msg)
            else:
                st.info(msg)
                
            if player['week'] > 38:
                player['season'] += 1
                player['week'] = 1
                player['age'] += 1
                player['points'] = 0
                st.success("🎉 賽季結束！進入新賽季！")
            st.rerun()

    st.divider()
    c1, c2, c3 = st.columns(3)
    c1.metric("聯賽積分", f"{player['points']} 分")
    c2.metric("總進球", player['goals'])
    c3.metric("總助攻", player['assists'])

# --- TAB 2: 轉會市場 (自主選擇球會) ---
with tab3 if False else tab2:
    st.header("💼 轉會市場與談判")
    ovr = get_ovr(player)
    
    st.subheader("📢 轉會意向")
    if player['transfer_requested']:
        st.warning("⏳ 你已提交轉會申請，經理人正在為你聯繫買家...")
        if st.button("撤回轉會申請"):
            player['transfer_requested'] = False
            st.rerun()
    else:
        if st.button("🙋‍♂️ 主動向球會提交轉會申請 (Request Transfer)"):
            player['transfer_requested'] = True
            st.success("已提交轉會申請！下一輪將會有更多球會聯繫你。")
            st.rerun()

    st.divider()
    st.subheader("📩 收到以下球會的正式報價（可自由選擇加盟）：")
    
    # 根據 OVR 與是否申請轉會生成潛在買家
    all_clubs = [
        ("日職聯 - 橫濱水手", 62, 2500),
        ("葡超 - 葡體 (Sporting CP)", 72, 12000),
        ("葡超 - 波圖 (FC Porto)", 75, 18000),
        ("西甲 - 皇家馬德里", 84, 85000),
        ("英超 - 曼城", 85, 90000)
    ]
    
    valid_offers = [c for c in all_clubs if ovr >= c[1] - (5 if player['transfer_requested'] else 0)]
    
    if not valid_offers:
        st.info("目前尚無符合你能力值的球會報價，請先透過訓練或比賽提升 OVR！")
    else:
        for c_name, req_ovr, wage_offer in valid_offers:
            col_c1, col_c2 = st.columns([3, 1])
            col_c1.write(f"⚽ **{c_name}** | 開出週薪：**${wage_offer:,}** (要求 OVR: {req_ovr})")
            
            if player['club'] == c_name:
                col_c2.button("現效力球會", disabled=True, key=c_name)
            else:
                if col_c2.button(f"簽約加盟", key=c_name, type="primary"):
                    player['club'] = c_name
                    player['wage'] = wage_offer
                    player['transfer_requested'] = False
                    player['logs'].insert(0, f"✍️ 重磅轉會！{player['name']} 正式加盟 {c_name}，號碼 {player['number']} 號，週薪 ${wage_offer:,}！")
                    st.success(f"成功加盟 {c_name}！")
                    st.rerun()

# --- TAB 3: 訓練中心 ---
with tab3:
    st.header("🏋️ 自主特訓")
    st.caption("每次訓練消耗 15 體力，指定提升 1 點屬性")
    t1, t2, t3, t4 = st.columns(4)
    with t1:
        if st.button("🎯 射門特訓"):
            if player['energy'] >= 15:
                player['energy'] -= 15; player['shooting'] += 1
                player['logs'].insert(0, "🏋️ 進行了射門特訓，射門 +1"); st.rerun()
    with t2:
        if st.button("🅰️ 傳球特訓"):
            if player['energy'] >= 15:
                player['energy'] -= 15; player['passing'] += 1
                player['logs'].insert(0, "🏋️ 進行了傳球特訓，傳球 +1"); st.rerun()
    with t3:
        if st.button("⚡ 盤帶特訓"):
            if player['energy'] >= 15:
                player['energy'] -= 15; player['dribbling'] += 1
                player['logs'].insert(0, "🏋️ 進行了盤帶特訓，盤帶 +1"); st.rerun()
    with t4:
        if st.button("😴 補充休息"):
            player['energy'] = min(100, player['energy'] + 45)
            player['logs'].insert(0, "😴 經過休息，體力恢復 45"); st.rerun()

# --- TAB 4: 個人資產 ---
with tab4:
    st.header("🏡 資產管理")
    col_a1, col_a2 = st.columns(2)
    with col_a1:
        if player['trainer']: st.success("✅ 已聘請私人體能教練 (比賽體力消耗 -5)")
        else:
            if st.button("聘請私人體能教練 ($10,000)"):
                if player['money'] >= 10000:
                    player['money'] -= 10000; player['trainer'] = True
                    player['logs'].insert(0, "💼 聘請了私人體能教練！"); st.rerun()
    with col_a2:
        st.write(f"目前住處：**{player['house']}**")
        if player['house'] == "標準公寓":
            if st.button("購買豪宅 ($100,000)"):
                if player['money'] >= 100000:
                    player['money'] -= 100000; player['house'] = "豪華別墅"; player['stamina'] += 5
                    player['logs'].insert(0, "🏡 搬入豪宅！體能 +5"); st.rerun()

# --- TAB 5: 生涯履歷 ---
with tab5:
    st.header("📜 生涯日誌")
    for log in player['logs']:
        st.write(f"- {log}")
