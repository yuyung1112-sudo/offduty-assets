# offduty-assets 개선계획 (Step by Step)

- 작성일: 2026-10-31 (토)
- 대상: `C:\Users\WD\Documents\GitHub\offduty-assets` (origin: `github.com/yuyung1112-sudo/offduty-assets`, 브랜치 `main`)
- 용도: @offduty___archive 인스타 캐러셀 슬라이드 이미지 공개 호스팅

---

## ① 결론

저장소는 동작은 하지만 **라이선스 표기 누락(EP05)**, **중복 이미지 누적**, **자동화 스크립트의 안전장치 부족** 세 가지가 핵심 문제입니다.
아래 6단계 순서로 진행하면 되고, **1단계(저작권 표기 보완)는 게시 리스크와 직결되므로 가장 먼저** 처리하는 것을 권장합니다.

| 단계 | 내용 | 우선순위 | 예상 소요 |
|---|---|---|---|
| 1 | 저작권·라이선스 표기 보완 | 긴급 | 30분 |
| 2 | 폴더 구조·버전 정리 | 높음 | 30분 |
| 3 | 중복·후보 이미지 정리 | 높음 | 20분 |
| 4 | 검색 스크립트 개선 | 보통 | 1시간 |
| 5 | GitHub Actions 워크플로 보강 | 보통 | 1시간 |
| 6 | README·운영 문서화 | 보통 | 30분 |

---

## ② 현황 검토

### 폴더 구성
| 폴더 | 내용 | 비고 |
|---|---|---|
| `photos/ep01~ep05` | 슬라이드에 들어간 원본 사진 (slide_01,02,04,05[,06]) | 03·07번은 텍스트 슬라이드로 추정 |
| `photos/cand`, `cand4`, `cand5` | 후보 사진 | **ep02~ep05 사진과 동일 파일 다수** |
| `slides/ep01~ep05` | 완성 슬라이드 7장씩 | |
| `slides/ep01_v2~ep03_v2` | EP01~03 수정본 | 어느 쪽이 최종인지 표시 없음 |
| `research/*.json` | Commons 검색 결과 (ep02_ep03, ep04, ep05) | ep01 결과 없음 |
| `scripts/commons_search.py` | Commons 검색 스크립트 | |
| `.github/workflows/` | `commons-search.yml`, `fetch-photos.yml` | 수동 실행(workflow_dispatch) |
| `README.md`, `CREDITS.md` | 소개 2줄, 회차별 출처 | |

### 발견된 문제
1. **CREDITS.md에 EP05가 없음** — `photos/ep05`, `slides/ep05`는 이미 있음. 게시 중이라면 출처 미표기 상태.
2. **출처 표기 요건 미흡** — CC BY / BY-SA는 저작자·라이선스명 외에 **원본 링크·라이선스 링크·변경 여부**를 표시해야 함. 현재 링크 없음.
3. **2차 저작물(텍스트 합성) 고지 불일치** — EP01·EP03에만 "adapted works" 문구가 있고, EP02(CC BY-SA 3.0)·EP04에는 없음.
4. **EP04 출처 불명확** — slide_05 "Nationaal Archief / No known restrictions", slide_06 "John Dillenbeck / CC0"는 원본 페이지가 기록돼 있지 않음.
5. **중복 이미지** — 파일 크기 대조 결과 동일 파일로 판단됨(예시):
   - `cand/Bergungsarbeiten_..._7553` = `ep02/slide_01` (771,485 B)
   - `cand/Burj_Dubai_1292322393` = `ep03/slide_01` (503,082 B)
   - `cand4/a~f` = `ep04/slide_01~06` 대부분
   - `cand5/c` = `ep05/slide_04` (225,718 B)
6. **v1/v2 혼재** — EP01~03은 두 벌, EP04~05는 한 벌. 공개 URL로 어느 쪽을 쓰는지 불명확.
7. **스크립트** — User-Agent에 연락처 없음(Wikimedia 정책상 연락처 포함 권장), `artist`에 HTML 태그가 그대로 저장됨, 오류·재시도 처리 없음, 파일을 닫지 않고 저장.
8. **워크플로** — 입력값 검증 없음(`dest`에 `../` 입력 시 폴더 밖 저장 가능), 동시 실행 시 push 충돌 가능, 다운로드 시 라이선스 메타데이터를 같이 남기지 않음.
9. **README** — 구조·사용법·최종본 기준이 없음.

---

## ③ 단계별 실행계획

### 1단계. 저작권·라이선스 표기 보완 (긴급)
**목표**: 게시 중인 모든 슬라이드의 출처를 요건에 맞게 표기.

**작업**
- [ ] `research/ep05.json`과 `photos/ep05` 대조해 EP05 출처 5건 작성
- [ ] 회차별 표를 아래 형식으로 통일
  | 슬라이드 | 저작자 | 라이선스 | 원본 링크 | 변경사항 |
  |---|---|---|---|---|
  | slide_01 | Dead.rabbit | CC BY-SA 4.0 | (Commons 페이지 URL) | 흑백, 텍스트 합성 |
- [ ] EP04 slide_05·06 원본 페이지 확인 후 링크 기재 (확인 안 되면 교체 검토)
- [ ] BY-SA 사진이 들어간 슬라이드는 회차마다 "CC BY-SA ○.0으로 공유" 문구 통일
- [ ] 문서 하단에 라이선스 전문 링크 모음 추가

**완료 기준**: 모든 `photos/epXX/*.jpg`에 대응하는 CREDITS 행이 있고, 행마다 원본 링크가 있음.

---

### 2단계. 폴더 구조·버전 정리
**목표**: 최종본이 무엇인지 한눈에 보이게.

