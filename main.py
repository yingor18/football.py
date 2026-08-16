import streamlit as st
import random
import plotly.graph_objects as go

st.set_page_config(page_title="綠茵傳奇 Pro - 深度職業版", page_icon="⚽", layout="wide")

# --- 全球國家與聯賽資料庫 ---
COUNTRIES_DB = {
    "🇯🇵 日本": {
        "J2 乙組聯賽 (起步)": [
            {"name": "橫濱FC", "tier": "乙組", "req_ovr": 0, "wage": 800},
            {"name": "清水心跳", "tier": "乙組", "req_ovr": 0, "wage": 850},
            {"name": "千葉市原", "tier": "乙組", "req_ovr": 0, "wage": 800},
        ],
        "J1 甲組聯賽": [
            {"name": "橫濱水手", "tier": "甲組", "req_ovr": 68, "wage": 3000},
            {"name": "川崎前鋒", "tier": "甲組", "req_ovr": 68, "wage": 3200},
            {"name": "浦和紅鑽", "tier": "甲組", "req_ovr": 70, "wage": 3500},
        ]
    },
    "🏴󠁧󠁢󠁥󠁮󠁧󠁿 英格蘭": {
        "英冠 乙組聯賽 (起步)": [
            {"name": "新特蘭 (Sunderland)", "tier": "乙組", "req_ovr": 0, "wage": 3000},
            {"name": "列斯聯 (Leeds United)", "tier": "乙組", "req_ovr": 0, "wage": 3500},
            {"name": "高雲地利 (Coventry)", "tier": "乙組", "req_ovr": 0, "wage": 2800},
        ],
        "英超 甲組聯賽": [
            {"name": "阿仙奴 (Arsenal)", "tier": "甲組", "req_ovr": 83, "wage": 85000},
            {"name": "曼城 (Manchester City)", "tier": "甲組", "req_ovr": 86, "wage": 110000},
            {"name": "利物浦 (Liverpool)", "tier": "甲組", "req_ovr": 85, "wage": 100000},
            {"name": "熱刺 (Tottenham)", "tier": "甲組", "req_ovr": 80, "wage": 60000},
        ]
    },
    "🇪🇸 西班牙": {
        "西乙 乙組聯賽 (起步)": [
            {"name": "愛斯賓奴 (Espanyol)", "tier": "乙組", "req_ovr": 0, "wage": 2500},
            {"name": "薩拉戈薩 (Zaragoza)", "tier": "乙組", "req_ovr": 0, "wage": 2000},
            {"name": "希昂 (Sporting Gijón)", "tier": "乙組", "req_ovr": 0, "wage": 2200},
        ],
        "西甲 甲組聯賽": [
            {"name": "皇家馬德里 (Real Madrid)", "tier": "甲組", "req_ovr": 86, "wage": 120000},
            {"name": "巴塞隆拿 (Barcelona)", "tier": "甲組", "req_ovr": 84, "wage": 95000},
            {"name": "馬德里體育會 (Atlético Madrid)", "tier": "甲組", "req_ovr": 82, "wage": 75000},
        ]
    },
    "🇵🇹 葡萄牙": {
        "葡甲 乙組聯賽 (起步)": [
            {"name": "馬里迪莫 (Marítimo)", "tier": "乙組", "req_ovr": 0, "wage": 1200},
            {"name": "費利拿 (Paços de Ferreira)", "tier": "乙組", "req_ovr": 0, "wage": 1100},
        ],
        "葡超 甲組聯賽": [
            {"name": "葡萄牙體育 (Sporting CP)", "tier": "甲組", "req_ovr": 74, "wage": 18000},
            {"name": "波圖 (Porto)", "tier": "甲組", "req_ovr": 75, "wage": 19000},
            {"name": "本菲卡 (Benfica)", "tier": "甲組", "req_ovr": 75, "wage": 20000},
        ]
    },
    "🇰🇷 韓國": {
        "K2 乙組聯賽 (起步)": [
            {"name": "水原三星", "tier": "乙組", "req_ovr": 0, "wage": 750},
            {"name": "釜山IPark", "tier": "乙組", "req_ovr": 0, "wage": 700},
        ],
        "K1 甲組聯賽": [
            {"name": "蔚山現代", "tier": "甲組", "req_ovr": 67, "wage": 2500},
            {"name": "全北現代", "tier": "甲組", "req_ovr": 67, "wage": 2600},
        ]
    },
    "🇦🇷 阿根廷": {
        "阿乙 乙組聯賽 (起步)": [
            {"name": "高隆 (Colón)", "tier": "乙組", "req_ovr": 0, "wage": 600},
            {"name": "阿爾馬格羅 (Almagro)", "tier": "乙組", "req_ovr": 0, "wage": 500},
        ],
        "阿甲 甲組聯賽": [
            {"name": "博卡青年 (Boca Juniors)", "tier": "甲組", "req_ovr": 72, "wage": 8000},
            {"name": "河床 (River Plate)", "tier": "甲組", "req_ovr": 73, "wage": 8500},
        ]
    }
}

