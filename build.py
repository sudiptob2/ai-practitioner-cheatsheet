#!/usr/bin/env python3
"""Wrap the cheatsheet source into a standalone index.html with PWA tags.

Usage: python3 build.py [path-to-source-html]
The source is the artifact-format page (starts with <title>, no doctype).
"""
import pathlib
import sys

SRC = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path('cheatsheet-src.html')
OUT = pathlib.Path(__file__).parent / 'index.html'

src = SRC.read_text()
src = src.replace('<meta name="claude:viewport-fit-sides" content="cover">\n', '')
head_part, body_part = src.split('</style>', 1)
head_part += '</style>'
body_part = body_part.replace(
    '<a href="#answers" style="--c:var(--exam)">Fast answers</a>',
    '<a href="#answers" style="--c:var(--exam)">Fast answers</a>\n'
    '  <a href="flashcards.html" style="--c:var(--fg)">Flashcards →</a>')

FAB = '''<a href="flashcards.html" class="fab" aria-label="Open flashcards" title="Flashcards">
<svg viewBox="0 0 24 24" width="26" height="26" aria-hidden="true" fill="none" stroke="#fff" stroke-width="2" stroke-linejoin="round">
<rect x="3" y="7" width="13" height="14" rx="2"/>
<path d="M8 7V5a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2h-2"/>
</svg></a>
<style>
.fab { position: fixed; z-index: 30;
  right: calc(18px + env(safe-area-inset-right, 0px));
  bottom: calc(18px + env(safe-area-inset-bottom, 0px));
  width: 56px; height: 56px; border-radius: 50%;
  background: var(--fg); display: flex; align-items: center; justify-content: center;
  box-shadow: 0 4px 14px rgba(28, 36, 50, 0.35); }
.fab:hover { background: var(--svc); }
</style>'''

html = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="One-page community cheatsheet for the AWS Certified AI Practitioner exam (AIF-C01).">
<meta name="theme-color" content="#ffffff">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" href="icon-192.png">
<link rel="apple-touch-icon" href="icon-192.png">
{head_part}
<style>body{{margin:0}}img{{max-width:100%}}</style>
</head>
<body>
{body_part}
{FAB}
<script>try {{ navigator.serviceWorker && navigator.serviceWorker.register('sw.js'); }} catch (e) {{}}</script>
</body>
</html>
'''
OUT.write_text(html)
print(f'wrote {OUT} ({len(html)} bytes)')
