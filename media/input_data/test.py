import os
import pandas as pd
from pathlib import Path
from weasyprint import HTML


dir_path = Path(__file__).parent
df = pd.read_csv("hf://datasets/opensporks/resumes/Resume/Resume.csv")

example = df.loc[0, "Resume_html"]
pdf_file = HTML(string=example).write_pdf()
file_path = os.path.join(dir_path, "resumes", "0.pdf")

with open(file_path, "wb") as f:
    f.write(pdf_file)