# --- 1. 創角系統 ---
if "created" not in st.session_state:
    st.session_state.created = False

if not st.session_state.created:
    st.title("⚽ 綠茵傳奇 Pro - 創建你的職業生涯")
    
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        name = st.text_input("球員姓名", placeholder="請輸入你的名字")
        position = st.selectbox("場上位置", [
            "門將 (GK)", "中堅 (CB)", "邊後衛 (LB/RB)", 
            "防守中場 (CDM)", "進攻中場 (CAM)", "翼鋒 (LW/RW)", "前鋒 (ST)"
        ])
        
        selected_country = st.selectbox("🌍 選擇起步國家", list(COUNTRIES_DB.keys()))
        
        # 取得該國家的乙組聯賽球會列表
        starter_league_key = [k for k in COUNTRIES_DB[selected_country].keys() if "乙組" in k][0]
        starter_clubs = COUNTRIES_DB[selected_country][starter_league_key]
        
        start_club_obj = st.selectbox(f"🐣 選擇起步球會 ({starter_league_key})", starter_clubs, format_func=lambda x: x['name'])

    with col_c2:
        st.info("💡 **真實職業生存法則**：\n"
                "- 新人必須從**乙組/低組別聯賽**開始打拼！\n"
                "- 初始能力較低時，你只能從**後備席（甚至看台）**開始，訓練表現好才能獲得出場時間！\n"
                "- 若在豪門或強隊上不了場，可選擇**外借租借（Loan Out）**去小球會累積比賽經驗。")

    if st.button("🚀 簽署首份職業合約", type="primary"):
        player_name = name.strip() if name.strip() else "新星小將"
        
        if "門將" in position: sh, pa, dr, st_attr = 30, 50, 40, 68
        elif "中堅" in position: sh, pa, dr, st_attr = 38, 52, 45, 70
        elif "邊後衛" in position: sh, pa, dr, st_attr = 45, 60, 60, 68
        elif "防守中場" in position: sh, pa, dr, st_attr = 48, 65, 55, 68
        elif "進攻中場" in position: sh, pa, dr, st_attr = 58, 68, 62, 62
        elif "翼鋒" in position: sh, pa, dr, st_attr = 60, 58, 68, 62
        else: # 前鋒
            sh, pa, dr, st_attr = 65, 52, 60, 62

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
            "shooting": sh,
            "passing": pa,
            "dribbling": dr,
            "stamina": st_attr,
            "ap": 3,
            "max_ap": 3,
            "fatigue": 0,
            "chemistry": 40,
            "form": "平穩",
            "injury_weeks": 0,
            "coach_trust": 45,  # 初始信任度較低，需要爭取正選
            "fans_love": 30,
            "matches": 0,
            "goals": 0,
            "assists": 0,
            "cleansheets": 0,
            "saves": 0,
            "trophies": [],
            "completed_milestones": [],
            "season": 1,
            "week": 1,
            "social_tweets": [
                f"媒體: 17 歲小將 {player_name} 正式加盟 {start_club_obj['name']}，將從預備隊/後備席開始爭取機會！"
            ],
            "match_in_progress": False,
            "match_role": "bench", # 'starter', 'sub', 'not_in_squad'
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

