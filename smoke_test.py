import numpy as np
import pandas as pd
from salary_model import analyze,design
rng=np.random.default_rng(3);n=120
frame=pd.DataFrame({'Years of Experience':rng.uniform(0,20,n),'Gender':rng.choice(['Male','Female'],n),'Education Level':rng.choice(["Bachelor's","Master's",'PhD'],n),'Job Title':rng.choice(['Engineer','Senior Engineer','Manager'],n)})
frame['Salary']=30000+frame['Years of Experience']*4000+rng.normal(0,1000,n)
result=analyze(frame)
assert result['train_rows']==96 and result['test_rows']==24
assert result['holdout_mae']<2000 and result['holdout_r2']>.95
assert 'experience' in result['selected_predictors']
assert result['hc3_intervals']['experience'][0]<4000<result['hc3_intervals']['experience'][1]
print('Training-only selection, predictive signal, split accounting, and robust interval checks passed.')
