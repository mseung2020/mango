from datetime import datetime, timedelta
import uuid

def _now_str():
    return datetime.utcnow().strftime("%Y-%m-%d %H:%M")

PROFILES = [
    {
        "id": "ev1",
        "name": "EV 사용자 A",
        "desc": (
            "- 출퇴근용으로 신차 EV를 쓰는 직장인.<br>"
            "- 급속 충전을 자주 이용해 배터리 온도 관리가 중요.<br>"
            "- 실시간 안전 공지와 충전 최적화 팁을 원함."
        ),
        "icon": "🚗",
    },
    {
        "id": "ev2",
        "name": "EV 사용자 B",
        "desc": (
            "- 중고 EV를 구매해 장기간 사용 중.<br>"
            "- 배터리 수명과 충전 효율에 민감함.<br>"
            "- 예방 차원의 관리 전략과 최신 업데이트 정보 필요."
        ),
        "icon": "⚡",
    },
    {
        "id": "ev3",
        "name": "EV 사고 경험자 C",
        "desc": (
            "- 과거 배터리 화재·리콜 사고를 직접 겪은 차주.<br>"
            "- 안전 알림과 사고 원인 분석에 특히 관심이 많음.<br>"
            "- 근거 기반의 가이드와 즉각적인 대응 전략을 중시."
        ),
        "icon": "🧯",
    },
]

CATS = ["사고", "기술", "기타"]

