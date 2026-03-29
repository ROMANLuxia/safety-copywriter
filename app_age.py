import streamlit as st
from google import genai

# 1. ページ基本設定
st.set_page_config(page_title="プレミアム体内年齢AI診断 | Luxia", page_icon="🧬", layout="wide")

st.title("🛡️ プレミアム体内年齢AI診断")
st.markdown("### 50項目の精密解析による未来予測レポート")

# --- セキュリティ設定 ---
try:
    raw_key = st.secrets.get("GEMINI_API_KEY", "")
    api_key = raw_key.strip() if raw_key else ""
except:
    api_key = ""

# --- 設問データの定義（5カテゴリー×10問 = 50問） ---
questions = {
    "🍎 食生活・栄養": [
        "朝食を抜くことが多い", "甘いものやジュースを毎日摂る", "揚げ物や炒め物をよく食べる", "野菜を毎食食べない", 
        "食べるスピードが早い", "寝る3時間以内に食事をする", "お酒を毎日飲む", "インスタント食品をよく利用する",
        "タンパク質（肉・魚・卵）が不足している", "水を1日1.5L以上飲まない"
    ],
    "🏃 運動・代謝": [
        "1日の歩数が5000歩以下", "階段よりエスカレーターを使う", "週に1回も汗をかく運動をしない", "同じ姿勢でいる時間が長い",
        "昔に比べて太りやすくなった", "足腰が疲れやすい", "柔軟性が低い（体が硬い）", "姿勢が悪いと言われる",
        "手足が冷えやすい", "湯船に浸からずシャワーで済ませる"
    ],
    "💤 睡眠・休息": [
        "睡眠時間が6時間未満", "寝る直前までスマホを見ている", "夜中に何度も目が覚める", "朝起きた時に疲れが取れていない",
        "寝る時間がバラバラ", "昼間に強い眠気に襲われる", "休日に寝溜めをする", "寝室がリラックスできる環境でない",
        "いびきをかく、または眠りが浅い", "入浴から寝るまでの時間が短すぎる"
    ],
    "🧘 精神・ストレス": [
        "イライラすることが多い", "最近、趣味を楽しめていない", "自分を褒めることが少ない", "常に仕事や家事のことが頭にある",
        "リラックスできる時間が1日15分以下", "他人の目が気になりやすい", "決断力が落ちたと感じる", "不安を感じやすい",
        "笑う機会が減った", "呼吸が浅いと感じる"
    ],
    "🏠 生活・肌習慣": [
        "日焼け止めを毎日塗らない", "喫煙習慣がある（または副流煙）", "PC・スマホの画面を見る時間が1日5時間以上", "定期的な健康診断を受けていない",
        "実年齢より老けて見られることがある", "肌の乾燥やツヤのなさが気になる", "季節の変わり目に体調を崩しやすい", "毎日同じ生活の繰り返しだと感じる",
        "洗顔後に適切なスキンケアをしていない", "将来の健康に強い不安がある"
    ]
}

# --- フォームの構築 ---
with st.form("premium_diagnosis"):
    col_basic1, col_basic2 = st.columns(2)
    with col_basic1:
        real_age = st.number_input("実年齢", min_value=18, max_value=100, value=30)
    with col_basic2:
        gender = st.selectbox("性別", ["女性", "男性"])

    st.divider()
    st.info("以下の50項目にチェックを入れてください。チェックが多いほど体内年齢に影響します。")

    # タブでカテゴリーを分けてUIを整理
    tabs = st.tabs(list(questions.keys()))
    user_answers = []

    for i, (category, q_list) in enumerate(questions.items()):
        with tabs[i]:
            st.markdown(f"#### {category}")
            for q in q_list:
                ans = st.checkbox(q, key=q)
                if ans:
                    user_answers.append(q)

    st.divider()
    submit_btn = st.form_submit_button("50項目から精密診断を実行", type="primary", use_container_width=True)

# --- AI解析ロジック ---
if submit_btn:
    if not api_key:
        st.error("APIキーが設定されていません。")
    else:
        with st.status("50項目のビッグデータを解析中...", expanded=True) as status:
            try:
                client = genai.Client(api_key=api_key)
                
                # 選択された項目をリスト化
                checked_list = "\n".join([f"- {a}" for a in user_answers])
                
                sys_msg = f"""
                あなたはアンチエイジング専門医、美容家、そして経営コンサルタントの3つの顔を持つAIです。
                実年齢：{real_age}歳（{gender}）
                【チェックされたリスク項目（50問中{len(user_answers)}個）】:
                {checked_list}
                
                【指示】
                1. 現在の体内年齢の算出：
                   - 0〜5個：実年齢-3歳〜±0歳
                   - 6〜15個：実年齢+3〜5歳
                   - 16〜30個：実年齢+6〜10歳
                   - 31個以上：実年齢+11〜20歳
                   上記を基準にしつつ、各項目の深刻度を考慮して精密な数値を出すこと。
                2. 分析レポート：
                   「食生活」「代謝」「睡眠」「メンタル」「生活習慣」の5つの観点から、なぜその年齢になったのかを専門的に解説せよ。
                3. 未来予測：
                   このまま50のリスクを放置した場合の5年後の体内年齢と、今サロンケア（機器・化粧品・サプリ）を取り入れた場合の5年後の体内年齢を数値で比較せよ。
                4. サロンオーナー向け：
                   この顧客のチェック傾向から、どの商品（美容機器、導入液、サプリ）を勧めるべきか、最強のクロージングトークを提案せよ。
                """
                
                response = client.models.generate_content(
                    model="gemini-1.5-flash",
                    contents="50項目のデータを元に精密診断を行ってください。",
                    config={'system_instruction': sys_msg}
                )
                
                st.divider()
                st.subheader("📋 超精密AI解析レポート")
                st.markdown(response.text)
                status.update(label="全ての解析が完了しました", state="complete")
                
            except Exception as e:
                status.update(label="エラー発生", state="error")
                st.error("解析に失敗しました。")
                st.code(str(e))