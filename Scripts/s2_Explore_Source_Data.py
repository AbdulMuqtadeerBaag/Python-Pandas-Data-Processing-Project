"""
================================================================================
                         EXPLORE SOURCE DATA
================================================================================
Project : Python-Pandas-Data-Processing-Project
Script  : s2_Explore_Source_Data.py
Author  : Abdul Muqtadeer Baag

Purpose:
    - Explore CRM and ERP source datasets.
    - Understand dataset structure and data types.
    - Identify missing values and duplicate records.
    - Review statistical summaries and memory usage.
--------------------------------------------------------------------------------
"""

# 1. IMPORT LIBRARIES AND FUNCTIONS:
from s1_Extract_Source_Data import extract_source_data


# 2. EXPLORE DATASET:
def explore_dataset(name, df):

    print("\n" + "=" * 65 )
    print(f"{name.upper()} DATASET EXPLORATION:")
    print("=" * 65)

    # 1. Dataset dimensions:
    print("1. DATASET SHAPE:")
    print(f"Rows    : {df.shape[0]}")
    print(f"Columns : {df.shape[1]}")

    # 2. Column names:
    print("\n2. COLUMN NAMES:")
    print(df.columns.tolist())

    # 3. Dataset information:
    print("\n3. DATASET INFORMATION:")
    df.info()

    # 4. Statistical summary:
    print("\n4. STATISTICAL SUMMARY:")
    print(df.describe(include="all").to_string())

    # 5. Missing values:
    print("\n5. MISSING VALUES:")
    print(df.isnull().sum())
    print(f"\nTotal Missing Values: {df.isnull().sum().sum()}")

    # 6. Duplicate records:
    print("\n6. DUPLICATE RECORDS:")
    print(f"Duplicate Rows: {df.duplicated().sum()}")

    # 7. Memory usage:
    print("\n7. MEMORY USAGE:")
    memory_mb = df.memory_usage(deep=True).sum() / (1024 ** 2)
    print(f"Memory: {memory_mb:.2f} MB")

# 3. MAIN FUNCTION:
def explore_data():

    datasets = extract_source_data()

    for name, df in datasets.items():
        explore_dataset(name, df)

    print("\n" + "-" * 65)
    print("       SOURCE DATA EXPLORATION COMPLETED SUCCESSFULLY!")
    print("-" * 65)

# 4. EXECUTION:
if __name__ == "__main__":
    
    explore_datasets = explore_data()
