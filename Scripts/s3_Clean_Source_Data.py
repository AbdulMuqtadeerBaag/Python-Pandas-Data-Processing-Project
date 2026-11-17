"""
================================================================================
                           CLEAN CRM AND ERP DATA
================================================================================
Project : Python-Pandas-Data-Processing-Project
Script  : s3_Clean_Source_Data.py
Author  : Abdul Muqtadeer Baag

Purpose:
    - Clean CRM customer data.
    - Clean CRM product data.
    - Clean CRM sales data.
    - Clean ERP customer data.
    - Clean ERP location data.
    - Clean ERP product category data.
--------------------------------------------------------------------------------
"""

# IMPORT LIBRARIES AND FUNCTIONS:
import pandas as pd
import numpy as np

from s1_Extract_Source_Data import extract_source_data

# 1. CLEAN CRM CUSTOMER:
def clean_crm_customer(df):

    clean_df = df.copy()

    clean_df.columns = clean_df.columns.str.lower().str.strip()

    # Remove Missing Customer ID:
    clean_df = clean_df.dropna(subset=["cust_id"])

    # Convert Customer Creation Date:
    clean_df["cst_create_date"] = pd.to_datetime(
        clean_df["cst_create_date"],
        errors="coerce"
    )

    # Keep the latest record for each customer:
    clean_df = clean_df.sort_values(
        "cst_create_date",
        ascending=False
    )

    clean_df = clean_df.drop_duplicates(
        subset=["cust_id"],
        keep="first"
    )

    # Clean Customer Names:
    for col in ["cust_firstname", "cst_lastname"]:
        clean_df[col] = (
            clean_df[col]
            .astype("string")
            .str.strip()
        )

    # Standardize Marital Status:
    clean_df["cst_marital_status"] = (
        clean_df["cst_marital_status"]
        .astype("string")
        .str.strip()
        .str.upper()
        .map({
            "S": "Single",
            "M": "Married"
        })
        .fillna("n/a")
    )

    # Standardize Gender:
    clean_df["cst_gndr"] = (
        clean_df["cst_gndr"]
        .astype("string")
        .str.strip()
        .str.upper()
        .map({
            "F": "Female",
            "M": "Male"
        })
        .fillna("n/a")
    )

    return clean_df

# 2. CLEAN CRM PRODUCT:
def clean_crm_product(df):

    clean_df = df.copy()

    clean_df.columns = clean_df.columns.str.lower().str.strip()

    # Extract Category ID:
    clean_df["catg_id"] = (
        clean_df["prd_key"]
        .astype("string")
        .str.slice(0, 5)
        .str.replace("-", "_", regex=False)
    )

    # Extract Product Key:
    clean_df["prd_key"] = (
        clean_df["prd_key"]
        .astype("string")
        .str.slice(6)
    )

    # Convert Product Cost to Numeric:
    clean_df["prd_cost"] = pd.to_numeric(
        clean_df["prd_cost"],
        errors="coerce"
    ).fillna(0)

    # Standardize Product Line:
    clean_df["prd_line"] = (
        clean_df["prd_line"]
        .astype("string")
        .str.strip()
        .str.upper()
        .map({
            "M": "Mountain",
            "R": "Road",
            "S": "Other Sales",
            "T": "Touring"
        })
        .fillna("n/a")
    )

    # Convert Product Start Date:
    clean_df["prd_start_dt"] = pd.to_datetime(
        clean_df["prd_start_dt"],
        errors="coerce"
    )

    # Calculate Product End Date:
    clean_df = clean_df.sort_values(
        ["prd_key", "prd_start_dt"]
    )

    clean_df["prd_end_dt"] = (
        clean_df.groupby("prd_key")["prd_start_dt"]
        .shift(-1) - pd.Timedelta(days=1)
    )

    return clean_df

