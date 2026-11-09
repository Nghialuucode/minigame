import json
from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Rút Gỗ Số", page_icon="🪵", layout="centered", initial_sidebar_state="collapsed")

# CSS ép iframe tự động co giãn vừa khít 100% màn hình điện thoại (100dvh)
st.markdown(
    """<style>
    .block-container {padding: 0 !important; max-width: 100% !important;}
    header[data-testid="stHeader"] {display: none !important;}
    iframe[title="streamlit_component"] {
        width: 100% !important;
        height: 100dvh !important; 
        border: none;
        display: block;
    }
    div[data-testid="stExpander"] { margin: 10px; background: #10131b; border-radius: 12px;}
    </style>""",
    unsafe_allow_html=True,
)

@st.cache_data(show_spinner=False)
def load_game_html() -> str:
    return (Path(__file__).parent / "game.html").read_text(encoding="utf-8")

ss = st.session_state
ss.setdefault("game_key", 0)
ss.setdefault("game_cfg", {"players": ["Người chơi 1", "Người chơi 2", "Người chơi 3"], "layers": 12})
ss.setdefault("sound_on", True)
ss.setdefault("volume", 70)

# Cấu hình hiển thị trên cùng
with st.expander("⚙️ Cấu hình ván chơi", expanded=False):
    with st.form("setup"):
        raw = st.text_area("Người chơi (tối đa 8, mỗi dòng 1 tên)", "\n".join(ss.game_cfg["players"]), height=100)
        layers = st.slider("Số tầng của tháp", 6, 18, ss.game_cfg["layers"])
        
        st.markdown("**🔊 Âm thanh**")
        col1, col2 = st.columns([1, 2])
        with col1:
            sound_on = st.toggle("Bật", value=ss.sound_on)
        with col2:
            volume = st.slider("Âm lượng", 0, 100, ss.volume, label_visibility="collapsed")
            
        started = st.form_submit_button("🎮 Bắt đầu / Chơi lại", type="primary", use_container_width=True)

    if started:
        players = [p.strip() for p in raw.splitlines() if p.strip()][:8] or ["Người chơi 1"]
        ss.game_cfg = {"players": players, "layers": int(layers)}
        ss.sound_on = sound_on
        ss.volume = volume
        ss.game_key += 1
    else:
        ss.sound_on = sound_on
        ss.volume = volume

# Chuẩn bị dữ liệu game
cfg = {
    "players": ss.game_cfg["players"],
    "layers":  ss.game_cfg["layers"],
    "sound":   bool(ss.sound_on),
    "volume":  max(0.0, min(1.0, ss.volume / 100.0)),
}
cfg_json = json.dumps(cfg, ensure_ascii=False).replace("<", "\\u003c")
marker = f"<!-- game_key:{ss.game_key} -->\n"

# Load game
components.html(marker + load_game_html().replace("__CONFIG__", cfg_json), height=700, scrolling=False)

# Bridge gửi âm thanh từ Streamlit sang Game
bridge = f"""
<script>
(function() {{
  const msg = {{ type: "sound", on: {str(bool(ss.sound_on)).lower()}, volume: {max(0.0, min(1.0, ss.volume / 100.0))} }};
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
