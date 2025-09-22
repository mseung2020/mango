import streamlit as st

# ------- 공통 UI -------
def profile_picker(profiles, on_pick):
    st.title("프로필을 선택하세요")
    st.caption("개인화된 대시보드 데모를 위해 임의의 프로필을 고릅니다.")
    cols = st.columns(3)
    for col, p in zip(cols, profiles):
        with col:
            st.markdown(f"### {p['icon']} {p['name']}")
            st.caption(p["desc"])
            st.button("선택", key=f"pick_{p['id']}", use_container_width=True,
                      on_click=on_pick, args=(p["id"],),)

def sidebar_info(profiles, profile_id, on_reset, cats):
    cur = next(p for p in profiles if p["id"] == profile_id)
    st.sidebar.subheader("현재 프로필")
    st.sidebar.write(f"{cur['icon']} **{cur['name']}**")
    st.sidebar.caption(cur["desc"])
    st.sidebar.button("프로필 변경", on_click=on_reset, use_container_width=True)

    st.sidebar.markdown("---")
    st.sidebar.subheader("필터")

    # Clear all 아이콘 숨김
    st.sidebar.markdown(
        '<style>.stMultiSelect [aria-label="Clear all"]{display:none!important;}</style>',
        unsafe_allow_html=True
    )

    # 리비전 키 (위젯 강제 재생성용)
    if "_filters_rev" not in st.session_state:
        st.session_state._filters_rev = 0

    # 초기화 버튼을 위젯 생성 전에 배치
    st.sidebar.button(
        "필터 초기화", use_container_width=True,
        on_click=lambda: st.session_state.update({"_filters_rev": st.session_state._filters_rev + 1})
    )

    # 멀티셀렉트: 초기 상태는 '선택 없음'
    ms_key = f"selected_cats_{st.session_state._filters_rev}"
    selected = st.sidebar.multiselect(
        "카테고리 (선택 없으면 전체 표시)", cats,
        default=[], key=ms_key
    )

    # 선택 없으면 전체 표시
    active = set(selected) if selected else set(cats)
    return active


def toolbar(on_add_latest, on_open_chat):
    left, right = st.columns([1, 1])
    with left:
        st.subheader("대시보드")
    with right:
        col1, col2 = st.columns(2)
        with col1:
            st.button("🔔 최신 알림 받기", use_container_width=True, on_click=on_add_latest)
        with col2:
            st.button("💬 챗봇 열기", use_container_width=True, on_click=on_open_chat)

# 배지용 CSS 1회 주입
def _inject_badge_css():
    st.markdown("""
    <style>
    .pill{display:inline-block;padding:2px 8px;border-radius:999px;
          font-size:12px;line-height:18px;margin-right:6px;}
    .pill-ok{background:#1f9d55;color:#fff;}
    .pill-warn{background:#d97706;color:#fff;}
    .pill-muted{background:#4b5563;color:#e5e7eb;}
    </style>
    """, unsafe_allow_html=True)

def _label_class(label:str)->str:
    return "pill-ok" if label=="확정" else ("pill-warn" if label=="추정" else "pill-muted")

def render_card(item, expanded_id=None, on_expand=None, on_collapse=None):
    _inject_badge_css()
    is_expanded = (expanded_id == item["id"])
    box = st.container(border=True)
    with box:
        tcol1, tcol2 = st.columns([6,1])
        with tcol1:
            st.markdown(f"**📅 {item['when']} · [{item['cat']}] {item['title']}**")
        with tcol2:
            if is_expanded:
                st.button("닫기", key=f"close_{item['id']}", use_container_width=True,
                          on_click=on_collapse)
            else:
                st.button("자세히", key=f"more_{item['id']}", use_container_width=True,
                          on_click=on_expand, args=(item["id"],))

        # 본문/배지
        if is_expanded:
            st.write(item["desc"])
            st.markdown(
                f"<span class='pill {_label_class(item.get('label','보류'))}'>{item.get('label','보류')}</span>"
                f"<span class='pill pill-muted'>갱신 {item.get('updated','-')}</span>",
                unsafe_allow_html=True
            )
            # 출처 링크(선택)
            if item.get("source"):
                st.markdown(f"[출처 보기]({item['source']})")
        else:
            st.caption(item["desc"])
            label = item.get("label","보류")
            updated = item.get("updated","-")
            new_badge = "<span class='pill pill-muted'>NEW</span>" if item.get("is_new") else ""
            st.markdown(
                f"<span class='pill {_label_class(label)}'>{label}</span>"
                f"<span class='pill pill-muted'>갱신 {updated}</span>"
                f"{new_badge}",
                unsafe_allow_html=True
            )

def render_news_list(news, selected_cats, expanded_id=None, on_expand=None, on_collapse=None):
    for it in [n for n in news if n["cat"] in selected_cats]:
        render_card(it, expanded_id=expanded_id, on_expand=on_expand, on_collapse=on_collapse)


# 하단 ‘맨 위로’
def bottom_scroll_button(key: str):
    st.markdown("")
    cols = st.columns([8, 2])
    with cols[1]:
        st.markdown(
            f"""
            <a href="#top-anchor" id="{key}" style="
                display:inline-block;width:100%;text-align:center;padding:8px 0;
                border:1px solid rgba(0,0,0,0.12);border-radius:6px;
                background:#2b2f3a;color:inherit;text-decoration:none;">
                ▲ 맨 위로
            </a>
            """,
            unsafe_allow_html=True
        )

# ---- 상세 패널(모달 느낌) ----
def render_detail_modal(item: dict, on_close):
    _inject_badge_css()
    st.markdown("### 상세 보기")
    c = st.container(border=True)
    with c:
        st.markdown(f"**{item['title']}**")
        st.caption(f"{item['when']} · [{item['cat']}]")
        st.markdown(
            f'<span class="pill {_label_class(item.get("label","보류"))}">{item.get("label","보류")}</span>'
            f'<span class="pill pill-muted">갱신 {item.get("updated","-")}</span>',
            unsafe_allow_html=True
        )
        st.write(item.get("desc",""))
        st.write(f"출처: {item.get('source','-')}")
        st.button("닫기", on_click=on_close, use_container_width=True)

# ---------------- CHAT ----------------
def chat_view(chat_history, faqs, show_suggests, on_quick, on_back, disabled=False):
    # 흐림 효과 CSS
    st.markdown("<style>.dimmed{opacity:.5;filter:grayscale(20%);} </style>", unsafe_allow_html=True)

    st.button("← 대시보드로 돌아가기", key="back_to_dash", on_click=on_back)
    st.markdown("### 챗봇")

    for m in chat_history:
        with st.chat_message("assistant" if m["role"] == "assistant" else "user"):
            st.markdown(m["content"])

    thinking_ph = st.empty()

    if show_suggests:
        st.markdown("##### 자주 묻는 질문")
        # ✅ 같은 컨테이너 안에서 <div> 열고 닫기까지 모두 처리
        with st.container():
            if disabled:
                st.markdown('<div class="dimmed">', unsafe_allow_html=True)

            cols = st.columns(len(faqs))
            for col, q in zip(cols, faqs):
                with col:
                    st.button(
                        q["text"],
                        key=f"faq_{q['id']}",
                        on_click=on_quick,
                        args=(q["id"],),
                        use_container_width=True,
                        disabled=disabled,
                    )

            if disabled:
                st.markdown("</div>", unsafe_allow_html=True)

        bottom_scroll_button(key="scroll_top_chat")

    return thinking_ph, False
