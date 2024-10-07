import pandas as pd
from regression import perform_regression_analysis_anova, perform_regression_analysis_anova_interaction
from export import export_significant_p_values_to_csv

# Define reference groups
reference_groups = [
    ['SI/SA with MDD with comorbidities with no sleep and bipolar', 'SI/SA with MDD with comorbidities with sleep']
]

# Placeholder for the actual data loading
# Assuming 'anova_merged_groups_dict_dti' and similar datasets are already loaded

def main():
    regression_results_dti1 = {}

    # Iterate through the datasets and perform regression analysis
    for dataset_name, group_dict in anova_merged_groups_dict_dti.items():
        combined_df = pd.DataFrame()
        for group_name, df in group_dict.items():
            df = df.copy()
            df.loc[:, 'group'] = group_name  # Avoid SettingWithCopyWarning
            combined_df = pd.concat([combined_df, df], ignore_index=True)

        # Filter for specific groups
        combined_df = combined_df[combined_df['group'].isin(['SI/SA with MDD with comorbidities with no sleep and bipolar',
                                                             'SI/SA with MDD with comorbidities with sleep'])]
        filtered_df = combined_df.loc[:, ~combined_df.columns.duplicated()]
        print(f"Processing dataset: {dataset_name}")

        # Perform regression analysis for each reference group
        for ref_group in reference_groups:
            results = perform_regression_analysis_anova(filtered_df, ref_group)
            regression_results_dti1[(dataset_name, ref_group[0])] = results

    # Export significant p-values to CSV
    export_significant_p_values_to_csv(regression_results_dti1, './significant_p_values_dti.csv')

if __name__ == "__main__":
    main()
