import pandas as pd
import statsmodels.formula.api as smf
from statsmodels.stats.multitest import multipletests

def perform_regression_analysis_anova(df, ref_group):
    if 'group' not in df.columns:
        raise KeyError("'group' column is not in the dataframe")
    
    df['group'] = df['group'].astype('category').cat.reorder_categories(ref_group)
    dependent_vars = df.select_dtypes(include='float64').columns.tolist()
    results = {}

    for var in dependent_vars:
        formula = (f"{var} ~ C(demo_gender_id_v2) + C(group) + C(demo_brthdat_v2) "
                   " + C(highest_household_education)+ C(demo_prnt_marital_v2) + "
                   "C(race) + C(household_income_per_year)")
        try:
            model = smf.ols(formula, data=df).fit()
            results[var] = model
        except Exception as e:
            print(f"Error fitting model for {var}: {e}")
    
    p_values = [model.f_pvalue for model in results.values()]
    _, corrected_p_values, _, _ = multipletests(p_values, method='fdr_bh')
    
    summaries = {}
    for var, model in results.items():
        summary = model.summary2().tables[1]
        summary['P>|t| (corrected)'] = corrected_p_values[list(results.keys()).index(var)]
        summaries[var] = summary[summary['P>|t| (corrected)'] < 0.05]
    
    return summaries

def perform_regression_analysis_anova_interaction(df, ref_group):
    df['group'] = df['group'].astype('category').cat.reorder_categories(ref_group)
    dependent_vars = df.select_dtypes(include='float64').columns.tolist()
    results = {}

    for var in dependent_vars:
        formula = (f"{var} ~ C(demo_gender_id_v2) + C(group) + C(demo_gender_id_v2):C(group) + "
                   "C(demo_brthdat_v2) + C(highest_household_education)+ C(demo_prnt_marital_v2) + "
                   "C(race) + C(household_income_per_year)")
        try:
            model = smf.ols(formula, data=df).fit()
            results[var] = model
        except Exception as e:
            print(f"Error fitting model for {var}: {e}")
    
    p_values = [model.f_pvalue for model in results.values()]
    _, corrected_p_values, _, _ = multipletests(p_values, method='fdr_bh')
    
    summaries = {}
    for var, model in results.items():
        summary = model.summary2().tables[1]
        summary['P>|t| (corrected)'] = corrected_p_values[list(results.keys()).index(var)]
        summaries[var] = summary[summary['P>|t| (corrected)'] < 0.05]
    
    return summaries
