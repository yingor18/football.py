import streamlit as st
import random
import time

st.set_page_config(page_title="足球生涯：綠茵傳奇", page_icon="⚽", layout="wide")

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
        "coach_trust": 60,   # 教練信任度 (影響是否正選)
        "fans_love": 50,     # 球迷喜愛度
        "matches": 0,
        "goals": 0,
        "assists": 0,
        "season": 1,
        "week": 1,
        "points": 0,
        "news": "【頭條】17歲新星 Ho Yin 正式簽約加盟球隊，本賽季備受期待！",
        "logs": []
    }

p = st.session_state.player

def get_ovr(player):
    return int(player['shooting'] * 0.35 + player['passing'] * 0.3 + player['dribbling'] * 0.25 + player['stamina'] * 0.1)

# 側邊欄：球員卡
st.sidebar.title("⚽ 綠茵傳奇")
st.sidebar.markdown(f"### 👤 **{p['name']}** (OVR: {get_ovr(p)})")
st.sidebar.caption(f"效力球會：{p['club']} | {p['age']} 歲")
st.sidebar.divider()

st.sidebar.markdown(f"💰 **週薪**：${p['wage']:,} | **存款**：${p['money']:,}")
st.sidebar.progress(p['energy'] / 100, text=f"⚡ 體力：{p['energy']}/100")
st.sidebar.progress(p['coach_trust'] / 100, text=f"🧢 教練信任度：{p['coach_trust']}%")
st.sidebar.progress(p['fans_love'] / 100, text=f"❤️ 球迷支持度：{p['fans_love']}%")

st.sidebar.divider()
st.sidebar.caption(f"第 {p['season']} 賽季 | 第 {p['week']}/38 週")

# 主介面
st.title("⚽ 足球生涯模擬器：綠茵傳奇")

# 顯示最新體育新聞
st.info(f"📰 **最新體育報章**：{p['news']}")

tab_match, tab_event, tab_train, tab_transfer, tab_career = st.tabs([
    "🏟️ 本週賽事", 
    "📰 突發事件 / 採訪", 
    "🏋️ 每日訓練", 
    "💼 經理人辦公室", 
    "📜 生涯日誌"
])

# --- TAB 1: 本週賽事 (故事化比賽過程) ---
with tab_match:
    st.header(f"第 {p['week']} 週：{p['club']} VS 勁敵球隊")
    
    # 檢查是否正選
    if p['coach_trust'] < 40:
        st.warning("⚠️ 由於你近期表現或態度問題，教練把你放在替補席上！")
        is_starter = False
    else:
        st.success("👕 你被選入本場比賽正選陣容！")
        is_starter = True

    if p['energy'] < 30:
        st.error("⚠️ 體力極度匱乏！本場比賽受傷風險極高。")

    st.divider()

    if st.button("🏁 開始比賽", type="primary", use_container_width=True):
        p['energy'] = max(10, p['energy'] - 20)
        p['matches'] += 1
        p['week'] += 1
        p['money'] += p['wage']
        
        # 模擬關鍵時刻 (2 個比賽事件)
        match_events = []
        match_goals = 0
        match_assists = 0
        
        # 事件 1：上半場
        st.subheader("⏱️ 上半場 35 分鐘：關鍵進攻")
        chance1 = random.choice(["shoot", "pass"])
        if chance1 == "shoot":
            if random.randint(1, 100) < p['shooting']:
                match_goals += 1
                match_events.append("⚽ 35' 你在禁區頂接應妙傳，一腳勁射破門！球進啦！")
            else:
                match_events.append("❌ 35' 你起腳遠射，可惜皮球擦柱而出！")
        else:
            if random.randint(1, 100) < p['passing']:
                match_assists += 1
                match_events.append("🅰️ 35' 你送出一記精準的手術刀直塞，隊友輕鬆推射破門！")
            else:
                match_events.append("❌ 35' 你嘗試穿透性傳球，被對方後衛斷下。")

        # 事件 2：下半場
        chance2 = random.choice(["dribble", "shoot"])
        if chance2 == "dribble":
            if random.randint(1, 100) < p['dribbling']:
                match_goals += 1
                match_events.append("⚽ 78' 你沿左路連續晃過兩名後衛，小角度抽射破門！太精彩了！")
            else:
                match_events.append("❌ 78' 你嘗試強行突破被對方雙人包抄把球破壞。")
        else:
            if random.randint(1, 100) < p['shooting']:
                match_goals += 1
                match_events.append("⚽ 88' 絕殺！你在角球混戰中頭槌破門！")
            else:
                match_events.append("❌ 88' 你在禁區內頭槌攻門，被門將神勇撲出！")

        p['goals'] += match_goals
        p['assists'] += match_assists

        # 播報比賽過程
        for ev in match_events:
            st.write(ev)

        # 比賽結算與新聞生成
        if match_goals > 0 or match_assists > 0:
            p['coach_trust'] = min(100, p['coach_trust'] + 8)
            p['fans_love'] = min(100, p['fans_love'] + 10)
            p['news'] = f"【賽後頭條】{p['name']} 展現球星價值！全場貢獻 {match_goals} 球 {match_assists} 助攻率隊取勝！"
            st.success(f"🎉 比賽結束！你獲得了 {match_goals} 進球，{match_assists} 助攻！")
        else:
            p['coach_trust'] = max(0, p['coach_trust'] - 3)
            p['news'] = f"【體育新聞】{p['club']} 鋒線乏力，{p['name']} 本場比賽表現平平未能建功。"
            st.info("比賽結束，你本場比賽未有進球或助攻。")

        # 賽季推進檢查
        if p['week'] > 38:
            p['season'] += 1
            p['week'] = 1
            p['age'] += 1
            st.balloons()
            st.success("🏆 賽季結束！進入全新賽季！")
        
        st.rerun()

