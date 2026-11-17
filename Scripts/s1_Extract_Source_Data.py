"""
================================================================================
                         EXTRACT SOURCE DATA
================================================================================
Project : Python-Pandas-Data-Processing-Project
Script  : s1_Extract_Source_Data.py
Author  : Abdul Muqtadeer Baag

Purpose:
    - Extract CRM(Customer Relationship Management) and 
              ERP(Enterprise Resource Planning) source CSV files.
    - Load data into Pandas DataFrames.
    - Return all six datasets in a dictionary.
--------------------------------------------------------------------------------
"""

# 1. IMPORT LIBRARIES:
import pandas as pd
from pathlib import Path

# 2. EXTRACT SOURCE DATA:
def extract_source_data():

    # Project directory:
    project_root = Path(__file__).resolve().parents[1]

    # Source directories:
    crm_path = project_root / "Datasets" / "Source_CRM"
    erp_path = project_root / "Datasets" / "Source_ERP"

    # Source file mapping:
    source_files = {
        "CRM Customer": crm_path / "Cust_Info.csv",
        "CRM Product": crm_path / "Prod_Info.csv",
        "CRM Sales": crm_path / "Sales_Details.csv",
        "ERP Customer": erp_path / "Cust_Mst.csv",
        "ERP Location": erp_path / "Loc_Mst.csv",
        "ERP Category": erp_path / "Prod_Catg.csv"
    }

    # Read CSV files:
    datasets = {}

    for name, file_path in source_files.items():

        if not file_path.is_file():
            raise FileNotFoundError(f"Source file not found: {file_path}")

        datasets[name] = pd.read_csv(file_path)

    return datasets

# 3. DISPLAY EXTRACTION SUMMARY:
def display_extraction_summary(datasets):

    print("=" * 65)
    print("              SOURCE DATA EXTRACTION COMPLETED!")
    print("=" * 65)

    for name, df in datasets.items():
        print(f"{name:<13} : {len(df)} Records")

    print("-" * 65)

# 4. MAIN FUNCTION:
def extract_data():

    datasets = extract_source_data()

    display_extraction_summary(datasets)

# 5. EXECUTION:
if __name__ == "__main__":
    
    extract_datasets = extract_data()