# 3. CLEAN CRM SALES:
def clean_crm_sales(df):

    clean_df = df.copy()

    clean_df.columns = clean_df.columns.str.lower().str.strip()

    # Convert Sales Date Columns:
    date_columns = [
        "sls_order_dt",
        "sls_ship_dt",
        "sls_due_dt"
    ]

    for col in date_columns:

        date_values = (
            clean_df[col]
            .astype("string")
            .str.strip()
        )

        date_values = date_values.where(
            date_values.str.len() == 8
        )

        date_values = date_values.where(
            date_values != "00000000"
        )

        clean_df[col] = pd.to_datetime(
            date_values,
            format="%Y%m%d",
            errors="coerce"
        )

    # Convert Numeric Columns:
    numeric_columns = [
        "sls_sales",
        "sls_quantity",
        "sls_price"
    ]

    for col in numeric_columns:
        clean_df[col] = pd.to_numeric(
            clean_df[col],
            errors="coerce"
        )

    # Replace Missing or Non-positive Prices:
    invalid_price = (
        clean_df["sls_price"].isna()
        | (clean_df["sls_price"] <= 0)
    )

    # Calculate Price from Sales and Quantity:
    calculated_price = (
        clean_df["sls_sales"]
        / clean_df["sls_quantity"].replace(0, np.nan)
    )

    # Recalculate Price:
    clean_df.loc[invalid_price, "sls_price"] = (
        calculated_price[invalid_price]
    )

    # Calculate Expected Sales:
    calculated_sales = (
        clean_df["sls_quantity"]
        * clean_df["sls_price"].abs()
    )

    # Identify Invalid Sales:
    invalid_sales = (
        clean_df["sls_sales"].isna()
        | (clean_df["sls_sales"] <= 0)
        | (clean_df["sls_sales"] != calculated_sales)
    )

    # Recalculate Sales:
    clean_df.loc[invalid_sales, "sls_sales"] = (
        calculated_sales[invalid_sales]
    )

    return clean_df

# 4. CLEAN ERP CUSTOMER:
def clean_erp_customer(df):

    clean_df = df.copy()

    clean_df.columns = clean_df.columns.str.lower().str.strip()

    # Remove NAS Prefix from Customer ID:
    clean_df["cid"] = (
        clean_df["cid"]
        .astype("string")
        .str.replace(r"^NAS", "", regex=True, case=False)
    )

    # Convert Birth Date:
    clean_df["bdate"] = pd.to_datetime(
        clean_df["bdate"],
        errors="coerce"
    )

    # Remove Future Birth Dates:
    clean_df.loc[
        clean_df["bdate"] > pd.Timestamp.now().normalize(),
        "bdate"
    ] = pd.NaT

    # Standardize Gender:
    clean_df["gen"] = (
        clean_df["gen"]
        .astype("string")
        .str.strip()
        .str.upper()
        .map({
            "F": "Female",
            "FEMALE": "Female",
            "M": "Male",
            "MALE": "Male"
        })
        .fillna("n/a")
    )

    return clean_df

# 5. CLEAN ERP LOCATION:
def clean_erp_location(df):

    clean_df = df.copy()

    clean_df.columns = clean_df.columns.str.lower().str.strip()

    # Remove Hyphens from Customer ID:
    clean_df["cid"] = (
        clean_df["cid"]
        .astype("string")
        .str.replace("-", "", regex=False)
    )

    # Standardize Country Names:
    country = (
        clean_df["cntry"]
        .astype("string")
        .str.strip()
        .str.upper()
    )

    clean_df["cntry"] = (
        country.map({
            "US": "UNITED STATES",
            "USA": "UNITED STATES",
            "DE": "GERMANY"
        }).fillna(country.mask(country.eq("")))
        .fillna("n/a")
    )

    return clean_df

# 6. CLEAN ERP PRODUCT CATEGORY:
def clean_erp_category(df):

    clean_df = df.copy()

    clean_df.columns = clean_df.columns.str.lower().str.strip()

    # Identify Text Columns:
    text_columns = clean_df.select_dtypes(
        include=["object", "string"]
    ).columns

    # Remove Leading and Trailing Whitespace:
    for col in text_columns:
        clean_df[col] = (
            clean_df[col]
            .astype("string")
            .str.strip()
            .replace("", pd.NA)
        )

    return clean_df


# MAIN CRM and ERP CLEANING FUNCTION:
def clean_source_data():
    
    print("\nStarting CRM and ERP Data Cleaning...")

    datasets = extract_source_data()

    # Clean CRM and ERP Datasets:
    clean_datasets = {

        "Clean CRM Customer": clean_crm_customer(
            datasets["CRM Customer"]
        ),

        "Clean CRM Product": clean_crm_product(
            datasets["CRM Product"]
        ),

        "Clean CRM Sales": clean_crm_sales(
            datasets["CRM Sales"]
        ),

        "Clean ERP Customer": clean_erp_customer(
            datasets["ERP Customer"]
        ),
        
        "Clean ERP Location": clean_erp_location(
            datasets["ERP Location"]
        ),
        
        "Clean ERP Category": clean_erp_category(
            datasets["ERP Category"]
        )
    }

    # Display Summary:
    print("\nCRM and ERP DATA CLEANING SUMMARY:")
    print("-" * 65)

    for name, df in clean_datasets.items():

        print(
            f"{name}: {len(df)} Records | "
            f"{len(df.columns)} Columns"
        )

    print("-" * 65)
    print("                CRM and ERP DATA CLEANING COMPLETED!")
    print("-" * 65)

    return clean_datasets


# EXECUTION:
if __name__ == "__main__":

    clean_source_datasets = clean_source_data()
