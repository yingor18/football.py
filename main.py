import streamlit as st
import random
import plotly.graph_objects as go

st.set_page_config(page_title="綠茵傳奇 Pro - 全位置版", page_icon="⚽", layout="wide")

# --- 1. 創角系統 (涵蓋所有球場位置) ---
if "created" not in st.session_state:
    st.session_state.created = False

if not st.session_state.created:
    st.title("⚽ 綠茵傳奇 Pro - 創建你的職業球員")
    st.write("歡迎來到職業足球生涯模擬器，請先建立你的球員檔案：")
    
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        name = st.text_input("球員姓名", value="Ho Yin")
        position = st.selectbox("場上位置", [
            "門將 (GK)", 
            "中堅 (CB)", 
            "邊後衛 (LB/RB)", 
            "防守中場 (CDM)", 
            "進攻中場 (CAM)", 
            "翼鋒 (LW/RW)", 
            "前鋒 (ST)"
        ])
    
    with col_c2:
        st.info(f"💡 **{position}** 屬性偏重與職責：\n"
                "- 門將/後衛看重 **防守/體能**，專注於 **零封 (Clean Sheet) 與搶斷/撲救**。\n"
                "- 中場看重 **傳球/盤帶**，專注於 **掌控節奏與助攻**。\n"
                "- 前鋒看重 **射門/速度**，專注於 **進球得分**。")

    if st.button("🚀 開始職業生涯", type="primary"):
        # 根據位置分配初始屬性
        if "門將" in position: sh, pa, dr, st_attr = 30, 50, 40, 75
        elif "中堅" in position: sh, pa, dr, st_attr = 40, 58, 50, 78
        elif "邊後衛" in position: sh, pa, dr, st_attr = 50, 68, 68, 76
        elif "防守中場" in position: sh, pa, dr, st_attr = 55, 72, 62, 75
        elif "進攻中場" in position: sh, pa, dr, st_attr = 65, 76, 70, 68
        elif "翼鋒" in position: sh, pa, dr, st_attr = 68, 65, 78, 68
        else: # 前鋒
            sh, pa, dr, st_attr = 75, 60, 68, 68
            
        st.session_state.player = {
            "name": name,
            "position": position,
            "age": 17,
            "club": "橫濱水手",
            "wage": 1500,
            "money": 5000,
            "shooting": sh,
            "passing": pa,
            "dribbling": dr,
            "stamina": st_attr,
            "ap": 3,
            "max_ap": 3,
            "fatigue": 0,
            "chemistry": 50,
            "form": "平穩",
            "injury_weeks": 0,
            "coach_trust": 65,
            "fans_love": 50,
            "matches": 0,
            "goals": 0,
            "assists": 0,
            "cleansheets": 0, # 防守球員/門將專用數據
            "saves": 0,       # 門將專用數據
            "trophies": [],
            "completed_milestones": [],
            "season": 1,
            "week": 1,
            "rival_goals": 10,
            "event_msg": None,
            "social_tweets": [
                f"球迷: 新星 {name} ({position}) 正式簽約加盟！",
                "媒體: 期待這位小將本賽季的表現。"
            ],
            "match_in_progress": False,
            "match_result": None
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

# 里程碑任務
milestones = [
    {"id": "first_match", "title": "👟 職業首秀", "desc": "完成職業生涯第一場比賽", "check": lambda p: p['matches'] >= 1},
    {"id": "chem_80", "title": "🤝 休息室領袖", "desc": "隊友默契度達到 80", "check": lambda p: p['chemistry'] >= 80},
    {"id": "ovr_80", "title": "🌟 洲際巨星", "desc": "綜合能力 (OVR) 達到 80", "check": lambda p: ovr >= 80},
    {"id": "rich", "title": "💎 百萬富翁", "desc": "個人存款達到 $100,000", "check": lambda p: p['money'] >= 100000},
]

for m in milestones:
    if m['id'] not in p['completed_milestones'] and m['check'](p):
        p['completed_milestones'].append(m['id'])
        st.toast(f"🏆 解鎖里程碑成就：【{m['title']}】！", icon="🎉")

# 側邊欄
st.sidebar.title("⚽ 綠茵傳奇 Pro")
st.sidebar.markdown(f"### 👤 **{p['name']}** (OVR: **{ovr}**)")
st.sidebar.caption(f"位置：**{p['position']}** | 效力：**{p['club']}**")

fig = go.Figure(data=go.Scatterpolar(
  r=[p['shooting'], p['passing'], p['dribbling'], p['stamina']],
  theta=['射門', '傳球', '盤帶', '體能/防守'],
  fill='toself', line_color='#00CC96'
))
fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[30, 100])), showlegend=False, margin=dict(l=20, r=20, t=20, b=20), height=170)
st.sidebar.plotly_chart(fig, use_container_width=True)