def seed_news(profile_id: str):
    prefix = {"ev1": "[A]", "ev2": "[B]", "ev3": "[C]"}[profile_id]
    base = datetime.utcnow()
    data = [
        {
            "when": "3일 전",
            "title": f"{prefix} 급속충전 중 온도 상승 이슈",
            "cat": "사고",
            "desc": "특정 구간에서 충전 중 온도 상승 보고.",
            "detail": (
                "해당 구간(SOC 60~80%)에서 셀 온도 스파이크 사례가 간헐적으로 관측되었습니다.<br>"
                "중대 이슈는 제조사/정부 **공식 공지 확인 후 확정**되며, 그 전에는 ’보류’로 표기됩니다.<br>"
                "동일/유사 보도는 **군집화**해 중복 알림을 줄이고 핵심만 제공합니다.<br>"
                "임시 조치: 급속 연속 사용을 줄이고, 앱의 온도 경보가 반복되면 **무상 점검 예약**을 권고합니다."
            ),
            "label": "보류",
            "updated": _now_str(),
            "source": "https://news.example/ev-heat",
        },
        {
            "when": "10일 전",
            "title": f"{prefix} BMS 업데이트 권고",
            "cat": "기술",
            "desc": "성능 개선 및 안전 패치 포함.",
            "detail": (
                "BMS 핫픽스에 **셀 밸런싱 보정/열관리 로직 강화**가 포함되었습니다.<br>"
                "OTA 가능 차량은 순차 배포되며, 미대상 차량은 서비스 센터에서 업데이트 지원합니다.<br>"
                "업데이트 후 급속 구간에서 온도 상승 억제와 충전 커트백 안정성이 개선됩니다.<br>"
                "알림/조치 이력은 대시보드 ’히스토리’에서 추적 가능합니다."
            ),
            "label": "확정",
            "updated": (base - timedelta(days=1)).strftime("%Y-%m-%d %H:%M"),
            "source": "https://news.example/bms-update",
        },
        {
            "when": "1개월 전",
            "title": f"{prefix} 배터리 냉각 개선 사례",
            "cat": "기술",
            "desc": "열관리 개선으로 효율 상승.",
            "detail": (
                "개선형 냉각 덕트/펌프 커브 적용 사례에서 고부하 충전 시 **셀 온도 상승률이 완만화**되었습니다.<br>"
                "고온 환경(여름/지하주차장)에서는 여전히 초기 온도 관리가 중요합니다.<br>"
                "충전 플랜: SOC 20~80% 구간 위주, 급가속/연속 급속 빈도 최소화가 권장됩니다.<br>"
                "이 내용은 근거형 요약 기준으로 제공됩니다(출처·갱신시각 병기)."
            ),
            "label": "추정",
            "updated": (base - timedelta(days=8)).strftime("%Y-%m-%d %H:%M"),
            "source": "https://news.example/cooling-case",
        },
        {
            "when": "2개월 전",
            "title": f"{prefix} 충전소 점검 캠페인",
            "cat": "기타",
            "desc": "일부 변압기 점검 안내.",
            "detail": (
                "도심 급속 충전소 일부에서 야간 **변압기/케이블 접점 점검**이 예정되었습니다.<br>"
                "점검 시간대에는 출력 제한 또는 일시 중단이 발생할 수 있어 우회 충전을 권합니다.<br>"
                "중복 공지는 군집화되어 1회로 묶이며, 중요 변경 시에만 재알림 합니다.<br>"
                "자세한 일정은 운영사 공지 URL에서 확인하세요."
            ),
            "label": "확정",
            "updated": (base - timedelta(days=35)).strftime("%Y-%m-%d %H:%M"),
            "source": "https://news.example/site-check",
        },
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
        {
            "title": "급속충전 커넥터 접점 점검 권고",
            "cat": "사고",
            "desc": "접점 과열 가능성. 서비스 센터 무상 점검.",
            "detail": (
                "커넥터 핀/소켓 접촉저항 상승 시 국부 과열이 발생할 수 있습니다.<br>"
                "증상이 재현되면 커넥터 교체 또는 클리닝을 무상 점검으로 지원합니다.<br>"
                "관련 보도는 **공식 공지** 확인 후 확정 처리되며, 그 전에는 보류로 표기됩니다."
            ),
            "label": "확정",
            "source": "https://news.example/connector",
        },
        {
            "title": "신규 BMS 핫픽스 배포",
            "cat": "기술",
            "desc": "셀 밸런싱 로직 보정 포함.",
            "detail": (
                "핫픽스는 특정 셀 불균형 상황에서의 잔여 용량 예측 오류를 보정합니다.<br>"
                "급속 종료 지점(80% 부근)에서 커트백 거동이 보다 안정화됩니다.<br>"
                "설치 후 히스토리 카드에 버전/갱신시각이 기록됩니다."
            ),
            "label": "확정",
            "source": "https://news.example/bms-hotfix",
        },
    ],
    "ev2": [
        {
            "title": "도심 충전소 화재 예방 점검",
            "cat": "사고",
            "desc": "일부 구간 야간 점검 예정.",
            "detail": (
                "분전함/케이블 트레이 열화 점검과 소화 설비 리필이 진행됩니다.<br>"
                "출력 제한 시 완속 대체를 권장하며, 알림은 **중복 묶음(군집화)**으로 최소화합니다."
            ),
            "label": "보류",
            "source": "https://news.example/city-prevent",
        },
        {
            "title": "열관리 펌웨어 업데이트",
            "cat": "기술",
            "desc": "고온 구간 보호 로직 강화.",
            "detail": (
                "배터리 입력 열유속이 높을 때 **냉각 목표온도/펌프 속도**가 상향 조정됩니다.<br>"
                "고온 여름철 급속 연속 사용 시 온도 안정화 시간이 단축됩니다."
            ),
            "label": "확정",
            "source": "https://news.example/thermal-fw",
        },
    ],
    "ev3": [
        {
            "title": "최근 사고 원인 중간 소견 공유",
            "cat": "사고",
            "desc": "충전 중 열폭주 의심. 상세 조사 중.",
            "detail": (
                "충전 중 셀 내부 단락 의심 정황이 있으며, 부품/환경 요인을 병행 조사 중입니다.<br>"
                "최종 결과는 **공식 발표** 시 반영하고, 그 전까지는 보수적으로 조치 가이드를 제공합니다."
            ),
            "label": "보류",
            "source": "https://news.example/mid-report",
        },
        {
            "title": "충전 습관 코칭 업데이트",
            "cat": "기타",
            "desc": "90% 이상 충전 빈도 감소 권장.",
            "detail": (
                "장기 수명 관점에서 상단 SOC 체류 시간을 줄이고, 20~80% 운용을 권장합니다.<br>"
                "사용자 히스토리를 반영해 맞춤 코칭이 순차 제공됩니다."
            ),
            "label": "확정",
            "source": "https://news.example/coach",
        },
    ],
}

def extra_alerts_for_profile(profile_id: str):
    return list(_EXTRA.get(profile_id, []))
