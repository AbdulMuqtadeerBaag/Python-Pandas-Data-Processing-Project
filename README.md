# Python Pandas Data Processing Project

**An End-to-End Data Processing Pipeline Using Python, Pandas & NumPy**

This project demonstrates an end-to-end data processing workflow that integrates CRM (Customer Relationship Management) and ERP (Enterprise Resource Planning) datasets using Python, Pandas, and NumPy.

The pipeline transforms raw source data into clean, validated, structured, and analysis-ready datasets through a systematic ETL (Extract, Transform, Load) process.

It covers data extraction, exploratory data analysis, data cleaning, quality validation, data integration, transformation, analytical reporting, and result export.

---

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Pandas | Data manipulation and processing |
| NumPy | Numerical operations and calculations |
| CSV | Source data format |
| Excel | Analytical report generation |
| GitHub | Project hosting |

---

## 🏗️ Project Workflow

The project follows a structured six-stage data processing pipeline.

![Project Workflow](Docs/Workflow.jpg)

---

## 📖 Project Overview

The project uses six source datasets from two different business systems.

**CRM (Customer Relationship Management)**
- Customer Information
- Product Information
- Sales Details

**ERP (Enterprise Resource Planning)**
- Customer Master
- Location Master
- Product Category

The objective is to integrate these datasets, resolve data quality issues, create structured analytical datasets, and generate meaningful sales reports.

---

## ⚙️ ETL Pipeline Implementation

### 01. Extract Source Data

**Script:** `s1_Extract_Source_Data.py`

- Read six source CSV files using Pandas.
- Load source datasets into DataFrames.
- Organize datasets using a Python dictionary.
- Implement file existence checks.
- Create reusable data extraction functions.

### 02. Explore Source Data

**Script:** `s2_Explore_Source_Data.py`

- Analyze dataset dimensions (rows and columns).
- Examine column names and data types.
- Generate descriptive statistical summaries.
- Identify missing values and duplicate records.
- Analyze DataFrame memory usage.

### 03. Clean CRM and ERP Data

**Script:** `s3_Clean_Source_Data.py`

- Standardize column names and text values.
- Handle missing customer identifiers.
- Remove duplicate customer records.
- Standardize gender and marital status.
- Convert date columns into datetime format.
- Convert numeric columns into appropriate data types.
- Standardize country and product information.
- Correct invalid sales prices and sales amounts.
- Calculate product end dates using Pandas operations.

### 04. Data Quality Validation

**Script:** `s4_Validate_Clean_Data.py`

- Validate missing and duplicate identifiers.
- Identify invalid customer and product records.
- Validate date formats and date sequences.
- Verify sales amount calculations.
- Check missing and non-positive sales values.
- Validate standardized categorical values.
- Generate a Data Quality Report with PASS/FAIL status.

### 05. Data Transformation and Integration

**Script:** `s5_Transform_Data.py`

- Integrate CRM and ERP customer datasets.
- Integrate product information with ERP categories.
- Join sales data with customer and product information.
- Generate Customer and Product Surrogate Keys.
- Create Customer Dimension data.
- Create Product Dimension data.
- Create an Analytical Sales Fact Table.
- Perform aggregations using groupby().
- Generate monthly sales analysis.
- Create sales pivot reports using pivot_table().

### 06. Export Processed Results

**Script:** `s6_Export_Result.py`

- Export cleaned CRM and ERP datasets into CSV files.
- Export Customer Dimension data.
- Export Product Dimension data.
- Export Analytical Sales data.
- Generate an Excel workbook containing multiple analytical reports.
- Organize final outputs into structured directories.

---

## 📊 Analytical Reporting

The project generates the following analytical outputs:

| Analysis | Description |
|---|---|
| Sales by Country | Analyze sales performance across countries |
| Sales by Category | Compare sales across product categories and subcategories |
| Monthly Sales | Analyze monthly sales trends |
| Sales Pivot | Compare country-wise sales across product lines |

### Final Data Models

**1. Customer Dimension**

Contains integrated customer information, including customer identifiers, names, country, marital status, gender, birth date, and creation date.

**2. Product Dimension**

Contains product identifiers, product names, categories, subcategories, maintenance information, cost, product line, and start date.

**3. Analytical Sales Fact Table**

Contains sales transactions linked with Customer and Product Surrogate Keys, order dates, shipping dates, quantities, prices, and sales amounts.

---

## 📂 Repository Structure

```text
Python-Pandas-Data-Processing-Project/
│
├── Datasets/
│   ├── Source_CRM/
│   │   ├── Cust_Info.csv
│   │   ├── Prod_Info.csv
│   │   └── Sales_Details.csv
│   │
│   └── Source_ERP/
│       ├── Cust_Mst.csv
│       ├── Loc_Mst.csv
│       └── Prod_Catg.csv
│
├── Docs/
│   └── Workflow.jpg
│
├── Scripts/
│   ├── s1_Extract_Source_Data.py
│   ├── s2_Explore_Source_Data.py
│   ├── s3_Clean_Source_Data.py
│   ├── s4_Validate_Clean_Data.py
│   ├── s5_Transform_Data.py
│   └── s6_Export_Result.py
│
├── Output/
│   ├── Cleaned_Data/
│   ├── Customer_Data.csv
│   ├── Product_Data.csv
│   ├── Analytical_Sales.csv
│   └── Sales_Analysis.xlsx
│
├── LICENSE
└── README.md
```

---

## 🎯 Key Technical Concepts Demonstrated

- Python Functions and Modular Programming
- Pandas DataFrames and Series
- Data Extraction and Exploration
- Data Cleaning and Standardization
- Missing Value and Duplicate Handling
- DateTime Conversion and Manipulation
- NumPy Numerical Operations
- DataFrame Merging and Joins
- GroupBy and Aggregation
- Pivot Tables
- Data Quality Validation
- Dimensional Data Modeling
- Surrogate Key Generation
- CSV and Excel File Handling
- ETL Pipeline Development

---

## 💡 Project Highlights

- Built a modular six-stage data processing pipeline.
- Integrated six datasets from CRM and ERP source systems.
- Implemented reusable Python functions for data processing.
- Applied data quality checks before analytical transformation.
- Integrated multiple datasets using Pandas merge operations.
- Created customer and product dimension datasets.
- Developed an analytical sales fact table.
- Generated country-wise, category-wise, and monthly sales reports.
- Automated the export of processed datasets into CSV and Excel formats.

---

## 🛡️ License

This project is licensed under the [MIT License](LICENSE).

---

## 👨‍💻 About the Author

**Abdul Muqtadeer Baag**

BCA Graduate | Aspiring Data Engineer | SQL & Python Enthusiast

I am interested in Data Engineering, Data Analytics, and Database Development. I enjoy building hands-on projects involving data extraction, cleaning, transformation, integration, and analytical reporting.

**Technical Skills:**

- Advanced SQL Server and T-SQL
- Python and Pandas
- NumPy
- Microsoft Excel
- Power BI
- Data Cleaning and Data Transformation
- ETL Pipeline Development
- Data Modeling and Data Warehousing
- Git and GitHub
- Linux

I continuously work on practical projects to strengthen my technical knowledge and develop solutions based on real-world data processing scenarios.

---

## 📬 Connect With Me

- **GitHub:** https://github.com/AbdulMuqtadeerBaag
- **LinkedIn:** https://www.linkedin.com/in/abdul-muqtadeer-baag-499926334
- **Email:** muqtadeerbaag@gmail.com

---

⭐ If you find this project useful, feel free to explore the repository and connect with me!
