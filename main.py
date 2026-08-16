import streamlit as st
import random
import json
import pandas as pd

st.set_page_config(page_title="綠茵傳奇 Pro - 動態局勢版", page_icon="⚽", layout="wide")

# --- 全球 10 大國家資料庫 (每國 9 支對手球會,聯賽榜共 10 隊) ---
ALL_COUNTRIES_DB = {
    "🇯🇵 日本": {
        "league": "J2 乙組聯賽", "national": "日本國家隊",
        "clubs": [{"name": "橫濱FC", "wage": 800}, {"name": "清水心跳", "wage": 850}, {"name": "千葉市原", "wage": 800}],
        "rivals": ["磐田喜悅", "大宮松鼠", "水戶蜀葵", "町田澤維亞", "秋田拿薩", "山形蒙迪奧", "琉球FC", "藤枝MYFC", "今治FC"],
        "top_club": {"name": "橫濱水手 (J1)", "req": 68, "wage": 3200}
    },
    "🏴󠁧󠁢󠁥󠁮󠁧󠁿 英格蘭": {
        "league": "英冠 乙組聯賽", "national": "英格蘭國家隊",
        "clubs": [{"name": "新特蘭 (Sunderland)", "wage": 3000}, {"name": "列斯聯 (Leeds)", "wage": 3500}, {"name": "高雲地利 (Coventry)", "wage": 2800}],
        "rivals": ["諾定咸森林", "屈福特", "般尼茅夫", "史篤城", "米杜士堡", "赫爾城", "普茨茅夫", "白禮頓", "諾域治"],
        "top_club": {"name": "阿仙奴 (Arsenal)", "req": 83, "wage": 85000}
    },
    "🇪🇸 西班牙": {
        "league": "西乙 乙組聯賽", "national": "西班牙國家隊",
        "clubs": [{"name": "愛斯賓奴 (Espanyol)", "wage": 2500}, {"name": "薩拉戈薩 (Zaragoza)", "wage": 2000}, {"name": "希昂 (Sporting Gijon)", "wage": 2200}],
        "rivals": ["卡斯特雲", "阿爾梅利亞", "特內里費", "布爾戈斯", "洛哥迪斯", "卡塔赫納", "埃爾切", "拉斯帕爾馬斯", "米蘭迪斯"],
        "top_club": {"name": "皇家馬德里 (Real Madrid)", "req": 86, "wage": 120000}
    },
    "🇵🇹 葡萄牙": {
        "league": "葡甲 乙組聯賽", "national": "葡萄牙國家隊",
        "clubs": [{"name": "馬里迪莫 (Maritimo)", "wage": 1200}, {"name": "費利拿 (Pacos)", "wage": 1100}],
        "rivals": ["法馬利卡奧", "納舍爾", "特里連斯", "彭納菲爾", "維塞拉", "菲蓋拉斯", "毛拉", "希科塔", "奧利韋倫斯"],
        "top_club": {"name": "葡萄牙體育 (Sporting CP)", "req": 74, "wage": 18000}
    },
    "🇮🇹 義大利": {
        "league": "意乙 乙組聯賽", "national": "意大利國家隊",
        "clubs": [{"name": "帕爾馬 (Parma)", "wage": 2200}, {"name": "桑普多利亞 (Sampdoria)", "wage": 2400}],
        "rivals": ["卡塔尼亞", "巴里", "科莫", "皮薩", "科森查", "斯佩齊亞", "布雷西亞", "薩勒尼塔納", "塔蘭托"],
        "top_club": {"name": "國際米蘭 (Inter)", "req": 82, "wage": 80000}
    },
    "🇩🇪 德國": {
        "league": "德乙 乙組聯賽", "national": "德國國家隊",
        "clubs": [{"name": "漢堡 (HSV)", "wage": 2800}, {"name": "史浩克04 (Schalke 04)", "wage": 3000}],
        "rivals": ["雲達不來梅", "紐倫堡", "杜塞爾多夫", "凱澤斯勞滕", "馬格德堡", "埃爾祖爾", "普勞恩", "希望之星", "波鴻"],
        "top_club": {"name": "拜仁慕尼黑 (Bayern)", "req": 85, "wage": 105000}
    },
    "🇫🇷 法國": {
        "league": "法乙 乙組聯賽", "national": "法國國家隊",
        "clubs": [{"name": "波爾多 (Bordeaux)", "wage": 2000}, {"name": "聖伊天 (Saint-Etienne)", "wage": 2100}],
        "rivals": ["蒙彼利埃", "阿雅克肖", "格勒諾布爾", "拉瓦爾", "安錫", "格勒", "羅底斯", "凱恩", "馬提格"],
        "top_club": {"name": "巴黎聖日耳門 (PSG)", "req": 85, "wage": 115000}
    },
    "🇳🇱 荷蘭": {
        "league": "荷乙 乙組聯賽", "national": "荷蘭國家隊",
        "clubs": [{"name": "威廉二世 (Willem II)", "wage": 1500}, {"name": "格羅寧根 (Groningen)", "wage": 1600}],
        "rivals": ["羅達JC", "登波士", "海爾蒙德", "泰爾斯達", "阿爾梅勒城", "多爾德雷赫特", "MVV馬斯特里赫特", "德托普", "VVV費諾"],
        "top_club": {"name": "阿積士 (Ajax)", "req": 74, "wage": 18000}
    },
    "🇦🇷 阿根廷": {
        "league": "阿乙 乙組聯賽", "national": "阿根廷國家隊",
        "clubs": [{"name": "高隆 (Colon)", "wage": 600}, {"name": "阿爾馬格羅 (Almagro)", "wage": 500}],
        "rivals": ["聖馬田", "查卡利達", "阿爾米蘭特布朗", "德弗羅", "阿爾瓦雷斯", "特姆佩利", "維克拉爾", "夸卡", "德芬索雷斯"],
        "top_club": {"name": "博卡青年 (Boca Juniors)", "req": 72, "wage": 8000}
    },
    "🇧🇷 巴西": {
        "league": "巴乙 乙組聯賽", "national": "巴西國家隊",
        "clubs": [{"name": "塞阿拉 (Ceara)", "wage": 700}, {"name": "瓜拉尼 (Guarani)", "wage": 650}],
        "rivals": ["諾提哥", "維拉諾亞", "巴拉那體育", "CRB", "沙佩科恩斯", "維拉利爾BR", "亞馬遜體育", "巴拉伊巴", "戈亞斯青年"],
        "top_club": {"name": "法林明高 (Flamengo)", "req": 73, "wage": 9000}
    }
}

