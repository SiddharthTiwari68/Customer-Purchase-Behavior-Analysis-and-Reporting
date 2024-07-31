CREATE DATABASE customer_purchase_db;
USE customer_purchase_db;

# Step 1: Data Normalization Steps
CREATE TABLE Customer (
    CustomerID INT PRIMARY KEY,
    CustomerName VARCHAR(255)
);

CREATE TABLE Product (
    ProductID INT PRIMARY KEY,
    ProductName VARCHAR(255),
    ProductCategory VARCHAR(255)
);

CREATE TABLE Country (
    CountryName VARCHAR(255) PRIMARY KEY
);

CREATE TABLE Purchase (
    TransactionID INT PRIMARY KEY,
    CustomerID INT,
    ProductID INT,
    PurchaseQuantity INT,
    PurchasePrice DECIMAL(10, 2),
    PurchaseDate DATE,
    CountryName VARCHAR(255),
    FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID),
    FOREIGN KEY (ProductID) REFERENCES Product(ProductID),
    FOREIGN KEY (CountryName) REFERENCES Country(CountryName)
);
# Step 2: Import Data into Normalized Tables

INSERT IGNORE INTO Customer (CustomerID, CustomerName)
SELECT DISTINCT CustomerID, CustomerName
FROM customer_purchase_master;
select * from customer;

INSERT IGNORE INTO Product (ProductID, ProductName, ProductCategory)
SELECT DISTINCT ProductID, ProductName, ProductCategory
FROM customer_purchase_master;
select * from product;

INSERT IGNORE INTO Country (CountryName)
SELECT DISTINCT Country
FROM customer_purchase_master;
select * from country;

INSERT INTO Purchase (TransactionID, CustomerID, ProductID, PurchaseQuantity, PurchasePrice, PurchaseDate, CountryName)
SELECT TransactionID, CustomerID, ProductID, PurchaseQuantity, PurchasePrice, PurchaseDate, Country
FROM customer_purchase_master;
select * from purchase;

# Check Customer Data
SELECT * FROM Customer;

# Check Product Data
SELECT * FROM Product;

# Check Country Data
SELECT * FROM Country;

# Check Purchase Data
SELECT * FROM Purchase;

# Handle Missing Values and Data Quality
SELECT * FROM Purchase
WHERE CustomerID NOT IN (SELECT CustomerID FROM Customer)
   OR ProductID NOT IN (SELECT ProductID FROM Product)
   OR CountryName NOT IN (SELECT CountryName FROM Country);

# Handle Missing Values
SET SQL_SAFE_UPDATES = 0;

DELETE FROM Purchase
WHERE CustomerID IS NULL
   OR ProductID IS NULL
   OR PurchaseQuantity IS NULL
   OR PurchasePrice IS NULL
   OR PurchaseDate IS NULL
   OR CountryName IS NULL;
   
  SELECT TransactionID
FROM Purchase
WHERE CustomerID IS NULL
   OR ProductID IS NULL
   OR PurchaseQuantity IS NULL
   OR PurchasePrice IS NULL
   OR PurchaseDate IS NULL
   OR CountryName IS NULL;
   
  # Create Relationships
  ALTER TABLE Purchase
ADD CONSTRAINT fk_customer
FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID);

ALTER TABLE Purchase
ADD CONSTRAINT fk_product
FOREIGN KEY (ProductID) REFERENCES Product(ProductID);

ALTER TABLE Purchase
ADD CONSTRAINT fk_country
FOREIGN KEY (CountryName) REFERENCES Country(CountryName);

# Advanced Queries

-- Total purchases per customer
SELECT 
    Purchase.CustomerID, 
    Customer.CustomerName, 
    SUM(Purchase.PurchaseQuantity) AS TotalQuantity, 
    SUM(Purchase.PurchasePrice * Purchase.PurchaseQuantity) AS TotalSales
FROM 
    Purchase
JOIN 
    Customer ON Purchase.CustomerID = Customer.CustomerID
GROUP BY 
    Purchase.CustomerID, Customer.CustomerName
LIMIT 0, 1000;

-- Total sales per product
SELECT 
    p.ProductID, 
    pr.ProductName, 
    SUM(p.PurchaseQuantity) AS TotalQuantity, 
    SUM(p.PurchasePrice * p.PurchaseQuantity) AS TotalSales
FROM 
    Purchase AS p
JOIN 
    Product AS pr ON p.ProductID = pr.ProductID
GROUP BY 
    p.ProductID, pr.ProductName
LIMIT 0, 1000;


-- Total sales per country
SELECT 
    c.CountryName, 
    SUM(p.PurchasePrice * p.PurchaseQuantity) AS TotalSales
FROM 
    Purchase AS p
JOIN 
    Country AS c ON p.CountryName = c.CountryName
GROUP BY 
    c.CountryName
LIMIT 0, 1000;




   
 












