SELECT *
FROM dbo.customers;

SELECT *
FROM dbo.geography;

--*********************************************************************************
--*********************************************************************************

-- Query to join customers and geography tables to enrich customer data with geographic info
SELECT
	c.CustomerID,  -- Selects the unique identifier for each customer
	c.CustomerName,  -- Selects the name of each customer
	c.Email,  -- Selects the email of each customer
	c.Gender,  -- Selects the gender of each customer
	c.Age, -- Selects the age of each customer
	g.Country,  -- Selects the country for the GeographyID
	g.City  -- Selects the city for the GeographyID

FROM 
	dbo.customers c
	LEFT JOIN  -- Shouldn't matter here but left join keeps customers with no geographic data
	dbo.geography g 

ON c.GeographyID = g.GeographyID; -- Joins the two tables on GeographyID to match customers with their geographic info