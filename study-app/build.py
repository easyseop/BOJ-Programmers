# -*- coding: utf-8 -*-
"""한자앱 + 단어장 + 문법 통합 빌드: kanji-app/*, vocab-app/words.py, grammar/grammar.py -> index.html"""
import json, sys, os

KA = os.path.join('..', 'kanji-app')
VA = os.path.join('..', 'vocab-app')
GA = os.path.join('..', 'grammar')
sys.path.insert(0, KA)
sys.path.insert(0, VA)
sys.path.insert(0, GA)

from ko import KO
from rich import RICH
from tips import TIPS
from words import WORDS
import grammar as GR

# ── 한자 ──
facts = json.load(open(os.path.join(KA, 'facts.json'), encoding='utf-8'))
order = {'N5': 0, 'N4': 1, 'N3': 2, 'N2': 3, 'N1': 4}
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
# 예문: ../vocab-app/examples/ch*.py 의 EX {"표기|읽기": [{jp, ko, form}, ...]}
import glob, importlib.util
EXS = {}
for fp in sorted(glob.glob(os.path.join(VA, 'examples', 'ch*.py'))):
    spec = importlib.util.spec_from_file_location(os.path.basename(fp)[:-3], fp)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    EXS.update(m.EX)
for e in words:
    ex = EXS.get(e['w'] + '|' + e['r'])
    if ex:
        e['ex'] = [{'jp': x['jp'], 'ko': x['ko'], 'form': x.get('form', '')} for x in ex]
print("예문", sum(len(e.get('ex', [])) for e in words), "개 /", sum(1 for e in words if e.get('ex')), "단어")
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
gram = {'topics': GR.TOPICS, 'items': GR.ITEMS, 'tables': GR.TABLES}
print("문법", len(GR.ITEMS), "문형 /", sum(len(i.get('q', [])) for i in GR.ITEMS), "빈칸문제")

j = lambda o: json.dumps(o, ensure_ascii=False, separators=(',', ':'))
data_js = ('window.KANJI=' + j(kanji) + ';'
           + 'window.WORDS=' + j(words) + ';'
           + 'window.GRAMMAR=' + j(gram) + ';'
           + 'const KANJI=window.KANJI,WORDS=window.WORDS;'
           + 'const KSET=new Set(KANJI.map(k=>k.char));')
tpl = open('template.html', encoding='utf-8').read()
open('index.html', 'w', encoding='utf-8').write(tpl.replace('/*__DATA__*/', data_js))
print("wrote index.html")