# 側邊欄
st.sidebar.title("⚽ 綠茵傳奇 Pro")
st.sidebar.markdown(f"### 👤 **{p['name']}** (OVR: **{ovr}**)")
st.sidebar.caption(f"位置：**{p['position']}**")

club_display = f"{p['club']}" + (" (租借中)" if p['is_loaned'] else "")
st.sidebar.markdown(f"效力球會：**{club_display}**")

radar_labels = ['射門/長傳', '傳球', '盤帶/反應', '體能/防守']
fig = go.Figure(data=go.Scatterpolar(
  r=[p['shooting'], p['passing'], p['dribbling'], p['stamina']],
  theta=radar_labels, fill='toself', line_color='#00CC96'
))
fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[30, 100])), showlegend=False, margin=dict(l=20, r=20, t=20, b=20), height=160)
st.sidebar.plotly_chart(fig, use_container_width=True)

st.sidebar.metric("💰 週薪", f"${p['wage']:,}")
st.sidebar.metric("💵 存款", f"${p['money']:,}")
st.sidebar.divider()

st.sidebar.markdown(f"⚡ **本週 AP：** {'⚡' * p['ap']}{'⚪' * (p['max_ap'] - p['ap'])}")
st.sidebar.progress(p['fatigue'] / 100, text=f"😫 疲勞度：{p['fatigue']}%")
st.sidebar.progress(p['coach_trust'] / 100, text=f"🧢 教練信任度：{p['coach_trust']}%")

# 主介面
st.title("⚽ 職業生涯主頁")

# 判斷球員在隊內的地位 (正選 / 後備 / 未入大名單)
if p['coach_trust'] >= 70:
    role_status = "⭐ 陣容首發 (正選)"
    p_role = "starter"
elif p['coach_trust'] >= 40:
    role_status = "🪑 替補席 (後備)"
    p_role = "sub"
else:
    role_status = "🚫 未進入比賽大名單"
    p_role = "not_in_squad"

col_top1, col_top2 = st.columns(2)
col_top1.info(f"💬 最新動態：{p['social_tweets'][0]}")
col_top2.warning(f"📋 當前隊內地位：**{role_status}**")

st.divider()

def next_week():
    p['week'] += 1
    p['ap'] = p['max_ap']
    p['money'] += p['wage']
    p['fatigue'] = max(0, p['fatigue'] - 12)
    p['match_result'] = None

    if p['week'] > 38:
        st.balloons()
        st.subheader("🏆 賽季結束")
        st.write(f"第 {p['season']} 賽季正式結算！總出場：{p['matches']} 場")
        
        # 租借到期歸隊
        if p['is_loaned']:
            p['club'] = p['parent_club']
            p['is_loaned'] = False
            p['parent_club'] = None
            st.info(f"🔄 租借期滿，你已返回母會 {p['club']}！")

        p['season'] += 1; p['week'] = 1; p['age'] += 1

if p['injury_weeks'] > 0:
    st.error(f"🚑 受傷休養中（剩餘 {p['injury_weeks']} 週）")
    if st.button("⏩ 跳過休養週"):
        p['injury_weeks'] -= 1
        next_week(); st.rerun()
