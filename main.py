import streamlit as st
import random
import plotly.graph_objects as go

st.set_page_config(page_title="綠茵傳奇 Pro - 動態局勢版", page_icon="⚽", layout="wide")

# --- 全球 10 大國家資料庫 ---
ALL_COUNTRIES_DB = {
    "🇯🇵 日本": {
        "league": "J2 乙組聯賽",
        "clubs": [{"name": "橫濱FC", "wage": 800}, {"name": "清水心跳", "wage": 850}, {"name": "千葉市原", "wage": 800}],
        "rivals": ["磐田喜悅", "大宮松鼠", "水戶蜀葵", "町田澤維亞", "秋田拿薩"],
        "top_club": {"name": "橫濱水手 (J1)", "req": 68, "wage": 3200}
    },
    "🏴󠁧󠁢󠁥󠁮󠁧󠁿 英格蘭": {
        "league": "英冠 乙組聯賽",
        "clubs": [{"name": "新特蘭 (Sunderland)", "wage": 3000}, {"name": "列斯聯 (Leeds)", "wage": 3500}, {"name": "高雲地利 (Coventry)", "wage": 2800}],
        "rivals": ["諾定咸森林", "屈福特", "般尼茅夫", "史篤城", "米杜士堡"],
        "top_club": {"name": "阿仙奴 (Arsenal)", "req": 83, "wage": 85000}
    },
    "🇪🇸 西班牙": {
        "league": "西乙 乙組聯賽",
        "clubs": [{"name": "愛斯賓奴 (Espanyol)", "wage": 2500}, {"name": "薩拉戈薩 (Zaragoza)", "wage": 2000}, {"name": "希昂 (Sporting Gijon)", "wage": 2200}],
        "rivals": ["卡斯特雲", "阿爾梅利亞", "特內里費", "布爾戈斯", "洛哥迪斯"],
        "top_club": {"name": "皇家馬德里 (Real Madrid)", "req": 86, "wage": 120000}
    },
    "🇵🇹 葡萄牙": {
        "league": "葡甲 乙組聯賽",
        "clubs": [{"name": "馬里迪莫 (Maritimo)", "wage": 1200}, {"name": "費利拿 (Pacos)", "wage": 1100}],
        "rivals": ["法馬利卡奧", "納舍爾", "特里連斯", "彭納菲爾"],
        "top_club": {"name": "葡萄牙體育 (Sporting CP)", "req": 74, "wage": 18000}
    },
    "🇮🇹 義大利": {
        "league": "意乙 乙組聯賽",
        "clubs": [{"name": "帕爾馬 (Parma)", "wage": 2200}, {"name": "桑普多利亞 (Sampdoria)", "wage": 2400}],
        "rivals": ["卡塔尼亞", "巴里", "科莫", "皮薩"],
        "top_club": {"name": "國際米蘭 (Inter)", "req": 82, "wage": 80000}
    },
    "🇩🇪 德國": {
        "league": "德乙 乙組聯賽",
        "clubs": [{"name": "漢堡 (HSV)", "wage": 2800}, {"name": "史浩克04 (Schalke 04)", "wage": 3000}],
        "rivals": ["雲達不來梅", "紐倫堡", "杜塞爾多夫", "凱澤斯勞滕"],
        "top_club": {"name": "拜仁慕尼黑 (Bayern)", "req": 85, "wage": 105000}
    },
    "🇫🇷 法國": {
        "league": "法乙 乙組聯賽",
        "clubs": [{"name": "波爾多 (Bordeaux)", "wage": 2000}, {"name": "聖伊天 (Saint-Etienne)", "wage": 2100}],
        "rivals": ["蒙彼利埃", "阿雅克肖", "格勒諾布爾", "拉瓦爾"],
        "top_club": {"name": "巴黎聖日耳門 (PSG)", "req": 85, "wage": 115000}
    },
    "🇳🇱 荷蘭": {
        "league": "荷乙 乙組聯賽",
        "clubs": [{"name": "威廉二世 (Willem II)", "wage": 1500}, {"name": "格羅寧根 (Groningen)", "wage": 1600}],
        "rivals": ["羅達JC", "登波士", "海爾蒙德", "泰爾斯達"],
        "top_club": {"name": "阿積士 (Ajax)", "req": 74, "wage": 18000}
    },
    "🇦🇷 阿根廷": {
        "league": "阿乙 乙組聯賽",
        "clubs": [{"name": "高隆 (Colon)", "wage": 600}, {"name": "阿爾馬格羅 (Almagro)", "wage": 500}],
        "rivals": ["聖馬田", "查卡利達", "阿爾米蘭特布朗", "德弗羅"],
        "top_club": {"name": "博卡青年 (Boca Juniors)", "req": 72, "wage": 8000}
    },
    "🇧🇷 巴西": {
        "league": "巴乙 乙組聯賽",
        "clubs": [{"name": "塞阿拉 (Ceara)", "wage": 700}, {"name": "瓜拉尼 (Guarani)", "wage": 650}],
        "rivals": ["諾提哥", "維拉諾亞", "巴拉那體育", "CRB"],
        "top_club": {"name": "法林明高 (Flamengo)", "req": 73, "wage": 9000}
    }
}

