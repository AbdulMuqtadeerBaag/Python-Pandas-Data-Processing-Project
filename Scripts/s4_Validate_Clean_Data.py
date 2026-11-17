"""
================================================================================
                         DATA QUALITY VALIDATION
================================================================================
Project : Python-Pandas-Data-Processing-Project
Script  : s4_Validate_Clean_Data.py
Author  : Abdul Muqtadeer Baag

Purpose:
    - Validate cleaned CRM and ERP datasets.
    - Check missing values, duplicates and invalid records.
    - Verify sales calculations and date formats.
    - Generate a Data Quality Report.
--------------------------------------------------------------------------------
"""

# IMPORT LIBRARIES AND FUNCTIONS:
import pandas as pd
import numpy as np

from s1_Extract_Source_Data import extract_source_data

from s3_Clean_Source_Data import (
    clean_crm_customer,
    clean_crm_product,
    clean_crm_sales,
    clean_erp_customer,
    clean_erp_location,
    clean_erp_category
)

# VALIDATION CHECK FUNCTION:
def check_validation(results, dataset, check_name, failed_records):

    failed_count = len(failed_records)

    status = "PASS" if failed_count == 0 else "FAIL"

    results.append({
        "Dataset": dataset,
        "Validation": check_name,
        "Failed Records": failed_count,
        "Status": status
    })

    print(f"{check_name}: {status}")
    print(f"Failed Records: {failed_count}")

    if failed_count > 0:
        print(failed_records.head(5))

    print("-" * 65)

# 1. VALIDATE CRM CUSTOMER:
def validate_crm_customer(df, results):

    dataset = "CRM Customer"

    print("\n1. CRM CUSTOMER VALIDATION:")
    print("=" * 65)

    # Missing Customer IDs:
    check_validation(
        results, dataset, "Missing Customer ID",
        df[df["cust_id"].isna()]
    )

    # Duplicate Customer IDs:
    check_validation(
        results, dataset, "Duplicate Customer ID",
        df[df.duplicated("cust_id", keep=False)]
    )

    # Invalid Marital Status:
    valid_status = ["Single", "Married", "n/a"]

    check_validation(
        results, dataset, "Invalid Marital Status",
        df[~df["cst_marital_status"].isin(valid_status)]
    )

    # Invalid Gender:
    valid_gender = ["Female", "Male", "n/a"]

    check_validation(
        results, dataset, "Invalid Gender",
        df[~df["cst_gndr"].isin(valid_gender)]
    )
    
# 2. VALIDATE CRM PRODUCT:
def validate_crm_product(df, results):

    dataset = "CRM Product"

    print("\n2. CRM PRODUCT VALIDATION:")
    print("=" * 65)

    # Missing Product IDs:
    check_validation(
        results, dataset, "Missing Product ID",
        df[df["prd_id"].isna()]
    )

    # Duplicate Product IDs:
    check_validation(
        results, dataset, "Duplicate Product ID",
        df[df.duplicated("prd_id", keep=False)]
    )

    # Check Whitespace in Product Name:
    check_validation(
        results, dataset, "Whitespace in Product Name",
        df[df["prd_nm"].astype("string")
        .str.strip()
        .ne(df["prd_nm"].astype("string"))
        .fillna(False)]
    )
    
    # Missing or Negative Product Cost:
    check_validation(
        results, dataset, "Missing or Negative Product Cost",
        df[df["prd_cost"].isna() | (df["prd_cost"] < 0)]
    )

    # Valid Product Line:
    valid_lines = [
        "Mountain", "Road", "Other Sales", "Touring", "n/a"
    ]

    check_validation(
        results, dataset, "Invalid Product Line",
        df[~df["prd_line"].isin(valid_lines)]
    )

    # Invalid Product Date Range:
    invalid_dates = (
        df["prd_start_dt"].notna()
        & df["prd_end_dt"].notna()
        & (df["prd_start_dt"] > df["prd_end_dt"])
    )

    check_validation(
        results, dataset, "Invalid Product Date Range",
        df[invalid_dates]
    )

# 3. VALIDATE CRM SALES:
def validate_crm_sales(df, raw_df, results):

    dataset = "CRM Sales"

    print("\n3. CRM SALES VALIDATION:")
    print("=" * 65)

    # Validate Original Date Formats:
    date_columns = [
        "sls_ship_dt",
        "sls_due_dt"
    ]

    for col in date_columns:

        raw_dates = raw_df[col].astype("string").str.strip()

        valid_format = (
            raw_dates.str.fullmatch(r"\d{8}", na=False)
            & raw_dates.ne("00000000")
        )

        parsed_dates = pd.to_datetime(
            raw_dates.where(valid_format),
            format="%Y%m%d",
            errors="coerce"
        )

        check_validation(
            results,
            dataset,
            f"Invalid Raw {col}",
            raw_df[parsed_dates.isna()]
        )

    # Check Order Date Against Ship and Due Dates:
    invalid_dates = (
        (
            df["sls_order_dt"].notna()
            & df["sls_ship_dt"].notna()
            & (df["sls_order_dt"] > df["sls_ship_dt"])
        )
        |
        (
            df["sls_order_dt"].notna()
            & df["sls_due_dt"].notna()
            & (df["sls_order_dt"] > df["sls_due_dt"])
        )
    )

    check_validation(
        results, dataset, "Invalid Order Date Sequence",
        df[invalid_dates]
    )

    # Check Sales Amount Consistency:
    expected_sales = df["sls_quantity"] * df["sls_price"]

    comparable = (
        df["sls_sales"].notna()
        & expected_sales.notna()
    )

    matches = np.isclose(
        df["sls_sales"].fillna(0),
        expected_sales.fillna(0),
        rtol=1e-5,
        atol=0.01
    )

    check_validation(
        results, dataset, "Sales Amount Mismatch",
        df[comparable & ~matches]
    )

    # Check Missing or Non-Positive Sales:
    check_validation(
        results, dataset, "Missing or Non-Positive Sales",
        df[df["sls_sales"].isna() | (df["sls_sales"] <= 0)]
    )

    # Check Missing or Non-Positive Quantity:
    check_validation(
        results, dataset, "Missing or Non-Positive Quantity",
        df[df["sls_quantity"].isna() | (df["sls_quantity"] <= 0)]
    )

    # Check Missing or Non-Positive Price:
    check_validation(
        results, dataset, "Missing or Non-Positive Price",
        df[df["sls_price"].isna() | (df["sls_price"] <= 0)]
    )

