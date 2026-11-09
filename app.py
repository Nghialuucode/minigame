"""Rút Gỗ Số - minigame Jenga có đánh số, chạy trên Streamlit.

Phần game (Three.js + cannon.js) nằm trong game.html và được nhúng qua
components.html, nên không cần cài thêm thư viện Python nào ngoài streamlit.
"""
import json
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Rút Gỗ Số", page_icon="🪵", layout="wide",
                   initial_sidebar_state="expanded")

st.markdown(
    """<style>
    .block-container{padding-top:1.2rem;padding-bottom:0;max-width:1400px}
    header[data-testid="stHeader"]{background:transparent}
    iframe{border-radius:18px;border:1px solid rgba(255,255,255,.08)}
    </style>""",
    unsafe_allow_html=True,
)

with st.sidebar:
    st.title("🪵 Rút Gỗ Số")
    raw = st.text_area("Người chơi (mỗi dòng một tên, tối đa 8)", "An\nBình\nChi", height=110)
    layers = st.slider("Số tầng của tháp", 6, 18, 12,
                       help="Nhiều tầng = nhiều khối hơn, vật lý nặng hơn trên máy yếu.")
    sound = st.toggle("Âm thanh", True)
    volume = st.slider("Âm lượng", 0, 100, 70)
    with st.expander("Luật chơi"):
        st.markdown(
            "- Mỗi khối gỗ có một số in trên mặt.\n"
            "- **Chọn khối**: bấm thẳng lên khối gỗ, hoặc bấm số ở *Bảng số*, hoặc nhập số.\n"
            "- Bấm **Rút gỗ** (hoặc bấm đúp vào khối) để rút.\n"
            "- Khối rút xong được xếp lên đỉnh tháp, rồi đến lượt người kế tiếp.\n"
            "- Không được rút khối ở tầng trên cùng.\n"
            "- Ai làm tháp đổ là người thua.\n"
            "- Kéo chuột/ngón tay để xoay, lăn chuột hoặc chụm hai ngón để zoom."
        )

players = [p.strip() for p in raw.splitlines() if p.strip()][:8] or ["Người chơi 1"]
cfg = {"players": players, "layers": layers, "sound": sound, "volume": volume / 100}

html = (Path(__file__).parent / "game.html").read_text(encoding="utf-8")
cfg_json = json.dumps(cfg, ensure_ascii=False).replace("<", "\\u003c")
components.html(html.replace("__CONFIG__", cfg_json), height=760, scrolling=False)
