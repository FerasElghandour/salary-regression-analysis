"""Reproducible salary regression with training-only model selection."""
import argparse
import json
from pathlib import Path
import numpy as np
import pandas as pd
import statsmodels.api as sm
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error,mean_squared_error,r2_score

def design(frame):
    required=['Years of Experience','Gender','Education Level','Job Title']
    if set(required)-set(frame):raise ValueError('Required salary predictors are missing')
    x=pd.DataFrame(index=frame.index)
    x['experience']=pd.to_numeric(frame['Years of Experience'],errors='raise')
    x['male']=frame['Gender'].eq('Male').astype(float)
    for word in ['director','junior','senior','manager','analyst','engineer']:
        x['title_'+word]=frame['Job Title'].astype(str).str.contains(word,case=False,regex=False).astype(float)
    x['masters']=frame['Education Level'].eq("Master's").astype(float)
    x['phd']=frame['Education Level'].eq('PhD').astype(float)
    if not np.isfinite(x.to_numpy()).all():raise ValueError('Predictors must be finite')
    return sm.add_constant(x,has_constant='add')

def analyze(frame,seed=42):
    frame=frame.dropna(subset=['Salary','Years of Experience','Gender','Education Level','Job Title']).copy()
    if len(frame)<40:raise ValueError('At least 40 complete observations required')
    train,test=train_test_split(frame,test_size=.2,random_state=seed)
    xtr,xte=design(train),design(test)
    # Keep an identified training design; constant/aliased indicators are omitted.
    independent=['const']
    for column in xtr.columns:
        if column!='const' and np.linalg.matrix_rank(xtr[independent+[column]].to_numpy())>len(independent):
            independent.append(column)
    xtr,xte=xtr[independent],xte[independent]
    candidate=sm.OLS(train['Salary'].astype(float),xtr).fit()
    selected=['const']+[k for k in xtr if k!='const' and candidate.pvalues[k]<.05]
    fitted=sm.OLS(train['Salary'].astype(float),xtr[selected]).fit(cov_type='HC3')
    pred=fitted.predict(xte[selected]);truth=test['Salary'].astype(float)
    return {'train_rows':len(train),'test_rows':len(test),'selected_predictors':selected,
      'holdout_mae':float(mean_absolute_error(truth,pred)),
      'holdout_rmse':float(np.sqrt(mean_squared_error(truth,pred))),
      'holdout_r2':float(r2_score(truth,pred)),
      'coefficients':{k:float(v) for k,v in fitted.params.items()},
      'hc3_intervals':{k:[float(v) for v in row] for k,row in fitted.conf_int().iterrows()}}

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('csv',type=Path);args=parser.parse_args()
    print(json.dumps(analyze(pd.read_csv(args.csv)),indent=2))
