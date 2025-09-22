from datetime import datetime, timedelta
import uuid

def _now_str():
    return datetime.utcnow().strftime("%Y-%m-%d %H:%M")

PROFILES = [
    {"id": "ev1", "name": "EV 사용자 A", "desc": "전기차 1 모델 이용자", "icon": "🚗"},
    {"id": "ev2", "name": "EV 사용자 B", "desc": "전기차 2 모델 이용자", "icon": "⚡"},
    {"id": "ev3", "name": "EV 사고 경험자", "desc": "사고 이력 기반 코칭 강화", "icon": "🧯"},
]

CATS = ["사고", "기술", "기타"]

def seed_news(profile_id: str):
    prefix = {"ev1": "[A]", "ev2": "[B]", "ev3": "[사고]"}[profile_id]
    base = datetime.utcnow()
    data = [
        {"when": "3일 전",   "title": f"{prefix} 급속충전 중 온도 상승 이슈", "cat": "사고",
         "desc": "특정 구간에서 충전 중 온도 상승 보고.", "label": "추정", "updated": _now_str(),
         "source": "https://news.example/ev-heat"},
        {"when": "10일 전",  "title": f"{prefix} BMS 업데이트 권고", "cat": "기술",
         "desc": "성능 개선 및 안전 패치 포함.", "label": "보류",
         "updated": (base - timedelta(days=1)).strftime("%Y-%m-%d %H:%M"),
         "source": "https://news.example/bms-update"},
        {"when": "1개월 전", "title": f"{prefix} 배터리 냉각 개선 사례", "cat": "기술",
         "desc": "열관리 개선으로 효율 상승.", "label": "추정",
         "updated": (base - timedelta(days=8)).strftime("%Y-%m-%d %H:%M"),
         "source": "https://news.example/cooling-case"},
        {"when": "2개월 전", "title": f"{prefix} 충전소 점검 캠페인", "cat": "기타",
         "desc": "일부 변압기 점검 안내.", "label": "확정",
         "updated": (base - timedelta(days=35)).strftime("%Y-%m-%d %H:%M"),
         "source": "https://news.example/site-check"},
    ]
    out = []
    ts = base.timestamp()
    for d in data:
        d["id"] = str(uuid.uuid4())
        d["is_new"] = False
        d["ts"] = ts
        out.append(d)
    return out

_EXTRA = {
    "ev1": [
        {"title": "급속충전 커넥터 접점 점검 권고", "cat": "사고", "desc": "접점 과열 가능성. 서비스 센터 무상 점검.",
         "label": "확정", "source": "https://news.example/connector"},
        {"title": "신규 BMS 핫픽스 배포", "cat": "기술", "desc": "셀 밸런싱 로직 보정 포함.",
         "label": "확정", "source": "https://news.example/bms-hotfix"},
    ],
    "ev2": [
        {"title": "도심 충전소 화재 예방 점검", "cat": "사고", "desc": "일부 구간 야간 점검 예정.",
         "label": "보류", "source": "https://news.example/city-prevent"},
        {"title": "열관리 펌웨어 업데이트", "cat": "기술", "desc": "고온 구간 보호 로직 강화.",
         "label": "확정", "source": "https://news.example/thermal-fw"},
    ],
    "ev3": [
        {"title": "최근 사고 원인 중간 소견 공유", "cat": "사고", "desc": "충전 중 열폭주 의심. 상세 조사 중.",
         "label": "보류", "source": "https://news.example/mid-report"},
        {"title": "충전 습관 코칭 업데이트", "cat": "기타", "desc": "90% 이상 충전 빈도 감소 권장.",
         "label": "확정", "source": "https://news.example/coach"},
    ],
}

def extra_alerts_for_profile(profile_id: str):
    return list(_EXTRA.get(profile_id, []))
e(profile_id: str):
    return list(_EXTRA.get(profile_id, []))
e(profile_id: str):
    return list(_EXTRA.get(profile_id, []))
