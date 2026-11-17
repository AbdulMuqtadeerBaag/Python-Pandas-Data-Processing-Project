"""
================================================================================
                            DATA EXPORT
================================================================================
Project : Python-Pandas-Data-Processing-Project
Script  : s6_Export_Result.py
Author  : Abdul Muqtadeer Baag

Purpose:
    - Export cleaned datasets into CSV files.
    - Export transformed datasets into CSV files.
    - Export sales analysis into an Excel workbook.
--------------------------------------------------------------------------------
"""

# IMPORT LIBRARIES AND FUNCTIONS:
import pandas as pd
from pathlib import Path

from s3_Clean_Source_Data import clean_source_data
from s5_Transform_Data import transform_data


# 1. EXPORT DATA:
def export_data(cleaned_data, results):

    # Output Folder:
    project_root = Path(__file__).resolve().parents[1]

    output_dir = project_root / "Output"
    output_dir.mkdir(parents=True, exist_ok=True)

    print("\nStarting Data Export...")
    print("=" * 65)

    # Export Cleaned Datasets:
    cleaned_dir = output_dir / "Cleaned_Data"
    cleaned_dir.mkdir(parents=True, exist_ok=True)

    for name, df in cleaned_data.items():

        file_name = (
            name.replace("Clean ", "")
            .replace(" ", "_")
            + ".csv"
        )

        file_path = cleaned_dir / file_name

        df.to_csv(file_path, index=False)

        print(f"Exported: Cleaned_Data/{file_path.name}")

    # Export Transformed Datasets:
    csv_datasets = {
        "Customer_Data": results["Customer Data"],
        "Product_Data": results["Product Data"],
        "Analytical_Sales": results["Analytical Sales"]
    }

    for name, df in csv_datasets.items():

        file_path = output_dir / f"{name}.csv"

        df.to_csv(file_path, index=False)

        print(f"Exported: {file_path.name}")

    # Export Sales Analysis to Excel:
    excel_path = output_dir / "Sales_Analysis.xlsx"

    with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:

        results["Sales by Country"].to_excel(
            writer,
            sheet_name="Sales by Country",
            index=False
        )

        results["Sales by Category"].to_excel(
            writer,
            sheet_name="Sales by Category",
            index=False
        )

        results["Monthly Sales"].to_excel(
            writer,
            sheet_name="Monthly Sales",
            index=False
        )

        results["Sales Pivot"].to_excel(
            writer,
            sheet_name="Sales Pivot"
        )

    print(f"Exported: {excel_path.name}")

    print("-" * 65)
    print("            DATA EXPORT COMPLETED SUCCESSFULLY!")
    print("-" * 65)


# 2. EXECUTION:
if __name__ == "__main__":

    print("\nStarting Data Processing...")

    # Load Cleaned Data:
    cleaned_data = clean_source_data()

    # Transform Data:
    results = transform_data(cleaned_data)

    # Export Final Data:
    export_data(cleaned_data, results)
