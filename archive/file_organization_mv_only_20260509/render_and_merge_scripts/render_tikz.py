import os
import subprocess

def render_tikz(filename, output_name):
    tex_content = f"""\\documentclass[tikz,border=2mm]{{standalone}}
\\usepackage{{amsmath,amssymb}}
\\usepackage{{mathptmx}}
\\usetikzlibrary{{arrows.meta,positioning,fit,calc}}
\\begin{{document}}
\\input{{{filename}}}
\\end{{document}}
"""
    with open("temp_render.tex", "w") as f:
        f.write(tex_content)

    subprocess.run(["tectonic", "temp_render.tex"])
    if os.path.exists("temp_render.pdf"):
        os.rename("temp_render.pdf", output_name)
        print(f"Rendered {output_name}")
    else:
        print(f"Failed to render {filename}")

os.chdir("/home/qiaosir/projects/compute_vit/paper/latex_gpt/")
render_tikz("supplementary/figS1_asymmetry_concept_tikz.tex", "figS1_test.pdf")
render_tikz("supplementary/figS2_nonideality_tikz.tex", "figS2_test.pdf")
