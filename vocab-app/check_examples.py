# -*- coding: utf-8 -*-
"""예문 파일 검사기.  사용: python3 check_examples.py CH1   (examples/ch1.py 검사)

예문 형식 (examples/chN.py)
EX = {
  "歩く|あるく": [
    {"jp": "毎朝(まいあさ)、駅(えき)まで【歩(ある)いて】います。", "ko": "매일 아침 역까지 걸어가요.", "form": "歩く → 歩いて (て형 + いる: ~하고 있다)"},
    ...
  ],
}
- 한자 뒤에는 반드시 (히라가나 읽기). 한자 덩어리 단위로: 駅(えき), 毎朝(まいあさ), 歩(ある)いて
- 공부할 단어(활용된 모양 그대로)를 【 】로 정확히 한 번 감싼다
- 동사·い형용사·な형용사는 예문 2개 이상(서로 다른 활용형), 나머지는 1개 이상
"""
import re, sys, importlib.util, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from words import WORDS

KANJI = r'[一-鿿々]'
RUBY = re.compile(r'(' + KANJI + r'+)\(([ぁ-ゟー]+)\)')


def plain(s):
    return RUBY.sub(r'\1', s).replace('【', '').replace('】', '')


def check(ch):
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'examples', ch.lower() + '.py')
    spec = importlib.util.spec_from_file_location('ex_' + ch, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    EX = mod.EX
    words = [w for w in WORDS if w[4] == ch]
    keys = {f"{w}|{r}": (w, r, ko, t) for (w, r, ko, t, c) in words}
    errs = []
    for k in keys:
        if k not in EX:
            errs.append(f"누락: {k}")
    for k, exs in EX.items():
        if k not in keys:
            errs.append(f"단어 목록에 없는 키: {k}")
            continue
        w, r, ko, t = keys[k]
        need = 2 if t in ('동사', 'い형용사', 'な형용사') else 1
        if not isinstance(exs, list) or len(exs) < need:
            errs.append(f"{k}: 예문 {need}개 이상 필요")
            continue
        for e in exs:
            jp = e.get('jp', '')
            if not e.get('ko') or 'form' not in e:
                errs.append(f"{k}: ko/form 키 누락")
            if jp.count('【') != 1 or jp.count('】') != 1 or jp.index('【') > jp.index('】'):
                errs.append(f"{k}: 【】가 정확히 한 쌍이어야 함 → {jp}")
                continue
            if re.search(r'\((?![ぁ-ゟー]+\))', jp) or re.search(r'(?<!' + KANJI + r')\(', jp):
                errs.append(f"{k}: 괄호는 한자 바로 뒤 (히라가나)만 → {jp}")
            rest = RUBY.sub('', jp)
            if re.search(KANJI, rest):
                errs.append(f"{k}: 읽기 없는 한자 있음 → {jp}")
            tgt = plain(jp[jp.index('【') + 1:jp.index('】')])
            if w[0] not in tgt:
                errs.append(f"{k}: 【】 안에 단어가 안 보임 → {tgt}")
            if len(plain(jp)) > 45:
                errs.append(f"{k}: 문장이 너무 김({len(plain(jp))}자)")
    return errs, len(keys), sum(len(v) for v in EX.values())


if __name__ == '__main__':
    ch = sys.argv[1]
    errs, n, m = check(ch)
    for e in errs:
        print(e)
    print(f"{ch}: 단어 {n}개 / 예문 {m}개 / 오류 {len(errs)}개")
    sys.exit(1 if errs else 0)
