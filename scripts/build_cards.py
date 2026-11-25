"""README용 SVG 카드 생성 스크립트.

프로젝트를 추가/수정하려면 아래 CARDS 목록만 고친 뒤 실행하세요.
    python3 scripts/build_cards.py
결과물은 assets/ 폴더에 저장됩니다.
"""
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "assets"
FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Apple SD Gothic Neo', 'Noto Sans KR', 'Malgun Gothic', sans-serif"

# width: 420(큰 카드) / 280(작은 카드). desc는 줄 단위로 직접 끊어서 적습니다.
CARDS = [
    # ---- Work ----
    dict(file="card-kaeri-qa", width=280, icon="atom", badge="WORK · 2023", accent="#38bdf8",
         title="파동이봇", subtitle="KAERI 사내 규정 챗봇",
         desc=["사내 규정 및 연구원 정보에 관한", "질의응답 서비스"],
         chips=["RAG", "LLM", "QA"]),
    dict(file="card-kaeri-line", width=280, icon="message", badge="WORK · 2023", accent="#4ade80",
         title="파동이봇 LINE", subtitle="캐릭터 대화 챗봇",
         desc=["캐릭터 '파동이'와", "원자력에 대해 친근하게 대화하는 챗봇"],
         chips=["Chatbot", "Persona", "LLM"]),
    dict(file="card-ondevice", width=280, icon="laptop", badge="WORK · 2024", accent="#fbbf24",
         title="ReportGen", subtitle="On-device 리포트 생성 앱",
         desc=["On-device sLM과 RAG를 활용해", "리포트 초안을 자동 생성하는 데스크톱 앱"],
         chips=["On-device", "sLM", "RAG"]),
    # ---- Personal ----
    dict(file="card-grounded", width=420, icon="scale", badge="2026", accent="#a78bfa",
         title="GROUNDED", subtitle="건축 법령 AI 에이전트 서비스",
         desc=["건축법률 기반의 정확한 답변·근거 제공에", "제출 문서 폼까지 자동으로 채워주는 플랫폼"],
         chips=["Multi Agent", "Harness", "Legal RAG", "Knowledge Graph"]),
    dict(file="card-saylong", width=420, icon="mic", badge="2026", accent="#f472b6",
         title="SayLong", subtitle="AI 영어 학습앱",
         desc=["짧은 문장에서 시작해 단계별로", "긴 문장을 완성하는 영어 학습앱"],
         chips=["Education", "LLM", "Rubric"]),
    dict(file="card-pomopet", width=420, icon="paw", badge="2026", accent="#fb923c",
         title="PomoPet", subtitle="데스크탑 펫 집중 타이머",
         desc=["귀여운 펫이 데스크탑 위에 상주하며", "뽀모도로 타이머로 집중 시간을 함께 기록하는 데스크탑 앱"],
         chips=["Desktop App", "Pomodoro"]),
    dict(file="card-natna", width=420, icon="heart", badge="2025", accent="#34d399",
         title="NaTna", subtitle="감정 공감 훈련 챗봇",
         desc=["T 성향을 가진 사람들이 감정 공감 훈련을 해볼 수 있는", "AI 챗봇 기반 감정 시뮬레이션 서비스"],
         chips=["Empathy", "Chatbot", "LLM"]),
]

# 선 아이콘 (24x24 기준 path, Lucide 스타일). 새 아이콘은 여기 추가 후 icon="키"로 사용.
ICONS = {
    "atom": '<circle cx="12" cy="12" r="1"/><path d="M20.2 20.2c2.04-2.03.02-7.36-4.5-11.9-4.54-4.52-9.87-6.54-11.9-4.5-2.04 2.03-.02 7.36 4.5 11.9 4.54 4.52 9.87 6.54 11.9 4.5Z"/><path d="M15.7 15.7c4.52-4.54 6.54-9.87 4.5-11.9-2.03-2.04-7.36-.02-11.9 4.5-4.52 4.54-6.54 9.87-4.5 11.9 2.03 2.04 7.36.02 11.9-4.5Z"/>',
    "message": '<path d="M7.9 20A9 9 0 1 0 4 16.1L2 22Z"/><path d="M8 12h.01M12 12h.01M16 12h.01"/>',
    "laptop": '<path d="M20 16V7a2 2 0 0 0-2-2H6a2 2 0 0 0-2 2v9m16 0H4m16 0 1.28 2.55a1 1 0 0 1-.9 1.45H3.62a1 1 0 0 1-.9-1.45L4 16"/>',
    "scale": '<path d="m16 16 3-8 3 8c-.87.65-1.92 1-3 1s-2.13-.35-3-1Z"/><path d="m2 16 3-8 3 8c-.87.65-1.92 1-3 1s-2.13-.35-3-1Z"/><path d="M7 21h10M12 3v18M3 7h2c2 0 5-1 7-2 2 1 5 2 7 2h2"/>',
    "mic": '<path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2M12 19v3"/>',
    "paw": '<circle cx="11" cy="4" r="2"/><circle cx="18" cy="8" r="2"/><circle cx="20" cy="16" r="2"/><path d="M9 10a5 5 0 0 1 5 5v3.5a3.5 3.5 0 0 1-6.84 1.045Q6.52 17.48 4.46 16.84A3.5 3.5 0 0 1 5.5 10Z"/>',
    "heart": '<path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/>',
}


