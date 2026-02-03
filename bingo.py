import streamlit as st
import random

# ページ設定（タイトルやアイコン、レイアウトを広めに）
st.set_page_config(page_title="ナイトレイン戦技ビンゴ", layout="wide")

# --- CSS設定（7x7用にボタンを少しコンパクトに調整） ---
st.markdown("""
<style>
    /* ボタンのスタイル調整 */
    .stButton button {
        height: 80px;  /* 高さを少し抑える */
        font-weight: bold;
        font-size: 14px; /* 文字サイズを調整 */
        white-space: pre-wrap; /* 改行を許可 */
        padding: 5px;
        line-height: 1.2;
    }
    /* 全体の余白調整 */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
    }
    /* 列の隙間を詰める */
    [data-testid="column"] {
        padding: 0 2px !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 1. データ定義（ファイルの内容を埋め込み） ---

SKILL_LISTS = {
    "ストームルーラー": ["ストームルーラー"],
    
    "初期戦技": [
        "踏み込み(斬り上げ)", "我慢", "居合", "クイックステップ", "突撃", "嵐脚", "デターミネーション", 
        "輝剣の円陣", "グラビタス", "炎撃", "溶岩噴火", "落雷", "雷撃斬", "祈りの一撃", "毒の霧", 
        "毒蛾は二度舞う", "血の刃", "切腹", "冷気の霧", "霜踏み", "白い影の誘い", "強射", 
        "アローレイン", "バックラーパリィ", "魔力の短剣"
    ],
    
    "汎用戦技": [
        "踏み込み(回転薙ぎ)", "乱撃", "獅子斬り", "岩石剣", "キック", "ヒップドロップ", "地揺らし", 
        "ホーラ・ルーの地揺らし", "ウォークライ", "野蛮な咆哮", "誇示する咆哮", "トロルの咆哮", "鎖回し", 
        "回転斬り", "貫通突き", "牙突き", "連続突き", "二連斬り", "剣舞", "猟犬のステップ", 
        "霧の猛禽", "獣の咆哮", "構え", "回転撃", "巨人狩り", "嵐の刃", "嵐の襲撃", "嵐呼び", 
        "真空斬り", "共撃の幻", "王騎士の決意", "輝石のつぶて", "カーリアの大剣", "グレート・カーリア", 
        "回れ回れ", "ローレッタの斬撃", "暗黒波", "赤獅子の炎", "司教の突進", "黒炎の渦", "雷の羊", 
        "聖なる刃", "聖なる光輪", "聖律", "聖律共有", "黄金の地", "黄金の尻撃", "黄金樹に誓って", "無敵", 
        "血の斬撃", "血の徴収", "氷槍", "幻影の槍", "命奪拳", "暗殺の作法", "貫通射撃", 
        "連続射撃", "空撃ち", "宿し撃ち", "松明攻撃", "パリィ", "黄金パリィ", "嵐の壁", 
        "シールドバッシュ", "突撃バッシュ", "鉄壁の盾", "トープスの力場", "カーリアの返報"
    ],
    
    "固有戦技": [
        "輝石の彗礫", "レドゥビアの血刃", "黄金の刃", "死の刃", "黄金の剣技", "弔いの墓標", "眠りの霧", 
        "防ぎ得ぬ刃", "夜と炎の構え", "死蝋斬り", "ミエロスの絶叫", "オルドビスの渦", "白王の引力波", 
        "霊炎発火", "滅びの霊炎", "エオヒドの剣舞", "略奪の炎", "黄金律掲揚", "月光剣", "黄金波", 
        "狼の襲撃", "女王の黒炎", "復讐の誓い", "崩壊波", "星呼び", "運命の死", "王朝剣技", 
        "雷雲の姿", "溶岩撒き", "流体化", "星雲", "死のフレア", "猟犬の剣技", "黒王の斥力波", 
        "ザミェルの氷嵐", "溶岩ギロチン", "呪血の斬撃", "束の間の月影", "死屍累々", "氷雷剣", 
        "水鳥乱舞", "血刃乱舞", "雷嵐", "ローゼスの呼び声", "霊障招き", "地に伏せよ！", 
        "神託のシャボン", "流体化", "爪弾き", "百智の世界", "黄金砕き", "家族の怨霊", "星雲", 
        "降り注ぐシャボン", "噴き上がる信仰", "獣王の爪", "世界喰らい", "錫杖の魔術", 
        "黄金樹の尻撃", "神託の大シャボン", "車輪回転", "重力雷", "王の雄叫び", "聖槍の壁", 
        "槍呼びの儀", "古雷の槍", "大蛇狩り", "シルリアの渦", "狂い火突き", "血授の儀", 
        "回転斬り", "軍旗の下に", "ミケラの光輪", "天使の翼", "溶岩の海", "炎の舞", "嵐蹴撃", 
        "ご照覧あれい！", "ラダーンの驟雨", "火吹き", "眠りの炎", "毒蛇の噛みつき", 
        "黄金の返報", "伝染する怒り", "火炎舌", "炎の唾"
    ]
}

# 全リスト統合版も作成
SKILL_LISTS["ランダム(全種)"] = SKILL_LISTS["初期戦技"] + SKILL_LISTS["汎用戦技"] + SKILL_LISTS["固有戦技"]

# --- 2. 設定サイドバー ---
st.sidebar.title("設定 (7x7)")

# エリアごとの設定
# 距離0: 中心(1マス)
# 距離1: 内周(8マス)
# 距離2: 中周(16マス)
# 距離3: 外周(24マス)

rule_center = st.sidebar.selectbox("中心 (1マス)", list(SKILL_LISTS.keys()), index=0) # デフォルト: ストームルーラー
rule_inner  = st.sidebar.selectbox("内周 (8マス)", list(SKILL_LISTS.keys()), index=3) # デフォルト: 固有
rule_middle = st.sidebar.selectbox("中周 (16マス)", list(SKILL_LISTS.keys()), index=2) # デフォルト: 汎用
rule_outer  = st.sidebar.selectbox("外周 (24マス)", list(SKILL_LISTS.keys()), index=1) # デフォルト: 初期

# ルール辞書を作成
zone_rules = {
    0: rule_center,
    1: rule_inner,
    2: rule_middle,
    3: rule_outer
}

# --- 3. ロジック関数 ---

def generate_bingo_card_7x7():
    # 7x7の空カードを作成
    card = [[None for _ in range(7)] for _ in range(7)]
    
    # 距離ごとの座標リストを作成
    zones = {0: [], 1: [], 2: [], 3: []}
    
    for r in range(7):
        for c in range(7):
            # 中心(3,3)からの距離計算
            dist = max(abs(r - 3), abs(c - 3))
            zones[dist].append((r, c))
            
    # 各ゾーンごとに抽選して埋める
    for dist, coords in zones.items():
        list_name = zone_rules[dist]
        source_list = SKILL_LISTS[list_name]
        count_needed = len(coords)
        
        # リストの要素数が足りるかチェック
        if len(source_list) >= count_needed:
            # 足りるなら重複なしで抽出 (sample)
            selected_skills = random.sample(source_list, count_needed)
        else:
            # 足りない場合（例:外周にストームルーラー）は、あるだけ全部＋不足分をランダム重複 (choices)
            # ※ユーザーへの配慮として、エラーで止めずに埋める
            selected_skills = source_list[:] # コピー
            remainder = count_needed - len(source_list)
            selected_skills += random.choices(source_list, k=remainder)
            random.shuffle(selected_skills)
            
        # 座標に割り当て
        for (r, c), skill in zip(coords, selected_skills):
            card[r][c] = {"name": skill, "checked": False}
            
    return card

# --- 4. メイン画面 ---

st.title("ナイトレイン戦技ビンゴ")

# セッション管理
if "bingo_card" not in st.session_state:
    st.session_state.bingo_card = generate_bingo_card_7x7()

# 生成ボタン
if st.sidebar.button("ビンゴを生成/リセット", type="primary"):
    st.session_state.bingo_card = generate_bingo_card_7x7()
    st.rerun()

# グリッド描画 (7x7)
for r in range(7):
    cols = st.columns(7) # 7列
    for c in range(7):
        cell = st.session_state.bingo_card[r][c]
        
        if cell["checked"]:
            label = f"✅\n{cell['name']}"
            kind = "primary"
        else:
            label = f"\n{cell['name']}"
            kind = "secondary"

        # ボタンのキーをユニークにする
        if cols[c].button(label, key=f"btn_{r}_{c}", use_container_width=True, type=kind):
            st.session_state.bingo_card[r][c]["checked"] = not cell["checked"]
            st.rerun()

# 脚注
st.markdown("---")
st.caption(f"設定: 中心={rule_center} / 内周={rule_inner} / 中周={rule_middle} / 外周={rule_outer}")


