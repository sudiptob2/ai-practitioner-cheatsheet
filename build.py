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
    '  <a href="flashcards.html" style="--c:var(--fg)">Flashcards</a>')

FAB = '''<a href="flashcards.html" class="fab" aria-label="Open flashcards" title="Flashcards">
<img src="logo.svg" alt="" width="28" height="28"><span>Flashcards</span></a>
<style>
.fab { position: fixed; z-index: 30;
  right: calc(18px + env(safe-area-inset-right, 0px));
  bottom: calc(18px + env(safe-area-inset-bottom, 0px));
  display: flex; align-items: center; gap: 9px;
  padding: 11px 16px; border-radius: 16px;
  background: var(--fg); color: #fff; text-decoration: none;
  font-family: var(--mono); font-size: 12px; font-weight: 700; letter-spacing: 1px; text-transform: uppercase;
  box-shadow: 0 4px 14px rgba(28, 36, 50, 0.35);
  transition: transform 0.08s ease; }
.fab:hover { transform: translateY(-2px); }
.fab:active { transform: scale(0.97); }
@media (max-width: 520px) { .fab span { display: none; } .fab { padding: 12px; border-radius: 50%; } }
</style>'''

html = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="One-page community cheatsheet for the AWS Certified AI Practitioner exam (AIF-C01).">
<meta name="theme-color" content="#ffffff">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" type="image/svg+xml" href="logo.svg">
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
