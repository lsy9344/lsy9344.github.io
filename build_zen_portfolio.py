import os

projects_data = [
    {
        'file': 'projects/beauty-brand-crm.html',
        'title': '제나셀 바이오 뷰티 CRM & 자동화 엔진',
        'meta': 'CONTRACT ₩8,500,000 · 60 DAYS · 1 ENGINEER',
        'shots': [
            {'src': '../images/crm/sources/01_rich_canvas.png', 'alt': '노드 기반 자동화 워크플로우 캔버스', 'desc': '노드를 잇습니다. 시나리오가 움직입니다.'},
            {'src': '../images/crm/sources/02_customer_profile.png', 'alt': '고객 단일 프로필 (SSOT)', 'desc': '결제와 상담을 단 하나의 타임라인으로 모았습니다.'},
            {'src': '../images/crm/sources/03_segment_builder.png', 'alt': 'RFM 다중 조건 세그먼트 빌더', 'desc': '이탈 직전 고객만 핀셋으로 골라냅니다.'},
            {'src': '../images/crm/sources/04_staff_tasks.png', 'alt': '운영자 안전 검수 큐', 'desc': '사람의 최종 검수 없이는 문자 한 통도 나가지 않습니다.'},
            {'src': '../images/crm/sources/02_customer_timeline.png', 'alt': '실제 결제 원장과 AI 예측 분리', 'desc': '결제 장부와 AI 예측을 엄격히 분리했습니다.'}
        ]
    },
    {
        'file': 'projects/beauty-band-automation.html',
        'title': '뷰티 브랜드 BAND 콘텐츠 운영 자동화',
        'meta': '60 DAYS · 1 ENGINEER · NAVER BAND API',
        'shots': [
            {'src': '../images/beauty-band-automation/sources/01_today_ko.png', 'alt': '일일 예약 및 발행 관제', 'desc': '오늘 발행할 콘텐츠를 한눈에 관제합니다.'},
            {'src': '../images/beauty-band-automation/sources/03_weekly_schedule_ko.png', 'alt': '주간 타임라인 스케줄러', 'desc': '일주일치 밴드 글을 타임라인에 미리 얹습니다.'},
            {'src': '../images/beauty-band-automation/sources/05_add_schedule_dialog_ko.png', 'alt': '예약 발행 다이얼로그', 'desc': '시간과 본문을 정하면, 정시에 밴드로 출발합니다.'},
            {'src': '../images/beauty-band-automation/sources/04_history_ko.png', 'alt': '발행 이력 및 감사 로그', 'desc': '언제 누가 발행했는지 1초의 오차 없이 남깁니다.'}
        ]
    },
    {
        'file': 'projects/beauty-erp-inventory.html',
        'title': '뷰티 브랜드 사내 ERP·재고·매출 관리',
        'meta': 'ENTERPRISE ERP · MULTI-CHANNEL RECONCILIATION · 1 ENGINEER',
        'shots': [
            {'src': '../images/beauty-erp-inventory/sources/01_workspace_home_ko.png', 'alt': '통합 워크스페이스 홈', 'desc': '모든 물류와 품목이 하나의 화면에서 시작됩니다.'},
            {'src': '../images/beauty-erp-inventory/sources/03_catalog_workspace_ko.png', 'alt': '제품 카탈로그 및 채널 매핑', 'desc': '채널마다 제각각인 상품명을 하나로 묶었습니다.'},
            {'src': '../images/beauty-erp-inventory/sources/04_inventory_workspace_ko.png', 'alt': '실재고 및 보정 제어', 'desc': '손실과 입고를 즉시 계산해 숫자를 맞춥니다.'},
            {'src': '../images/beauty-erp-inventory/sources/06_inventory_reconciliation_actual_ko.png', 'alt': '실시간 재고 대사', 'desc': '창고의 실물과 장부의 차이를 0으로 수렴시킵니다.'}
        ]
    },
    {
        'file': 'projects/beauty-review-platform.html',
        'title': '뷰티 브랜드 다국어 상품 후기 플랫폼',
        'meta': 'MULTILINGUAL REVIEW · DATA READINESS · 1 ENGINEER',
        'shots': [
            {'src': '../images/beauty-review-platform/sources/01_internal_readiness_ko.png', 'alt': '내부 상품 준비 상태 점검', 'desc': '진짜 후기만 남기도록 데이터 정합성을 검증합니다.'},
            {'src': '../images/beauty-review-platform/sources/03_internal_readiness_valid_ko.png', 'alt': '리뷰 유효성 및 발행 검수', 'desc': '검증된 후기만 다국어 채널로 안전하게 송출합니다.'}
        ]
    },
    {
        'file': 'projects/boothy-photo-booth.html',
        'title': 'Boothy · 무인 사진관 촬영·프리셋·운영 제어',
        'meta': 'KIOSK HARDWARE CONTROL · 300DPI RENDER · 1 ENGINEER',
        'shots': [
            {'src': '../images/boothy-photo-booth/sources/01-session-redesign.png', 'alt': '세션 진입 및 모드 선택', 'desc': '손님이 들어서면 부스는 촬영 준비를 끝냅니다.'},
            {'src': '../images/boothy-photo-booth/sources/02-looks-redesign.png', 'alt': '실시간 필터 및 룩 프리셋', 'desc': '셔터를 누르는 순간, 조명과 색감이 정렬됩니다.'},
            {'src': '../images/boothy-photo-booth/sources/03-preview-redesign.png', 'alt': '4컷 레이아웃 실시간 프리뷰', 'desc': '가장 자연스러운 네 컷을 캔버스에 앉힙니다.'},
            {'src': '../images/boothy-photo-booth/sources/04-operator-redesign.png', 'alt': '점주 원격 제어 인터페이스', 'desc': '기기 장애와 카메라 상태를 원격에서 즉시 다룹니다.'}
        ]
    },
    {
        'file': 'projects/multi-branch-studio-erp.html',
        'title': '다지점 사진관 운영·급여·주차·보정 ERP',
        'meta': 'MULTI-BRANCH ERP · AUTO PAYROLL · 1 ENGINEER',
        'shots': [
            {'src': '../images/multi-branch-studio-erp/sources/01_admin_dashboard_ko.png', 'alt': '지점별 실시간 매출 대시보드', 'desc': '여러 지점의 예약과 매출을 한 장표에 올렸습니다.'},
            {'src': '../images/multi-branch-studio-erp/sources/02_work_status_ko.png', 'alt': '촬영 및 보정 작업 배정 현황', 'desc': '보정본이 오가는 길목을 막힘없이 잇습니다.'},
            {'src': '../images/multi-branch-studio-erp/sources/03_payroll_ko.png', 'alt': '작가별 작업량 기반 급여 자동 정산', 'desc': '작업한 컷수만큼 급여가 1원 단위까지 계산됩니다.'},
            {'src': '../images/multi-branch-studio-erp/sources/04_staff_ko.png', 'alt': '지점 스태프 권한 관리', 'desc': '지점마다 다른 권한을 안전하게 나눕니다.'}
        ]
    },
    {
        'file': 'projects/cuteditor-photo-tool.html',
        'title': 'CutEditor · 네컷사진 인화 편집 웹 도구',
        'meta': 'WEB CANVAS · 300DPI PRINT PIPELINE · 1 ENGINEER',
        'shots': [
            {'src': '../images/cuteditor-photo-tool/sources/01_layout_gallery_ko.png', 'alt': '레이아웃 템플릿 갤러리', 'desc': '원하는 프레임을 고릅니다.'},
            {'src': '../images/cuteditor-photo-tool/sources/02b_editor_with_demo_photos_ko.png', 'alt': '슬롯 기반 사진 배치 캔버스', 'desc': '사진을 끌어다 놓으면 비율대로 자리를 잡습니다.'},
            {'src': '../images/cuteditor-photo-tool/sources/03_text_panel_ko.png', 'alt': '텍스트 타이포그래피 도구', 'desc': '글씨로 순간의 기억을 덧입힙니다.'},
            {'src': '../images/cuteditor-photo-tool/sources/04_sticker_panel_ko.png', 'alt': '벡터 스티커 오버레이', 'desc': '취향대로 스티커를 얹습니다.'},
            {'src': '../images/cuteditor-photo-tool/sources/06_editor_real_photo_text_sticker_ko.png', 'alt': '인화용 고해상도 렌더링', 'desc': '300DPI 인쇄 규격 그대로 깨짐 없이 렌더링합니다.'}
        ]
    },
    {
        'file': 'projects/sms-automation-review.html',
        'title': '네이버 플레이스 예약 SMS 발송기',
        'meta': 'BOOKING SIGNAL · CARRIER GATEWAY · 1 ENGINEER',
        'shots': [
            {'src': '../images/sms-automation-review/sources/00-cover-source.png', 'alt': '실시간 예약 감지 대시보드', 'desc': '예약이 들어오는 찰나를 낚아챕니다.'},
            {'src': '../images/sms-automation-review/sources/01-booking-sms-flow-source.png', 'alt': '방문 시간 기반 발송 파이프라인', 'desc': '방문 1시간 전, 길 안내 문자가 자동으로 떠납니다.'},
            {'src': '../images/sms-automation-review/sources/02-send-timing-source.png', 'alt': '지연 없는 타이머 트리거', 'desc': '수신 거부 고객을 걸러 불필요한 과금을 막습니다.'},
            {'src': '../images/sms-automation-review/sources/03-result-marking-source.png', 'alt': '통신사 발송 결과 마킹', 'desc': '단 한 건의 누락도 없이 결과를 장부에 새깁니다.'}
        ]
    },
    {
        'file': 'projects/vietnam-aesthetic-erp.html',
        'title': '베트남 에스테틱 다국어 운영 ERP',
        'meta': 'CROSS-BORDER ERP · MULTILINGUAL · 1 ENGINEER',
        'shots': [
            {'src': '../images/vietnam-aesthetic-erp/sources/01_actual_dashboard_ko.png', 'alt': '한국 본사 관리자 관제 대시보드', 'desc': '서울 본사에서 하노이 매장의 베드를 실시간으로 봅니다.'},
            {'src': '../images/vietnam-aesthetic-erp/sources/04_actual_call_ledger_vi.png', 'alt': '현지 베트남어 콜/예약 원장', 'desc': '현지 직원은 베트남어로, 관리자는 한국어로 소통합니다.'},
            {'src': '../images/vietnam-aesthetic-erp/sources/05_actual_live_rooms_vi.png', 'alt': '실시간 룸 및 베드 배정 그리드', 'desc': '방이 비는 즉시 다음 고객을 안내합니다.'},
            {'src': '../images/vietnam-aesthetic-erp/sources/06_actual_settlement_vi.png', 'alt': '다국어 화폐(VND/KRW) 결제 정산', 'desc': '베트남 동과 원화의 환율 차이를 정산에서 잠재웁니다.'}
        ]
    },
    {
        'file': 'projects/seafood-distribution-erp.html',
        'title': '수산물 유통·장부 엑셀 자동화 ERP',
        'meta': 'DAILY SETTLEMENT · EXCEL PIPELINE · 1 ENGINEER',
        'shots': [
            {'src': '../images/seafood-distribution-erp/sources/01_dashboard_populated_ko.png', 'alt': '일일 수산물 입출고 대시보드', 'desc': '새벽마다 널뛰는 수산물 단가를 한 장에 묶습니다.'},
            {'src': '../images/seafood-distribution-erp/sources/02_daily_report_populated_ko.png', 'alt': '새벽 시세 정산 장부 엑셀 생성', 'desc': '수기로 쓰던 거래명세서를 엑셀 클릭 1번에 뽑아냅니다.'}
        ]
    },
    {
        'file': 'projects/military-meal-management.html',
        'title': '군 식수 인원 관리 시스템',
        'meta': 'REALTIME HEADCOUNT · QR VERIFICATION · 1 ENGINEER',
        'shots': [
            {'src': '../images/military-meal-management/sources/user-direct-capture.png', 'alt': '장병 모바일 식수 신청 화면', 'desc': '장병이 오늘 먹을 끼니를 직접 신청합니다.'},
            {'src': '../images/military-meal-management/sources/ticket-direct-capture.png', 'alt': '바코드 배식 인증 화면', 'desc': '배식대에서 식별 코드를 찍고 입장합니다.'},
            {'src': '../images/military-meal-management/sources/admin-direct-capture.png', 'alt': '급식 담당관 일일 식수 집계 대시보드', 'desc': '남는 밥과 모자란 국이 없도록 식수를 실시간으로 맞춥니다.'}
        ]
    },
    {
        'file': 'projects/multimarket-crawler.html',
        'title': '이커머스 가격 모니터링 크롤러',
        'meta': 'SCRAPING ENGINE · REALTIME PRICE ALERT · 1 ENGINEER',
        'shots': [
            {'src': '../images/multimarket-crawler/sources/gmarket_ui_original.png', 'alt': '실시간 마켓 상품 스크래핑 엔진', 'desc': '오픈마켓 수만 개의 가격표를 쉼 없이 읽어옵니다.'},
            {'src': '../images/multimarket-crawler/sources/actual_app_synthetic_results_fresh.png', 'alt': '경쟁사 최저가 변동 감지 결과', 'desc': '경쟁사가 가격을 내리면 즉시 알림을 띄웁니다.'}
        ]
    },
    {
        'file': 'projects/kakaotalk-unread-excel.html',
        'title': '카카오톡 미확인 채팅 추출 및 엑셀화 도구',
        'meta': 'WINDOWS AUTOMATION · DESKTOP HOOK · 1 ENGINEER',
        'shots': [
            {'src': '../images/kakaotalk-unread-excel/sources/01_completion_ko.png', 'alt': '미확인 메시지 감지 및 엑셀 저장 완료', 'desc': '수백 개의 단체방 속 놓친 메시지를 엑셀 한 줄로 추출합니다.'}
        ]
    },
    {
        'file': 'projects/tactrun-delivery-landing.html',
        'title': '배달 라이더 택트런 솔루션 랜딩',
        'meta': 'RIDER DISPATCH · REALTIME SIGNAL · 1 ENGINEER',
        'shots': [
            {'src': '../images/tactrun-delivery-landing/sources/01_hero_ko.png', 'alt': '라이더 전용 랜딩 히어로', 'desc': '달리는 라이더를 위해 군더더기를 모두 뺐습니다.'},
            {'src': '../images/tactrun-delivery-landing/sources/02_operations_map_ko.png', 'alt': '실시간 배달 권역 맵', 'desc': '배달 권역과 신호를 지도 위에 선명하게 띄웁니다.'},
            {'src': '../images/tactrun-delivery-landing/sources/03_message_preview_ko.png', 'alt': '콜 배차 알림 카드', 'desc': '꼭 필요한 배차 정보만 1초 만에 읽힙니다.'},
            {'src': '../images/tactrun-delivery-landing/sources/05_cancellation_chain_ko.png', 'alt': '취소 방어 체인', 'desc': '돌발 취소에도 라이더의 이동 동선을 안전하게 지킵니다.'}
        ]
    }
]