else:
    col_w1, col_w2 = st.columns([3, 1])
    col_w1.markdown(f"## 🗓️ 第 {p['season']} 賽季 - 第 {p['week']}/38 週")
    if col_w2.button("⏩ 結束本週日程", type="secondary", use_container_width=True):
        next_week(); st.rerun()

    # 比賽戰報
    if p['match_result']:
        res = p['match_result']
        st.markdown("### 📊 比賽發揮與結果")
        if res['success']:
            st.success(f"🎉 **【發揮出色】** {res['detail']}")
        else:
            st.error(f"❌ **【表現欠佳】** {res['detail']}")
            
        st.info(f"📈 賽後影響：教練信任度 {res['trust_change']} | 疲勞度 +{res['fatigue_add']}%")
        
        if st.button("確定並返回日程 ➔", type="primary"):
            p['match_result'] = None
            if p['ap'] <= 0: next_week()
            st.rerun()

    # 進行比賽關鍵時刻
    elif p['match_in_progress']:
        st.subheader(f"📡 比賽現場 ({p['position']})")
        
        if p['match_role'] == "sub":
            st.write("⏱️ **75' 分鐘**：教練在下半場把你替補換上場，你需要把握有限時間展現價值！")
        else:
            st.write("⏱️ **85' 分鐘**：身為正選的你打滿全場，比賽來到最關鍵時刻！")

        choice = None
        c_m1, c_m2, c_m3 = st.columns(3)
        
        if "門將" in p['position']:
            if c_m1.button("🧤 門前反應極限撲救"): choice = "save"
            if c_m2.button("🚪 果斷出擊封堵單刀"): choice = "save"
            if c_m3.button("🎯 精準長傳發動反擊"): choice = "pass"
        else:
            if c_m1.button("🚀 起腳遠射 / 門前抽射"): choice = "shoot"
            if c_m2.button("👟 手術刀直塞傳球"): choice = "pass"
            if c_m3.button("⚡ 強行盤帶突破"): choice = "dribble"

        if choice:
            check_attr = p['shooting'] if choice == "shoot" else (p['passing'] if choice == "pass" else p['dribbling'])
            if choice == "save": check_attr = p['stamina']
            
            success = (random.randint(1, 100) + int(p['chemistry']/10)) < check_attr
            
            fatigue_add = 20 if p['match_role'] == "starter" else 10
            p['fatigue'] = min(100, p['fatigue'] + fatigue_add)
            
            if success:
                if choice == "shoot": p['goals'] += 1; detail = "精彩起腳破門得分！"
                elif choice == "pass": p['assists'] += 1; detail = "送出關鍵致命助攻！"
                else: p['saves'] += 1; detail = "成功化解對方必進球！"
                
                trust_inc = 6 if p['match_role'] == "sub" else 4 # 替補建功信任度加更多
                p['coach_trust'] = min(100, p['coach_trust'] + trust_inc)
                trust_msg = f"+{trust_inc}%"
            else:
                detail = "關鍵時刻處理被對手看破化解。"
                p['coach_trust'] = max(0, p['coach_trust'] - 3)
                trust_msg = "-3%"

            p['match_in_progress'] = False
            p['match_result'] = {
                "success": success, "detail": detail, 
                "trust_change": trust_msg, "fatigue_add": fatigue_add
            }
            st.rerun()

    # 日程選單
    else:
        if p['ap'] <= 0: st.info("💡 本週 AP 已耗盡，請點擊上方【結束本週日程】。")
        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.subheader("🏟️ 本週賽事")
            if p_role == "not_in_squad":
                st.caption("🚫 未進入大名單")
                st.error("教練信任度過低 (<40)，本週你只能在看台觀戰。請多加訓練提升信任！")
            else:
                st.caption(f"身份：{role_status}")
                if st.button("🔥 登場比賽", type="primary", use_container_width=True, disabled=(p['ap'] < 1)):
                    p['ap'] -= 1; p['matches'] += 1
                    p['match_role'] = p_role
                    p['match_in_progress'] = True; st.rerun()

        with c2:
            st.subheader("🏋️ 隊內自主訓練")
            st.caption("消耗 1 AP | 信任+3, 疲勞+15%")
            t_choice = st.selectbox("訓練項目", ["🎯 射門/搶斷", "🅰️ 傳球組織", "⚡ 盤帶速度", "💪 體能加強"])
            if st.button("💪 開始自主訓練", use_container_width=True, disabled=(p['ap'] < 1)):
                p['ap'] -= 1; p['fatigue'] = min(100, p['fatigue'] + 15)
                p['coach_trust'] = min(100, p['coach_trust'] + 3) # 勤奮訓練能增加教練信任
                
                if "射門" in t_choice: p['shooting'] += 1
                elif "傳球" in t_choice: p['passing'] += 1
                elif "盤帶" in t_choice: p['dribbling'] += 1
                else: p['stamina'] += 1
                
                st.success("訓練成果顯著，教練對你的勤奮表示滿意！")
                if p['ap'] <= 0: next_week()
                st.rerun()

        with c3:
            st.subheader("🍻 與隊友/教練交流")
            st.caption("消耗 1 AP | 默契+10")
            if st.button("🤝 建立關係", use_container_width=True, disabled=(p['ap'] < 1)):
                p['ap'] -= 1; p['chemistry'] = min(100, p['chemistry'] + 10)
                st.success("休息室默契度提升！")
                if p['ap'] <= 0: next_week()
                st.rerun()

        with c4:
            st.subheader("🛌 理療休養")
            st.caption("消耗 1 AP | 疲勞 -35%")
            if st.button("☕ 充分休息", use_container_width=True, disabled=(p['ap'] < 1)):
                p['ap'] -= 1; p['fatigue'] = max(0, p['fatigue'] - 35)
                st.success("身體狀態恢復！")
                if p['ap'] <= 0: next_week()
                st.rerun()

