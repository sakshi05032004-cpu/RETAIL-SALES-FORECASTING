-- RETAIL SALES ANALYSIS
#CREATE DATABASE
CREATE DATABASE retail_sales_db;
USE retail_sales_db;

#CREATE SALES TABLE

CREATE TABLE retail_sales (
    Date DATE,
    Store_ID VARCHAR(20),
    Category VARCHAR(50),
    Units_Sold INT,
    Unit_Price DECIMAL(10,2),
    Discount_Percent DECIMAL(5,2),
    Promotion INT,
    Holiday INT,
    Sales DECIMAL(15,2)
);

#CHECK TOTAL RECORDS
SELECT COUNT(*) AS Total_Records
FROM retail_sales;

#TOTAL SALES
SELECT
    ROUND(SUM(Sales), 2) AS Total_Sales
FROM retail_sales;

#TOTAL UNITS SOLD
SELECT
    SUM(Units_Sold) AS Total_Units_Sold
FROM retail_sales;

#AVERAGE SALES
SELECT
    ROUND(AVG(Sales), 2) AS Average_Sales
FROM retail_sales;

# TOTAL SALES BY CATEGORY
SELECT
    Category,
    ROUND(SUM(Sales), 2) AS Total_Sales
FROM retail_sales
GROUP BY Category
ORDER BY Total_Sales DESC;

#TOTAL UNITS BY CATEGORY
SELECT
    Category,
    SUM(Units_Sold) AS Total_Units
FROM retail_sales
GROUP BY Category
ORDER BY Total_Units DESC;

#SALES BY STORE
SELECT
    Store_ID,
    ROUND(SUM(Sales), 2) AS Total_Sales
FROM retail_sales
GROUP BY Store_ID
ORDER BY Total_Sales DESC;

#TOP 5 STORES
SELECT
    Store_ID,
    ROUND(SUM(Sales), 2) AS Total_Sales
FROM retail_sales
GROUP BY Store_ID
ORDER BY Total_Sales DESC
LIMIT 5;


#MONTHLY SALES
SELECT
    YEAR(Date) AS Year,
    MONTH(Date) AS Month,
    ROUND(SUM(Sales), 2) AS Monthly_Sales
FROM retail_sales
GROUP BY
    YEAR(Date),
    MONTH(Date)
ORDER BY
    Year,
    Month;
#YEARLY SALES
SELECT
    YEAR(Date) AS Year,
    ROUND(SUM(Sales), 2) AS Total_Sales
FROM retail_sales
GROUP BY YEAR(Date)
ORDER BY Year;

#SALES BY DAY OF WEEK
SELECT
    DAYNAME(Date) AS Day_Name,
    ROUND(SUM(Sales), 2) AS Total_Sales
FROM retail_sales
GROUP BY DAYNAME(Date)
ORDER BY Total_Sales DESC;

#WEEKEND VS WEEKDAY SALES
SELECT
    CASE
        WHEN DAYOFWEEK(Date) IN (1, 7)
        THEN 'Weekend'
        ELSE 'Weekday'
    END AS Day_Type,

    ROUND(SUM(Sales), 2) AS Total_Sales
FROM retail_sales
GROUP BY Day_Type;

#PROMOTION VS NON-PROMOTION SALES
SELECT
    CASE
        WHEN Promotion = 1
        THEN 'Promotion'
        ELSE 'No Promotion'
    END AS Promotion_Status,

    ROUND(SUM(Sales), 2) AS Total_Sales,
    SUM(Units_Sold) AS Total_Units
FROM retail_sales
GROUP BY Promotion_Status;

#HOLIDAY VS NON-HOLIDAY SALES
SELECT
    CASE
        WHEN Holiday = 1
        THEN 'Holiday'
        ELSE 'Non-Holiday'
    END AS Holiday_Status,

    ROUND(SUM(Sales), 2) AS Total_Sales,
    SUM(Units_Sold) AS Total_Units
FROM retail_sales
GROUP BY Holiday_Status;

#DISCOUNT ANALYSIS
SELECT
    Discount_Percent,
    ROUND(SUM(Sales), 2) AS Total_Sales,
    SUM(Units_Sold) AS Total_Units
FROM retail_sales
GROUP BY Discount_Percent
ORDER BY Discount_Percent;

#CATEGORY PERFORMANCE BY STORE
SELECT
    Store_ID,
    Category,
    ROUND(SUM(Sales), 2) AS Total_Sales
FROM retail_sales
GROUP BY
    Store_ID,
    Category
