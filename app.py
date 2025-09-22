import time
import streamlit as st
from data import PROFILES, CATS, seed_news, extra_alerts_for_profile
from actions import (
    pick_profile, reset_profile, add_latest_alert, ensure_news_for_profile,
    expand_item, collapse_expanded
)
from ui import (
    profile_picker, sidebar_info, toolbar, render_news_list,
    chat_view, bottom_scroll_button
)
from chat import FAQS, answer_for

st.set_page_config(page_title="망고재배국 프로토타입", page_icon="🥭", layout="wide")
st.markdown("""
<style>
html { scroll-behavior: smooth; }
#top-anchor { position: relative; top: -200px; height: 0; }
</style>
<div id="top-anchor"></div>
""", unsafe_allow_html=True)

# 상태 기본값
if "profile" not in st.session_state: st.session_state.profile = None
if "view" not in st.session_state: st.session_state.view = "dashboard"
if "chat_history" not in st.session_state: st.session_state.chat_history = []
if "chat_show_suggests" not in st.session_state: st.session_state.chat_show_suggests = True

def open_chat():
    st.session_state.view = "chat"
    key = f"chat_init_for_{st.session_state.profile}"
    if not st.session_state.get(key):
        st.session_state.chat_history = [
            {"role": "assistant", "content": "안녕하세요! 무엇을 도와드릴까요? 아래 질문 중에서 선택해 보세요."}
        ]
        st.session_state.chat_show_suggests = True
        st.session_state[key] = True

def back_to_dashboard(): st.session_state.view = "dashboard"

if "chat_busy" not in st.session_state: st.session_state.chat_busy = False

def ask_quick(qid: str):
    if st.session_state.chat_busy:   # ▶ 이미 처리 중이면 무시
        return
    qtext = next(q["text"] for q in FAQS if q["id"] == qid)
    st.session_state.chat_history.append({"role": "user", "content": qtext})
    st.session_state.chat_pending = qid
    st.session_state.chat_busy = True  # ▶ 버튼 잠금

# 라우팅
if st.session_state.profile is None:
    profile_picker(PROFILES, on_pick=pick_profile)
else:
    ensure_news_for_profile(st.session_state.profile, seed_news, extra_alerts_for_profile)
    selected_cats = sidebar_info(PROFILES, st.session_state.profile, on_reset=reset_profile, cats=CATS)

    if st.session_state.view == "dashboard":
        toolbar(on_add_latest=add_latest_alert, on_open_chat=open_chat)

        if st.session_state.pop("alert_added", False): st.success("새 알림 1건이 추가되었습니다.")
        if st.session_state.pop("no_more_alerts", False): st.info("더 이상 표시할 새 뉴스가 없습니다.")

        render_news_list(
            st.session_state.news,
            selected_cats,
            expanded_id=st.session_state.get("expanded_id"),
            on_expand=expand_item,
            on_collapse=collapse_expanded
        )
        bottom_scroll_button(key="scroll_top_dash")

    else:
        # chat_view 호출부
        thinking_ph, _ = chat_view(
            chat_history=st.session_state.chat_history,
            faqs=FAQS,
            show_suggests=True,             # 항상 노출
            on_quick=ask_quick,
            on_back=back_to_dashboard,
            disabled=st.session_state.chat_busy,  # ▶ 비활성 상태 전달
        )
        if st.session_state.get("chat_pending") and not st.session_state.get("chat_processing"):
            st.session_state.chat_processing = True
            with thinking_ph.container():
                st.caption("🤖 챗봇이 답을 준비하고 있어요..."); time.sleep(1.0)
            ans = answer_for(st.session_state.profile, st.session_state.chat_pending)
            st.session_state.chat_history.append({"role":"assistant","content":ans})
            st.session_state.chat_history.append({"role":"assistant","content":"더 궁금한 점이 있으면 아래에서 선택해 주세요."})
            st.session_state.chat_pending = None
            st.session_state.chat_processing = False
            st.session_state.chat_busy = False   # ▶ 버튼 해제
            st.rerun()

