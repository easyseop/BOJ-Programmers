# -*- coding: utf-8 -*-
"""한자앱 + 단어장 통합 빌드: kanji-app/*, vocab-app/words.py -> index.html"""
import json, sys, os

KA = os.path.join('..', 'kanji-app')
VA = os.path.join('..', 'vocab-app')
sys.path.insert(0, KA)
sys.path.insert(0, VA)

from ko import KO
from rich import RICH
from tips import TIPS
from words import WORDS

# ── 한자 ──
facts = json.load(open(os.path.join(KA, 'facts.json'), encoding='utf-8'))
order = {'N5': 0, 'N4': 1, 'N3': 2, 'N2': 3}
kanji, missing = [], []
for ch, f in facts.items():
    ko = KO.get(ch)
    if not ko:
        missing.append(ch)
    e = {'char': ch, 'level': f['level'], 'strokes': f['strokes'],
         'on': f['on'], 'kun': f['kun'], 'ko': ko or '', 'en': f['meanings']}
    r = RICH.get(ch)
    if r:
        e['shape'] = r['shape']
        e['onNote'] = r.get('onNote', '')
        e['onWords'] = r['onWords']
        e['kunNote'] = r.get('kunNote', '')
        e['kunWords'] = r['kunWords']
    t = TIPS.get(ch)
    if t:
        e['tip'] = t
    kanji.append(e)
kanji.sort(key=lambda e: (order[e['level']], -(e['strokes'] or 0), e['char']))
if missing:
    print("한국어 훈음 누락:", ''.join(missing))

# ── 단어 ──
words = [{'w': w, 'r': r, 'ko': ko, 't': t, 'ch': ch} for (w, r, ko, t, ch) in WORDS]
seen, dup = set(), []
for e in words:
    k = (e['w'], e['r'])
    if k in seen:
        dup.append(e['w'])
    seen.add(k)
if dup:
    print("⚠️ 단어 중복:", ", ".join(dup))

from collections import Counter
print("한자", len(kanji), "자 / 상세", sum(1 for e in kanji if 'shape' in e))
print("단어", len(words), "개 /", dict(Counter(e['t'] for e in words)))

j = lambda o: json.dumps(o, ensure_ascii=False, separators=(',', ':'))
data_js = ('window.KANJI=' + j(kanji) + ';'
           + 'window.WORDS=' + j(words) + ';'
           + 'const KANJI=window.KANJI,WORDS=window.WORDS;'
           + 'const KSET=new Set(KANJI.map(k=>k.char));')
tpl = open('template.html', encoding='utf-8').read()
open('index.html', 'w', encoding='utf-8').write(tpl.replace('/*__DATA__*/', data_js))
print("wrote index.html")
