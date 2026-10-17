"""Fit train-selected OLS and export coefficients, intervals and held-out metrics."""
from pathlib import Path
import argparse,hashlib,json,pandas as pd
from salary_model import analyze
p=argparse.ArgumentParser(description=__doc__);p.add_argument('csv',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
if a.output.exists():raise ValueError('Use a new output directory')
a.output.mkdir(parents=True);result=analyze(pd.read_csv(a.csv));result['input_sha256']=hashlib.sha256(a.csv.read_bytes()).hexdigest();result['seed']=42
(a.output/'model.json').write_text(json.dumps(result,indent=2)+'\n')
