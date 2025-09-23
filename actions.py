import streamlit as st
from datetime import datetime
import uuid

def _clear_state(preserve_profile: bool):
    st.session_state.view = "dashboard"
    for k in ["alert_added","no_more_alerts","remaining_alerts","news_profile","news",
              "chat_history","chat_pending","chat_processing","chat_show_suggests",
              "detail_item","expanded_id","_filters_rev"]:
        st.session_state.pop(k, None)
    # 동적으로 만든 멀티셀렉트 키들도 제거
    for k in list(st.session_state.keys()):
        if isinstance(k, str) and k.startswith("selected_cats_"):
            del st.session_state[k]
    if not preserve_profile and "profile" in st.session_state:
        del st.session_state["profile"]

def reset_profile():
    _clear_state(preserve_profile=False)

def pick_profile(pid: str):
    _clear_state(preserve_profile=True)
    st.session_state.profile = pid

def ensure_news_for_profile(profile_id: str, seed_fn, extra_fn):
    if "news_profile" not in st.session_state or st.session_state.news_profile != profile_id:
        st.session_state.news = seed_fn(profile_id)
        st.session_state.remaining_alerts = extra_fn(profile_id)
        st.session_state.news_profile = profile_id

def add_latest_alert():
    remain = st.session_state.get("remaining_alerts", [])
    if remain:
        tpl = remain.pop(0)
        item = {
            "id": str(uuid.uuid4()),
            "when": "방금 전",
            "title": tpl["title"],
            "cat": tpl["cat"],
            "desc": tpl["desc"],
            "detail": tpl.get("detail"),   # ✅ detail 전달
            "label": tpl.get("label","확정"),
            "updated": datetime.utcnow().strftime("%Y-%m-%d %H:%M"),
            "source": tpl.get("source","https://news.example/new"),
            "is_new": True,
            "ts": datetime.utcnow().timestamp() + 1,
        }
        st.session_state.news.insert(0, item)
        st.session_state.alert_added = True
    else:
        st.session_state.no_more_alerts = True


# ▼ 인라인 확장 제어
def expand_item(item_id: str):
    st.session_state.expanded_id = item_id

def collapse_expanded():
    if "expanded_id" in st.session_state:
        del st.session_state["expanded_id"]