NAME_POOL = ["拿玆里奧", "史密夫", "加西亞", "洛倫索", "中村", "克萊恩", "華倫西亞",
             "杜蘭特", "柏克萊", "菲爾南德斯", "健二", "馬田尼斯", "科斯達", "范德堡", "羅西"]

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
    "international": ("🌍 為國效力", "首次入選國家隊", lambda p: p['caps'] >= 1),
    "veteran_age": ("🧓 薑越老越辣", "35歲仍然活躍於賽場", lambda p: p['age'] >= 35),
    "target_hit": ("🎯 KPI 達人", "首次達成賽季目標", lambda p: p['season_targets_hit'] >= 1),
}

WEEKLY_FLAVOR_EVENTS_TEMPLATE = [
    "📰 地方傳媒訪問你,報導你近期表現受球迷關注。",
    "🤝 一間本地運動品牌向你提出小額贊助合約。",
    "😤 {rival} 喺更衣室因為出場時間問題向教練投訴,氣氛略為緊張。",
    "📱 你喺社交媒體分享訓練片段,獲得球迷熱烈迴響。",
    "🩺 隊醫提醒你要注意休息,避免過度疲勞。",
    "🚗 你買咗人生第一架屬於自己嘅車,感覺踏入職業球員新階段。",
    "🗞️ 有傳言指其他球會嘅球探正在留意你嘅表現。",
    "💬 教練 {coach} 私下同你傾偈,分析你近期表現。",
    "🍽️ 你同隊友 {teammate} 一齊食飯,默契更進一步。",
]

MONEY_EVENTS = {2: 300, 5: -1, 8: 0}  # 索引對應觸發事件時嘅金額變化(部分事件冇金錢影響)

def gen_flavor_text(p):
    idx = random.randint(0, len(WEEKLY_FLAVOR_EVENTS_TEMPLATE) - 1)
    text = WEEKLY_FLAVOR_EVENTS_TEMPLATE[idx].format(
        rival=p.get('rival_name', '隊友'), coach=p.get('coach_name', '教練'), teammate=p.get('teammate_name', '隊友')
    )
    trust_delta = {2: -1, 3: 1, 7: 1}.get(idx, 0)
    money_delta = {1: 300, 5: -500}.get(idx, 0)
    return text, trust_delta, money_delta

# --- 名人堂(留喺 session 內,新開生涯唔會清空) ---
if "hall_of_fame" not in st.session_state:
    st.session_state.hall_of_fame = []

# --- 1. 創角系統 / 讀取存檔 ---
if "created" not in st.session_state:
    st.session_state.created = False

