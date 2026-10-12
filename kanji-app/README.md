# 일본어 한자 공부 (JLPT N5 · N4 · N3 · N2)

JLPT **N5 · N4 · N3 · N2 = 984자**를 담은 일본어 한자 학습 웹앱.
빌드 도구 없이 **단일 `index.html` 하나만** 열면 바로 동작합니다.

## 기능
- **목록**: 등급 필터(전체/N5/N4/N3/N2) · `모두/즐겨찾기/미암기` 필터 · 검색(한자·뜻·읽기·**로마자**·영어)
- **상세**: 기본정보 → ①한자 모양 해설(어원) + 💡암기 꿀팁 → ②음독 상세 → ③훈독 상세. 대표단어는 후리가나+한국어. 이전/다음 이동(←/→), 획순(KanjiVG, 온라인 시)
- **카드**: 플래시카드. 뒷면에 `뜻 / 음독 / 훈독` + 읽기별 **예시 단어 2개와 작은 뜻**
- **퀴즈**: 4지선다(뜻/읽기), 필터별 출제
- **학습 진도**: 즐겨찾기·암기 체크를 브라우저(localStorage)에 저장 · 진도바
- **발음 듣기**(TTS, ja-JP) · **다크 모드**

## 바로 보기 / 배포
- 로컬: `index.html` 더블클릭
- 링크: https://claude.ai/artifact/LgCMubWBk9qs6HyAaMqn16 (`?k=日` 로 특정 한자 바로 열기)
- 배포 중: https://easyseop.github.io (레포 `easyseop/easyseop.github.io` 의 `index.html`을 덮어쓰면 갱신)

## 데이터 출처 & 라이선스
- 읽기·획수·JLPT 등급·영어 의미: 공개 데이터셋 [davidluzgouveia/kanji-data](https://github.com/davidluzgouveia/kanji-data) (KANJIDIC2/JMdict 기반, EDRDG)
- 한국어 훈음·어원 해설·암기 꿀팁·예시 번역: 직접 작성
- 획순 SVG: [KanjiVG](https://github.com/KanjiVG/kanjivg) (CC BY-SA, 런타임 로드)

## 빌드 (콘텐츠 갱신 시)
데이터를 수정하면 아래로 `index.html`을 재생성합니다.

```bash
python3 build.py   # facts.json + ko.py + rich.py + tips.py -> index.html
```

- `facts.json` : 979자 읽기/획수/등급/영어뜻 (공개 데이터에서 추출)
- `ko.py` : 979자 한국어 훈음 `KO = {한자: "훈 음"}`
- `rich.py` : 어원 해설 + 음독/훈독 대표단어 `RICH = {한자: {...}}`
- `tips.py` : 한자별 암기 꿀팁(연상법) `TIPS = {한자: "..."}`
- `template.html` : UI 템플릿(`/*__DATA__*/` 자리에 데이터 주입)

## 진행 현황
| 등급 | 자수 | 훈음 | 상세(어원+예시) | 꿀팁 |
|---|---|---|---|---|
| N5 | 80 | ✅ | ✅ | ✅ |
| N4 | 166 | ✅ | ✅ | ✅ |
| N3 | 368 | ✅ | ✅ | ✅ |
| N2 | 370 | ✅ | ✅ | ✅ |
| **합계** | **984** | **984** | **984** | **984** |

- ✅ **전 등급 완료** (데이터셋에 등급이 비어 있던 分·身·丈·寿·叱 5자 수동 추가)
- 자세한 이어가기 방법은 [`HANDOFF.md`](HANDOFF.md) 참고