template = '''<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} — Noah Park</title>
  <meta name="description" content="{desc_first}">
  <link rel="stylesheet" href="../style.css">
  <script src="../theme.js"></script>
  <script src="../lightbox.js" defer></script>
  <script src="../admin.js" defer></script>
</head>

<body class="article-page">
  <header class="site-header">
    <h1>
      <a class="name" href="../index.html">Noah Park</a>
    </h1>
    <nav aria-label="Main navigation">
      <a href="../index.html#project">Project</a>
      <a href="../index.html#writing">Writing</a>
      <a class="social-link" href="https://github.com" target="_blank" rel="noopener noreferrer">GitHub</a>
      <button class="theme-toggle" type="button" data-theme-toggle aria-label="Dark mode toggle" aria-pressed="false">
        <span data-theme-icon aria-hidden="true">☾</span>
      </button>
    </nav>
  </header>

  <main class="article">
    <a href="../index.html#project" class="back-link">← Project</a>

    <header class="article-header" style="margin-bottom: 96px;">
      <h1 style="font-size: 21px; font-weight: 500; letter-spacing: -0.3px;">{title}</h1>
      <span class="date" style="font-family: ui-monospace, Menlo, monospace; font-size: 11px; color: var(--muted); margin-top: 6px;">
        {meta}
      </span>
    </header>

{sections}

    <div style="margin: 160px 0 32px; padding-top: 24px; border-top: 1px solid var(--rule);">
      <a href="../index.html#project" class="back-link" style="margin-bottom: 0;">← Back to Project</a>
    </div>
  </main>

  <footer class="site-footer">
    <span>© 2026 Noah Park. Crafted with care.</span>
    <span><a href="mailto:noah.park.dev@example.com">Contact</a></span>
  </footer>
</body>
</html>'''

for p in projects_data:
    sections_html = []
    for s in p['shots']:
        sec = f'''    <section class="zen-section-xl" style="margin: 180px 0;">
      <figure style="margin: 0;">
        <img class="zoomable" src="{s['src']}" alt="{s['alt']} (클릭하여 확대)" />
      </figure>
      <div class="zen-caption">
        {s['desc']}
      </div>
    </section>'''
        sections_html.append(sec)

    desc_first = p['shots'][0]['desc'] if p['shots'] else p['title']
    content = template.format(
        title=p['title'],
        meta=p['meta'],
        desc_first=desc_first,
        sections='\n\n'.join(sections_html)
    )

    with open(p['file'], 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Rendered Zen Style 3: {p["file"]}')