st.divider()

# 轉會與租借市場
st.subheader("💼 經理人轉會與租借市場")
col_m1, col_m2 = st.columns(2)

with col_m1:
    st.markdown("#### 🔄 外借租借 (Loan Out) 市場")
    st.caption("如果你在現有球會缺乏出場時間，可選擇租借到低組別/小球會作為主力積累經驗！")
    
    if p_role != "starter" and not p['is_loaned']:
        if st.button("📢 讓經理人尋找外借機會"):
            st.success("收到乙組球會【橫濱FC】的半季租借邀請！承諾給予正選位置。")
            if st.button("✍️ 接受租借加盟 橫濱FC"):
                p['parent_club'] = p['club']
                p['club'] = "橫濱FC (租借)"
                p['is_loaned'] = True
                p['coach_trust'] = 85 # 租借過去直接給予高信任度
                p['social_tweets'].insert(0, f"官宣！{p['name']} 被租借至 橫濱FC 尋求出場時間！")
                st.rerun()
    elif p['is_loaned']:
        st.info(f"你目前正從 {p['parent_club']} 租借效力至 {p['club']}。")
    else:
        st.caption("你目前是隊內正選主力，暫不需要外借。")

with col_m2:
    st.markdown("#### 🏆 豪門與更高聯賽轉會邀約")
    
    all_clubs = []
    for c_data in COUNTRIES_DB.values():
        for l_clubs in c_data.values():
            all_clubs.extend(l_clubs)

    eligible_offers = [c for c in all_clubs if c['name'] != p['club'] and ovr >= c['req_ovr'] and c['req_ovr'] > 0]

    if eligible_offers:
        for offer in eligible_offers[:3]:
            st.write(f"✨ **{offer['name']}** ({offer['tier']}) 意向加盟！週薪：**${offer['wage']:,}** (要求 OVR {offer['req_ovr']})")
            if st.button(f"✍️ 正式轉會 {offer['name']}", key=offer['name']):
                p['club'] = offer['name']
                p['wage'] = offer['wage']
                p['is_loaned'] = False
                p['coach_trust'] = 50 # 新加盟球會信任度重置，需重新爭取正選
                p['social_tweets'].insert(0, f"重磅！{p['name']} 正式轉會加盟 {offer['name']}！")
                st.success(f"成功轉會至 {offer['name']}！"); st.rerun()
    else:
        st.caption("當前能力值 (OVR) 尚不足以吸引更高階球會的轉會邀約，請繼續提升能力！")
