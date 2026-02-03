import streamlit as st
import random

# ページ設定（タイトルやアイコン、レイアウトを広めに）
st.set_page_config(page_title="ELDEN RING BINGO", layout="wide")

# --- CSSで配信向けに見た目を整える ---
st.markdown("""
<style>
    /* ボタンの文字サイズを大きく */
    .stButton button {
        height: 100px;
        font-weight: bold;
        font-size: 20px;
        white-space: pre-wrap; /* 改行を許可 */
    }
    /* 全体の余白調整 */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# --- 1. データ定義 ---
ashes_of_war = {
    "初期戦技": ["キック", "我慢", "踏み込み", "構え", "パリィ", "バックラーパリィ", "クイックステップ", "突撃"],
    "汎用戦技": ["嵐の刃", "聖なる刃", "炎撃", "落雷", "剣舞", "二連斬り", "巨人狩り", "切腹", "猟犬のステップ", "王騎士の決意", "暗黒波", "獅子斬り"],
    "固有戦技": ["死の刃", "ミケラの光", "夜と炎の構え", "星雲", "水鳥乱舞", "血の徴収", "黄金の地", "暗月", "運命の死", "雷雲の姿", "天使の翼"],
    "ランダム": [] # ロジック内で全リストを統合して扱う
}
# ランダム用に全リストを結合
ashes_of_war["ランダム"] = ashes_of_war["初期戦技"] + ashes_of_war["汎用戦技"] + ashes_of_war["固有戦技"]

# --- 2. サイドバー（設定画面） ---
st.sidebar.title("設定")
st.sidebar.caption("各エリアに出現する戦技の種類を選んでください")

# セレクトボックスで種類を選ばせる
center_rule = st.sidebar.selectbox("中心 (1マス)", list(ashes_of_war.keys()), index=2) # デフォルト: 固有
inner_rule = st.sidebar.selectbox("内周 (8マス)", list(ashes_of_war.keys()), index=1)  # デフォルト: 汎用
outer_rule = st.sidebar.selectbox("外周 (16マス)", list(ashes_of_war.keys()), index=0) # デフォルト: 初期

# --- 3. ロジック関数 ---

def get_target_pool(row, col):
    """座標に応じて、サイドバーで選ばれたリストのキーを返す"""
    dist_r = abs(row - 2)
    dist_c = abs(col - 2)
    distance = max(dist_r, dist_c)

    if distance == 0:
        return center_rule
    elif distance == 1:
        return inner_rule
    else:
        return outer_rule

def generate_bingo_card():
    card = []
    # 各カテゴリをシャッフルしたコピーを作成
    pool_state = {k: random.sample(v, len(v)) for k, v in ashes_of_war.items()}
    
    # イテレータ化
    iters = {k: iter(v) for k, v in pool_state.items()}

    for r in range(5):
        row_data = []
        for c in range(5):
            pool_key = get_target_pool(r, c)
            
            try:
                skill_name = next(iters[pool_key])
            except StopIteration:
                # リストが尽きたらもう一度シャッフルして補充（あるいは"自由"などにする）
                new_pool = random.sample(ashes_of_war[pool_key], len(ashes_of_war[pool_key]))
                iters[pool_key] = iter(new_pool)
                skill_name = next(iters[pool_key])
            
            row_data.append({"name": skill_name, "checked": False})
        card.append(row_data)
    return card

# --- 4. メイン画面 ---

st.title("ELDEN RING BINGO")

# セッション管理
if "bingo_card" not in st.session_state:
    st.session_state.bingo_card = generate_bingo_card()

# 生成ボタン（サイドバーに配置しても良い）
if st.sidebar.button("ビンゴを生成/リセット", type="primary"):
    st.session_state.bingo_card = generate_bingo_card()
    st.rerun()

# グリッド描画
for r in range(5):
    cols = st.columns(5)
    for c in range(5):
        cell = st.session_state.bingo_card[r][c]
        
        # 状態に応じたラベルと色
        if cell["checked"]:
            label = f"✅\n{cell['name']}"
            kind = "primary"
        else:
            label = f"\n{cell['name']}"
            kind = "secondary"

        if cols[c].button(label, key=f"btn_{r}_{c}", use_container_width=True, type=kind):
            st.session_state.bingo_card[r][c]["checked"] = not cell["checked"]
            st.rerun()