# --- 成就系統定義 (id: (名稱, 描述, 條件函數)) ---
ACHIEVEMENTS = {
    "first_goal": ("⚽ 處子入球", "職業生涯第一個入球", lambda p: p['goals'] >= 1),
    "first_assist": ("🅰️ 妙傳首秀", "職業生涯第一個助攻", lambda p: p['assists'] >= 1),
    "hat_trick_career": ("🎩 生涯5球", "生涯累積5個入球", lambda p: p['goals'] >= 5),
    "playmaker": ("🧠 組織核心", "生涯累積5次助攻", lambda p: p['assists'] >= 5),
    "wall": ("🧤 銅牆鐵壁", "生涯累積10次撲救", lambda p: p['saves'] >= 10),
    "starter_status": ("⭐ 正選常客", "教練信任度達到70%", lambda p: p['coach_trust'] >= 70),
    "big_move": ("🏆 豪門之路", "成功加盟頂級豪門球會", lambda p: p.get('joined_top_club', False)),
    "veteran": ("📅 老將風範", "生涯踢滿20場比賽", lambda p: p['matches'] >= 20),
    "rich": ("💰 小富翁", "存款突破 $10,000", lambda p: p['money'] >= 10000),
    "loan_survivor": ("🔄 租借磨練", "完成一次外借經歷", lambda p: p['is_loaned']),
}

# --- 每週隨機小事件(增加新鮮感,唔一定影響數值,但會影響動態) ---
WEEKLY_FLAVOR_EVENTS = [
    {"text": "📰 地方傳媒訪問你,報導你近期表現受球迷關注。", "trust": 1, "money": 0},
    {"text": "🤝 一間本地運動品牌向你提出小額贊助合約。", "trust": 0, "money": 300},
    {"text": "😤 更衣室內有隊友因為出場時間問題向教練投訴,氣氛略為緊張。", "trust": -1, "money": 0},
    {"text": "📱 你喺社交媒體分享訓練片段,獲得球迷熱烈迴響。", "trust": 1, "money": 0},
    {"text": "🩺 隊醫提醒你要注意休息,避免過度疲勞。", "trust": 0, "money": 0},
    {"text": "🚗 你買咗人生第一架屬於自己嘅車,感覺踏入職業球員新階段。", "trust": 0, "money": -500},
    {"text": "🗞️ 有傳言指其他球會嘅球探正在留意你嘅表現。", "trust": 0, "money": 0},
]

# --- 1. 創角系統 ---
if "created" not in st.session_state:
    st.session_state.created = False

