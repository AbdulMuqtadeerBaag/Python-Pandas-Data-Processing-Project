"""
================================================================================
                         DATA TRANSFORMATION
================================================================================
Project : Python-Pandas-Data-Processing-Project
Script  : s5_Transform_Data.py
Author  : Abdul Muqtadeer Baag

Purpose:
    - Integrate cleaned CRM and ERP datasets.
    - Match sales with customer and product information.
    - Create customer and product surrogate keys.
    - Perform sales analysis using Pandas.
--------------------------------------------------------------------------------
"""

# IMPORT LIBRARIES AND FUNCTIONS:
import pandas as pd

from s3_Clean_Source_Data import clean_source_data


# 1. INTEGRATE CUSTOMER DATA:
def integrate_customer_data(clean_datasets):

    crm_customer = clean_datasets["Clean CRM Customer"][
        ["cust_id", "cust_key", "cust_firstname", "cst_lastname", "cst_marital_status", "cst_gndr", "cst_create_date"]]

    erp_customer = clean_datasets["Clean ERP Customer"][
        ["cid", "bdate", "gen"]]

    erp_location = clean_datasets["Clean ERP Location"][
        ["cid", "cntry"]]

    # Join CRM Customer with ERP Customer:
    customer_data = crm_customer.merge(
        erp_customer,
        left_on="cust_key",
        right_on="cid",
        how="left",
        validate="many_to_one"
    )

    # Join CRM Customer with ERP Location:
    customer_data = customer_data.merge(
        erp_location,
        left_on="cust_key",
        right_on="cid",
        how="left",
        validate="many_to_one"
    )

    # CRM Gender First, ERP Gender as Fallback:
    customer_data["gender"] = (
        customer_data["cst_gndr"]
        .where(
            customer_data["cst_gndr"].ne("n/a"),
            customer_data["gen"]
        )
        .fillna("n/a")
    )

    # Create Customer Surrogate Key:
    customer_data = customer_data.sort_values(
        "cust_id"
    ).reset_index(drop=True)

    customer_data.insert(
        0,
        "customer_key",
        range(1, len(customer_data) + 1)
    )

    # Rename Customer Columns:
    customer_data = customer_data.rename(
        columns={
            "customer_key": "Customer_Key",     
            "cust_id": "Customer_Id",
            "cust_key": "Customer_Number",
            "cust_firstname": "First_Name",
            "cst_lastname": "Last_Name",
            "cntry": "Country",
            "cst_marital_status": "Marital_Status",
            "gender": "Gender",
            "bdate": "Birth_Date",
            "cst_create_date": "Create_Date"
    })

# Select Required Customer Columns:
    customer_data = customer_data[
        [
            "Customer_Key",
            "Customer_Id",
            "Customer_Number",
            "First_Name",
            "Last_Name",
            "Country",
            "Marital_Status",
            "Gender",
            "Birth_Date",
            "Create_Date"
        ]
    ]

    return customer_data


# 2. INTEGRATE PRODUCT DATA:
def integrate_product_data(clean_datasets):

    product = clean_datasets["Clean CRM Product"][
        ["prd_id", "catg_id","prd_key", "prd_nm", "prd_cost", "prd_line", "prd_start_dt", "prd_end_dt"]]
    
    # Select Current Products Only:
    product = product[
        product["prd_end_dt"].isna()
    ].copy()

    category = clean_datasets["Clean ERP Category"][
        ["id", "cat", "subcat", "maintenance"]]

    # Join CRM Product with ERP Category:
    product_data = product.merge(
        category,
        left_on="catg_id",
        right_on="id",
        how="left",
        validate="many_to_one"
    )

    # Create Product Surrogate Key:
    product_data = product_data.sort_values(
        ["prd_start_dt", "prd_key"]
    ).reset_index(drop=True)

    product_data.insert(
        0,
        "product_key",
        range(1, len(product_data) + 1)
    )
 
    # Rename Product Columns:
    product_data = product_data.rename(columns={
        "product_key": "Product_Key",
        "prd_id": "Product_Id",
        "prd_key": "Product_Number",
        "prd_nm": "Product_Name",
        "catg_id": "Category_Id",
        "cat": "Category",
        "subcat": "Sub_Category",
        "maintenance": "Maintenance",
        "prd_cost": "Cost",
        "prd_line": "Product_Line",
        "prd_start_dt": "Start_Date"
    })

    # Select Required Product Columns:
    product_data = product_data[
        [
            "Product_Key",
            "Product_Id",
            "Product_Number",
            "Product_Name",
            "Category_Id",
            "Category",
            "Sub_Category",
            "Maintenance",
            "Cost",
            "Product_Line",
            "Start_Date"
        ]
    ]

    return product_data


# 3. INTEGRATE SALES WITH PRODUCTS:
def integrate_sales_product(sales, products):

    # Select Product Surrogate Key and Join Column:
    product_columns = products[
        ["Product_Key", "Product_Number"]
    ]

    # Join CRM Sales with Final Products:
    sales_data = sales.merge(
        product_columns,
        left_on="sls_prd_key",
        right_on="Product_Number",
        how="left",
        validate="many_to_one"
    )

    return sales_data

