import streamlit as st
from google import genai

# ---------------------------------------------------------
# 1. ページ基本設定（ブランドアイデンティティの統一）
# ---------------------------------------------------------
st.set_page_config(
    page_title="AI薬機法コピーライター | Luxia",
    page_icon="🛡️",
    layout="centered"
)

# スタイル調整：表示バグを抑えるため複雑なCSSは排除し、最小限の装飾に留める
st.markdown("""
    <style>
    .stTextArea textarea { font-size: 1.1rem; }
    .report-card { border: 1px solid #e0e0e0; padding: 20px; border-radius: 10px; background-color: #f9f9f9; }
    </style>
""", unsafe_allow_html=True)

st.title("🛡️ AI薬機法コピーライター")
st.caption("Luxia AI Compliance Engine v3.0 | 2026 Stable Edition")

# ---------------------------------------------------------
# 2. セキュリティと設定（Secrets & Sidebar）
# ---------------------------------------------------------
try:
    # クラウド(Streamlit Secrets)またはローカル(.streamlit/secrets.toml)から取得
    raw_key = st.secrets.get("GEMINI_API_KEY", "")
    api_key = raw_key.strip() if raw_key else ""
except:
    api_key = ""

with st.sidebar:
    st.header("⚙️ システム設定")
    if not api_key:
        api_key = st.text_input("Gemini APIキーを入力", type="password").strip()
    
    category = st.selectbox(
        "商品区分を選択", 
        ["化粧品（スキンケア・ヘアケア）", "美容機器・雑貨", "健康食品"]
    )
    st.divider()
    st.info("提供：株式会社Luxia (2026)")
    st.caption("※画面が正常に動かない場合は、ブラウザの翻訳機能をオフにしてください。")

# ---------------------------------------------------------
# 3. メインロジック（入力・解析・出力）
# ---------------------------------------------------------
st.subheader("📝 原稿の入力")
input_text = st.text_area(
    "チェック・リライトしたい文章を入力してください",
    height=300,
    placeholder="例：この美容液でシミが消えて、肌が10歳若返ります！"
)

# 実行ボタン
if st.button("リーガルチェック＆リライトを実行", type="primary", use_container_width=True):
    if not api_key:
        st.error("APIキーが設定されていません。サイドバーを確認してください。")
    elif not input_text:
        st.warning("文章を入力してください。")
    else:
        # 最新の st.status で解析状況を可視化
        with st.status("AIが法規制（薬機法・景表法）を照合中...", expanded=True) as status:
            try:
                # 2026年最新のSDKクライアント初期化
                client = genai.Client(api_key=api_key)
                
                # 高倉様の「薬機法管理者」としてのロジックをプロンプトに凝縮
                sys_msg = f"""
                あなたは美容業界専門のリーガルコピーライターです。
                対象：{category}
                
                【指示】
                1. NG箇所の特定：医学的効能（治る、消える、若返る、浸透する等）を厳格に抽出せよ。
                2. リスクの解説：なぜ行政指摘のリスクがあるのか、薬機法・景表法の観点から論理的に説明せよ。
                3. 言い換え案（3パターン）：元の訴求力を維持しつつ、合法的な「攻め」の案を提示せよ。
                   - 【感性訴求】感情や体験（鏡を見るのが楽しくなる、等）
                   - 【事実訴求】物理的・成分的な事実（キメを整える、くすみを防ぐ、等）
                   - 【ベネフィット訴求】使用後の自信（自信が持てる肌へ、等）
                """
                
                # 最新・高速モデル gemini-2.0-flash を使用
                response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=input_text,
                    config={'system_instruction': sys_msg}
                )
                
                # 結果表示
                st.divider()
                st.subheader("📋 診断・リライトレポート")
                if response.text:
                    # st.write(response.text) は表示バグに最も強い
                    st.write(response.text)
                    status.update(label="解析が正常に完了しました！", state="complete")
                else:
                    st.error("AIからの回答が空でした。再度お試しください。")
                    status.update(label="エラー", state="error")
                
            except Exception as e:
                status.update(label="システムエラー発生", state="error")
                st.error("解析中に技術的な問題が発生しました。")
                st.code(str(e))

# ---------------------------------------------------------
# 4. フッター
# ---------------------------------------------------------
st.divider()
st.caption("© 2026 株式会社Luxia | Luxia AI Compliance System v3.0")