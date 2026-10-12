# -*- coding: utf-8 -*-
"""words.py -> 단일 index.html 생성"""
import json
from words import WORDS

# 한자앱 링크: 단어 속 한자를 클릭하면 해당 한자 상세로 이동
KANJI_URL = "https://claude.ai/artifact/LgCMubWBk9qs6HyAaMqn16"
try:
    kf = json.load(open('../kanji-app/facts.json', encoding='utf-8'))
    KSET = sorted(kf.keys())
except FileNotFoundError:
    KSET = []
    print("⚠️ kanji-app/facts.json 없음 - 한자 링크 비활성화")

items = [{'w': w, 'r': r, 'ko': ko, 't': t, 'ch': ch} for (w, r, ko, t, ch) in WORDS]

# 중복 검사 (표기+읽기 기준)
seen, dup = set(), []
for e in items:
    k = (e['w'], e['r'])
    if k in seen:
        dup.append(e['w'])
    seen.add(k)
if dup:
    print("⚠️ 중복:", ", ".join(dup))

from collections import Counter
print("총", len(items), "단어 /", dict(Counter(e['t'] for e in items)))

data_js = ('window.KURL=' + json.dumps(KANJI_URL) + ';'
           + 'window.KSET=new Set(' + json.dumps("".join(KSET), ensure_ascii=False) + ');'
           + 'window.WORDS=' + json.dumps(items, ensure_ascii=False, separators=(',', ':')) + ';'
           + 'const WORDS=window.WORDS,KURL=window.KURL,KSET=window.KSET;')
tpl = open('template.html', encoding='utf-8').read()
open('index.html', 'w', encoding='utf-8').write(tpl.replace('/*__DATA__*/', data_js))
print("한자 링크:", len(KSET), "자")
print("wrote index.html")
