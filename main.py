import streamlit as st
import random
import plotly.graph_objects as go

st.set_page_config(page_title="綠茵傳奇 Pro", page_icon="⚽", layout="wide")

# --- 1. 創角系統 (若未初始化，先進行創角) ---
if "created" not in st.session_state:
    st.session_state.created = False

if not st.session_state.created:
    st.title("⚽ 綠茵傳奇 Pro - 創建你的職業球員")
    st.write("歡迎來到職業足球生涯模擬器，請先建立你的球員檔案：")
    
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        name = st.text_input("球員姓名", value="Ho Yin")
        position = st.selectbox("場上位置", ["前鋒 (ST)", "進攻中場 (CAM)", "翼鋒 (LW/RW)"])
    
    with col_c2:
        st.info("💡 不同位置會有不同的初始屬性偏重與比賽特點：\n- **前鋒**：射門能力突出\n- **中場**：傳球與視野突出\n- **翼鋒**：盤帶與速度突出")

    if st.button("🚀 開始職業生涯", type="primary"):
        # 根據位置設定初始屬性
        if "前鋒" in position:
            sh, pa, dr, st_attr = 72, 60, 65, 68
        elif "中場" in position:
            sh, pa, dr, st_attr = 62, 74, 66, 70
        else: # 翼鋒
            sh, pa, dr, st_attr = 66, 62, 75, 68
            
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
            "energy": 100,
            "form": "平穩",
            "injury_weeks": 0,
            "coach_trust": 65,
            "fans_love": 50,
            "matches": 0,
            "goals": 0,
            "assists": 0,
            "trophies": [],
            "season": 1,
            "week": 1,
            "has_trainer": False,
            "house": "租房",
            "rival_goals": 10,
            "social_tweets": [
                f"球迷: 青訓營新星 {name} ({position}) 正式亮相！",
                "媒體: 期待這位小將本賽季的表現。"
            ],
            "match_in_progress": False,
            "match_state": None
        }
        st.session_state.created = True
        st.rerun()

    st.stop()

# --- 2. 遊戲主體 ---
p = st.session_state.player

def get_ovr(player):
    return int(player['shooting'] * 0.35 + player['passing'] * 0.3 + player['dribbling'] * 0.25 + player['stamina'] * 0.1)

ovr = get_ovr(p)

# 側邊欄
st.sidebar.title("⚽ 綠茵傳奇 Pro")
st.sidebar.markdown(f"### 👤 **{p['name']}** (OVR: **{ovr}**)")
st.sidebar.caption(f"位置：**{p['position']}** | 效力：**{p['club']}**")

fig = go.Figure(data=go.Scatterpolar(
  r=[p['shooting'], p['passing'], p['dribbling'], p['stamina']],
  theta=['射門', '傳球', '盤帶', '體能'],
  fill='toself', line_color='#00CC96'
))
fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[40, 100])), showlegend=False, margin=dict(l=20, r=20, t=20, b=20), height=170)
st.sidebar.plotly_chart(fig, use_container_width=True)

st.sidebar.metric("💰 週薪", f"${p['wage']:,}")
st.sidebar.metric("💵 存款", f"${p['money']:,}")
st.sidebar.divider()

if p['injury_weeks'] > 0:
    st.sidebar.error(f"🚑 受傷休養中（剩餘 {p['injury_weeks']} 週）")
else:
    st.sidebar.progress(p['energy'] / 100, text=f"⚡ 體力：{p['energy']}/100")

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

# 受傷處理
if p['injury_weeks'] > 0:
    st.error(f"🚑 你正在受傷休養中，無法參加比賽！(還需休養 {p['injury_weeks']} 週)")
    if st.button("⏩ 跳過本週休養"):
        p['injury_weeks'] -= 1
        p['week'] += 1
        p['energy'] = min(100, p['energy'] + 30)
        p['money'] += p['wage']
        st.rerun()
