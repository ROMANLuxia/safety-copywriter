import streamlit as st
from google import genai

# 1. ページ基本設定
st.set_page_config(page_title="Luxia AI プレミアム診断", page_icon="🧬", layout="wide")

# 2. セキュリティ：裏側のSecretsから取得
try:
    # 画面には出さないブラックボックス仕様
    api_key = st.secrets["GEMINI_API_KEY"].strip()
except Exception:
    st.error("ライセンス認証エラー：管理者（株式会社Luxia）へお問い合わせください。")
    st.stop()

# 3. ブランディング（サイドバー）
with st.sidebar:
    st.header("🛡️ Luxia AI System")
    st.write("本システムは株式会社Luxiaのライセンスに基づき、正規導入サロン様へ提供されています。")
    st.divider()
    st.caption("ver 3.5 | 2026 Edition")
    st.info("※ブラウザの自動翻訳機能をオフにしてご使用ください。")

st.title("🧬 プレミアム体内年齢AI診断")
st.markdown("### 50項目の精密解析による「未来予測」レポート")

# 4. 50問の設問データ
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

# 5. 入力フォームの構築
with st.form("premium_diagnosis_form"):
    col_basic1, col_basic2 = st.columns(2)
    with col_basic1:
        real_age = st.number_input("実年齢", min_value=18, max_value=100, value=30)
    with col_basic2:
        gender = st.selectbox("性別", ["女性", "男性"])

    st.divider()
    tabs = st.tabs(list(questions.keys()))
    user_answers = []

    for i, (category, q_list) in enumerate(questions.items()):
        with tabs[i]:
            st.markdown(f"#### {category}")
            for q in q_list:
                # 設問にチェックが入ればリストに追加
                if st.checkbox(q, key=f"q_{i}_{q}"):
                    user_answers.append(q)

    st.divider()
    # ここで submit_btn を定義（これより下で if submit_btn を使う）
    submit_btn = st.form_submit_button("精密AI診断を実行（約10秒）", type="primary", use_container_width=True)

# 6. 解析実行（ボタンが押された後の処理）
if submit_btn:
    with st.status("Gemini 2.0 が50項目のビッグデータを解析中...", expanded=True) as status:
        try:
            # クライアント初期化（安定版 v1 パス）
            client = genai.Client(api_key=api_key, http_options={'api_version': 'v1'})
            
            checked_text = "\n".join([f"- {a}" for a in user_answers])
            
            # 高密度プロンプト（システム命令をメインに統合してエラー回避）
            analysis_prompt = f"""
            あなたはアンチエイジング専門医、美容家、そして凄腕のサロンコンサルタントです。
            以下の顧客データから、【体内年齢の算出】【詳細分析】【未来予測】【クロージング提言】を行ってください。

            ### 顧客データ
            - 実年齢：{real_age}歳
            - 性別：{gender}
            - 50項目中のリスク該当数：{len(user_answers)}個
            - 具体的なリスク項目:
            {checked_text}

            ### 回答の構成（プロフェッショナルなトーンで）
            1. **現在の体内年齢**: 科学的根拠を感じさせる具体的な数値を算出。
            2. **リスク分析**: なぜその結果になったのか、5つの観点から専門的に解説。
            3. **未来予測シミュレーション**: 現状維持 vs ケア開始後の5年後を比較。
            4. **サロンオーナーへの提言**: この顧客に「美容機器」「健康食品」「導入液」のどれを、どう提案すべきか。
            """

            # 解析実行
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=analysis_prompt
            )
            
            st.divider()
            st.subheader("📋 超精密AI解析レポート")
            if response.text:
                st.markdown(response.text)
                status.update(label="解析完了！お客様への解説を開始してください。", state="complete")
            else:
                st.error("AIからの回答が空でした。再度実行してください。")

        except Exception as e:
            status.update(label="システムエラー発生", state="error")
            st.error("解析に失敗しました。管理者へ連絡してください。")
            st.code(str(e))

st.divider()
st.caption("© 2026 株式会社Luxia | 次世代AIカウンセリングシステム")
