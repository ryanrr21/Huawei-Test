-- SQL Script 2: Update engineer salaries
-- This script updates all employees with position "engineer" 
-- to have a standardized salary of $85
UPDATE employee
SET Salary = 85
WHERE Position = 'engineer';
-- Verification query to show all engineers and their updated salaries
SELECT Name,
    Position,
    Salary
FROM employee
WHERE Position = 'engineer'
ORDER BY Name;