def text_w(s: str, size: float) -> float:
    """대략적인 텍스트 폭 (한글/이모지는 넓게)."""
    w = 0.0
    for ch in s:
        if ord(ch) > 0x2E80:
            w += size * 1.0
        elif ch.isupper():
            w += size * 0.66
        elif ch == " ":
            w += size * 0.3
        else:
            w += size * 0.56
    return w


def card(c: dict) -> str:
    W, H = c["width"], 212
    a = c["accent"]
    pad = 24
    badge = c["badge"]
    bw = text_w(badge, 10.5) + 22
    dot = ""
    if c.get("live"):
        bw += 12
        dot = (f'<circle cx="{W - pad - bw + 13}" cy="33" r="3.2" fill="{a}">'
               f'<animate attributeName="opacity" values="1;.25;1" dur="1.6s" repeatCount="indefinite"/></circle>')
    btx = W - pad - bw / 2 + (6 if c.get("live") else 0)

    chips, x = [], pad
    for ch in c["chips"]:
        cw = text_w(ch, 11.5) + 20
        chips.append(
            f'<rect x="{x}" y="170" width="{cw:.0f}" height="22" rx="11" fill="{a}" fill-opacity=".12" stroke="{a}" stroke-opacity=".35"/>'
            f'<text x="{x + cw / 2:.0f}" y="185" text-anchor="middle" font-size="11.5" font-weight="600" fill="{a}">{escape(ch)}</text>')
        x += cw + 6

    desc = "".join(
        f'<text x="{pad}" y="{136 + i * 20}" font-size="13.5" fill="#c9d1d9">{escape(l)}</text>'
        for i, l in enumerate(c["desc"]))

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{FONT}">
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#151b2e"/><stop offset="1" stop-color="#0d1117"/></linearGradient>
  <linearGradient id="bd" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{a}" stop-opacity=".75"/><stop offset=".5" stop-color="{a}" stop-opacity=".12"/><stop offset="1" stop-color="{a}" stop-opacity=".4"/></linearGradient>
  <radialGradient id="gl" cx="1" cy="0" r="1"><stop offset="0" stop-color="{a}" stop-opacity=".28"/><stop offset="1" stop-color="{a}" stop-opacity="0"/></radialGradient>
  <clipPath id="cl"><rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="16"/></clipPath>
</defs>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="16" fill="url(#bg)"/>
<g clip-path="url(#cl)"><circle cx="{W}" cy="0" r="{W * .55:.0f}" fill="url(#gl)"/><rect x="1" y="1" width="5" height="{H}" fill="{a}" opacity=".9"/></g>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="16" fill="none" stroke="url(#bd)" stroke-width="1.5"/>
<rect x="{pad}" y="16" width="36" height="36" rx="10" fill="{a}" fill-opacity=".14" stroke="{a}" stroke-opacity=".35"/>
<g transform="translate({pad + 8} 24) scale(.8333)" fill="none" stroke="{a}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">{ICONS[c["icon"]]}</g>
<rect x="{W - pad - bw:.0f}" y="22" width="{bw:.0f}" height="22" rx="11" fill="#ffffff" fill-opacity=".06" stroke="#ffffff" stroke-opacity=".14"/>
{dot}
<text x="{btx:.0f}" y="37" text-anchor="middle" font-size="10.5" font-weight="700" letter-spacing=".6" fill="#8b949e">{escape(badge)}</text>
<text x="{pad}" y="84" font-size="22" font-weight="800" fill="#f0f6fc">{escape(c["title"])}</text>
<text x="{pad}" y="107" font-size="13" font-weight="600" fill="{a}">{escape(c["subtitle"])}</text>
{desc}
{"".join(chips)}
</svg>
'''


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    for c in CARDS:
        (OUT / f'{c["file"]}.svg').write_text(card(c), encoding="utf-8")
        print("wrote", c["file"])
