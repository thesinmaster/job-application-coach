#!/usr/bin/env python3
"""
Edit a candidate's own .docx CV without breaking its formatting.

Word splits text into many small "runs", so a plain find/replace often misses
text that looks continuous on screen. This tool first merges adjacent runs that
share identical formatting, then applies a list of edit operations.

Usage:
    python docx_tools.py IN.docx OUT.docx OPS.json
    python docx_tools.py IN.docx --dump            # list paragraphs with index

OPS.json is a list of operations, applied in order:
    {"op": "replace",     "old": "exact text", "new": "new text"}
    {"op": "set",         "anchor": "unique text in paragraph", "text": "whole new paragraph text"}
    {"op": "set_two_part","anchor": "...", "left": "Company - Title", "right": "Jan 2020 - Present | City"}
    {"op": "clone_after", "anchor": "...", "text": "new paragraph with the same style (e.g. a bullet)"}
    {"op": "drop",        "anchor": "..."}
    {"op": "metadata",    "author": "First Last", "title": "First Last CV"}

Every anchor / old text must match exactly once. If any operation fails,
nothing is written and the script exits with code 1.
Requires: python-docx (pip install python-docx)
"""
import copy, json, re, sys, zipfile, shutil
import docx
from docx.oxml.ns import qn
from docx.text.paragraph import Paragraph
from docx.text.run import Run

W_R, W_T, W_RPR = qn('w:r'), qn('w:t'), qn('w:rPr')
SIMPLE_CHILDREN = {W_RPR, W_T}


# ---------------------------------------------------------------- run merging
def _rpr_key(r):
    rpr = r.find(W_RPR)
    if rpr is None:
        return b''
    rpr = copy.deepcopy(rpr)
    for el in rpr.iter():
        for a in list(el.attrib):
            if 'rsid' in a:
                del el.attrib[a]
    from lxml import etree
    return etree.tostring(rpr)


def _is_simple(r):
    return all(c.tag in SIMPLE_CHILDREN for c in r) and r.find(W_T) is not None


def merge_runs(document):
    body = document.element.body
    for pe in list(body.iter(qn('w:proofErr'))):
        pe.getparent().remove(pe)
    for container in list(body.iter(qn('w:p'))) + list(body.iter(qn('w:hyperlink'))):
        runs = [c for c in container if c.tag == W_R]
        prev = None
        for r in runs:
            if prev is not None and r.getprevious() is prev and _is_simple(prev) and _is_simple(r) \
                    and _rpr_key(prev) == _rpr_key(r):
                pt, rt = prev.find(W_T), r.find(W_T)
                pt.text = (pt.text or '') + (rt.text or '')
                pt.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
                container.remove(r)
                continue
            prev = r


# ---------------------------------------------------------------- helpers
def paragraphs(document):
    return [Paragraph(p, document) for p in document.element.body.iter(qn('w:p'))]


def all_runs(p):
    return [Run(r, p) for r in p._p.iter(W_R)]


def text_of(p):
    return ''.join(t.text or '' for t in p._p.iter(W_T))


def find_one(document, anchor):
    hits = [p for p in paragraphs(document) if anchor in text_of(p)]
    if len(hits) != 1:
        raise ValueError(f'anchor matched {len(hits)} paragraphs: {anchor[:60]!r}')
    return hits[0]


def set_text(p, text):
    rs = [r for r in all_runs(p) if r._r.find(W_T) is not None]
    if not rs:
        raise ValueError('paragraph has no text runs')
    for i, r in enumerate(rs):
        r.text = text if i == 0 else ''


def set_two_part(p, left, right):
    left_done = right_done = False
    for r in all_runs(p):
        t = r.text
        if t != '' and t.strip() == '':
            continue
        if r.bold:
            r.text = '' if left_done else left
            left_done = True
        else:
            r.text = '' if right_done else right
            right_done = True
    if not (left_done and right_done):
        raise ValueError('paragraph does not have a bold part and a plain part')


def replace_text(document, old, new):
    hits = []
    for p in paragraphs(document):
        for r in all_runs(p):
            if old in r.text:
                hits.append(r)
    if len(hits) != 1:
        total = sum(text_of(p).count(old) for p in paragraphs(document))
        raise ValueError(f'"replace" found {len(hits)} runs ({total} in text): {old[:60]!r} '
                         '(if text spans different formatting, use "set" on the paragraph)')
    hits[0].text = hits[0].text.replace(old, new, 1)


def clone_after(p, text):
    new = copy.deepcopy(p._p)
    for a in list(new.attrib):
        if 'paraId' in a or 'textId' in a:
            del new.attrib[a]
    p._p.addnext(new)
    set_text(Paragraph(new, p._parent), text)


def drop(p):
    p._p.getparent().remove(p._p)


def strip_package_metadata(path):
    """Remove custom properties (template / tracking IDs), company and manager fields."""
    tmp = path + '.tmp'
    with zipfile.ZipFile(path) as zin, zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename == 'docProps/custom.xml':
                data = re.sub(rb'<property .*?</property>', b'', data, flags=re.S)
            elif item.filename == 'docProps/app.xml':
                data = re.sub(rb'<Company>.*?</Company>', b'<Company></Company>', data)
                data = re.sub(rb'<Manager>.*?</Manager>', b'<Manager></Manager>', data)
            zout.writestr(item, data)
    shutil.move(tmp, path)


# ---------------------------------------------------------------- main
def main():
    if len(sys.argv) == 3 and sys.argv[2] == '--dump':
        d = docx.Document(sys.argv[1])
        merge_runs(d)
        for i, p in enumerate(paragraphs(d)):
            t = text_of(p)
            if t.strip():
                print(f'{i:3d} [{p.style.name}] {t}')
        return
    if len(sys.argv) != 4:
        print(__doc__)
        sys.exit(2)
    src, out, ops_path = sys.argv[1:]
    ops = json.load(open(ops_path, encoding='utf-8'))
    d = docx.Document(src)
    merge_runs(d)
    meta = None
    errors = []
    for n, op in enumerate(ops, 1):
        try:
            kind = op['op']
            if kind == 'replace':
                replace_text(d, op['old'], op['new'])
            elif kind == 'set':
                set_text(find_one(d, op['anchor']), op['text'])
            elif kind == 'set_two_part':
                set_two_part(find_one(d, op['anchor']), op['left'], op['right'])
            elif kind == 'clone_after':
                clone_after(find_one(d, op['anchor']), op['text'])
            elif kind == 'drop':
                drop(find_one(d, op['anchor']))
            elif kind == 'metadata':
                meta = op
            else:
                raise ValueError(f'unknown op {kind!r}')
        except Exception as e:
            errors.append(f'op {n} ({op.get("op")}): {e}')
    if errors:
        print('NOTHING WRITTEN. Fix these and run again:')
        for e in errors:
            print('  -', e)
        sys.exit(1)
    if meta:
        cp = d.core_properties
        cp.author = cp.last_modified_by = meta.get('author', '')
        cp.title = meta.get('title', '')
        cp.comments = cp.subject = cp.keywords = cp.category = ''
        cp.revision = 1
    d.save(out)
    if meta:
        strip_package_metadata(out)
    print(f'ok: {len(ops)} operations applied -> {out}')


if __name__ == '__main__':
    try:
        main()
    except BrokenPipeError:
        pass
