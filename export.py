import pandas as pd

def export_significant_p_values_to_csv(regression_results, output_file):
    significant_results = []

    for key, summaries in regression_results.items():
        dataset_name, ref_group = key
        for dep_var, summary in summaries.items():
            if not summary.empty:
                summary['Dataset'] = dataset_name
                summary['Reference Group'] = ref_group
                summary['Dependent Variable'] = dep_var
                summary['Independent Variable'] = summary.index
                significant_results.append(summary)

    if significant_results:
        significant_df = pd.concat(significant_results)
        significant_df.to_csv(output_file, index=False)
    else:
        print("No significant p-values found.")
