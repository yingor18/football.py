import streamlit as st
import random
import plotly.graph_objects as go

st.set_page_config(page_title="綠茵傳奇 Pro - 終極職業生涯", page_icon="⚽", layout="wide")

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
        "form": "平穩",        # 狀態：火熱, 平穩, 低迷
        "injury_weeks": 0,    # 受傷週數
        "coach_trust": 65,
        "fans_love": 50,
        "national_team": False, # 是否入選國家隊
        "matches": 0,
        "goals": 0,
        "assists": 0,
        "trophies": [],        # 榮譽獎杯
        "season": 1,
        "week": 1,
        "points": 15,
        "has_trainer": False,
        "house": "無 (租房)",
        "rival_goals": 12,
        "social_tweets": [
            "球迷A: 橫濱水手新星 Ho Yin 備受期待！",
            "媒體: 本賽季神射手之爭異常激烈。"
        ],
        "match_in_progress": False,
        "match_state": None,
        "logs": ["17 歲正式簽約，開啟職業足球生涯！"]
    }

p = st.session_state.player

def get_ovr(player):
    return int(player['shooting'] * 0.35 + player['passing'] * 0.3 + player['dribbling'] * 0.25 + player['stamina'] * 0.1)

ovr = get_ovr(p)

# 自動檢查國家隊徵召
if ovr >= 75 and not p['national_team']:
    p['national_team'] = True
    p['social_tweets'].insert(0, f"🚨【重磅】{p['name']} 憑藉優異表現首度獲國家隊徵召！")

# 側邊欄
st.sidebar.title("⚽ 綠茵傳奇 Pro")
st.sidebar.markdown(f"### 👤 **{p['name']}** (OVR: **{ovr}**)")
st.sidebar.caption(f"效力：**{p['club']}** {'(國家隊成員)' if p['national_team'] else ''} | {p['age']} 歲")

fig = go.Figure(data=go.Scatterpolar(
  r=[p['shooting'], p['passing'], p['dribbling'], p['stamina']],
  theta=['射門', '傳球', '盤帶', '體能'],
  fill='toself', line_color='#00CC96'
))
fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[40, 100])), showlegend=False, margin=dict(l=20, r=20, t=20, b=20), height=180)
st.sidebar.plotly_chart(fig, use_container_width=True)

st.sidebar.metric("💰 週薪", f"${p['wage']:,}")
st.sidebar.metric("💵 存款", f"${p['money']:,}")
st.sidebar.divider()

if p['injury_weeks'] > 0:
    st.sidebar.error(f"🚑 受傷休養中（剩餘 {p['injury_weeks']} 週）")
else:
    st.sidebar.progress(p['energy'] / 100, text=f"⚡ 體力：{p['energy']}/100")

st.sidebar.info(f"🔥 當前手感/狀態：**{p['form']}**")
st.sidebar.progress(p['coach_trust'] / 100, text=f"🧢 教練信任：{p['coach_trust']}%")

# 主介面
st.title("⚽ 綠茵傳奇 Pro - 職業足球生涯")

# 檢查退役 (38 歲)
if p['age'] >= 38:
    st.balloons()
    st.header("🏆 傳奇退役 - 生涯總結")
    st.write(f"你在 38 歲正式掛靴，結束了輝煌的職業足球生涯！")
    st.metric("生涯總出場", f"{p['matches']} 場")
    st.metric("生涯總進球", f"{p['goals']} 球")
    st.metric("生涯總助攻", p['assists'])
    st.metric("累積財富", f"${p['money']:,}")
    
    score = p['goals'] * 2 + p['assists'] + len(p['trophies']) * 20
    if score > 200: rating = "S (球史傳奇 / 金球獎得主)"
    elif score > 100: rating = "A (世界級巨星)"
    else: rating = "B (聯賽名宿)"
    st.success(f"👑 你的生涯最終評級：**{rating}**")
    st.stop()

# 頂部：新聞動態
st.markdown("### 📱 社交媒體與動態")
c_tw1, c_tw2 = st.columns(2)
c_tw1.info(f"💬 {p['social_tweets'][0]}")
c_tw2.info(f"💬 {p['social_tweets'][1] if len(p['social_tweets']) > 1 else ''}")

st.divider()

# 受傷狀態處理
if p['injury_weeks'] > 0:
    st.error(f"🚑 你正在受傷休養中，無法參加比賽或訓練！(還需休養 {p['injury_weeks']} 週)")
    if st.button("⏩ 跳過本週休養"):
        p['injury_weeks'] -= 1
        p['week'] += 1
        p['energy'] = min(100, p['energy'] + 30)
        p['money'] += p['wage']
        if p['week'] > 38:
            p['season'] += 1; p['week'] = 1; p['age'] += 1
        st.rerun()
