#!/usr/bin/env python3
"""
Pre-send check for a CV or cover letter (.docx).

Reports four things:
  1. Hidden content  - hidden or white text, tiny fonts, watermarks, shapes,
                       comments, tracked changes, invisible Unicode characters.
  2. Metadata        - author, title, company, template name, custom properties
                       (CV services often leave tracking IDs here).
  3. ATS structure   - tables, text boxes, images, contact details in headers
                       or footers, odd characters some parsers mangle.
  4. Writing signals - stock phrases and patterns that make text read as
                       generic or machine-written. These are prompts for a
                       human rewrite, not proof of anything.

Usage:  python docx_check.py FILE.docx [FILE2.docx ...]
Requires: python-docx
"""
import re, sys, zipfile, unicodedata
import docx

STOCK_PHRASES = [
    'delve', 'leverage', 'leveraging', 'seamless', 'seamlessly', 'robust', 'cutting-edge',
    'landscape', 'tapestry', 'furthermore', 'moreover', 'in conclusion', 'passionate',
    'synergy', 'spearhead', 'pivotal', 'holistic', 'game-changer', 'navigate the',
    'realm', 'excited to apply', 'thrilled', 'i am confident that', 'unwavering',
    'testament to', 'foster', 'elevate', 'empower', 'underscore', 'journey',
    'proven track record', 'results-driven', 'team player', 'go-getter', 'meticulous',
    'dynamic professional', 'perfect fit', 'ever-evolving', 'fast-paced world',
    'i believe my skills', 'align perfectly', 'i would be a great asset',
    'hard-working', 'detail-oriented', 'think outside the box',
]
CONTRAST_PATTERNS = [
    (r'\brather than\b', '"rather than" contrast'),
    (r'\bnot (?:just|only|merely) [^.]{1,60}?,? but\b', '"not just X but Y"'),
    (r'\bwas never the hard part\b|\bthe hard part was\b', '"the hard part was" framing'),
    (r'\bby design\b', '"by design" flourish'),
]
INVISIBLE = {'​', '‌', '‍', '⁠', '﻿', '­'}
ODD_FOR_ATS = {'│': 'box-drawing bar', '—': 'em dash', '': 'private-use bullet'}


def check(path):
    print('=' * 70)
    print(path)
    print('=' * 70)
    z = zipfile.ZipFile(path)
    names = z.namelist()
    xml = {n: z.read(n).decode('utf-8', 'ignore') for n in names if n.endswith('.xml') or n.endswith('.rels')}
    issues, warns = [], []

    # ---- 1. hidden content
    body_parts = [n for n in xml if n.startswith('word/') and n.endswith('.xml')]
    joined = '\n'.join(xml[n] for n in body_parts)
    checks = {
        'hidden text (w:vanish)': r'<w:vanish/>|<w:vanish w:val="(?:1|true)"',
        'white text': r'<w:color w:val="(?:FFFFFF|ffffff)"',
        'tiny font (<= 2pt)': r'<w:sz w:val="[1-4]"/>',
        'watermark / WordArt': r'(?i)watermark|PowerPlusWaterMarkObject|WordArt',
        'page background': r'<w:background ',
        'tracked insertions/deletions': r'<w:ins |<w:del ',
    }
    for label, pat in checks.items():
        n = len(re.findall(pat, joined))
        if n:
            issues.append(f'{label}: {n}')
    comments = xml.get('word/comments.xml', '')
    nc = len(re.findall(r'<w:comment ', comments))
    if nc:
        issues.append(f'comments: {nc}')

    d = docx.Document(path)
    text = '\n'.join(p.text for p in d.paragraphs)
    for t in d.tables:
        for row in t.rows:
            text += '\n' + ' | '.join(c.text for c in row.cells)
    inv = sum(text.count(c) for c in INVISIBLE)
    if inv:
        issues.append(f'invisible Unicode characters: {inv}')

    # ---- 2. metadata
    cp = d.core_properties
    meta = {'title': cp.title, 'author': cp.author, 'last modified by': cp.last_modified_by,
            'revision': cp.revision, 'comments field': cp.comments, 'keywords': cp.keywords}
    app = xml.get('docProps/app.xml', '')
    for tag in ('Company', 'Manager', 'Template'):
        m = re.search(fr'<{tag}>(.*?)</{tag}>', app)
        if m and m.group(1).strip() and m.group(1).strip() not in ('Normal', 'Normal.dotm'):
            meta[tag.lower()] = m.group(1)
    custom = xml.get('docProps/custom.xml', '')
    props = re.findall(r'<property [^>]*name="([^"]+)"[^>]*>.*?<vt:[a-z0-9]+>(.*?)</vt:', custom, re.S)

    # ---- 3. ATS structure
    if d.tables:
        warns.append(f'{len(d.tables)} table(s): some ATS parsers read tables out of order')
    if re.search(r'<w:txbxContent', joined):
        warns.append('text box(es): many ATS parsers skip text inside text boxes')
    if re.search(r'<w:drawing>|<w:pict>', xml.get('word/document.xml', '')):
        warns.append('image(s) or shapes in body')
    if re.search(r'<w:cols w:num="[2-9]"', joined):
        warns.append('multi-column layout: parsers may interleave columns')
    for n in body_parts:
        if re.match(r'word/(header|footer)\d*\.xml', n):
            ht = ' '.join(re.findall(r'<w:t[^>]*>(.*?)</w:t>', xml[n]))
            if re.search(r'@|\+?\d[\d ]{7,}|linkedin', ht, re.I):
                warns.append(f'contact details inside {n}: some ATS ignore headers/footers')
    for ch, label in ODD_FOR_ATS.items():
        if ch in text:
            warns.append(f'{label} ({text.count(ch)}x): replace with a plain character')

    # ---- 4. writing signals
    low = text.lower()
    stock = [w for w in STOCK_PHRASES if w in low]
    contrasts = [(lbl, len(re.findall(p, low))) for p, lbl in CONTRAST_PATTERNS]
    contrasts = [(l, n) for l, n in contrasts if n]
    sents = [s for s in re.split(r'(?<=[.!?])\s+|\n+', text) if len(s.split()) > 3 and '\u2022' not in s]
    lens = [len(s.split()) for s in sents]

    # ---- report
    print('\n[1] HIDDEN CONTENT')
    print('    ' + ('\n    '.join(issues) if issues else 'none found'))
    print('\n[2] METADATA')
    for k, v in meta.items():
        print(f'    {k}: {v!r}')
    if props:
        print('    custom properties (remove before sending):')
        for k, v in props:
            print(f'      {k} = {v}')
    else:
        print('    custom properties: none')
    print('\n[3] ATS STRUCTURE')
    print('    ' + ('\n    '.join(warns) if warns else 'no structural problems found'))
    print('\n[4] WRITING SIGNALS (review, then rewrite in the candidate\'s own words)')
    print(f'    stock phrases: {", ".join(stock) if stock else "none"}')
    print(f'    contrast patterns: {", ".join(f"{l} x{n}" for l, n in contrasts) if contrasts else "none"}')
    if lens:
        long = [s for s in sents if len(s.split()) > 45]
        print(f'    sentences: {len(lens)}, shortest {min(lens)}, longest {max(lens)}, '
              f'average {sum(lens) / len(lens):.0f} words')
        for s in long[:3]:
            print(f'      long sentence ({len(s.split())} words): {s[:90]}...')
    print(f'    word count: {len(text.split())}')
    print()
    return not issues and not props


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    ok = all([check(p) for p in sys.argv[1:]])
    sys.exit(0 if ok else 1)