**작업**
- [ ] EP01~03 중 실제 게시본이 v1인지 v2인지 확인 (**확인 필요: 사용자**)
- [ ] 권장안: 최종본은 `slides/epXX/`에 두고, 이전 버전은 `slides/_archive/epXX_v1/`로 이동
  - 단, 이미 외부에 공개 URL(raw.githubusercontent 등)로 링크된 경우 **경로 변경 시 링크가 깨지므로** 이동 대신 README에 "최종본 표"만 추가
- [ ] 회차 메타파일 `episodes.json`(회차명, 게시일, 최종 슬라이드 폴더, 인스타 링크) 추가 검토

**완료 기준**: README 또는 episodes.json만 보고 회차별 최종본 폴더를 알 수 있음.

---

### 3단계. 중복·후보 이미지 정리
**목표**: 저장소 용량 축소(현재 pack 약 40MB), 혼선 제거.

**작업**
- [ ] 해시(SHA-1) 비교로 `cand*`와 `ep*` 중복 목록 확정
- [ ] 채택된 후보는 삭제, 미채택 후보는 `photos/_candidates/`로 통합하거나 삭제 (`cand`, `cand4`, `cand5` → 이름 규칙 없음)
- [ ] 앞으로 후보는 저장소에 커밋하지 않고 `research/*.json`의 링크로만 관리 (`.gitignore`에 `photos/_candidates/` 추가)
- [ ] 참고: 삭제해도 git 이력에는 남으므로 용량이 즉시 줄지는 않음. 이력 정리(history rewrite)는 위험하니 별도 판단.

**완료 기준**: `photos/` 아래에는 게시용 `epXX` 폴더만 남음.

---

### 4단계. 검색 스크립트 개선 (`scripts/commons_search.py`)
**목표**: 출처 정보를 정확하고 깔끔하게 수집.

**작업**
- [ ] User-Agent에 연락처 추가 (예: `OffdutyArchive/0.2 (contact: GitHub 저장소 URL)`)
- [ ] `artist`, `desc`의 HTML 태그 제거
- [ ] `LicenseUrl`, `Credit`, `AttributionRequired` 필드 추가 저장 → CREDITS 작성 시 그대로 사용
- [ ] 요청 실패 시 재시도(최대 3회), 요청 간 대기
- [ ] 결과 0건 쿼리 표시 (예: ep04 "steel frame 1930" 0건)
- [ ] `with open(..., encoding="utf-8")`로 저장
- [ ] (선택) PNG/TIFF 허용 옵션, 최소 해상도 필터

**완료 기준**: 새로 생성한 research JSON에서 저작자가 순수 텍스트, 라이선스 링크 포함.

---

### 5단계. GitHub Actions 워크플로 보강
**목표**: 잘못된 입력·동시 실행으로 저장소가 꼬이지 않게.

**작업**
- [ ] `fetch-photos.yml`: `dest`가 `epNN/slide_NN.jpg` 형식인지 검사, `..` 포함 시 중단
- [ ] 다운로드 후 파일이 실제 JPEG인지 확인
- [ ] 다운로드 시 해당 파일의 라이선스 메타데이터를 `photos/epXX/credits.json`으로 같이 저장 → 1단계 CREDITS 자동화 기반
- [ ] 두 워크플로에 `concurrency` 설정, push 전 `git pull --rebase`
- [ ] `commons-search.yml`: `name` 입력값을 영문·숫자·`_`만 허용
- [ ] (선택) CREDITS.md 누락 검사 워크플로: `photos/epXX`에 있는데 CREDITS에 없는 파일이 있으면 실패

**완료 기준**: 잘못된 입력으로 실행 시 워크플로가 실패하고, 정상 입력 시 사진+출처 메타데이터가 함께 커밋됨.

---

### 6단계. README·운영 문서화
**목표**: 나중에 봐도 바로 작업 가능하게.

**작업**
- [ ] README에 폴더 구조, 회차별 최종본 표, 공개 URL 형식 추가
- [ ] 신규 회차 작업 순서 정리: 검색(commons-search) → 선정 → 다운로드(fetch-photos) → 슬라이드 제작 → CREDITS 작성 → 게시
- [ ] 파일 이름 규칙: `slide_NN.jpg`(두 자리), 버전은 폴더가 아닌 커밋으로 관리
- [ ] 저장소 자체 라이선스 문구 추가 (슬라이드 2차 저작물은 CC BY-SA 4.0 등)

**완료 기준**: README만 보고 EP06을 처음부터 끝까지 만들 수 있음.

---

## ④ 실무상 주의사항

- **공개 URL 유지**: 인스타 게시물이나 다른 곳에서 이 저장소 이미지 URL을 쓰고 있다면 파일 이동·이름 변경 전에 반드시 확인하세요.
- **삭제는 되돌리기 어렵지 않지만 이력은 남음**: git에서 지운 파일도 이력에 남습니다. 용량 축소를 위해 이력을 다시 쓰는 작업(force push)은 별도 승인 후 진행하는 게 안전합니다.
- **라이선스는 원본 페이지 기준**: Commons의 라이선스 표기가 업로드 후 바뀌는 경우가 있으니, 게시 시점의 원본 페이지 링크를 남겨 두세요.
- **"No known restrictions"·"Public domain"**도 기관 표기(크레딧) 요청이 있는 경우가 많아 출처는 그대로 적는 게 좋습니다.

## 확인이 필요한 사항
1. EP01~03 게시본이 v1인지 v2인지
2. 이미지 공개 URL을 외부에서 이미 사용 중인지 (경로 변경 가능 여부)
3. EP05 게시 여부 (게시됐다면 1단계를 바로 진행)
4. 후보 사진(cand 폴더)을 보관할지 삭제할지