if not st.session_state.created:
    st.title("⚽ 綠茵傳奇 Pro - 創角與生涯選拔")

    tab_new, tab_load = st.tabs(["🆕 開始新生涯", "📂 讀取存檔"])

    with tab_load:
        st.write("有舊存檔？上傳 JSON 檔案繼續你嘅生涯。")
        uploaded = st.file_uploader("選擇存檔檔案 (.json)", type=["json"])
        if uploaded is not None:
            try:
                data = json.load(uploaded)
                data['achievements'] = set(data.get('achievements', []))
                if 'potential' not in data:
                    data['potential'] = {
                        "shooting": min(99, data['shooting'] + 20), "passing": min(99, data['passing'] + 20),
                        "dribbling": min(99, data['dribbling'] + 20), "stamina": min(99, data['stamina'] + 20),
                        "defending": min(99, data.get('defending', 40) + 20),
                    }
                if 'defending' not in data:
                    data['defending'] = 40
                if 'defending' not in data['potential']:
                    data['potential']['defending'] = min(99, data['defending'] + 20)
                st.session_state.player = data
                st.session_state.created = True
                st.success("存檔讀取成功！")
                st.rerun()
            except Exception as e:
                st.error(f"讀取失敗：{e}")

    with tab_new:
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
            st.info("💡 **本版新增內容**：\n"
                    "- 10 隊聯賽榜,排名持續變化\n"
                    "- 成就系統 + 賽季 KPI 目標\n"
                    "- 教練/隊友/對手 NPC 有名有姓\n"
                    "- 30 歲後屬性會自然衰退\n"
                    "- 38 歲可退役,進入名人堂\n"
                    "- OVR 夠高有機會入選國家隊\n"
                    "- 全頁面手機直向排版,唔使開側邊欄\n"
                    "- 可匯出/匯入存檔 JSON 檔案")
            if st.session_state.hall_of_fame:
                st.markdown("#### 🏛️ 名人堂(過往生涯)")
                for legend in st.session_state.hall_of_fame:
                    st.caption(f"👤 {legend['name']} — {legend['goals']}球 {legend['assists']}助攻 | 效力：{legend['final_club']}")

        if st.button("🚀 簽署職業合約並開始", type="primary"):
            player_name = name.strip() if name.strip() else "新星小將"

            if "門將" in position: sh, pa, dr, st_attr, df = 30, 50, 40, 68, 45
            elif "中堅" in position: sh, pa, dr, st_attr, df = 38, 52, 45, 70, 68
            elif "邊後衛" in position: sh, pa, dr, st_attr, df = 45, 60, 60, 68, 58
            elif "防守中場" in position: sh, pa, dr, st_attr, df = 48, 65, 55, 68, 60
            elif "進攻中場" in position: sh, pa, dr, st_attr, df = 58, 68, 62, 62, 35
            elif "翼鋒" in position: sh, pa, dr, st_attr, df = 60, 58, 68, 62, 30
            else: sh, pa, dr, st_attr, df = 65, 52, 60, 62, 25

            rivals = random.sample(c_info["rivals"], min(9, len(c_info["rivals"])))
            league_table = {start_club_obj['name']: {"points": 0, "played": 0, "gf": 0, "ga": 0}}
            for r in rivals:
                league_table[r] = {"points": random.randint(0, 6), "played": random.randint(0, 3), "gf": random.randint(0, 6), "ga": random.randint(0, 6)}

            npc_names = random.sample(NAME_POOL, 3)
            is_gk_or_def = ("門將" in position or "中堅" in position)

            # 潛力值:每個屬性有隱藏上限,越後期練習難度越高
            potential = {
                "shooting": min(99, sh + random.randint(10, 30)),
                "passing": min(99, pa + random.randint(10, 30)),
                "dribbling": min(99, dr + random.randint(10, 30)),
                "stamina": min(99, st_attr + random.randint(10, 30)),
                "defending": min(99, df + random.randint(10, 30)),
            }

            st.session_state.player = {
                "name": player_name, "position": position, "age": 17,
                "country": selected_country, "club": start_club_obj['name'],
                "is_loaned": False, "parent_club": None, "wage": start_club_obj['wage'], "money": 2000,
                "shooting": sh, "passing": pa, "dribbling": dr, "stamina": st_attr, "defending": df,
                "ap": 3, "max_ap": 3, "fatigue": 0, "chemistry": 40, "form": "平穩",
                "injury_weeks": 0, "coach_trust": 45, "matches": 0, "goals": 0, "assists": 0, "saves": 0, "tackles": 0,
                "season": 1, "week": 1,
                "social_tweets": [f"新聞: {player_name} 正式加盟 {start_club_obj['name']}！"],
                "match_in_progress": False, "match_event": None, "match_role": "bench", "match_result": None,
                "league_table": league_table, "rivals": rivals,
                "achievements": set(), "new_achievements": [], "joined_top_club": False,
                "coach_name": npc_names[0], "rival_name": npc_names[1], "teammate_name": npc_names[2],
                "season_goals": 0, "season_assists": 0, "season_saves": 0, "season_targets_hit": 0,
                "season_target": {
                    "goals": 1 if is_gk_or_def else 5,
                    "assists": 2,
                    "saves": 15 if "門將" in position else 0,
                },
                "caps": 0, "call_up_pending": False, "retired": False,
                "potential": potential, "bench_result": None,
            }
            st.session_state.created = True
            st.rerun()

    st.stop()

