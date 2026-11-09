#!/usr/bin/env python3
"""
Compare a job posting with a CV and list the posting's terms the CV does not use.

The output is a prompt for judgement, not a to-do list: add a missing term to the
CV only if the candidate genuinely has that experience. A term the candidate
does not have stays out, and becomes an interview-preparation topic instead.

Usage:
    python keyword_gap.py POSTING.txt CV.docx [--terms "term one, term two"]

Recommended: pass the posting's requirement terms explicitly with --terms
(Claude extracts them from the requirement bullets). Without --terms the script
falls back to rough automatic extraction; add --auto to combine both.
Requires: python-docx
"""
import re, sys, argparse, collections
import docx

STOP = set('''a an and or the of to in on for with by at from as is are be been being this that these those
it its into across our your their we you they he she will would can could should may might must not no
all any each other such than then so very more most also well both either neither per via etc
experience experienced years year strong ability skills skill knowledge proven excellent good including
role position candidate team work working within ensure ensuring support supporting lead leading manage
managing management key new across related relevant preferred required requirements responsibilities
what ll about job our help future less believe benefits benefit join us make makes making real every
day best world first right thing things way ways people person someone want wants need needs like
learn learning shape great opportunity opportunities apply applying offer offers provide providing
significant meaningful actionable nice-to-haves must-haves bring brings own owning drive driving deliver
delivering create creating build building maintain maintaining across through while where when which who
ve ile bir bu için olan da de en az veya ya ile ilgili tercihen sahip deneyimli konusunda gibi olarak
'''.split())


def extract_terms(text, top=35):
    grams = collections.Counter()
    for clause in re.split(r'[\n.,;:()\u2022\-\u2013\u2014!?]+', text):
        words = re.findall(r"[A-Za-zÀ-ÿĞğİıŞşÇçÖöÜü][A-Za-zÀ-ÿĞğİıŞşÇçÖöÜü&/+]*", clause)
        toks = [w.lower() for w in words]
        for n in (1, 2, 3):
            for i in range(len(toks) - n + 1):
                g = toks[i:i + n]
                if g[0] in STOP or g[-1] in STOP or any(len(t) < 2 for t in g):
                    continue
                if n > 1 and sum(t in STOP for t in g) > 1:
                    continue
                if n == 1 and len(g[0]) < 4:
                    continue
                grams[' '.join(g)] += 1
    # prefer multi-word phrases, drop single words already covered by a kept phrase
    ranked = sorted(grams.items(), key=lambda kv: (-kv[1] * (1 + 0.6 * kv[0].count(' ')), kv[0]))
    kept = []
    for term, _ in ranked:
        if any(term != k and term in k for k in kept):
            continue
        kept.append(term)
        if len(kept) >= top:
            break
    # acronyms (SAP, KPI, SLA, ATS...)
    acr = sorted(set(re.findall(r'\b[A-Z][A-Z0-9&]{1,6}\b', text)))
    return kept, acr


def cv_text(path):
    d = docx.Document(path)
    parts = [p.text for p in d.paragraphs]
    for t in d.tables:
        for r in t.rows:
            parts += [c.text for c in r.cells]
    return '\n'.join(parts)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('posting')
    ap.add_argument('cv')
    ap.add_argument('--terms', default='', help='comma-separated requirement terms taken from the posting')
    ap.add_argument('--auto', action='store_true', help='also add automatically extracted terms')
    a = ap.parse_args()
    jd = open(a.posting, encoding='utf-8').read()
    cv = cv_text(a.cv)
    cv_low = cv.lower()
    auto, acr = extract_terms(jd)
    if a.terms:
        terms = [t.strip().lower() for t in a.terms.split(',') if t.strip()]
        if a.auto:
            terms += [t for t in auto if t not in terms]
    else:
        terms = auto
    def found(t):
        words = t.split()
        variants = {t, ' '.join(words[:-1] + [words[-1].rstrip('s')]), t + 's'}
        return any(v and v in cv_low for v in variants)
    present = [t for t in terms if found(t)]
    missing = [t for t in terms if not found(t)]
    acr_missing = [x for x in acr if not re.search(rf'\b{re.escape(x)}\b', cv)]
    print('IN POSTING AND IN CV:')
    print('  ' + ', '.join(present) if present else '  (none)')
    print('\nIN POSTING, NOT IN CV (add only where true; otherwise prepare for the interview):')
    for t in missing:
        print('  -', t)
    print('\nACRONYMS IN POSTING, NOT IN CV:', ', '.join(acr_missing) if acr_missing else 'none')


if __name__ == '__main__':
    try:
        main()
    except BrokenPipeError:
        pass
