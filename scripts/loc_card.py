#!/usr/bin/env python3
"""Render a lines-of-code SVG card from cloc JSON output.
Usage: loc_card.py cloc.json REPO_COUNT > loc.svg
"""
import json
import sys
from xml.sax.saxutils import escape

COLORS = {
    "Python": "#3572A5", "JavaScript": "#f1e05a", "TypeScript": "#3178c6",
    "JSX": "#f1e05a", "TSX": "#3178c6", "Go": "#00ADD8", "Rust": "#dea584",
    "Java": "#b07219", "Kotlin": "#A97BFF", "Swift": "#F05138", "C": "#555555",
    "C++": "#f34b7d", "C/C++ Header": "#555555", "C#": "#178600",
    "PHP": "#4F5D95", "Ruby": "#701516", "Dart": "#00B4AB", "Lua": "#000080",
    "Bourne Shell": "#89e051", "Bourne Again Shell": "#89e051",
    "PowerShell": "#012456", "HTML": "#e34c26", "CSS": "#663399",
    "SCSS": "#c6538c", "Vuejs Component": "#41b883", "Svelte": "#ff3e00",
    "SQL": "#e38c00", "HCL": "#844FBA", "Dockerfile": "#384d54",
    "YAML": "#cb171e", "JSON": "#8f8f8f", "Markdown": "#083fa1",
    "Other": "#8b949e",
}
NAMES = {"Bourne Shell": "Shell", "Bourne Again Shell": "Bash",
         "Vuejs Component": "Vue", "C/C++ Header": "C/C++ Header"}
TOP_N = 6

data = json.load(open(sys.argv[1]))
repos = int(sys.argv[2]) if len(sys.argv) > 2 else 0
total = data["SUM"]["code"]

langs = sorted(
    ((k, v["code"]) for k, v in data.items() if k not in ("header", "SUM")),
    key=lambda x: -x[1],
)
shown = langs[:TOP_N]
rest = sum(c for _, c in langs[TOP_N:])
if rest:
    shown.append(("Other", rest))

W, PAD = 495, 25
BAR_W = W - 2 * PAD
rows = (len(shown) + 1) // 2
H = 140 + rows * 24

out = []
a = out.append
a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{total:,} lines of code">')
a("""<style>
text{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans',Helvetica,Arial,sans-serif}
.bg{fill:#ffffff;stroke:#d0d7de}
.title{font-size:18px;font-weight:600;fill:#2f80ed}
.total{font-size:34px;font-weight:700;fill:#1f2328}
.sub{font-size:13px;fill:#59636e}
.lang{font-size:12px;fill:#1f2328}
.pct{font-size:12px;fill:#59636e}
.track{fill:#eff2f5}
@media (prefers-color-scheme:dark){
.bg{fill:#0d1117;stroke:#30363d}.title{fill:#58a6ff}.total,.lang{fill:#e6edf3}
.sub,.pct{fill:#9198a1}.track{fill:#21262d}}
</style>""")
a(f'<rect class="bg" x="0.5" y="0.5" rx="6" width="{W-1}" height="{H-1}"/>')
a(f'<text class="title" x="{PAD}" y="38">Lines of code</text>')
a(f'<text class="total" x="{PAD}" y="84">{total:,}</text>')
if repos:
    a(f'<text class="sub" x="{W-PAD}" y="82" text-anchor="end">across {repos} repositories</text>')

# Stacked language bar
a(f'<clipPath id="bar"><rect x="{PAD}" y="102" width="{BAR_W}" height="8" rx="4"/></clipPath>')
a(f'<g clip-path="url(#bar)"><rect class="track" x="{PAD}" y="102" width="{BAR_W}" height="8"/>')
x = PAD
for name, code in shown:
    w = BAR_W * code / total
    a(f'<rect x="{x:.2f}" y="102" width="{w + 0.5:.2f}" height="8" fill="{COLORS.get(name, "#8b949e")}"/>')
    x += w
a("</g>")

# Legend, two columns
for i, (name, code) in enumerate(shown):
    col, row = i % 2, i // 2
    lx = PAD + col * (BAR_W // 2 + 10)
    ly = 142 + row * 24
    label = escape(NAMES.get(name, name))
    a(f'<circle cx="{lx + 5}" cy="{ly - 4}" r="5" fill="{COLORS.get(name, "#8b949e")}"/>')
    a(f'<text x="{lx + 16}" y="{ly}"><tspan class="lang">{label}</tspan>'
      f'<tspan class="pct" dx="6">{code / total * 100:.1f}%</tspan></text>')

a("</svg>")
print("\n".join(out))