st.sidebar.metric("💰 週薪", f"${p['wage']:,}")
st.sidebar.metric("💵 存款", f"${p['money']:,}")
st.sidebar.divider()

st.sidebar.markdown(f"⚡ **本週 AP：** {'⚡' * p['ap']}{'⚪' * (p['max_ap'] - p['ap'])}")
st.sidebar.progress(p['fatigue'] / 100, text=f"😫 疲勞度：{p['fatigue']}%")
st.sidebar.progress(p['chemistry'] / 100, text=f"🤝 隊友默契：{p['chemistry']}%")

if p['fatigue'] >= 80: st.sidebar.warning("⚠️ 極度疲勞，受傷風險高！")
if p['injury_weeks'] > 0: st.sidebar.error(f"🚑 受傷休養中（剩餘 {p['injury_weeks']} 週）")

st.sidebar.info(f"🔥 當前狀態：**{p['form']}**")
st.sidebar.progress(p['coach_trust'] / 100, text=f"🧢 教練信任：{p['coach_trust']}%")

# 主介面
st.title("⚽ 綠茵傳奇 Pro - 職業生涯")

# 新聞動態
st.markdown("### 📱 社交媒體與新聞")
c_tw1, c_tw2 = st.columns(2)
c_tw1.info(f"💬 {p['social_tweets'][0]}")
c_tw2.info(f"💬 {p['social_tweets'][1] if len(p['social_tweets']) > 1 else ''}")

st.divider()

def next_week():
    p['week'] += 1
    p['ap'] = p['max_ap']
    p['money'] += p['wage']
    p['fatigue'] = max(0, p['fatigue'] - 10)
    p['event_msg'] = None
    
    if random.random() < 0.15 and p['injury_weeks'] == 0:
        events = [
            ("隊友深夜派對邀請！去放鬆還是自主訓練？", "party"),
            ("媒體發起爭議採訪，問你對教練戰術的看法。", "media")
        ]
        p['event_msg'] = random.choice(events)

    if p['week'] > 38:
        st.balloons()
        st.subheader("🏆 賽季結算典禮")
        st.write(f"第 {p['season']} 賽季正式結束！")
        st.write(f"📊 本季數據：進球 **{p['goals']}** | 助攻 **{p['assists']}** | 零封場次 **{p['cleansheets']}**")
        
        if p['goals'] >= p['rival_goals']:
            st.success("🥇 恭喜獲得個人賽季最佳獎項！")
            p['trophies'].append(f"第 {p['season']} 賽季最佳球員")

        p['season'] += 1; p['week'] = 1; p['age'] += 1

if p['injury_weeks'] > 0:
    st.error(f"🚑 休養中，無法進行高強度活動！(剩餘 {p['injury_weeks']} 週)")
    if st.button("⏩ 跳過本週休養"):
        p['injury_weeks'] -= 1; p['fatigue'] = max(0, p['fatigue'] - 30)
        next_week(); st.rerun()
