import streamlit as st
from google import genai

# 1. ページ基本設定
st.set_page_config(
    page_title="Luxia AI プレミアム診断 | 2026 Edition",
    page_icon="🧬",
    layout="wide"
)

st.title("🛡️ プレミアム体内年齢AI診断")
st.markdown("### Gemini 2.0 Flash 高精度解析エンジン搭載")
st.caption("Produced by 株式会社Luxia | 2026 Anti-Aging Project")

# --- セキュリティ設定（Secrets優先、サイドバー予備） ---
try:
    raw_key = st.secrets.get("GEMINI_API_KEY", "")
    default_key = raw_key.strip() if raw_key else ""
except:
    default_key = ""

with st.sidebar:
    st.header("⚙️ システム設定")
    api_key_input = st.text_input("Gemini APIキー", value=default_key, type="password")
    api_key = api_key_input.strip()
    st.divider()
    st.info("提供：株式会社Luxia (2026)")
    st.caption("※最新のGemini 2.0エンジンを使用しています。")

# --- 50問の設問データ定義 ---
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

# --- フォーム構築 ---
with st.form("premium_diagnosis"):
    col_basic1, col_basic2 = st.columns(2)
    with col_basic1:
        real_age = st.number_input("お客さまの実年齢", min_value=18, max_value=100, value=30)
    with col_basic2:
        gender = st.selectbox("性別", ["女性", "男性"])

    st.divider()
    tabs = st.tabs(list(questions.keys()))
    user_answers = []

    for i, (category, q_list) in enumerate(questions.items()):
        with tabs[i]:
            st.markdown(f"#### {category}")
            for q in q_list:
                if st.checkbox(q, key=f"q_{i}_{q}"):
                    user_answers.append(q)

    st.divider()
    submit_btn = st.form_submit_button("Gemini 2.0 で精密解析を実行", type="primary", use_container_width=True)

# --- AI解析ロジック（Gemini 2.0 Flash 最適化版） ---
if submit_btn:
    if not api_key:
        st.error("APIキーが設定されていません。")
    else:
        with st.status("最新AIモデルが50項目を多角的に分析中...", expanded=True) as status:
            try:
                # 2.0対応のクライアント初期化
                client = genai.Client(api_key=api_key)
                
                checked_text = "\n".join([f"- {a}" for a in user_answers])
                
                # Gemini 2.0 の性能を最大化する高密度プロンプト
                sys_instruction = f"""
                あなたはアンチエイジング専門医、美容家、そして凄腕のサロン経営コンサルタントです。
                以下の顧客データから、科学的根拠に基づいた【体内年齢の算出】【詳細分析】【未来予測】【クロージング提言】を、
                一切の妥協なくプロフェッショナルなトーンで行ってください。

                ### 顧客データ
                - 実年齢：{real_age}歳 / 性別：{gender}
                - リスク項目（50問中{len(user_answers)}個）:
                {checked_text}

                ### 必須アウトプット項目（マークダウン形式）
                1. **現在の体内年齢**: 
                   項目数と深刻度（特に喫煙、糖質、睡眠不足）を独自のアルゴリズムで点数化し、実年齢との差を算出。
                2. **5つの指標別・リスク評価**: 
                   「食生活」「運動」「睡眠」「精神」「生活習慣」を5段階で評価し、老化の主因を特定。
                3. **衝撃の未来シミュレーション**: 
                   このまま5年過ごした場合の「老化の加速」と、ケア介入による「若返りの可能性」を数値で対比。
                4. **サロンオーナーへの戦略的提言**: 
                   この顧客の性格や傾向を推察し、美容機器・健康食品をどう提案すれば「即決」されるか、具体的なトークスクリプトを提示。
                """

                # Gemini 2.0 Flash を使用（configではなく最新の引数形式に合わせる）
                response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents="解析を開始してください。",
                    config={
                        'system_instruction': sys_instruction,
                        'temperature': 0.7
                    }
                )
                
                st.divider()
                st.subheader("📋 超精密AI解析レポート（Gemini 2.0）")
                if response.text:
                    st.markdown(response.text)
                    status.update(label="解析完了！クロージングフェーズへ移行してください。", state="complete")
                else:
                    st.error("AIからの回答が空でした。")
                
            except Exception as e:
                status.update(label="エラー発生", state="error")
                st.error("最新モデルの呼び出しに失敗しました。")
                st.code(str(e))

st.divider()
st.caption("© 2026 株式会社Luxia | 次世代AIカウンセリングシステム")