ORDER BY
    Store_ID,
    Total_Sales DESC;

#TOP 10 STORE-CATEGORY COMBINATIONS
SELECT
    Store_ID,
    Category,
    ROUND(SUM(Sales), 2) AS Total_Sales
FROM retail_sales
GROUP BY
    Store_ID,
    Category
ORDER BY Total_Sales DESC
LIMIT 10;

#AVERAGE UNIT PRICE BY CATEGORY
SELECT
    Category,
    ROUND(AVG(Unit_Price), 2) AS Average_Unit_Price
FROM retail_sales
GROUP BY Category
ORDER BY Average_Unit_Price DESC;

#AVERAGE DISCOUNT BY CATEGORY
SELECT
    Category,
    ROUND(AVG(Discount_Percent), 2) AS Average_Discount
FROM retail_sales
GROUP BY Category
ORDER BY Average_Discount DESC;

#DAILY SALES
SELECT
    Date,
    ROUND(SUM(Sales), 2) AS Daily_Sales
FROM retail_sales
GROUP BY Date
ORDER BY Date;

#HIGHEST SALES DAY
SELECT
    Date,
    ROUND(SUM(Sales), 2) AS Total_Sales
FROM retail_sales
GROUP BY Date
ORDER BY Total_Sales DESC
LIMIT 1;

#LOWEST SALES DAY
SELECT
    Date,
    ROUND(SUM(Sales), 2) AS Total_Sales
FROM retail_sales
GROUP BY Date
ORDER BY Total_Sales
LIMIT 1;

#MONTH-OVER-MONTH SALES GROWTH
WITH monthly_sales AS (
SELECT
        DATE_FORMAT(Date, '%Y-%m') AS Sales_Month,
        SUM(Sales) AS Total_Sales

    FROM retail_sales

    GROUP BY DATE_FORMAT(Date, '%Y-%m')
)

SELECT
    Sales_Month,
    ROUND(Total_Sales, 2) AS Total_Sales,

    ROUND(
        (
            Total_Sales -
            LAG(Total_Sales)
            OVER (ORDER BY Sales_Month)
        )
        /
        LAG(Total_Sales)
        OVER (ORDER BY Sales_Month)
        * 100,
        2
    ) AS MoM_Growth_Percent

FROM monthly_sales
ORDER BY Sales_Month;

#CATEGORY SALES CONTRIBUTION
SELECT
    Category,

    ROUND(
        SUM(Sales),
        2
    ) AS Category_Sales,

    ROUND(
        SUM(Sales)
        /
        (SELECT SUM(Sales)
         FROM retail_sales)
        * 100,
        2
    ) AS Sales_Contribution_Percent
FROM retail_sales
GROUP BY Category
ORDER BY Category_Sales DESC;

#STORE SALES CONTRIBUTION
SELECT
    Store_ID,

    ROUND(
        SUM(Sales),
        2
    ) AS Store_Sales,

    ROUND(
        SUM(Sales)
        /
        (SELECT SUM(Sales)
         FROM retail_sales)
        * 100,
        2
    ) AS Sales_Contribution_Percent
FROM retail_sales
GROUP BY Store_ID
ORDER BY Store_Sales DESC;

#MONTHLY CATEGORY PERFORMANCE
SELECT
    YEAR(Date) AS Year,
    MONTH(Date) AS Month,
    Category,

    ROUND(
        SUM(Sales),
        2
    ) AS Total_Sales
FROM retail_sales
GROUP BY
    YEAR(Date),
    MONTH(Date),
    Category
ORDER BY
    Year,
    Month,
    Total_Sales DESC;

#SALES AND UNITS BY PROMOTION
SELECT
    Promotion,

    SUM(Units_Sold) AS Total_Units,

    ROUND(
        SUM(Sales),
        2
    ) AS Total_Sales,

    ROUND(
        AVG(Sales),
        2
    ) AS Average_Sales
FROM retail_sales
GROUP BY Promotion;

#FINAL KPI SUMMARY
SELECT
 COUNT(*) AS Total_Transactions,
 SUM(Units_Sold) AS Total_Units_Sold,
ROUND(
        SUM(Sales),
        2
    ) AS Total_Sales,
 ROUND(
        AVG(Sales),
        2
    ) AS Average_Sales,
ROUND(
        AVG(Unit_Price),
        2
    ) AS Average_Unit_Price,
 ROUND(
        AVG(Discount_Percent),
        2
    ) AS Average_Discount
FROM retail_sales;
