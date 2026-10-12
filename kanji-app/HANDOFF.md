# 인수인계 (HANDOFF)

다른 세션에서 이 프로젝트를 이어받을 때 읽는 문서입니다.

## 1. 어디에 있나

| 항목 | 값 |
|---|---|
| 레포 | `easyseop/BOJ-Programmers` |
| 브랜치 | `claude/vibrant-franklin-7mmx4f` |
| 폴더 | `kanji-app/` |
| 배포처 | https://easyseop.github.io (별도 레포 `easyseop/easyseop.github.io`) |

> ⚠️ 배포는 **수동**입니다. `kanji-app/index.html`을 `easyseop.github.io` 레포 루트에
> 덮어써야 사이트가 갱신됩니다. (현재 세션의 GitHub 권한은 `BOJ-Programmers`에만 있어 자동 배포 불가)

## 2. 코드 구조

```
kanji-app/
├─ index.html      ← 빌드 산출물. 이 파일 하나만 열면 앱이 동작 (데이터가 안에 박혀 있음)
├─ build.py        ← facts.json + ko.py + rich.py + tips.py → index.html
├─ template.html   ← UI 템플릿. `/*__DATA__*/` 자리에 `window.KANJI=[...]` 주입
├─ facts.json      ← 979자 {level, strokes, on, kun, meanings}
├─ ko.py           ← KO  = {한자: "훈 음"}            (한국어 훈음)
├─ rich.py         ← RICH= {한자: {shape, onNote, onWords, kunNote, kunWords}}
└─ tips.py         ← TIPS= {한자: "암기 꿀팁 한 줄"}
```

**수정은 항상 소스 4개(`facts.json`/`ko.py`/`rich.py`/`tips.py`) 또는 `template.html`에서 하고,
`python3 build.py`로 `index.html`을 재생성합니다. `index.html`을 직접 고치지 마세요.**

### rich.py 한 항목 형식
```python
"半":{"shape":["半은 소(牛)를 둘로 가른 모습에서 “절반”을 나타냅니다."],
  "onNote":"보통 ハン으로 읽습니다.",
  "onWords":[{"r":"ハン","words":[["半","はん","分","ぶん","절반"],["前","ぜん","半","はん","전반"]]}],
  "kunNote":"",
  "kunWords":[{"r":"なか","words":[["半","なか","ば","ば","중간/절반"]]}]},
```
- 단어 = `[앞표기, 앞후리가나, 뒤표기, 뒤후리가나, 한국어뜻]` (두 덩이로 쪼개 루비 표시)
- 한 덩이뿐이면 뒤 두 칸을 `""`로: `["石","いし","","","돌"]`
- 음독/훈독이 거의 안 쓰이면 `"onWords":[]` + `"onNote":"음독은 거의 쓰이지 않습니다."`

## 3. 진행 현황

| 등급 | 자수 | 훈음 | 상세 | 꿀팁 |
|---|---|---|---|---|
| N5 | 79 | ✅ | ✅ | ✅ |
| N4 | 166 | ✅ | ✅ | ✅ |
| N3 | 367 | ✅ | ✅ | ✅ |
| N2 | 367 | ✅ | 🔄 190 | 🔄 190 |

**남은 일: N2 상세+꿀팁 177자** (배치 3/4 → 90자, 배치 4/4 → 87자)

### 배치 3 (90자)
```
占胃悩昇濃極逆巨庫児凍幼清録券移並乾欧臣略航板詰照快版預延翌符編普掃泥棒孫帯粉菜貨陸均採永液績複党卵捨汚机簡誌宝尊敬灰砂著蒸蔵装裏諸臓純紅拝劇承損枝測講紹介湖銅油旧姓貿将伸幅甘換療
```
### 배치 4 (87자)
```
般依漁募患湾爆跡香兆齢刊傾奥贈超雇片群埋駐柱鋭殿薄伺炭包衣鉱双床掘泊荒袋珍籍刷封筒柔沈辛匹叫涙缶粒塔肌舟曇磨湿硬鈍涼零綿帽憎滴畳畜溶踊賢灯咲塗召挟枯沸濯燥瓶耕肯脂膚軒軟郊隅隻
```

## 4. 작업 루틴 (매 배치마다)

```bash
cd kanji-app
# 1) rich.py 끝의 닫는 `}` 앞에 새 항목 추가
# 2) tips.py 끝의 닫는 `}` 앞에 같은 한자들의 꿀팁 추가
# 3) 검증 + 빌드
python3 - <<'PY'
import json,re
from collections import Counter
f=json.load(open('facts.json'))
ns={}; exec(compile(open('rich.py').read(),'rich.py','exec'),ns); R=set(ns['RICH'])
ts={}; exec(compile(open('tips.py').read(),'tips.py','exec'),ts); T=set(ts['TIPS'])
n2=[k for k,v in f.items() if v['level']=='N2']
print("N2 상세",len([k for k in n2 if k in R]),"/367  꿀팁",len([k for k in n2 if k in T]),"/367")
print("rich 중복:",{k:c for k,c in Counter(re.findall(r'\n "(.)":\{',open('rich.py').read())).items() if c>1})
print("tips 중복:",{k:c for k,c in Counter(re.findall(r'\n "(.)":"',open('tips.py').read())).items() if c>1})
PY
python3 build.py
# 4) JS 문법 검증
python3 -c "h=open('index.html').read();open('_c.js','w').write(h.split('<script>')[1].split('</script>')[0])"
node --check _c.js && echo "JS OK"; rm -f _c.js
# 5) 커밋 & 푸시
git add kanji-app && git commit -m "..." && git push origin claude/vibrant-franklin-7mmx4f
```

**주의:** `rich.py`/`tips.py`에 **같은 한자를 두 번 넣지 마세요.** (위 중복 검사로 꼭 확인)

## 5. 데이터 보충이 필요할 때

원본 데이터셋(N1까지 포함, 13,108자):
```bash
curl -sSL -o kd.json https://raw.githubusercontent.com/davidluzgouveia/kanji-data/master/kanji.json
```
- `jsdelivr`는 네트워크 정책에 막힘 → **`raw.githubusercontent.com` 사용**
- `jlpt_new` 필드: 5/4/3/2/1
- facts.json 형식 변환: 음독 히라가나→가타카나, 훈독 앞뒤 `-` 제거, 중복 제거

## 6. 알려진 이슈 / 메모
- **배포가 안 바뀐다**는 문의가 잦음 → 대부분 (a) 새 `index.html` 업로드 안 함, (b) 사파리 캐시.
  새 버전 확인법: 검색창 안내문에 `nichi`가 있거나, 등급 필터에 **N2 칩**이 보이면 최신.
- `咲`(필/웃을 소)는 N2에 포함되어 있음.
- 로마자 검색은 헵번식·훈령식 둘 다 지원 (`shi`/`si`, `sha`/`sya`, `tsu`/`tu`).
