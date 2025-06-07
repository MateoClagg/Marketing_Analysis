SELECT *
FROM dbo.products;

--**************************************************************************
--**************************************************************************

-- Query to categorize products 
SELECT
	ProductID,	-- Selects the unique identifier for each product
	ProductName,  -- Selects the name of each product
	Price,  --Selects the price of each product

	CASE  -- Categorizes the products into price categories: Low, Medium, or High
		WHEN Price <50 THEN 'Low'
		WHEN Price BETWEEN 50 and 200 THEN 'Medium'
		ELSE 'High'
	END AS PriceCategory -- Name of new column containing prce categories

FROM dbo.products;
