"""Rút Gỗ Số - minigame Jenga có đánh số, chạy trên Streamlit."""

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


@st.cache_data(show_spinner=False)
def load_game_html() -> str:
    return (Path(__file__).parent / "game.html").read_text(encoding="utf-8")


ss = st.session_state
ss.setdefault("game_key", 0)
ss.setdefault("game_cfg", None)

# ================= SIDEBAR =================
with st.sidebar:
    st.title("🪵 Rút Gỗ Số")

    # ---- Cấu hình ván (reset ván khi áp dụng) ----
    with st.form("setup"):
        st.markdown("**Cấu hình ván mới**")
        raw = st.text_area("Người chơi (mỗi dòng một tên, tối đa 8)",
                           "An\nBình\nChi", height=110)
        layers = st.slider("Số tầng của tháp", 6, 18, 10,
                           help="Ít tầng hơn = tháp vững hơn.")
        started = st.form_submit_button("🎮 Bắt đầu / Chơi lại",
                                        type="primary", use_container_width=True)

    if started:
        players = [p.strip() for p in raw.splitlines() if p.strip()][:8] or ["Người chơi 1"]
        ss.game_cfg = {"players": players, "layers": int(layers)}
        ss.game_key += 1

    st.divider()

    # ---- Âm thanh: LIVE, áp dụng ngay không cần "Bắt đầu" ----
    st.markdown("**🔊 Âm thanh** _(áp dụng ngay)_")
    sound_on = st.toggle("Bật âm thanh", True, key="snd_on")
    volume   = st.slider("Âm lượng", 0, 100, 70, key="vol")

    with st.expander("📖 Luật chơi"):
        st.markdown(
            "- Mỗi khối gỗ có một số in trên mặt.\n"
            "- **Chọn khối**: bấm lên khối, bấm số ở *Bảng số*, hoặc nhập số.\n"
            "- Bấm **Rút gỗ** (hoặc đúp chuột vào khối) để rút.\n"
            "- **Khối rút ra biến mất** và cộng điểm — không xếp lại lên tháp.\n"
            "- Không được rút khối ở tầng trên cùng.\n"
            "- Ai làm tháp đổ là người thua.\n"
            "- Kéo chuột/ngón tay để xoay, lăn chuột / chụm 2 ngón để zoom."
        )

if ss.game_cfg is None:
    st.info("👈 Cấu hình ở thanh bên, sau đó bấm **Bắt đầu / Chơi lại**.")
    st.stop()

# ================= VÙNG GAME (iframe ổn định) =================
cfg = {
    "players": ss.game_cfg["players"],
    "layers":  ss.game_cfg["layers"],
    "sound":   bool(sound_on),
    "volume":  max(0.0, min(1.0, volume / 100.0)),
}
cfg_json = json.dumps(cfg, ensure_ascii=False).replace("<", "\\u003c")
marker = f"<!-- game_key:{ss.game_key} -->\n"

components.html(marker + load_game_html().replace("__CONFIG__", cfg_json),
                height=760, scrolling=False)

# ================= BRIDGE: sidebar -> iframe game =================
# iframe game đã có window message listener (xem game.html).
# Bridge này gửi trạng thái âm thanh mỗi lần Streamlit rerun.
bridge = f"""
<script>
(function() {{
  const msg = {{ type: "sound",
                on: {str(bool(sound_on)).lower()},
                volume: {max(0.0, min(1.0, volume / 100.0))} }};
  function send() {{
    try {{
      const frames = window.parent.frames;
      for (let i = 0; i < frames.length; i++) {{
        try {{ frames[i].postMessage(msg, "*"); }} catch (e) {{}}
      }}
    }} catch (e) {{}}
  }}
  send();
  setTimeout(send, 200); setTimeout(send, 800); setTimeout(send, 1800);
}})();
</script>
"""
components.html(bridge, height=0, scrolling=False)
