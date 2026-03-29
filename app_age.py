import streamlit as st
from google import genai

# 1. ページ基本設定
st.set_page_config(page_title="Luxia AI プレミアム診断", page_icon="🧬", layout="wide")

# 2. セキュリティ：裏側のSecretsからのみ取得
try:
    api_key = st.secrets["GEMINI_API_KEY"].strip()
except:
    st.error("システムエラー：ライセンス認証に失敗しました。管理者（株式会社Luxia）にお問い合わせください。")
    st.stop()

# サイドバー（ブランディングのみ）
with st.sidebar:
    st.header("🛡️ Luxia AI System")
    st.write("本システムは株式会社Luxiaのライセンスに基づき提供されています。")
    st.divider()
    st.caption("ver 3.5 (2026 Edition)")

st.title("🛡️ プレミアム体内年齢AI診断")
st.markdown("### 50項目の精密データ解析による「未来予測」レポート")

# --- 50問の設問データ定義（中略：前回と同じため省略せずフルで実装してください） ---
# [ここには前回お渡しした50問の辞書データとフォーム構築部分が入ります]

# --- フォーム・AI解析ロジック ---
# [中略：submit_btn のロジックへ]
if submit_btn:
    with st.status("AIがデータを精密解析中...", expanded=True) as status:
        try:
            # 顧客には見えない裏側のAPIキーを使用
            client = genai.Client(api_key=api_key, http_options={'api_version': 'v1'})
            
            # [中略：プロンプト構築と生成部分]
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=combined_prompt
            )
            
            st.divider()
            st.subheader("📋 超精密AI解析レポート")
            st.markdown(response.text)
            status.update(label="解析完了！", state="complete")
        except Exception as e:
            st.error("現在、アクセスが集中しています。しばらく経ってから再度お試しください。")
