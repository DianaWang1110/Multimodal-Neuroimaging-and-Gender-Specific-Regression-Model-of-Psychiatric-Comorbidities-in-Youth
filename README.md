
# Multimodal Neuroimaging and Gender-Specific Regression Analyses of Psychiatric Comorbidities in Youth: Insights from Structural MRI, dMRI, and rs-fMRI

This project contains scripts for loading, preprocessing, and merging neuroimaging data from various modalities (e.g., dMRI, rs-fMRI, MID, n-back, SST) as part of a research project focused on neuroimaging signatures of suicide in depression with comorbidities. The scripts also handle demographic data preprocessing to support further analysis.

  
## Preprocessing Overview

The preprocessing pipeline involves the following steps:

1. **Loading Neuroimaging Data**:
    - The script loads multiple neuroimaging datasets (e.g., dMRI, rs-fMRI, MID, n-back, SST) from CSV files using pattern matching.
    - Baseline year data (`baseline_year_1_arm_1`) is filtered for further analysis.
  
2. **Merging Imaging Data with Demographic Information**:
    - Imaging data is merged with demographic data (e.g., age, gender, race, household income, education).
    - Each group is merged with the imaging dataset, and only specific columns are retained (e.g., subject ID, demographic variables, and imaging measures).
  
3. **Group Filtering**:
    - The subjects are grouped based on various conditions such as suicidal ideation/suicide attempt (SI/SA), major depressive disorder (MDD), and comorbidities (e.g., sleep disorders, bipolar disorder).
    - Groups include:
      - Healthy controls.
      - SI/SA without MDD.
      - SI/SA with MDD (with or without comorbidities).
      - Specific comorbidity subgroups (sleep disorders, bipolar, and their combination).

4. **Adding Quality Control (QC) Scores**:
    - Quality control scores for each imaging modality are added to the subject data. These QC scores are crucial to filter out subjects with poor imaging quality.

5. **Demographic Data Preprocessing**:
    - Demographic data (e.g., race, gender, age, marital status, household income, education) is preprocessed and added to the imaging datasets.
    - A custom function determines race based on multiple binary columns and maps it to a specific value.
  
## Files

### `preprocessing.py`

This file contains the following key functions:

- **`load_csv_files(path, pattern)`**: Loads CSV files from a specified directory using a matching pattern (e.g., `mri_y_dti*.csv`) and returns a dictionary of baseline DataFrames.
  
- **`filter_groups_by_condition(group_dict, condition_filter)`**: Filters groups based on a specific condition (e.g., sleep or bipolar disorder diagnoses) and returns a dictionary of filtered DataFrames.

- **`merge_and_keep_columns(groups, dataset, columns_to_keep)`**: Merges each group with the corresponding imaging dataset and retains specific columns for further analysis.

- **`add_column_from_another_df(src_df, src_col, target_df, target_col)`**: Adds a column from a source DataFrame to a target DataFrame based on the subject ID (`src_subject_id`).

- **`load_mri_data(path, modality, pattern)`**: Loads MRI data files based on the given modality (e.g., dti, rsfmri) and pattern and filters for baseline year.

- **`preprocess_demo_data(abcd_demo_file)`**: Processes demographic data from the `abcd_p_demo.csv` file, adding derived columns (e.g., race, education, household income).

### Usage Example

To use the `preprocessing.py` functions, import them and call the respective functions for each neuroimaging modality and demographic data:

```python
from preprocessing import load_csv_files, merge_and_keep_columns, preprocess_demo_data

# Load dMRI data
dti_data = load_csv_files('./data/imaging/', 'mri_y_dti*.csv')

# Load demographic data and preprocess
abcd_demo_baseline = preprocess_demo_data('./data/abcd_p_demo.csv')

# Merge dMRI groups with demographic information and imaging data
merged_groups_dti = merge_and_keep_columns(groups_dti, dti_data['abcd_dti_fa_fs_baseline'], columns_to_keep=['src_subject_id', 'demo_gender_id_v2', 'demo_brthdat_v2', 'demo_prnt_marital_v2', 'race'])
```


### Output

The functions will output filtered and merged DataFrames for different imaging modalities and groups (e.g., SI/SA with MDD, healthy controls), ready for further analysis such as machine learning or statistical tests.
