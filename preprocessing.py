import pandas as pd
import os
import glob

def load_csv_files(path, pattern):
    """
    Loads CSV files from a specified path that match a given pattern.

    Parameters:
    - path: The directory where the files are located.
    - pattern: The pattern to match for file selection (e.g., 'mri_y_dti*.csv').

    Returns:
    - dataframes_dict: A dictionary where keys are file names and values are pandas DataFrames filtered by baseline year.
    """
    csv_files = glob.glob(os.path.join(path, pattern))
    dataframes_dict = {}

    for file in csv_files:
        file_name = os.path.basename(file)
        name = file_name.replace('.csv', '').replace('mri_y_', 'abcd_')

        df = pd.read_csv(file)
        df_baseline = df[df['eventname'] == 'baseline_year_1_arm_1']
        dataframes_dict[f"{name}_baseline"] = df_baseline

    return dataframes_dict

def filter_groups_by_condition(group_dict, condition_filter):
    """
    Filters the groups in a dictionary based on a condition.

    Parameters:
    - group_dict: Dictionary containing different groups as DataFrames.
    - condition_filter: Filter condition (e.g., columns related to 'sleep' or 'bipolar').

    Returns:
    - filtered_groups: Dictionary with groups filtered by the condition.
    """
    filtered_groups = {}
    for group_name, df in group_dict.items():
        filtered_groups[group_name] = df[condition_filter]
    
    return filtered_groups

def merge_and_keep_columns(groups, dataset, columns_to_keep):
    """
    Merges groups with dataset and keeps specific columns.

    Parameters:
    - groups: Dictionary of groups to be merged.
    - dataset: DataFrame to merge with groups.
    - columns_to_keep: List of columns to keep after merging.

    Returns:
    - merged_groups: Dictionary of merged DataFrames.
    """
    merged_groups = {}
    for group_name, group_df in groups.items():
        merged_df = group_df.merge(dataset, on='src_subject_id', how='inner')
        merged_df = merged_df[columns_to_keep]
        merged_groups[group_name] = merged_df

    return merged_groups

def add_column_from_another_df(src_df, src_col, target_df, target_col):
    """
    Adds a column to the target DataFrame based on the source DataFrame column.

    Parameters:
    - src_df: Source DataFrame from which to copy the column.
    - src_col: The column to copy from the source DataFrame.
    - target_df: The DataFrame to which the column will be added.
    - target_col: The name of the new column in the target DataFrame.

    Returns:
    - target_df: Updated DataFrame with the new column.
    """
    if src_col not in src_df.columns:
        raise ValueError(f"Column {src_col} not found in the DataFrame.")
    
    qc_scores = src_df.set_index('src_subject_id')[src_col].fillna(0).astype(int).to_dict()
    target_df[target_col] = target_df['src_subject_id'].map(qc_scores).fillna(0).astype(int)
    
    return target_df

def load_mri_data(path, modality, pattern):
    """
    Loads MRI data by modality and pattern.

    Parameters:
    - path: Directory containing the MRI files.
    - modality: MRI modality (e.g., 'dti', 'rsfmri').
    - pattern: File matching pattern.

    Returns:
    - dataframes_dict: Dictionary of MRI DataFrames filtered by baseline year.
    """
    csv_files = glob.glob(os.path.join(path, f'mri_y_{modality}_{pattern}*.csv'))
    dataframes_dict = {}

    for file in csv_files:
        file_name = os.path.basename(file)
        name = file_name.replace('.csv', '').replace(f'mri_y_{modality}_', f'abcd_{modality}_')
        
        df = pd.read_csv(file)
        df_baseline = df[df['eventname'] == 'baseline_year_1_arm_1']
        dataframes_dict[f"{name}_baseline"] = df_baseline

    return dataframes_dict

def preprocess_demo_data(abcd_demo_file):
    """
    Preprocesses demographic data for use in further analysis.

    Parameters:
    - abcd_demo_file: Path to the demographic CSV file.

    Returns:
    - abcd_demo_baseline: Preprocessed demographic DataFrame filtered by baseline year.
    """
    abcd_demo = pd.read_csv(abcd_demo_file)
    abcd_demo_baseline = abcd_demo[abcd_demo['eventname'] == 'baseline_year_1_arm_1']
    
    race_mapping = {
        'demo_race_a_p___10': 1, # White
        'demo_race_a_p___11': 2, # Black
        'demo_race_a_p___12': 4, # Other/Multiracial
        # Add other race mappings here
    }

    def determine_race(row):
        races = set()
        for col, race in race_mapping.items():
            if row[col] == 1:
                races.add(race)
        if len(races) == 1:
            return races.pop()
        elif len(races) > 1:
            return 4 # Other/Multiracial
        else:
            return 0 # Unknown
    
    abcd_demo_baseline['race'] = abcd_demo_baseline.apply(determine_race, axis=1)

    return abcd_demo_baseline