# 4. CREATE ANALYTICAL SALES DATA (Fact Table):
def create_analytical_dataset(clean_datasets, customer_data, product_data):

    # Join Sales with Product Key:
    sales = integrate_sales_product(
        clean_datasets["Clean CRM Sales"],
        product_data
    )

    # Select Only Customer Number and Customer Key:
    customer_columns = customer_data[
        [
            "Customer_Key",
            "Customer_Id"
        ]
    ]

    # Join CRM Sales with Final Customers:
    analytical_data = sales.merge(
        customer_columns,
        left_on="sls_cust_id",
        right_on="Customer_Id",
        how="left",
        validate="many_to_one"
    )
    
    # Rename Columns:
    analytical_data = analytical_data.rename(
        columns={
            "sls_ord_num": "Order_Number",
            "sls_order_dt": "Order_Date",
            "sls_ship_dt": "Shipping_Date",
            "sls_due_dt": "Due_Date",
            "sls_sales": "Sales_Amount",
            "sls_quantity": "Quantity",
            "sls_price": "Price"
        }
    )

    # Select Only Required Fact Table Columns:
    analytical_data = analytical_data[
        [
            "Order_Number",
            "Product_Key",      # Surrogate Key
            "Customer_Key",     #Surrogate Key
            "Order_Date",
            "Shipping_Date",
            "Due_Date",
            "Sales_Amount",
            "Quantity",
            "Price"
        ]
    ]

    return analytical_data


# 5. CREATE SALES ANALYSIS:
def create_sales_analysis(analytical_data, customer_data, product_data):

    # Sales by Country:
    sales_country = analytical_data.merge(
        customer_data[
            ["Customer_Key", "Country"]
        ],
        on="Customer_Key",
        how="left"
    )

    sales_by_country = (
        sales_country
        .groupby("Country", dropna=False)["Sales_Amount"]
        .sum()
        .reset_index()
        .sort_values("Sales_Amount", ascending=False)
    )

    # Sales by Category and Subcategory:
    sales_category = analytical_data.merge(
        product_data[
            ["Product_Key", "Category", "Sub_Category"]
        ],
        on="Product_Key",
        how="left"
    )

    sales_by_category = (
        sales_category
        .groupby(
            ["Category", "Sub_Category"],
            dropna=False
        )["Sales_Amount"]
        .sum()
        .reset_index()
        .sort_values("Sales_Amount", ascending=False)
    )

    # Monthly Sales:
    monthly_data = analytical_data.copy()

    monthly_data["Sales_Month"] = (
        pd.to_datetime(monthly_data["Order_Date"])
        .dt.to_period("M")
        .astype(str)
    )

    monthly_sales = (
        monthly_data
        .groupby("Sales_Month")["Sales_Amount"]
        .sum()
        .reset_index()
        .sort_values("Sales_Month")
    )

    # Sales Pivot: Country vs Product Line:
    pivot_data = analytical_data.merge(
        customer_data[
            ["Customer_Key", "Country"]
        ],
        on="Customer_Key",
        how="left"
    )

    pivot_data = pivot_data.merge(
        product_data[
            ["Product_Key", "Product_Line"]
        ],
        on="Product_Key",
        how="left"
    )

    sales_pivot = pd.pivot_table(
        pivot_data,
        values="Sales_Amount",
        index="Country",
        columns="Product_Line",
        aggfunc="sum",
        fill_value=0
    )

    return {
        "Sales by Country": sales_by_country,
        "Sales by Category": sales_by_category,
        "Monthly Sales": monthly_sales,
        "Sales Pivot": sales_pivot
    }


# 6. TRANSFORM ALL CLEANED DATASETS:
def transform_data(clean_datasets):

    # Create Customer Dimension:
    customer_data = integrate_customer_data(clean_datasets)

    # Create Product Dimension:
    product_data = integrate_product_data(clean_datasets)

    # Create Sales Fact Table:
    analytical_data = create_analytical_dataset(
        clean_datasets,
        customer_data,
        product_data
    )

    # Create Sales Analysis:
    sales_analysis = create_sales_analysis(
        analytical_data,
        customer_data,
        product_data
    )

    return {
        "Customer Data": customer_data,
        "Product Data": product_data,
        "Analytical Sales": analytical_data,
        **sales_analysis
    }


# 7. EXECUTION:
if __name__ == "__main__":

    print("\nStarting Data Transformation...")

    # Load Cleaned Data:
    cleaned_data = clean_source_data()

    # Transform Data:
    results = transform_data(cleaned_data)

    # Display Summary:
    print("\n" + "=" * 65)
    print("             DATA TRANSFORMATION SUMMARY")
    print("=" * 65)

    for name, df in results.items():

        print(
            f"{name:<22}: "
            f"{df.shape[0]:,} Rows | "
            f"{df.shape[1]} Columns"
        )

    print("-" * 65)

    # Display Unmatched Records:
    print("\nDATA INTEGRATION SUMMARY:")
    print("-" * 65)

    print(
        "Unmatched Sales Products:",
        results["Analytical Sales"]["Product_Key"].isna().sum()
    )

    print(
        "Unmatched Sales Customers:",
        results["Analytical Sales"]["Customer_Key"].isna().sum()
    )

    print(
        "Products Without ERP Category:",
        results["Product Data"]["Category"].isna().sum()
    )

    print("-" * 65)
    print("                  DATA TRANSFORMATION COMPLETED!")
    print("=" * 65)

    # Preview Customer Data:
    print("\n========= CUSTOMER DATA =========:")
    print(results["Customer Data"].head())

    # Preview Product Data:
    print("\n========= PRODUCT DATA =========:")
    print(results["Product Data"].head())

    # Preview Analytical Data:
    print("\n========= ANALYTICAL SALES DATA =========:")
    print(results["Analytical Sales"].head())

    print("\n========= SALES BY COUNTRY =========:")
    print(results["Sales by Country"].head())

    print("\n========= SALES BY CATEGORY =========:")
    print(results["Sales by Category"].head())

    print("\n========= MONTHLY SALES =========:")
    print(results["Monthly Sales"].head())

    print("\n========= SALES PIVOT =========:")
    print(results["Sales Pivot"].head())
