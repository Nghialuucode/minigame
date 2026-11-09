import json
from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Rút Gỗ Số", page_icon="🪵", layout="wide",
                   initial_sidebar_state="expanded")

# CSS tối ưu cho cả PC và Mobile
st.markdown(
    """<style>
    .block-container{padding:0 !important; max-width:100% !important;}
    header[data-testid="stHeader"]{display:none !important;}
    iframe{border-radius:0; border:none; display:block;}
    </style>""",
    unsafe_allow_html=True,
)

@st.cache_data(show_spinner=False)
def load_game_html() -> str:
    return (Path(__file__).parent / "game.html").read_text(encoding="utf-8")

ss = st.session_state
ss.setdefault("game_key", 0)
ss.setdefault("game_cfg", None)

# Tự động tạo cấu hình mặc định để chơi ngay lập tức (Không cần bấm Bắt đầu)
if ss.game_cfg is None:
    ss.game_cfg = {
        "players": ["Người chơi 1", "Người chơi 2", "Người chơi 3"],
        "layers": 12
    }

with st.sidebar:
    st.title("🪵 Rút Gỗ Số")
    st.caption("💡 Trên điện thoại, hãy bấm biểu tượng **>>** ở góc trên cùng bên trái để mở menu này.")
    
    with st.form("setup"):
        st.markdown("**Cấu hình ván mới**")
        default_players = "\n".join(ss.game_cfg["players"])
        raw = st.text_area("Người chơi (tối đa 8, mỗi dòng 1 tên)", default_players, height=110)
        layers = st.slider("Số tầng của tháp", 6, 18, ss.game_cfg["layers"])
        started = st.form_submit_button("🎮 Bắt đầu / Chơi lại", type="primary", use_container_width=True)

    if started:
        players = [p.strip() for p in raw.splitlines() if p.strip()][:8] or ["Người chơi 1"]
        ss.game_cfg = {"players": players, "layers": int(layers)}
        ss.game_key += 1

    st.divider()
    st.markdown("**🔊 Âm thanh** _(áp dụng ngay)_")
    sound_on = st.toggle("Bật âm thanh", True, key="snd_on")
    volume   = st.slider("Âm lượng", 0, 100, 70, key="vol")

    with st.expander("📖 Luật chơi"):
        st.markdown(
            "- Chọn khối bằng cách bấm lên khối hoặc nhập số.\n"
            "- Bấm **Rút gỗ** để rút. Khối rút ra sẽ biến mất và cộng điểm.\n"
            "- Không được rút khối ở tầng trên cùng.\n"
            "- Ai làm tháp đổ là người thua."
        )

cfg = {
    "players": ss.game_cfg["players"],
    "layers":  ss.game_cfg["layers"],
    "sound":   bool(sound_on),
    "volume":  max(0.0, min(1.0, volume / 100.0)),
}
cfg_json = json.dumps(cfg, ensure_ascii=False).replace("<", "\\u003c")
marker = f"<!-- game_key:{ss.game_key} -->\n"

# Load game
components.html(marker + load_game_html().replace("__CONFIG__", cfg_json), height=850, scrolling=False)

# Bridge gửi âm thanh từ Sidebar sang Game
bridge = f"""
<script>
(function() {{
  const msg = {{ type: "sound", on: {str(bool(sound_on)).lower()}, volume: {max(0.0, min(1.0, volume / 100.0))} }};
  function send() {{
    try {{
      const frames = window.parent.frames;
      for (let i = 0; i < frames.length; i++) {{
        try {{ frames[i].postMessage(msg, "*"); }} catch (e) {{}}
      }}
    }} catch (e) {{}}
  }}
  send(); setTimeout(send, 300); setTimeout(send, 1000);
}})();
</script>
"""
components.html(bridge, height=0, scrolling=False)