else:
    # 核心日程
    st.markdown(f"## 🗓️ 第 {p['season']} 賽季 - 第 {p['week']}/38 週")

    # 比賽進行中模式 (現場文字直播與決策)
    if p['match_in_progress']:
        st.subheader("📡 現場比賽直播中 - 關鍵時刻！")
        m_state = p['match_state']
        st.write(f"⏱️ **{m_state['time']}**：{m_state['desc']}")
        
        c_m1, c_m2, c_m3 = st.columns(3)
        choice = None
        if c_m1.button("🚀 大力抽射"): choice = "shoot"
        if c_m2.button("👟 精準直塞"): choice = "pass"
        if c_m3.button("⚡ 強行盤帶突破"): choice = "dribble"
        
        if choice:
            # 結算選擇
            bonus = 10 if p['form'] == "火熱" else (0 if p['form'] == "平穩" else -10)
            success = False
            if choice == "shoot" and (random.randint(1, 100) + bonus) < p['shooting']: success = True; p['goals'] += 1
            elif choice == "pass" and (random.randint(1, 100) + bonus) < p['passing']: success = True; p['assists'] += 1
            elif choice == "dribble" and (random.randint(1, 100) + bonus) < p['dribbling']: success = True; p['goals'] += 1
            
            if success:
                st.balloons()
                st.success("⚽ GOAL/ASSIST！完美的決策，為球隊攻入關鍵一球！")
                p['form'] = "火熱"
                p['coach_trust'] = min(100, p['coach_trust'] + 5)
                p['social_tweets'].insert(0, f"球迷: {p['name']} 剛才那個關鍵決策太精彩了！天秀！")
            else:
                st.error("❌ 決策被對手破解，進攻挫敗。")
                p['form'] = "平穩"
            
            p['match_in_progress'] = False
            p['week'] += 1
            if p['week'] > 38:
                p['season'] += 1; p['week'] = 1; p['age'] += 1
            st.button("繼續日程")
            st.rerun()

    else:
        col_act1, col_act2, col_act3 = st.columns(3)

        # 動作 1：比賽
        with col_act1:
            st.subheader("🏟️ 進行聯賽")
            st.write(f"對手：**聯賽勁敵**")
            
            if st.button("🔥 進入比賽 (消耗 20 體力)", type="primary", use_container_width=True):
                if p['energy'] >= 20:
                    p['energy'] -= (15 if p['has_trainer'] else 22)
                    p['matches'] += 1
                    p['money'] += p['wage']
                    
                    # 受傷風險判定 (體力少於 30 時增加受傷機率)
                    if p['energy'] < 20 and random.random() < 0.35:
                        p['injury_weeks'] = random.randint(2, 5)
                        p['social_tweets'].insert(0, f"🚑【傷情】{p['name']} 在比賽中不幸拉傷，將缺陣數週。")
                        st.error("糟糕！你在比賽中肌肉嚴重拉傷！")
                        st.rerun()

                    # 進入關鍵時刻直播
                    p['match_in_progress'] = True
                    p['match_state'] = {
                        "time": f"{random.randint(60, 88)} 分鐘",
                        "desc": "雙方比數膠著，你在禁區頂接應到隊友的傳球，對手後衛正在逼近，你選擇："
                    }
                    st.rerun()
                else:
                    st.error("體力不足，帶傷強行上陣極易受傷！請先休養。")

        # 動作 2：特訓
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
                    st.success("能力提升！")
                    st.rerun()
                else: st.error("體力不足！")

        # 動作 3：休養
        with col_act3:
            st.subheader("🛌 休養復原")
            st.write("充分休養恢復體力與狀態。")
            if st.button("☕ 休養一週 (體力 +50)", use_container_width=True):
                p['energy'] = min(100, p['energy'] + 50)
                p['form'] = "平穩"
                p['week'] += 1
                p['money'] += p['wage']
                if p['week'] > 38:
                    p['season'] += 1; p['week'] = 1; p['age'] += 1
                st.rerun()

st.divider()

# 下方：轉會談判與榮譽
col_b1, col_b2 = st.columns(2)

with col_b1:
    st.subheader("💼 經理人轉會與合約談判")
    offers = [
        ("葡超 - 葡萄牙體育 (Sporting CP)", 73, 15000),
        ("西甲 - 皇家馬德里", 83, 90000),
        ("英超 - 曼城", 86, 100000)
    ]
    has_offer = False
    for c_name, req_ovr, offer_wage in offers:
        if ovr >= req_ovr:
            has_offer = True
            st.write(f"✨ **{c_name}** 意向加盟！談判週薪：**${offer_wage:,}**")
            if st.button(f"✍️ 簽約加盟 {c_name}", key=c_name):
                p['club'] = c_name
                p['wage'] = offer_wage
                p['social_tweets'].insert(0, f"官宣！{p['name']} 正式加盟 {c_name}！")
                st.success(f"恭喜加盟 {c_name}！")
                st.rerun()
    if not has_offer:
        st.caption("目前尚無符合能力的豪門報價，請繼續努力提升 OVR。")

with col_b2:
    st.subheader("🏆 榮譽櫃與個人資產")
    st.write(f"現有住處：**{p['house']}**")
    if p['house'] == "無 (租房)" and st.button("買豪宅 ($80,000)"):
        if p['money'] >= 80000:
            p['money'] -= 80000; p['house'] = "豪華別墅"; st.rerun()
            
    if not p['has_trainer'] and st.button("聘請私人體能教練 ($8,000)"):
        if p['money'] >= 8000:
            p['money'] -= 8000; p['has_trainer'] = True; st.rerun()
