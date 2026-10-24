# Project: Noah Park Portfolio — 14 Real Projects Case Studies

## Architecture
- **Framework & Foundation**: Pure Semantic HTML5, Vanilla CSS Variables (`style.css`), Zero-Dependency JavaScript (`theme.js`), Pure Python Verification (`scripts/verify_portfolio.py`).
- **Design Philosophy**: Karri Saarinen (480px single column readability, Paper/Ink aesthetic, braille bullets `⡢`, `<figure>`/`<figcaption>` framed screenshots) × Arlan Marat (2-column project list, pure CSS Focus Dim micro-interaction, clean typography).
- **Directory Layout**:
  - `index.html`: Root portfolio overview with 4 categorized domains and 14 projects with Focus Dim effect.
  - `projects/<project_slug>.html`: 14 dedicated case study pages (5 standard sections: Overview, Problem & Integrity, Architecture & Flow, Key Features, Key Takeaways).
  - `images/<project_slug>/`: High-resolution real application screenshots extracted from Notion.
  - `style.css`: Unified styling (theme variables, layout, typography, micro-interactions).
  - `theme.js`: Instant dark/light mode toggle (FOUC-free IIFE).
  - `scripts/verify_portfolio.py`: Zero-dependency 4-tier E2E verification test runner.

## Feature Inventory
| # | Feature | Description | Milestone | Source |
|---|---------|-------------|-----------|--------|
| 1 | Notion S3 Asset Extraction | Download 63 genuine screenshot assets for 13 projects into `images/<slug>/` | M1 | ORIGINAL_REQUEST §R1 |
| 2 | Commerce & SaaS Case Studies | 3 detailed pages (`beauty-review-platform`, `beauty-band-automation`, `beauty-erp-inventory`) | M2-A | ORIGINAL_REQUEST §R2 |
| 3 | Media & Photo Booth Case Studies | 4 detailed pages (`boothy-photo-booth`, `multi-branch-studio-erp`, `sms-automation-review`, `cuteditor-photo-tool`) | M2-B | ORIGINAL_REQUEST §R2 |
| 4 | Industry ERP Case Studies | 3 detailed pages (`vietnam-aesthetic-erp`, `seafood-distribution-erp`, `military-meal-management`) | M2-C | ORIGINAL_REQUEST §R2 |
| 5 | Automation Tools Case Studies | 3 detailed pages (`multimarket-crawler`, `kakaotalk-unread-excel`, `tactrun-delivery-landing`) | M2-D | ORIGINAL_REQUEST §R2 |
| 6 | Main Index Link Integration | Update `index.html` with 14 local project links replacing external Notion URLs | M3 | ORIGINAL_REQUEST §R3 |
| 7 | Focus Dim & Theme Continuity | Preserve pure CSS Focus Dim effect and FOUC-free theme toggling across all pages | M3 | DESIGN.md & SKILL.md |
| 8 | E2E Python Verification Suite | Standalone Zero-Dependency 4-Tier test runner (`scripts/verify_portfolio.py`) | M-TEST | ORIGINAL_REQUEST §Verification |
| 9 | 4-Tier Automated Validation | File integrity, semantic 404 guard, interaction tokens, and live HTTP 200 server test | M4 | TEST_INFRA.md |

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| M-TEST | E2E Test Suite Creation | Create `scripts/verify_portfolio.py` per `TEST_INFRA.md` | Survey complete | DONE |
| M1 | Notion Asset Extraction | Download 63 genuine images to `images/<slug>/` via Notion API | Survey complete | DONE |
| M2-A | Commerce & SaaS Pages | 3 case studies HTML in `projects/` | M1, M-TEST | DONE |
| M2-B | Media & Photo Booth Pages | 4 case studies HTML in `projects/` | M1, M-TEST | DONE |
| M2-C | Industry ERP Pages | 3 case studies HTML in `projects/` | M1, M-TEST | DONE |
| M2-D | Automation & Tools Pages | 3 case studies HTML in `projects/` | M1, M-TEST | DONE |
| M3 | Index Integration | Connect all 14 project links in `index.html` & verify Focus Dim | M2 (all) | DONE |
| M4 | Comprehensive Gate & Audit | Run 4-Tier verification, Reviewers, Challengers, and Forensic Audit | M3 | DONE |

## Interface Contracts
### `index.html` ↔ `projects/<project_slug>.html`
- Hyperlinks inside `index.html` must point to `./projects/<project_slug>.html`.
- Backlinks inside each `projects/<project_slug>.html` must point to `../index.html#project`.
- Assets linked in `projects/<project_slug>.html` must use relative paths:
  - `<link rel="stylesheet" href="../style.css">`
  - `<script src="../theme.js"></script>`
  - `<img src="../images/<project_slug>/<filename>" alt="..." />`

### 14 Projects Slug & Asset Directory Mapping
| # | Project Name | Slug | HTML Path | Images Directory |
|---|--------------|------|-----------|------------------|
| 01 | 뷰티 브랜드 고객 CRM | `beauty-brand-crm` | `projects/beauty-brand-crm.html` | `images/crm/` |
| 02 | 뷰티 브랜드 상품 후기 플랫폼 | `beauty-review-platform` | `projects/beauty-review-platform.html` | `images/beauty-review-platform/` |
| 03 | 뷰티 브랜드 BAND 운영 자동화 | `beauty-band-automation` | `projects/beauty-band-automation.html` | `images/beauty-band-automation/` |
| 04 | 뷰티 브랜드 사내 ERP | `beauty-erp-inventory` | `projects/beauty-erp-inventory.html` | `images/beauty-erp-inventory/` |
| 05 | Boothy 무인 사진관 제어 | `boothy-photo-booth` | `projects/boothy-photo-booth.html` | (Text & Architecture only) |
| 06 | 다지점 사진관 운영 ERP | `multi-branch-studio-erp` | `projects/multi-branch-studio-erp.html` | `images/multi-branch-studio-erp/` |
| 07 | 다지점 문자 발송 자동화 | `sms-automation-review` | `projects/sms-automation-review.html` | `images/sms-automation-review/` |
| 08 | 브라우저 사진 편집 도구 | `cuteditor-photo-tool` | `projects/cuteditor-photo-tool.html` | `images/cuteditor-photo-tool/` |
| 09 | 베트남 에스테틱 ERP | `vietnam-aesthetic-erp` | `projects/vietnam-aesthetic-erp.html` | `images/vietnam-aesthetic-erp/` |
| 10 | 수산물 유통 통합 ERP | `seafood-distribution-erp` | `projects/seafood-distribution-erp.html` | `images/seafood-distribution-erp/` |
| 11 | 군부대 식권·급여 공제 관리 | `military-meal-management` | `projects/military-meal-management.html` | `images/military-meal-management/` |
| 12 | 멀티마켓 공개정보 수집 | `multimarket-crawler` | `projects/multimarket-crawler.html` | `images/multimarket-crawler/` |
| 13 | 카카오톡 1:1 대화방 정리 | `kakaotalk-unread-excel` | `projects/kakaotalk-unread-excel.html` | `images/kakaotalk-unread-excel/` |
| 14 | 배달센터 실적 소개 웹 (TactRun) | `tactrun-delivery-landing` | `projects/tactrun-delivery-landing.html` | `images/tactrun-delivery-landing/` |

## Code Layout
- `index.html`: Main landing page
- `style.css`: Core design system & theme variables
- `theme.js`: Dark/Light mode theme logic
- `projects/`: 14 case study HTML files
- `images/`: Subdirectories per project slug with real screenshots
- `scripts/`: Verification scripts (`verify_portfolio.py`)