if not st.session_state.created:
    st.title("⚽ 綠茵傳奇 Pro - 創角與生涯選拔")

    if "random_3_countries" not in st.session_state:
        st.session_state.random_3_countries = random.sample(list(ALL_COUNTRIES_DB.keys()), 3)

    col_c1, col_c2 = st.columns(2)
    with col_c1:
        name = st.text_input("球員姓名", placeholder="請輸入你的名字")
        position = st.selectbox("場上位置", [
            "門將 (GK)", "中堅 (CB)", "邊後衛 (LB/RB)",
            "防守中場 (CDM)", "進攻中場 (CAM)", "翼鋒 (LW/RW)", "前鋒 (ST)"
        ])

        st.write("🎲 **本局抽中的 3 個起步國家選項：**")
        selected_country = st.radio("選擇你的職業起點國家：", st.session_state.random_3_countries)

        c_info = ALL_COUNTRIES_DB[selected_country]
        starter_clubs = c_info["clubs"]

        start_club_obj = st.selectbox(f"🐣 選擇起步球會 ({c_info['league']})", starter_clubs, format_func=lambda x: x['name'])

        if st.button("🎲 重新刷新 3 個國家"):
            st.session_state.random_3_countries = random.sample(list(ALL_COUNTRIES_DB.keys()), 3)
            st.rerun()

    with col_c2:
        st.info("💡 **隨機起步機制說明**：\n"
                "- 每次開局系統會隨機提供 3 個國家供你選擇。\n"
                "- 你將從該國家的**乙組/低組別聯賽**開啟球員生涯。\n"
                "- 比賽中將會隨機觸發多種不同比賽時段與緊急情境！\n"
                "- 新增：聯賽榜排名、成就系統、每週隨機事件！")

    if st.button("🚀 簽署職業合約並開始", type="primary"):
        player_name = name.strip() if name.strip() else "新星小將"

        if "門將" in position: sh, pa, dr, st_attr = 30, 50, 40, 68
        elif "中堅" in position: sh, pa, dr, st_attr = 38, 52, 45, 70
        elif "邊後衛" in position: sh, pa, dr, st_attr = 45, 60, 60, 68
        elif "防守中場" in position: sh, pa, dr, st_attr = 48, 65, 55, 68
        elif "進攻中場" in position: sh, pa, dr, st_attr = 58, 68, 62, 62
        elif "翼鋒" in position: sh, pa, dr, st_attr = 60, 58, 68, 62
        else: sh, pa, dr, st_attr = 65, 52, 60, 62

        # 建立簡易聯賽榜:玩家球會 + 4 支隨機對手球會
        rivals = random.sample(c_info["rivals"], min(4, len(c_info["rivals"])))
        league_table = {start_club_obj['name']: {"points": 0, "played": 0, "gf": 0, "ga": 0}}
        for r in rivals:
            league_table[r] = {"points": random.randint(0, 6), "played": random.randint(0, 3), "gf": random.randint(0, 6), "ga": random.randint(0, 6)}

        st.session_state.player = {
            "name": player_name,
            "position": position,
            "age": 17,
            "country": selected_country,
            "club": start_club_obj['name'],
            "is_loaned": False,
            "parent_club": None,
            "wage": start_club_obj['wage'],
            "money": 2000,
            "shooting": sh, "passing": pa, "dribbling": dr, "stamina": st_attr,
            "ap": 3, "max_ap": 3, "fatigue": 0, "chemistry": 40, "form": "平穩",
            "injury_weeks": 0, "coach_trust": 45, "matches": 0, "goals": 0, "assists": 0, "saves": 0,
            "season": 1, "week": 1,
            "social_tweets": [f"新聞: {player_name} 正式加盟 {start_club_obj['name']}！"],
            "match_in_progress": False, "match_event": None, "match_role": "bench", "match_result": None,
            "league_table": league_table, "rivals": rivals,
            "achievements": set(), "new_achievements": [], "joined_top_club": False,
        }
        st.session_state.created = True
        st.rerun()

    st.stop()

# --- 2. 遊戲主體 ---
p = st.session_state.player

def get_ovr(player):
    if "門將" in player['position'] or "中堅" in player['position']:
        return int(player['stamina'] * 0.4 + player['passing'] * 0.3 + player['dribbling'] * 0.2 + player['shooting'] * 0.1)
    else:
        return int(player['shooting'] * 0.35 + player['passing'] * 0.3 + player['dribbling'] * 0.25 + player['stamina'] * 0.1)

