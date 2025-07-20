-- SQL Script 1: Insert new employee Albert
-- This script inserts a new employee with the following details:
-- Name: Albert
-- Position: engineer
-- Join Date: January 24, 2024
-- Years of Experience: 2.5
-- Salary: $50
INSERT INTO employee (
        Name,
        Position,
        Join_Date,
        Year_of_Experience,
        Salary
    )
VALUES ('Albert', 'engineer', '24-Jan-24', 2.5, 50);
-- Verification query to confirm the insertion
SELECT *
FROM employee
WHERE Name = 'Albert';