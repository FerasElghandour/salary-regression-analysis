"""Point predictions using the released design and frozen fitted coefficients."""
from pathlib import Path
import argparse,json,pandas as pd
from salary_model import design
p=argparse.ArgumentParser();p.add_argument('model',type=Path);p.add_argument('csv',type=Path);a=p.parse_args();m=json.loads(a.model.read_text());x=design(pd.read_csv(a.csv));pred=x[m['selected_predictors']]@pd.Series(m['coefficients'])
print(pred.to_json(orient='values'))