ovr = get_ovr(p)

def check_achievements():
    """檢查有冇新解鎖嘅成就"""
    for aid, (aname, adesc, cond) in ACHIEVEMENTS.items():
        if aid not in p['achievements'] and cond(p):
            p['achievements'].add(aid)
            p['new_achievements'].append((aname, adesc))

def simulate_other_matches():
    """模擬聯賽榜入面其他球隊嘅賽果,令排名持續變化"""
    for club in p['league_table']:
        if club == p['club']:
            continue
        if random.random() < 0.6:  # 唔係每隊每週都踢
            gf = random.randint(0, 3)
            ga = random.randint(0, 3)
            p['league_table'][club]['played'] += 1
            p['league_table'][club]['gf'] += gf
            p['league_table'][club]['ga'] += ga
            if gf > ga:
                p['league_table'][club]['points'] += 3
            elif gf == ga:
                p['league_table'][club]['points'] += 1

# 側邊欄
st.sidebar.title("⚽ 綠茵傳奇 Pro")
st.sidebar.markdown(f"### 👤 **{p['name']}** (OVR: **{ovr}**)")
st.sidebar.caption(f"位置：**{p['position']}** | 球會：**{p['club']}**")

fig = go.Figure(data=go.Scatterpolar(
  r=[p['shooting'], p['passing'], p['dribbling'], p['stamina']],
  theta=['射門', '傳球', '盤帶', '體能'], fill='toself', line_color='#00CC96'
))
fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[30, 100])), showlegend=False, margin=dict(l=20, r=20, t=20, b=20), height=150)
st.sidebar.plotly_chart(fig, use_container_width=True)

st.sidebar.metric("💰 週薪", f"${p['wage']:,}")
st.sidebar.metric("💵 存款", f"${p['money']:,}")
st.sidebar.divider()
st.sidebar.progress(p['fatigue'] / 100, text=f"😫 疲勞度：{p['fatigue']}%")
st.sidebar.progress(p['coach_trust'] / 100, text=f"🧢 教練信任度：{p['coach_trust']}%")

with st.sidebar.expander(f"🏅 成就系統 ({len(p['achievements'])}/{len(ACHIEVEMENTS)})"):
    for aid, (aname, adesc, cond) in ACHIEVEMENTS.items():
        if aid in p['achievements']:
            st.markdown(f"✅ **{aname}** - {adesc}")
        else:
            st.markdown(f"🔒 ~~{aname}~~ - {adesc}")

# 彈出新解鎖成就通知
if p['new_achievements']:
    for aname, adesc in p['new_achievements']:
        st.toast(f"🏅 解鎖成就：{aname}！", icon="🎉")
    p['new_achievements'] = []

# 主介面
st.title("⚽ 職業生涯主頁")

if p['coach_trust'] >= 70:
    role_status = "⭐ 陣容首發 (正選)"
    p_role = "starter"
elif p['coach_trust'] >= 40:
    role_status = "🪑 替補席 (後備)"
    p_role = "sub"
else:
    role_status = "🚫 未進入大名單"
    p_role = "not_in_squad"

st.info(f"💬 最新動態：{p['social_tweets'][0]}")
st.warning(f"📋 當前隊內地位：**{role_status}**")

# 聯賽榜
with st.expander("📊 查看聯賽積分榜", expanded=False):
    table_rows = []
    for club, stats in p['league_table'].items():
        gd = stats['gf'] - stats['ga']
        table_rows.append((club, stats['played'], stats['points'], gd))
    table_rows.sort(key=lambda x: (-x[2], -x[3]))
    for rank, (club, played, points, gd) in enumerate(table_rows, start=1):
        marker = "👉 " if club == p['club'] else ""
        st.write(f"{rank}. {marker}**{club}** — {points} 分 | {played} 場 | 淨勝球 {gd:+d}")

st.divider()