# --- TAB 2: 突發事件 / 賽後採訪 ---
with tab_event:
    st.header("📰 場外新聞與抉擇")
    st.caption("作為一名職業球員，你在場外的言行舉止同樣影響著你的職業生涯。")
    
    st.subheader("🎙️ 記者會提問：")
    st.write("記者：「對於近期隊中的競爭，以及教練的戰術安排，你有甚麼睇法？」")
    
    col_ans1, col_ans2, col_ans3 = st.columns(3)
    if col_ans1.button("🗣️ 『服從教練安排，團隊利益高於一切。』"):
        p['coach_trust'] = min(100, p['coach_trust'] + 10)
        p['logs'].insert(0, f"第 {p['week']} 週：你在採訪中展現職業態度，教練信任度提升。")
        st.success("教練對你的發言非常滿意！(教練信任度 +10)")
        st.rerun()
        
    if col_ans2.button("🔥 『我覺得我應該得到更多正選時間！』"):
        p['fans_love'] = min(100, p['fans_love'] + 8)
        p['coach_trust'] = max(0, p['coach_trust'] - 10)
        p['logs'].insert(0, f"第 {p['week']} 週：你公開表達對上場時間的不滿，引發球迷熱議。")
        st.warning("球迷喜歡你的霸氣，但教練對你的言論感到不悅！(球迷喜愛 +8, 教練信任 -10)")
        st.rerun()

    if col_ans3.button("😶 『無可奉告，我只想專注於訓練。』"):
        st.info("你平淡地回應了記者。")

# --- TAB 3: 每日訓練 ---
with tab_train:
    st.header("🏋️ 訓練與狀態恢復")
    
    c_tr1, c_tr2 = st.columns(2)
    with c_tr1:
        st.subheader("🎯 技術特訓")
        if st.button("加練射門與進攻 (體力 -20)"):
            if p['energy'] >= 20:
                p['energy'] -= 20
                p['shooting'] += 1
                st.success("射門能力 +1！")
                st.rerun()
            else: st.error("體力不足！")

        if st.button("加練傳球與視野 (體力 -20)"):
            if p['energy'] >= 20:
                p['energy'] -= 20
                p['passing'] += 1
                st.success("傳球能力 +1！")
                st.rerun()
            else: st.error("體力不足！")

    with c_tr2:
        st.subheader("🛌 休息與復原")
        if st.button("進行理療與按摩休息 (體力 +40)"):
            p['energy'] = min(100, p['energy'] + 40)
            p['week'] += 1
            st.success("體力大幅恢復！(消耗一週時間)")
            st.rerun()

# --- TAB 4: 經理人辦公室 ---
with tab_transfer:
    st.header("💼 經理人辦公室")
    ovr = get_ovr(p)
    
    st.write(f"目前你的經理人收到以下球會的關注：")
    
    offers = [
        ("葡超 - 葡萄牙體育 (Sporting CP)", 72, 12000),
        ("西甲 - 皇家馬德里", 82, 85000),
        ("英超 - 曼城", 85, 95000)
    ]
    
    for club_name, req_ovr, wage in offers:
        col_o1, col_o2 = st.columns([3, 1])
        col_o1.write(f"⚽ **{club_name}** | 提議週薪：**${wage:,}** (要求 OVR: {req_ovr})")
        if ovr >= req_ovr:
            if col_o2.button(f"簽約加盟", key=club_name):
                p['club'] = club_name
                p['wage'] = wage
                p['news'] = f"【重磅轉會】官宣！{p['name']} 以天價薪酬加盟 {club_name}！"
                st.success(f"恭喜加盟 {club_name}！")
                st.rerun()
        else:
            col_o2.button("實力未達標", disabled=True, key=club_name)

# --- TAB 5: 生涯日誌 ---
with tab_career:
    st.header("📜 生涯統計與記錄")
    st.metric("總出場數", f"{p['matches']} 場")
    st.metric("總進球數", f"{p['goals']} 球")
    st.metric("總助攻數", f"{p['assists']} 次")
    
    st.divider()
    st.subheader("📖 歷史日誌")
    for log in p['logs']:
        st.write(f"- {log}")
