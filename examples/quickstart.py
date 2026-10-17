"""Offline example using the public implementation; see README for evidence scope."""
import sys
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))
os.chdir(ROOT)

import numpy as np
import pandas as pd
from salary_model import analyze,design
# Generated fixtures demonstrate current API behavior only.
rng=np.random.default_rng(3);n=120
frame=pd.DataFrame({'Years of Experience':rng.uniform(0,20,n),'Gender':rng.choice(['Male','Female'],n),'Education Level':rng.choice(["Bachelor's","Master's",'PhD'],n),'Job Title':rng.choice(['Engineer','Senior Engineer','Manager'],n)})
frame['Salary']=30000+frame['Years of Experience']*4000+rng.normal(0,1000,n)
result=analyze(frame)
import json
print(json.dumps(result, indent=2))