def next_week():
    p['week'] += 1
    p['ap'] = p['max_ap']
    p['money'] += p['wage']
    p['fatigue'] = max(0, p['fatigue'] - 12)
    p['match_result'] = None
    simulate_other_matches()
    # 每週隨機小事件(約 45% 機率觸發)
    if random.random() < 0.45:
        evt = random.choice(WEEKLY_FLAVOR_EVENTS)
        p['coach_trust'] = max(0, min(100, p['coach_trust'] + evt['trust']))
        p['money'] += evt['money']
        p['social_tweets'].insert(0, evt['text'])
    check_achievements()
    if p['week'] > 38:
        st.balloons()
        st.subheader("🏆 賽季結束結算")
        p['season'] += 1; p['week'] = 1; p['age'] += 1

if p['injury_weeks'] > 0:
    st.error(f"🚑 受傷休養中（剩餘 {p['injury_weeks']} 週）")
    if st.button("⏩ 跳過休養週"):
        p['injury_weeks'] -= 1; next_week(); st.rerun()
else:
    col_w1, col_w2 = st.columns([3, 1])
    col_w1.markdown(f"## 🗓️ 第 {p['season']} 賽季 - 第 {p['week']}/38 週")
    if col_w2.button("⏩ 結束本週日程", type="secondary", use_container_width=True):
        next_week(); st.rerun()

    # 比賽結果顯示
    if p['match_result']:
        res = p['match_result']
        st.markdown("### 📊 比賽處理戰報")
        if res['success']: st.success(f"🎉 **【完美處置】** {res['detail']}")
        else: st.error(f"❌ **【遺憾失誤】** {res['detail']}")

        st.markdown(f"#### 🏟️ 全場賽果：{p['club']} {res['team_score'][0]} - {res['team_score'][1]} {res['opponent']}")
        st.info(f"📈 賽後影響：教練信任度 {res['trust_change']} | 疲勞度 +{res['fatigue_add']}%")
        if st.button("確定並返回日程 ->", type="primary"):
            p['match_result'] = None
            check_achievements()
            if p['ap'] <= 0: next_week()
            st.rerun()

    # 進行比賽（隨機動態事件生成器）
    elif p['match_in_progress']:
        st.subheader(f"📡 比賽現場關鍵局勢 ({p['position']}) — 對手：{p.get('current_opponent', '未知球會')}")

        if not p['match_event']:
            events_pool = [
                {"time": "12'", "title": "⚡ 開局高位逼搶反擊", "desc": "對方後衛傳球失誤！你在禁區前沿攔截成功，出現絕佳進攻機會！", "type": "attack"},
                {"time": "44'", "title": "🎯 上半場結束前十二碼判罰", "desc": "隊友在禁區內被絆倒獲判十二碼！教練指名讓你來主罰！", "type": "penalty"},
                {"time": "68'", "title": "🛑 少打一人的防守拉鋸戰", "desc": "隊友領到紅牌被罰下，對方發動猛烈反攻，需要你回深防守！", "type": "defend"},
                {"time": "89'", "title": "🔥 補時階段角球絕殺戰術", "desc": "最後一次角球機會，隊友將球傳向禁區混戰區域！", "type": "attack"},
                {"time": "75'", "title": "🚪 門前混戰一觸即發", "desc": "對方前鋒突破獲得單刀機會，威脅球門！", "type": "gk_event"}
            ]
            p['match_event'] = random.choice(events_pool)

        evt = p['match_event']
        st.write(f"⏱️ **{evt['time']}** - 【**{evt['title']}**】")
        st.write(f"📖 {evt['desc']}")

        def success_rate(attr_value):
            """粗略計算成功率百分比,俾玩家有策略資訊"""
            rate = attr_value - 50 + int(p['chemistry'] / 10) * 10
            rate = max(5, min(95, rate))
            return rate

        choice = None
        c_m1, c_m2, c_m3 = st.columns(3)

        if "門將" in p['position']:
            st.caption(f"💡 撲救成功率約 {success_rate(p['stamina'])}%（受體能與默契影響）")
            if c_m1.button("🧤 飛身極限撲救"): choice = "save"
            if c_m2.button("🚪 果斷出擊封堵角度"): choice = "save"
            if c_m3.button("🗣️ 指揮後線卡位"): choice = "pass"
        else:
            if evt['type'] == "penalty":
                st.caption(f"💡 射門成功率約 {success_rate(p['shooting'])}%（受射門與默契影響）")
                if c_m1.button("🎯 大力抽射球門左上死角"): choice = "shoot"
                if c_m2.button("👟 冷靜推射右下角"): choice = "shoot"
                if c_m3.button("💥 踢勺子踢法 (Panenka)"): choice = "shoot"
            else:
                st.caption(f"💡 成功率參考：射門 {success_rate(p['shooting'])}% ｜ 傳球 {success_rate(p['passing'])}% ｜ 盤帶 {success_rate(p['dribbling'])}%")
                if c_m1.button("🚀 果斷起腳起腳轟門"): choice = "shoot"
                if c_m2.button("👟 手術刀直塞分球"): choice = "pass"
                if c_m3.button("⚡ 強行盤帶連過一人"): choice = "dribble"

        if choice:
            check_attr = p['shooting'] if choice == "shoot" else (p['passing'] if choice == "pass" else p['dribbling'])
            if choice == "save": check_attr = p['stamina']

            success = (random.randint(1, 100) + int(p['chemistry']/10)) < check_attr
            fatigue_add = 20 if p['match_role'] == "starter" else 10
            p['fatigue'] = min(100, p['fatigue'] + fatigue_add)

            if success:
                if choice == "shoot": p['goals'] += 1; detail = "冷靜處理，皮球應聲入網！"
                elif choice == "pass": p['assists'] += 1; detail = "精準傳球送出致命助攻！"
                else: p['saves'] += 1; detail = "神級反應，成功拯救球隊！"

                trust_inc = 6 if p['match_role'] == "sub" else 4
                p['coach_trust'] = min(100, p['coach_trust'] + trust_inc)
                trust_msg = f"+{trust_inc}%"
            else:
                detail = "關鍵處理欠佳，被對方成功解圍/撲出。"
                p['coach_trust'] = max(0, p['coach_trust'] - 3)
                trust_msg = "-3%"

            # 模擬全場賽果(受個人表現影響機率)
            base_gf = random.randint(0, 2)
            base_ga = random.randint(0, 2)
            if success:
                base_gf += 1
            else:
                base_ga += random.choice([0, 1])
            opponent = p.get('current_opponent', '對手球會')

            p['league_table'][p['club']]['played'] += 1
            p['league_table'][p['club']]['gf'] += base_gf
            p['league_table'][p['club']]['ga'] += base_ga
            if base_gf > base_ga:
                p['league_table'][p['club']]['points'] += 3
                match_result_text = f"{p['club']} 主場獲勝！"
            elif base_gf == base_ga:
                p['league_table'][p['club']]['points'] += 1
                match_result_text = "雙方打成平手。"
            else:
                match_result_text = f"{p['club']} 不敵 {opponent}。"

            p['match_in_progress'] = False
            p['match_event'] = None
            p['match_result'] = {
                "success": success, "detail": detail, "trust_change": trust_msg,
                "fatigue_add": fatigue_add, "team_score": (base_gf, base_ga),
                "opponent": opponent
            }
            p['social_tweets'].insert(0, f"賽後快訊：{match_result_text}")
            st.rerun()

    # 日程選單
    else:
        if p['ap'] <= 0: st.info("💡 本週 AP 已耗盡，請點擊上方【結束本週日程】。")
        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.subheader("🏟️ 本週賽事")
            if p_role == "not_in_squad":
                st.caption("🚫 未進入大名單")
                st.error("教練信任度過低，本週看台觀戰。請加強訓練！")
            else:
                st.caption(f"身份：{role_status}")
                if st.button("🔥 登場比賽", type="primary", use_container_width=True, disabled=(p['ap'] < 1)):
                    p['ap'] -= 1; p['matches'] += 1
                    p['match_role'] = p_role
                    p['current_opponent'] = random.choice(p['rivals']) if p.get('rivals') else "對手球會"
                    p['match_in_progress'] = True; st.rerun()

        with c2:
            st.subheader("🏋️ 隊內特訓")
            st.caption("消耗 1 AP | 信任+3, 疲勞+15%")
            t_choice = st.selectbox("訓練項目", ["🎯 射門/搶斷", "🅰️ 傳球組織", "⚡ 盤帶速度", "💪 體能加強"])
            if st.button("💪 開始特訓", use_container_width=True, disabled=(p['ap'] < 1)):
                p['ap'] -= 1; p['fatigue'] = min(100, p['fatigue'] + 15)
                p['coach_trust'] = min(100, p['coach_trust'] + 3)
                if "射門" in t_choice: p['shooting'] += 1
                elif "傳球" in t_choice: p['passing'] += 1
                elif "盤帶" in t_choice: p['dribbling'] += 1
                else: p['stamina'] += 1
                st.success("能力獲得提升，教練對你表示肯定！")
                check_achievements()
                if p['ap'] <= 0: next_week()
                st.rerun()

        with c3:
            st.subheader("🍻 休息室社交")
            st.caption("消耗 1 AP | 默契+10")
            if st.button("🤝 建立關係", use_container_width=True, disabled=(p['ap'] < 1)):
                p['ap'] -= 1; p['chemistry'] = min(100, p['chemistry'] + 10)
                st.success("隊友默契度提升！")
                if p['ap'] <= 0: next_week()
                st.rerun()

        with c4:
            st.subheader("🛌 理療休養")
            st.caption("消耗 1 AP | 疲勞 -35%")
            if st.button("☕ 充分休息", use_container_width=True, disabled=(p['ap'] < 1)):
                p['ap'] -= 1; p['fatigue'] = max(0, p['fatigue'] - 35)
                st.success("疲勞度大幅降低！")
                if p['ap'] <= 0: next_week()
                st.rerun()

