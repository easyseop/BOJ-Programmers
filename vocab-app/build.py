# -*- coding: utf-8 -*-
"""words.py -> 단일 index.html 생성"""
import json
from words import WORDS

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

data_js = 'window.WORDS=' + json.dumps(items, ensure_ascii=False, separators=(',', ':')) + ';const WORDS=window.WORDS;'
tpl = open('template.html', encoding='utf-8').read()
open('index.html', 'w', encoding='utf-8').write(tpl.replace('/*__DATA__*/', data_js))
print("wrote index.html")
