-- SQL Script 4: Top 3 employees with highest years of experience
-- This script retrieves the top three employees with the highest years of experience,
-- ordered in descending order
SELECT Name,
    Position,
    Year_of_Experience,
    Salary
FROM employee
ORDER BY Year_of_Experience DESC
LIMIT 3;
-- Alternative approach using ROW_NUMBER() for more complex scenarios
-- SELECT * FROM (
--     SELECT 
--         Name,
--         Position,
--         Year_of_Experience,
--         Salary,
--         ROW_NUMBER() OVER (ORDER BY Year_of_Experience DESC) as rank
--     FROM employee
-- ) ranked_employees
-- WHERE rank <= 3;