# --- 2. 遊戲主體 ---
p = st.session_state.player

DEFENSIVE_POSITION_KEYWORDS = ["中堅", "邊後衛", "防守中場"]

def is_defensive_position(position):
    return any(k in position for k in DEFENSIVE_POSITION_KEYWORDS)

def get_ovr(player):
    if "門將" in player['position']:
        return int(player['stamina'] * 0.4 + player['passing'] * 0.3 + player['dribbling'] * 0.2 + player['shooting'] * 0.1)
    elif is_defensive_position(player['position']):
        return int(player['defending'] * 0.35 + player['stamina'] * 0.25 + player['passing'] * 0.25 + player['dribbling'] * 0.15)
    else:
        return int(player['shooting'] * 0.35 + player['passing'] * 0.3 + player['dribbling'] * 0.25 + player['stamina'] * 0.1)

ovr = get_ovr(p)

def check_achievements():
    for aid, (aname, adesc, cond) in ACHIEVEMENTS.items():
        if aid not in p['achievements'] and cond(p):
            p['achievements'].add(aid)
            p['new_achievements'].append((aname, adesc))

def simulate_other_matches():
    for club in p['league_table']:
        if club == p['club']:
            continue
        if random.random() < 0.6:
            gf = random.randint(0, 3)
            ga = random.randint(0, 3)
            p['league_table'][club]['played'] += 1
            p['league_table'][club]['gf'] += gf
            p['league_table'][club]['ga'] += ga
            if gf > ga:
                p['league_table'][club]['points'] += 3
            elif gf == ga:
                p['league_table'][club]['points'] += 1

def apply_age_decline():
    """30歲後每季有機會自然衰退,模擬體能下滑"""
    if p['age'] >= 30:
        decline = random.randint(1, 3)
        stat_keys = ["shooting", "passing", "dribbling", "stamina", "defending"]
        for _ in range(decline):
            k = random.choice(stat_keys)
            p[k] = max(20, p[k] - 1)

