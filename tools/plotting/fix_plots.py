import re
from pathlib import Path

path = Path(__file__).resolve().parent / "plot_paper_figures.py"
lines = path.read_text().splitlines(keepends=True)

for i, line in enumerate(lines):
    if 'edgecolor="white"' in line and "edgecolor='#222222'" in line:
        lines[i] = line.replace(', edgecolor="white", linewidth=0.8, zorder=3, edgecolor=\'#222222\', linewidth=0.8', ', edgecolor="#222222", linewidth=1.0, zorder=3')
    elif 'edgecolor="white"' in line and "edgecolor=" in line:
        match = re.search(r"^(.*?)(edgecolor=.*?)(edgecolor=.*?)$", line)
        if match:
            pass

    if "edgecolor" in line and line.count("edgecolor") > 1:
        line = re.sub(r", edgecolor='#222222', linewidth=0.8", "", line)
        line = line.replace('edgecolor="white"', 'edgecolor="#222222"')
        line = line.replace("linewidth=0.8", "linewidth=1.0")
        lines[i] = line

path.write_text("".join(lines))