else:
    col_w1, col_w2 = st.columns([3, 1])
    col_w1.markdown(f"## 🗓️ 第 {p['season']} 賽季 - 第 {p['week']}/38 週")
    if col_w2.button("⏩ 結束本週日程", type="secondary", use_container_width=True):
        next_week(); st.rerun()

    if p['event_msg']:
        st.warning(f"🎭 **【突發事件】** {p['event_msg'][0]}")
        col_ev1, col_ev2 = st.columns(2)
        if p['event_msg'][1] == "party":
            if col_ev1.button("🍻 參加派對 (默契+15, 疲勞+10)"):
                p['chemistry'] = min(100, p['chemistry'] + 15)
                p['fatigue'] = min(100, p['fatigue'] + 10); p['event_msg'] = None; st.rerun()
            if col_ev2.button("🏋️ 婉拒並早睡 (教練信任+5)"):
                p['coach_trust'] = min(100, p['coach_trust'] + 5); p['event_msg'] = None; st.rerun()
        elif p['event_msg'][1] == "media":
            if col_ev1.button("🗣️ 力挺教練 (教練信任+10)"):
                p['coach_trust'] = min(100, p['coach_trust'] + 10); p['event_msg'] = None; st.rerun()
            if col_ev2.button("🔥 砲轟戰術 (球迷熱度+15, 教練信任-15)"):
                p['coach_trust'] = max(0, p['coach_trust'] - 15); p['event_msg'] = None; st.rerun()

    # A. 比賽戰報
    elif p['match_result']:
        res = p['match_result']
        st.markdown("### 📊 本場比賽戰報")
        if res['success']:
            st.balloons(); st.success(f"🎉 **【關鍵決策成功！】** {res['detail']}")
        else:
            st.error(f"❌ **【防守/進攻挫敗】** {res['detail']}")
            
        st.info(f"📈 賽後影響：教練信任 {res['trust_change']} | 疲勞度 +25%")
        
        if st.button("確定並回到日程選單 ➔", type="primary"):
            p['match_result'] = None
            if p['ap'] <= 0: next_week()
            st.rerun()

    # B. 進行比賽關鍵決策 (根據 6 大位置提供專屬選項)
    elif p['match_in_progress']:
        st.subheader(f"📡 比賽現場關鍵時刻 ({p['position']})")
        st.write(f"⏱️ **85' 分鐘**：比賽進入最後關鍵時刻！身為 **{p['position']}** 的你面臨考驗：")
        
        c_m1, c_m2, c_m3 = st.columns(3)
        choice = None
        
        if "門將" in p['position']:
            if c_m1.button("🧤 飛身極限撲救 (考驗體能/反應)"): choice = "defend"
            if c_m2.button("🚪 果斷出擊封堵近角"): choice = "defend"
            if c_m3.button("🎯 長傳發動快速反擊"): choice = "pass"
        elif "中堅" in p['position']:
            if c_m1.button("💥 關鍵滑鏟攔截 (考驗防守)"): choice = "defend"
            if c_m2.button("🗣️ 指揮防線並高空解圍"): choice = "defend"
            if c_m3.button("👟 冷靜後場組織傳球"): choice = "pass"
        elif "邊後衛" in p['position']:
            if c_m1.button("⚡ 邊路插上精準傳中"): choice = "pass"
            if c_m2.button("🛡️ 一對一死貼對手翼鋒"): choice = "defend"
            if c_m3.button("🚀 內切遠射試運氣"): choice = "shoot"
        elif "防守中場" in p['position']:
            if c_m1.button("🛑 戰術犯規破壞對方反擊"): choice = "defend"
            if c_m2.button("👟 手術刀長傳轉移"): choice = "pass"
            if c_m3.button("☄️ 禁區外重炮轟門"): choice = "shoot"
        elif "進攻中場" in p['position'] or "翼鋒" in p['position']:
            if c_m1.button("👟 致命直塞助攻"): choice = "pass"
            if c_m2.button("⚡ 盤帶內切突破"): choice = "dribble"
            if c_m3.button("🚀 禁區弧線球射門"): choice = "shoot"
        else: # 前鋒
            if c_m1.button("🚀 大力抽射門前死角"): choice = "shoot"
            if c_m2.button("💥 禁區頭鎚搶點"): choice = "shoot"
            if c_m3.button("🗣️ 回撤接應並分球"): choice = "pass"

        if choice:
            bonus = (10 if p['form'] == "火熱" else ( -10 if p['form'] == "低迷" else 0)) + int(p['chemistry'] / 10)
            success, m_g, m_a, m_cs, detail_msg = False, 0, 0, 0, ""
            
            check_attr = p['stamina'] if choice == "defend" else (p['shooting'] if choice == "shoot" else (p['passing'] if choice == "pass" else p['dribbling']))
            
            if (random.randint(1, 100) + bonus) < check_attr:
                success = True
                if choice == "shoot": m_g = 1; detail_msg = "完美的起腳，皮球應聲入網！進球！"
                elif choice == "pass": m_a = 1; detail_msg = "精準的傳球徹底撕開對手防線！助攻成功！"
                elif choice == "defend": m_cs = 1; detail_msg = "神級防守！你成功化解了對手的必進球，力保球門不失！"
                else: m_g = 1; detail_msg = "漂亮的突破後冷靜推射得手！"
            else:
                detail_msg = "關鍵處置被對手識破，沒能達到預期效果。"

            p['goals'] += m_g; p['assists'] += m_a; p['cleansheets'] += m_cs
            p['fatigue'] = min(100, p['fatigue'] + 25)
            
            if success:
                p['form'] = "火熱"; p['coach_trust'] = min(100, p['coach_trust'] + 5); trust_msg = "+5%"
            else:
                p['form'] = "平穩"; p['coach_trust'] = max(0, p['coach_trust'] - 3); trust_msg = "-3%"

            p['match_in_progress'] = False
            p['match_result'] = {"success": success, "detail": detail_msg, "trust_change": trust_msg}
            st.rerun()

    # C. 日程選單
    else:
        if p['ap'] <= 0: st.info("💡 本週 AP 已耗盡，請點擊上方【結束本週日程】。")
        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.subheader("🏟️ 進行聯賽")
            st.caption("消耗 1 AP | 疲勞 +25%")
            if st.button("🔥 登場比賽", type="primary", use_container_width=True, disabled=(p['ap'] < 1)):
                p['ap'] -= 1; p['matches'] += 1
                if p['fatigue'] >= 75 and random.random() < 0.4:
                    p['injury_weeks'] = random.randint(2, 4)
                    st.error("過度疲勞導致肌肉拉傷！"); st.rerun()
                p['match_in_progress'] = True; st.rerun()

        with c2:
            st.subheader("🏋️ 針對性特訓")
            st.caption("消耗 1 AP | 疲勞 +15%")
            t_choice = st.selectbox("特訓項目", ["🎯 射門", "🅰️ 傳球", "⚡ 盤帶", "💪 防守/體能"])
            if st.button("💪 開始特訓", use_container_width=True, disabled=(p['ap'] < 1)):
                p['ap'] -= 1; p['fatigue'] = min(100, p['fatigue'] + 15)
                if "射門" in t_choice: p['shooting'] += 1
                elif "傳球" in t_choice: p['passing'] += 1
                elif "盤帶" in t_choice: p['dribbling'] += 1
                elif "防守" in t_choice: p['stamina'] += 1
                st.success("能力提升！")
                if p['ap'] <= 0: next_week()
                st.rerun()

        with c3:
            st.subheader("🍻 隊友社交聚會")
            st.caption("消耗 1 AP | 默契 +10")
            if st.button("🎉 參加聚會", use_container_width=True, disabled=(p['ap'] < 1)):
                p['ap'] -= 1; p['chemistry'] = min(100, p['chemistry'] + 10)
                st.success("隊友默契度提升！")
                if p['ap'] <= 0: next_week()
                st.rerun()

        with c4:
            st.subheader("🛌 理療與休養")
            st.caption("消耗 1 AP | 疲勞 -35%")
            if st.button("☕ 充分休息", use_container_width=True, disabled=(p['ap'] < 1)):
                p['ap'] -= 1; p['fatigue'] = max(0, p['fatigue'] - 35); p['form'] = "平穩"
                st.success("疲勞大幅降低！")
                if p['ap'] <= 0: next_week()
                st.rerun()

st.divider()

# 里程碑與轉會
col_b1, col_b2 = st.columns(2)

with col_b1:
    st.subheader("🏆 里程碑成就 (Milestones)")
    for m in milestones:
        if m['id'] in p['completed_milestones']: st.success(f"✅ **{m['title']}** - {m['desc']}")
        else: st.caption(f"🔒 **{m['title']}** - {m['desc']}")

with col_b2:
    st.subheader("💼 經理人轉會快訊")
    offers = [
        ("葡超 - 葡萄牙體育 (Sporting CP)", 72, 15000),
        ("西甲 - 皇家馬德里", 82, 90000),
        ("英超 - 曼城", 85, 100000)
    ]
    for c_name, req_ovr, offer_wage in offers:
        if ovr >= req_ovr:
            st.write(f"✨ **{c_name}** 意向加盟！底薪：**${offer_wage:,}**")
            if st.button(f"✍️ 加盟 {c_name}", key=c_name):
                p['club'] = c_name; p['wage'] = offer_wage
                p['social_tweets'].insert(0, f"官宣！{p['name']} 重磅加盟 {c_name}！")
                st.success(f"成功加盟 {c_name}！"); st.rerun()