else:
    st.markdown(f"## 🗓️ 第 {p['season']} 賽季 - 第 {p['week']}/38 週")

    # 關鍵時刻比賽直播 (根據位置顯示專屬選擇)
    if p['match_in_progress']:
        st.subheader(f"📡 比賽現場 - 關鍵時刻 ({p['position']})")
        m_state = p['match_state']
        st.write(f"⏱️ **{m_state['time']}**：{m_state['desc']}")
        
        c_m1, c_m2, c_m3 = st.columns(3)
        choice = None
        
        if "前鋒" in p['position']:
            if c_m1.button("🚀 大力抽射"): choice = "shoot"
            if c_m2.button("🗣️ 呼喚隊友分球"): choice = "pass"
            if c_m3.button("💥 禁區頭鎚搶點"): choice = "shoot"
        elif "中場" in p['position']:
            if c_m1.button("👟 手術刀直塞"): choice = "pass"
            if c_m2.button("☄️ 禁區外遠射"): choice = "shoot"
            if c_m3.button("⚡ 擺脫防守掌控節奏"): choice = "dribble"
        else: # 翼鋒
            if c_m1.button("⚡ 邊路突破內切"): choice = "dribble"
            if c_m2.button("🎯 高空傳中"): choice = "pass"
            if c_m3.button("🚀 內切起腳弧線球"): choice = "shoot"

        if choice:
            bonus = 10 if p['form'] == "火熱" else 0
            success = False
            if choice == "shoot" and (random.randint(1, 100) + bonus) < p['shooting']: success = True; p['goals'] += 1
            elif choice == "pass" and (random.randint(1, 100) + bonus) < p['passing']: success = True; p['assists'] += 1
            elif choice == "dribble" and (random.randint(1, 100) + bonus) < p['dribbling']: success = True; p['goals'] += 1
            
            if success:
                st.balloons()
                st.success("⚽ 完美的決策！你成功的發揮為球隊改寫比數！")
                p['form'] = "火熱"
                p['coach_trust'] = min(100, p['coach_trust'] + 5)
            else:
                st.error("❌ 決策被對手防線破解。")
                p['form'] = "平穩"
            
            p['match_in_progress'] = False
            p['week'] += 1
            
            # 賽季結束 (第 38 週)
            if p['week'] > 38:
                st.balloons()
                st.subheader("🏆 賽季結算典禮")
                st.write(f"第 {p['season']} 賽季正式結束！")
                st.write(f"你在本賽季一共攻入 **{p['goals']}** 球，送出 **{p['assists']}** 次助攻！")
                
                if p['goals'] >= p['rival_goals']:
                    st.success("🥇 恭喜獲得【聯賽金靴獎（神射手）】榮譽！")
                    p['trophies'].append(f"第 {p['season']} 賽季金靴獎")
                
                p['season'] += 1
                p['week'] = 1
                p['age'] += 1
                p['rival_goals'] = random.randint(12, 20)
                
            st.button("繼續下週日程")
            st.rerun()

    else:
        col_act1, col_act2, col_act3 = st.columns(3)

        with col_act1:
            st.subheader("🏟️ 進行聯賽")
            if st.button("🔥 開賽 (消耗 20 體力)", type="primary", use_container_width=True):
                if p['energy'] >= 20:
                    p['energy'] -= (15 if p['has_trainer'] else 22)
                    p['matches'] += 1
                    p['money'] += p['wage']
                    
                    if random.random() < 0.3:
                        p['rival_goals'] += 1

                    # 進入關鍵直播
                    p['match_in_progress'] = True
                    p['match_state'] = {
                        "time": f"{random.randint(65, 85)} 分鐘",
                        "desc": f"比賽進入關鍵階段，身為 {p['position']} 的你在前場拿到關鍵球權！"
                    }
                    st.rerun()
                else:
                    st.error("體力不足！請先休養。")

        with col_act2:
            st.subheader("🏋️ 針對性特訓")
            t_choice = st.selectbox("特訓項目", ["🎯 射門", "🅰️ 傳球", "⚡ 盤帶", "💪 體能"])
            if st.button("💪 開始特訓 (消耗 15 體力)", use_container_width=True):
                if p['energy'] >= 15:
                    p['energy'] -= 15
                    if "射門" in t_choice: p['shooting'] += 1
                    elif "傳球" in t_choice: p['passing'] += 1
                    elif "盤帶" in t_choice: p['dribbling'] += 1
                    elif "體能" in t_choice: p['stamina'] += 1
                    st.success("能力提升成功！")
                    st.rerun()
                else: st.error("體力不足！")

        with col_act3:
            st.subheader("🛌 休養復原")
            if st.button("☕ 休養一週 (體力 +50)", use_container_width=True):
                p['energy'] = min(100, p['energy'] + 50)
                p['form'] = "平穩"
                p['week'] += 1
                p['money'] += p['wage']
                if p['week'] > 38:
                    p['season'] += 1; p['week'] = 1; p['age'] += 1
                st.rerun()

st.divider()

# 下方：轉會與榮譽櫃
col_b1, col_b2 = st.columns(2)

with col_b1:
    st.subheader("💼 經理人轉會快訊")
    offers = [
        ("葡超 - 葡萄牙體育 (Sporting CP)", 73, 15000),
        ("西甲 - 皇家馬德里", 83, 90000),
        ("英超 - 曼城", 86, 100000)
    ]
    for c_name, req_ovr, offer_wage in offers:
        if ovr >= req_ovr:
            st.write(f"✨ **{c_name}** 發出邀請！週薪：**${offer_wage:,}**")
            if st.button(f"✍️ 加盟 {c_name}", key=c_name):
                p['club'] = c_name
                p['wage'] = offer_wage
                p['social_tweets'].insert(0, f"官宣！{p['name']} 重磅加盟 {c_name}！")
                st.success(f"成功加盟 {c_name}！")
                st.rerun()

with col_b2:
    st.subheader("🏆 個人榮譽櫃")
    if p['trophies']:
        for t in p['trophies']:
            st.write(f"🥇 {t}")
    else:
        st.caption("目前尚無榮譽獎盃，繼續努力！")