st.divider()

# 轉會與租借市場
st.subheader("💼 經理人轉會與租借市場")
col_m1, col_m2 = st.columns(2)

with col_m1:
    st.markdown("#### 🔄 外借租借 (Loan Out)")
    if p_role != "starter" and not p['is_loaned']:
        if st.button("📢 申請外借至乙組球會"):
            p['parent_club'] = p['club']
            p['club'] = f"{p['country']} 乙組球會 (租借)"
            p['is_loaned'] = True; p['coach_trust'] = 85
            if p['club'] not in p['league_table']:
                p['league_table'][p['club']] = {"points": 0, "played": 0, "gf": 0, "ga": 0}
            p['social_tweets'].insert(0, f"官宣！{p['name']} 已被外借尋求正選機會！")
            check_achievements()
            st.rerun()
    elif p['is_loaned']:
        st.info(f"你目前正外借效力中 (母會：{p['parent_club']})")
    else:
        st.caption("目前你是主力球員，無外借需求。")

with col_m2:
    st.markdown("#### 🏆 豪門轉會邀約")
    c_info = ALL_COUNTRIES_DB.get(p['country'])
    if c_info and ovr >= c_info['top_club']['req']:
        top = c_info['top_club']
        st.write(f"✨ **{top['name']}** 提出合約！週薪：**${top['wage']:,}**")
        if st.button(f"✍️ 加盟 {top['name']}"):
            p['club'] = top['name']; p['wage'] = top['wage']; p['is_loaned'] = False
            p['coach_trust'] = 50; p['joined_top_club'] = True
            if p['club'] not in p['league_table']:
                p['league_table'][p['club']] = {"points": 0, "played": 0, "gf": 0, "ga": 0}
            p['social_tweets'].insert(0, f"重磅！{p['name']} 加盟豪門 {top['name']}！")
            check_achievements()
            st.rerun()
    else:
        st.caption("當前能力值 (OVR) 尚不足以吸引頂級豪門，請繼續努力！")