def evaluate_season_target():
    """季尾檢查 KPI 有冇達標,影響信任度與獎金"""
    t = p['season_target']
    hit = (p['season_goals'] >= t['goals']) and (p['season_assists'] >= t['assists']) and (p['season_saves'] >= t['saves'])
    if hit:
        p['coach_trust'] = min(100, p['coach_trust'] + 10)
        p['money'] += 1500
        p['season_targets_hit'] += 1
        p['social_tweets'].insert(0, f"📈 賽季總結：你達成咗球會嘅 KPI 目標！獲發額外獎金 $1,500。")
    else:
        p['coach_trust'] = max(0, p['coach_trust'] - 8)
        p['social_tweets'].insert(0, f"📉 賽季總結：未能達成球會嘅 KPI 目標,教練對你表現略感失望。")
    p['season_goals'] = 0; p['season_assists'] = 0; p['season_saves'] = 0
    is_gk_or_def = ("門將" in p['position'] or "中堅" in p['position'])
    p['season_target'] = {
        "goals": 1 if is_gk_or_def else max(3, 5 + p['season'] // 3),
        "assists": 2,
        "saves": (15 + p['season']) if "門將" in p['position'] else 0,
    }

def maybe_trigger_national_call_up():
    if p['caps'] < 200 and ovr >= 65 and random.random() < 0.15:
        p['call_up_pending'] = True

def next_week():
    p['week'] += 1
    p['ap'] = p['max_ap']
    p['money'] += p['wage']
    p['fatigue'] = max(0, p['fatigue'] - 16)
    p['match_result'] = None
    simulate_other_matches()
    if random.random() < 0.45:
        text, trust_d, money_d = gen_flavor_text(p)
        p['coach_trust'] = max(0, min(100, p['coach_trust'] + trust_d))
        p['money'] += money_d
        p['social_tweets'].insert(0, text)
    maybe_trigger_national_call_up()
    check_achievements()
    if p['week'] > 38:
        evaluate_season_target()
        apply_age_decline()
        st.balloons()
        p['season'] += 1; p['week'] = 1; p['age'] += 1
        if p['age'] >= 38:
            p['retired'] = True

# --- 頂部狀態列(取代側邊欄,方便手機使用) ---
st.title("⚽ 職業生涯主頁")

status_c1, status_c2, status_c3, status_c4, status_c5, status_c6 = st.columns(6)
status_c1.metric("👤 OVR", ovr)
status_c2.metric("⚡ 行動點數 AP", f"{p['ap']} / {p['max_ap']}")
status_c3.metric("💰 週薪", f"${p['wage']:,}")
status_c4.metric("💵 存款", f"${p['money']:,}")
status_c5.metric("😫 疲勞", f"{p['fatigue']}%")
status_c6.metric("🧢 信任度", f"{p['coach_trust']}%")
st.caption(f"**{p['name']}** | {p['position']} | {p['club']} | {p['age']}歲 | 🌍 {p['caps']} 次國際賽出場")

with st.expander("📋 查看能力數值"):
    st.caption("ℹ️ 每項屬性喺生涯開始時已隨機決定咗一個隱藏「潛力上限」（初始值 +10~30，上限99）。距離上限越遠，特訓/比賽進步機率越高；越接近上限，進步越困難。")
    pot = p['potential']
    stat_labels = [("射門", "shooting"), ("傳球", "passing"), ("盤帶", "dribbling"), ("體能", "stamina"), ("防守", "defending")]
    for label, key in stat_labels:
        cur = p[key]
        cap = pot[key]
        filled = int(cur / 99 * 20)
        bar = "█" * filled + "░" * (20 - filled)
        near_cap = " 🔒接近極限" if cur >= cap - 3 else ""
        st.text(f"{label}｜{bar}｜{cur} / 潛力上限約{cap}{near_cap}")

if p['new_achievements']:
    for aname, adesc in p['new_achievements']:
        st.toast(f"🏅 解鎖成就：{aname}！", icon="🎉")
    p['new_achievements'] = []

if p['coach_trust'] >= 70:
    role_status = "⭐ 陣容首發 (正選)"; p_role = "starter"
elif p['coach_trust'] >= 40:
    role_status = "🪑 替補席 (後備)"; p_role = "sub"
else:
    role_status = "🚫 未進入大名單"; p_role = "not_in_squad"

st.info(f"💬 最新動態：{p['social_tweets'][0]}")
st.warning(f"📋 當前隊內地位：**{role_status}** ｜ 教練：{p['coach_name']} ｜ 更衣室勁敵：{p['rival_name']} ｜ 好隊友：{p['teammate_name']}")

t = p['season_target']
st.progress(min(1.0, (p['season_goals'] / t['goals']) if t['goals'] else 1.0),
            text=f"🎯 賽季KPI：入球 {p['season_goals']}/{t['goals']} ｜ 助攻 {p['season_assists']}/{t['assists']}" + (f" ｜ 撲救 {p['season_saves']}/{t['saves']}" if t['saves'] else ""))

st.divider()

# --- 分頁式主功能區(手機友好) ---
tab_home, tab_league, tab_achv, tab_market, tab_career, tab_save = st.tabs(
    ["🏠 本週日程", "📊 聯賽榜", "🏅 成就", "💼 轉會市場", "🎖️ 生涯總結", "💾 存檔"]
)

# ============ TAB 1: 本週日程 ============
with tab_home:
    if p['retired']:
        st.error("你已到達 38 歲,球會決定唔再續約。請到「🎖️ 生涯總結」分頁正式宣布退役。")
    elif p['injury_weeks'] > 0:
        st.error(f"🚑 受傷休養中（剩餘 {p['injury_weeks']} 週）")
        if st.button("⏩ 跳過休養週"):
            p['injury_weeks'] -= 1; next_week(); st.rerun()
    else:
        col_w1, col_w2 = st.columns([3, 1])
        col_w1.markdown(f"## 🗓️ 第 {p['season']} 賽季 - 第 {p['week']}/38 週")
        if col_w2.button("⏩ 結束本週日程", type="secondary", use_container_width=True):
            next_week(); st.rerun()

        if p['call_up_pending']:
            c_info_now = ALL_COUNTRIES_DB[p['country']]
            st.success(f"🌍 國家隊召集！{c_info_now['national']} 教練組邀請你出席集訓同友誼賽！")
            cu1, cu2 = st.columns(2)
            if cu1.button("✅ 接受召集(消耗1 AP,獲得聲望與獎金)", disabled=(p['ap'] < 1)):
                p['ap'] -= 1
                p['caps'] += 1
                p['money'] += 1000
                p['coach_trust'] = min(100, p['coach_trust'] + 5)
                p['call_up_pending'] = False
                p['social_tweets'].insert(0, f"🌍 你首次代表 {c_info_now['national']} 出戰,獲發集訓獎金 $1,000！")
                check_achievements()
                if p['ap'] <= 0: next_week()
                st.rerun()
            if cu2.button("❌ 婉拒(專注球會賽事)"):
                p['call_up_pending'] = False
                st.rerun()

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

        elif p.get('bench_result'):
            bres = p['bench_result']
            st.markdown("### 🪑 教練今場排陣")
            st.warning(bres['message'])
            st.caption(f"📈 影響：冇落場,疲勞維持不變（+{bres['fatigue_add']}%）")
            if st.button("確定並返回日程 ->", type="primary", key="bench_confirm"):
                p['bench_result'] = None
                if p['ap'] <= 0: next_week()
                st.rerun()

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
                rate = attr_value - 50 + int(p['chemistry'] / 10) * 10
                return max(5, min(95, rate))

            choice = None

            if "門將" in p['position']:
                st.caption(f"💡 撲救成功率約 {success_rate(p['stamina'])}%（受體能與默契影響）")
                if st.button("🧤 飛身極限撲救", use_container_width=True): choice = "save"
                if st.button("🚪 果斷出擊封堵角度", use_container_width=True): choice = "save"
                if st.button("🗣️ 指揮後線卡位", use_container_width=True): choice = "pass"
            else:
                if evt['type'] == "penalty":
                    st.caption(f"💡 射門成功率約 {success_rate(p['shooting'])}%（受射門與默契影響）")
                    if st.button("🎯 大力抽射球門左上死角", use_container_width=True): choice = "shoot"
                    if st.button("👟 冷靜推射右下角", use_container_width=True): choice = "shoot"
                    if st.button("💥 踢勺子踢法 (Panenka)", use_container_width=True): choice = "shoot"
                elif evt['type'] == "defend":
                    st.caption(f"💡 防守成功率約 {success_rate(p['defending'])}%（受防守與默契影響）")
                    if st.button("🛡️ 頂身拼搶解圍", use_container_width=True): choice = "defend"
                    if st.button("🧱 回撤補位協防", use_container_width=True): choice = "defend"
                    if st.button("⚔️ 強硬正面攔截", use_container_width=True): choice = "defend"
                else:
                    st.caption(f"💡 成功率參考：射門 {success_rate(p['shooting'])}% ｜ 傳球 {success_rate(p['passing'])}% ｜ 盤帶 {success_rate(p['dribbling'])}%")
                    if st.button("🚀 果斷起腳轟門", use_container_width=True): choice = "shoot"
                    if st.button("👟 手術刀直塞分球", use_container_width=True): choice = "pass"
                    if st.button("⚡ 強行盤帶連過一人", use_container_width=True): choice = "dribble"

            if choice:
                if choice == "shoot": check_attr = p['shooting']
                elif choice == "pass": check_attr = p['passing']
                elif choice == "dribble": check_attr = p['dribbling']
                elif choice == "defend": check_attr = p['defending']
                else: check_attr = p['stamina']  # save

                success = (random.randint(1, 100) + int(p['chemistry'] / 10)) < check_attr
                fatigue_add = 20 if p['match_role'] == "starter" else 10
                p['fatigue'] = min(100, p['fatigue'] + fatigue_add)

                growth_msg = ""
                if success:
                    if choice == "shoot":
                        p['goals'] += 1; p['season_goals'] += 1; detail = "冷靜處理，皮球應聲入網！"
                    elif choice == "pass":
                        p['assists'] += 1; p['season_assists'] += 1; detail = "精準傳球送出致命助攻！"
                    elif choice == "defend":
                        p['tackles'] += 1; detail = "一次乾淨利落嘅防守，成功化解對方攻勢！"
                    else:
                        p['saves'] += 1; p['season_saves'] += 1; detail = "神級反應，成功拯救球隊！"
                    trust_inc = 6 if p['match_role'] == "sub" else 4
                    p['coach_trust'] = min(100, p['coach_trust'] + trust_inc)
                    trust_msg = f"+{trust_inc}%"
                    # 表現出色有機會直接喺比賽中成長,唔一定要靠特訓
                    if random.random() < 0.15:
                        growable = [k for k in ["shooting", "passing", "dribbling", "stamina", "defending"] if p[k] < p['potential'][k]]
                        if growable:
                            gk = random.choice(growable)
                            p[gk] = min(p['potential'][gk], p[gk] + 1)
                            stat_name_map = {"shooting": "射門", "passing": "傳球", "dribbling": "盤帶", "stamina": "體能", "defending": "防守"}
                            growth_msg = f" 呢場比賽嘅實戰經驗令你嘅{stat_name_map[gk]}略有進步！"
                else:
                    if choice == "defend":
                        detail = "回防步伐慢半拍，被對方輕鬆突破防線。"
                    else:
                        detail = "關鍵處理欠佳，被對方成功解圍/撲出。"
                    p['coach_trust'] = max(0, p['coach_trust'] - 3)
                    trust_msg = "-3%"

                base_gf = random.randint(0, 2)
                base_ga = random.randint(0, 2)
                if success: base_gf += 1
                else: base_ga += random.choice([0, 1])
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
                    "success": success, "detail": detail + growth_msg, "trust_change": trust_msg,
                    "fatigue_add": fatigue_add, "team_score": (base_gf, base_ga), "opponent": opponent
                }
                p['social_tweets'].insert(0, f"賽後快訊：{match_result_text}")
                st.rerun()

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
                    selection_chance = 88 if p_role == "starter" else 55
                    st.caption(f"💡 正選成員都唔一定必然上陣，本場獲派正式出場機率約 {selection_chance}%（教練會輪換陣容）")
                    if st.button("🔥 出戰本週賽事", type="primary", use_container_width=True, disabled=(p['ap'] < 1)):
                        p['ap'] -= 1
                        if random.randint(1, 100) <= selection_chance:
                            p['matches'] += 1
                            p['match_role'] = p_role
                            p['current_opponent'] = random.choice(p['rivals']) if p.get('rivals') else "對手球會"
                            p['match_in_progress'] = True
                        else:
                            bench_msgs = [
                                f"{p['coach_name']}決定今場輪換陣容，你今仗屈居後備席，全程未有落場。",
                                f"教練話想保留你嘅體能應付下一場硬仗，你今場冇被派上陣。",
                                f"對方今仗派出強陣，{p['coach_name']}選擇更穩陣嘅陣容，你今場未有出場機會。",
                            ]
                            p['bench_result'] = {"message": random.choice(bench_msgs), "fatigue_add": 0}
                        st.rerun()

            with c2:
                st.subheader("🏋️ 隊內特訓")
                st.caption("消耗 1 AP | 信任+2, 疲勞+15% | 效果視乎潛力與狀態浮動")
                is_gk = "門將" in p['position']
                is_def = is_defensive_position(p['position'])
                if is_gk:
                    t_map = {"🧤 撲救反應訓練": "stamina", "🗣️ 防線指揮訓練": "passing", "🚪 出擊步法訓練": "dribbling"}
                elif is_def:
                    t_map = {"🛡️ 防守站位訓練": "defending", "🎯 射門/搶截訓練": "shooting", "🅰️ 傳球組織": "passing", "⚡ 盤帶速度": "dribbling", "💪 體能加強": "stamina"}
                else:
                    t_map = {"🎯 射門/搶斷": "shooting", "🅰️ 傳球組織": "passing", "⚡ 盤帶速度": "dribbling", "💪 體能加強": "stamina"}
                t_choice = st.selectbox("訓練項目", list(t_map.keys()))
                stat_key = t_map[t_choice]
                gap = p['potential'][stat_key] - p[stat_key]
                train_chance = max(15, min(90, 30 + gap * 3))
                st.caption(f"💡 今次特訓進步機率約 {train_chance}%（越接近潛力上限，進步越難）")
                if st.button("💪 開始特訓", use_container_width=True, disabled=(p['ap'] < 1)):
                    p['ap'] -= 1; p['fatigue'] = min(100, p['fatigue'] + 15)
                    overtrain_injury = p['fatigue'] >= 85 and random.random() < 0.12
                    if overtrain_injury:
                        p['injury_weeks'] = random.randint(1, 2)
                        st.error(f"⚠️ 疲勞過度導致輕微拉傷，需要休養 {p['injury_weeks']} 週！")
                    elif random.randint(1, 100) <= train_chance:
                        p[stat_key] = min(p['potential'][stat_key], p[stat_key] + 1)
                        p['coach_trust'] = min(100, p['coach_trust'] + 2)
                        st.success(f"能力獲得提升，{p['coach_name']}對你表示肯定！")
                    else:
                        st.warning(f"今日狀態麻麻，{p['coach_name']}話你仲需要多啲時間磨練，未見明顯進步。")
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

