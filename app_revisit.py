import streamlit as st
from google import genai
from datetime import datetime

# 1. ページ基本設定
st.set_page_config(
    page_title="Luxia LTV Booster | 顧客呼び戻しシステム",
    page_icon="📈",
    layout="wide"
)

# 2. セキュリティ：裏側のSecretsから取得（ブラックボックス仕様）
try:
    api_key = st.secrets["GEMINI_API_KEY"].strip()
except Exception:
    st.error("ライセンス認証エラー：管理者（株式会社Luxia）へお問い合わせください。")
    st.stop()

# 3. ブランディング（サイドバー）
with st.sidebar:
    st.header("📈 Luxia LTV Booster")
    st.write("眠れる既存顧客を再活性化し、売上を最大化する。")
    st.divider()
    st.info("Produced by 株式会社Luxia (2026)")
    st.caption("ver 1.5 | 顧客離脱防止エンジン搭載")

st.title("📈 顧客呼び戻し＆LINE生成システム")
st.markdown("### 「失客」を「再来店」に変えるAIメッセージ作成ツール")

# 4. 顧客データ入力フォーム
with st.form("customer_data_form"):
    st.subheader("👤 ターゲット顧客の情報")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        name = st.text_input("顧客名（苗字のみ可）", placeholder="例：高倉様")
        last_visit = st.date_input("最終来店日", value=datetime(2026, 1, 15))
    with col2:
        frequency = st.number_input("通算来店回数", min_value=1, value=3)
        last_menu = st.text_input("前回の施術メニュー", placeholder="例：ハイドラフェイシャル")
    with col3:
        customer_note = st.text_area("顧客の特徴・会話内容", placeholder="例：乾燥肌を気にしていた。来月旅行に行くと言っていた。")

    st.divider()
    st.subheader("🎁 今回のオファー（特典）")
    offer = st.text_input("再来店特典", placeholder="例：ROMANローションのサンプル進呈、10%OFFなど")
    
    submit_btn = st.form_submit_button("離脱リスク解析 ＆ LINE文章生成", type="primary", use_container_width=True)

# 5. 解析実行ロジック
if submit_btn:
    # 離脱日数の計算
    days_since_last = (datetime.now().date() - last_visit).days
    
    # リスク判定
    if days_since_last > 90:
        risk_status = "🚨 離脱警告（休眠状態）"
        risk_color = "red"
    elif days_since_last > 45:
        risk_status = "⚠️ 要注意（離脱リスク高）"
        risk_color = "orange"
    else:
        risk_status = "✅ 良好（安定顧客）"
        risk_color = "green"

    with st.status("AIが顧客心理を分析し、最適な文面を構築中...", expanded=True) as status:
        try:
            # クライアント初期化（安定版 v1 パス）
            client = genai.Client(api_key=api_key, http_options={'api_version': 'v1'})
            
            # 心理学に基づいたプロンプト統合方式
            revisit_prompt = f"""
            あなたは凄腕のサロンコンサルタント兼コピーライターです。
            長期間来店が途絶えている顧客に対し、思わず「また行こうかな」と思わせる、
            優しさとプロの気遣いが詰まったLINEメッセージを作成してください。

            ### 顧客データ
            - 名前：{name}
            - 最終来店から：{days_since_last}日経過
            - 来店回数：{frequency}回
            - 前回の施術：{last_menu}
            - 特徴メモ：{customer_note}
            - 今回のオファー：{offer}

            ### 出力項目
            1. 離脱原因の推測（サロンオーナー向け解説）
            2. LINE送信用テキスト案（コピー＆ペースト用）
            3. 送信のアドバイス（タイミング等）

            ### LINE文章のポイント
            - 冒頭で{last_menu}後の状態を気遣う。
            - {customer_note}のエピソードを盛り込み、「あなた専用」感を出す。
            - {offer}を魅力的に伝える。
            - 押し売り感を消し、プロとしての「アフターフォロー」の体裁を保つ。
            """

            # Gemini 2.0 Flash で生成
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=revisit_prompt
            )
            
            # 結果表示
            st.divider()
            st.markdown(f"### 📊 診断結果: <span style='color:{risk_color}'>{risk_status}</span>", unsafe_allow_html=True)
            st.info(f"最終来店から **{days_since_last}日** が経過しています。")
            
            if response.text:
                st.markdown("### 📱 AI生成レポート ＆ LINE案")
                st.write(response.text)
                status.update(label="文章生成が完了しました！", state="complete")
            else:
                st.error("AIからの回答が空でした。再度お試しください。")

        except Exception as e:
            status.update(label="システムエラー発生", state="error")
            st.error("解析中に問題が発生しました。")
            st.code(str(e))

st.divider()
st.caption("© 2026 株式会社Luxia | サロンのLTV最大化を支援するAIシステム")
