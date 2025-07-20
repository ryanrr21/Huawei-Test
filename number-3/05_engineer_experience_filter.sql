-- SQL Script 5: Engineers with 3 years or less experience
-- This script uses a subquery to demonstrate nested filtering logic
-- Returns employees with position "engineer" whose years of experience <= 3
SELECT Name,
    Position,
    Year_of_Experience,
    Salary
FROM employee
WHERE Position = 'engineer'
    AND Year_of_Experience <= 3
ORDER BY Year_of_Experience DESC,
    Name;
-- Alternative approach using subquery for demonstration
-- SELECT 
--     Name,
--     Position,
--     Year_of_Experience,
--     Salary
-- FROM employee 
-- WHERE Position IN (
--     SELECT DISTINCT Position 
--     FROM employee 
--     WHERE Position = 'engineer'
-- )
-- AND Year_of_Experience <= 3
-- ORDER BY Year_of_Experience DESC, Name;