# ============ TAB 2: 聯賽榜 ============
with tab_league:
    st.subheader(f"📊 {ALL_COUNTRIES_DB[p['country']]['league']} 積分榜")
    st.caption("🟢 綠色 = 升班區（頭2名）　🔴 紅色 = 降班區（尾2名）　🟡 黃色 = 你所屬球隊")

    table_rows = []
    for club, stats in p['league_table'].items():
        gd = stats['gf'] - stats['ga']
        table_rows.append({"球隊": club, "賽": stats['played'], "入球": stats['gf'], "失球": stats['ga'], "淨勝球": gd, "積分": stats['points']})
    table_rows.sort(key=lambda x: (-x['積分'], -x['淨勝球']))

    n = len(table_rows)
    df = pd.DataFrame(table_rows)
    df.insert(0, "名次", range(1, n + 1))
    medal = {1: "🥇", 2: "🥈", 3: "🥉"}
    df["名次"] = df["名次"].apply(lambda r: f"{medal.get(r, '')} {r}".strip())

    def highlight_row(row):
        idx = row.name
        rank_num = idx + 1
        club_name = row["球隊"]
        if club_name == p['club']:
            return ['background-color: #FFF3B0; font-weight: bold'] * len(row)
        elif rank_num <= 2:
            return ['background-color: #D6F5D6'] * len(row)
        elif rank_num > n - 2:
            return ['background-color: #FADADD'] * len(row)
        return [''] * len(row)

    styled = df.style.apply(highlight_row, axis=1)
    st.dataframe(styled, use_container_width=True, hide_index=True)

    my_rank = next(i for i, row in enumerate(table_rows, start=1) if row["球隊"] == p['club'])
    if my_rank <= 2:
        st.success(f"🟢 你嘅球隊目前排第 {my_rank} 位，處於升班區！")
    elif my_rank > n - 2:
        st.error(f"🔴 你嘅球隊目前排第 {my_rank} 位，處於降班區，要打醒精神！")
    else:
        st.info(f"⚪ 你嘅球隊目前排第 {my_rank} 位，中游位置。")

