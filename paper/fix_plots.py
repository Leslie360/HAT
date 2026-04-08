import re

with open("paper/plot_paper_figures.py", "r") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    # Fix repeated edgecolor and linewidth
    if 'edgecolor="white"' in line and "edgecolor='#222222'" in line:
        lines[i] = line.replace(', edgecolor="white", linewidth=0.8, zorder=3, edgecolor=\'#222222\', linewidth=0.8', ', edgecolor="#222222", linewidth=1.0, zorder=3')
    elif 'edgecolor="white"' in line and "edgecolor=" in line:
        # Generic fix for any line that has two edgecolors
        # We'll just carefully strip the second one or replace the first
        match = re.search(r"^(.*?)(edgecolor=.*?)(edgecolor=.*?)$", line)
        if match:
            # If we find this, we'll need to be careful
            pass

    # Specifically line 990:
    if "edgecolor" in line and line.count("edgecolor") > 1:
        # Strip the last occurrence
        line = re.sub(r", edgecolor='#222222', linewidth=0.8", "", line)
        # And make sure the first occurrence is dark
        line = line.replace('edgecolor="white"', 'edgecolor="#222222"')
        line = line.replace('linewidth=0.8', 'linewidth=1.0')
        lines[i] = line

with open("paper/plot_paper_figures.py", "w") as f:
    f.writelines(lines)
