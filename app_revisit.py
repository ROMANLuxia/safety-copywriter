import streamlit as st
from google import genai
from datetime import datetime

# 1. ページ基本設定
st.set_page_config(page_title="Luxia LTV Booster | 再来店予測", page_icon="📈", layout="wide")

st.title("📈 顧客呼び戻し＆LINE生成システム")
st.markdown("### 眠れる資産（既存顧客）を再活性化し、LTVを最大化する")
st.caption("Produced by 株式会社Luxia | 2026 Customer Success Tool")

# --- セキュリティ設定 ---
try:
    raw_key = st.secrets.get("GEMINI_API_KEY", "")
    default_key = raw_key.strip() if raw_key else ""
except:
    default_key = ""

with st.sidebar:
    st.header("⚙️ 設定")
    api_key = st.text_input("Gemini APIキー", value=default_key, type="password").strip()
    st.divider()
    st.info("このツールはサロン専用の『休眠客掘り起こし』特化型AIです。")

# --- 2. 顧客データ入力（簡易版：現場で即入力可能な設計） ---
with st.form("customer_data"):
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

# --- 3. 解析ロジック ---
if submit_btn:
    if not api_key:
        st.error("APIキーが設定されていません。")
    else:
        # 離脱日数の計算
        days_since_last = (datetime.now().date() - last_visit).days
        
        # リスク判定（サロン業界の標準的なRFM指標をベースに）
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
                # 安定版 v1 パスを指定
                client = genai.Client(api_key=api_key, http_options={'api_version': 'v1'})
                
                # 心理学に基づいた再来促しプロンプト
                prompt = f"""
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

                ### 指示
                1. 冒頭：久しぶりの連絡であることを詫びつつ、{last_menu}後の状態を気遣う一言。
                2. 本文：{customer_note}に基づいた「あなただけのことを覚えています」というパーソナルなエピソードを挿入。
                3. 提案：現在の季節やトレンド（例：3月末なら花粉や紫外線）に合わせた、{name}に必要なケアの重要性を説く。
                4. 特典：{offer}をさりげなく提示。
                5. 締め：予約を強要せず、「相談だけでもお気軽に」というスタンス。
                6. トーン：親しみやすくも礼儀正しい。

                ### 出力形式
                - 離脱原因の推測（サロンオーナー向け）
                - LINE送信用テキスト（コピー＆ペースト用）
                - 送信のベストタイミング（例：土曜の午前中など）
                """

                response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=prompt
                )
                
                # 結果表示
                st.divider()
                st.markdown(f"### 📊 診断結果: <span style='color:{risk_color}'>{risk_status}</span>", unsafe_allow_html=True)
                st.info(f"最終来店から **{days_since_last}日** が経過しています。")
                
                if response.text:
                    st.markdown("### 📱 生成されたLINEメッセージ案")
                    st.write(response.text)
                    status.update(label="解析と文章生成が完了しました！", state="complete")
                
            except Exception as e:
                status.update(label="エラー発生", state="error")
                st.error("解析に失敗しました。")
                st.code(str(e))

st.divider()
st.caption("© 2026 株式会社Luxia | サロンのLTV最大化を支援するAI")