# ============ TAB 3: 成就 ============
with tab_achv:
    st.subheader(f"🏅 成就系統 ({len(p['achievements'])}/{len(ACHIEVEMENTS)})")
    for aid, (aname, adesc, cond) in ACHIEVEMENTS.items():
        if aid in p['achievements']:
            st.markdown(f"✅ **{aname}** - {adesc}")
        else:
            st.markdown(f"🔒 ~~{aname}~~ - {adesc}")

# ============ TAB 4: 轉會市場 ============
with tab_market:
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

    st.markdown("#### 🌍 國家隊生涯")
    st.write(f"代表 **{ALL_COUNTRIES_DB[p['country']]['national']}** 出場次數：**{p['caps']}** 次")
    st.caption("提示：OVR 越高,每週收到國家隊召集嘅機率越大。")

# ============ TAB 5: 生涯總結 / 退役 ============
with tab_career:
    st.subheader("🎖️ 生涯數據總結")
    cc1, cc2, cc3, cc4, cc5 = st.columns(5)
    cc1.metric("出場", p['matches'])
    cc2.metric("入球", p['goals'])
    cc3.metric("助攻", p['assists'])
    cc4.metric("撲救", p['saves'])
    cc5.metric("防守成功", p.get('tackles', 0))
    st.write(f"🏅 成就解鎖：{len(p['achievements'])} / {len(ACHIEVEMENTS)}")
    st.write(f"🎯 賽季 KPI 達標次數：{p['season_targets_hit']} 次")
    st.write(f"🌍 國家隊出場：{p['caps']} 次")

    st.divider()
    if p['age'] >= 30:
        st.warning("你已經踏入生涯後段,可以考慮光榮退役,將戰績永久留存喺名人堂。")
        if st.button("🏁 宣布退役", type="primary"):
            st.session_state.hall_of_fame.append({
                "name": p['name'], "goals": p['goals'], "assists": p['assists'],
                "saves": p['saves'], "matches": p['matches'], "final_club": p['club'],
                "achievements": len(p['achievements']), "caps": p['caps'],
            })
            st.session_state.created = False
            del st.session_state.player
            st.success("恭喜完成一段精彩嘅職業生涯！已存入名人堂。")
            st.rerun()
    else:
        st.caption("30 歲後先可以選擇退役(38歲會強制退役)。")

    if st.session_state.hall_of_fame:
        st.divider()
        st.markdown("#### 🏛️ 名人堂(歷屆球員)")
        for legend in st.session_state.hall_of_fame:
            st.write(f"👤 **{legend['name']}** — {legend['goals']}球 {legend['assists']}助攻 {legend['saves']}撲救 | "
                     f"{legend['matches']}場 | 國際賽{legend['caps']}次 | 最終效力：{legend['final_club']}")

# ============ TAB 6: 存檔 ============
with tab_save:
    st.subheader("💾 匯出 / 匯入存檔")
    st.caption("由於瀏覽器重新整理會清空進度,建議定期匯出存檔,下次可以喺開始畫面上傳讀取。")
    export_data = dict(p)
    export_data['achievements'] = list(p['achievements'])
    json_str = json.dumps(export_data, ensure_ascii=False, indent=2)
    st.download_button("⬇️ 下載存檔 (JSON)", data=json_str, file_name=f"{p['name']}_save.json", mime="application/json")
    st.caption("上傳存檔請返回遊戲開始畫面(重新整理頁面)使用「📂 讀取存檔」分頁。")