# 4. VALIDATE ERP CUSTOMER:
def validate_erp_customer(df, results):

    dataset = "ERP Customer"

    print("\n4. ERP CUSTOMER VALIDATION:")
    print("=" * 65)

    # Invalid Future Birth Dates:
    future_dates = (
        df["bdate"].notna()
        & (df["bdate"] > pd.Timestamp.now().normalize())
    )

    check_validation(
        results, dataset, "Future Birth Date",
        df[future_dates]
    )

    # Invalid Gender:
    valid_gender = ["Female", "Male", "n/a"]

    check_validation(
        results, dataset, "Invalid Gender",
        df[~df["gen"].isin(valid_gender)]
    )

# 5. VALIDATE ERP LOCATION:
def validate_erp_location(df, results):

    dataset = "ERP Location"

    print("\n5. ERP LOCATION VALIDATION:")
    print("=" * 65)

    # Check NULL or Blank Country:
    invalid_country = (
        df["cntry"].isna()
        | df["cntry"].astype("string").str.strip().eq("").fillna(False)
    )

    check_validation(
        results, dataset, "Missing or Invalid Country",
        df[invalid_country]
    )

    # Display Distinct Countries:
    print("\nDistinct Countries:")
    print(df["cntry"].unique())

# 6. VALIDATE ERP CATEGORY:
def validate_erp_category(df, results):

    dataset = "ERP Category"

    print("\n6. ERP CATEGORY VALIDATION")
    print("=" * 65)

    # Check Missing Category Names:
    check_validation(
        results, dataset, "Missing Category",
        df[df["cat"].isna()]
    )

    # Check Missing Subcategory Names:
    check_validation(
        results, dataset, "Missing Subcategory",
        df[df["subcat"].isna()]
    )

    # Check Whitespace in Text columns:
    columns = [
        "cat",
        "subcat",
        "maintenance"
    ]

    for column in columns:

        raw_col = df[
            df[column].astype("string")
            .str.strip()
            .ne(df[column].astype("string"))
            .fillna(False)
        ]

        check_validation(
            results, dataset, f"Whitespace in {column}",
            raw_col
        )

    # Display Distinct Maintenance Values:
    print("\nDistinct Maintenance Values:")
    print(df["maintenance"].unique())

# EXECUTE DATA VALIDATION:
def validate_clean_data():

    results = []

    # Extract Raw Data
    source_datasets = extract_source_data()

    # Clean CRM and ERP Data
    cleaned_data = {
        "CRM Customer": clean_crm_customer(
            source_datasets["CRM Customer"]
        ),
        "CRM Product": clean_crm_product(
            source_datasets["CRM Product"]
        ),
        "CRM Sales": clean_crm_sales(
            source_datasets["CRM Sales"]
        ),
        "ERP Customer": clean_erp_customer(
            source_datasets["ERP Customer"]
        ),
        "ERP Location": clean_erp_location(
            source_datasets["ERP Location"]
        ),
        "ERP Category": clean_erp_category(
            source_datasets["ERP Category"]
        )
    }

    # CRM Data Validation
    validate_crm_customer(
        cleaned_data["CRM Customer"], results
    )

    validate_crm_product(
        cleaned_data["CRM Product"], results
    )

    validate_crm_sales(
        cleaned_data["CRM Sales"],
        source_datasets["CRM Sales"],
        results
    )

    # ERP Data Validation
    validate_erp_customer(
        cleaned_data["ERP Customer"], results
    )

    validate_erp_location(
        cleaned_data["ERP Location"], results
    )

    validate_erp_category(
        cleaned_data["ERP Category"], results
    )

    # Generate Data Quality Report
    quality_report = pd.DataFrame(results)

    # Final Summary
    print("\n" + "=" * 65)
    print("                 FINAL DATA QUALITY SUMMARY")
    print("=" * 65)

    print(quality_report.to_string(index=False))

    total_checks = len(quality_report)
    passed_checks = (quality_report["Status"] == "PASS").sum()
    failed_checks = (quality_report["Status"] == "FAIL").sum()

    print("\nTotal Checks :", total_checks)
    print("Passed Checks:", passed_checks)
    print("Failed Checks:", failed_checks)

    return quality_report

# EXECUTION:
if __name__ == "__main__":
    
    quality_report = validate_clean_data()
