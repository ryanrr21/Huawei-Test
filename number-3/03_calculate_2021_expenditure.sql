-- SQL Script 3: Calculate total salary expenditure for 2021
-- This script calculates the total salary expenditure for employees
-- who were active during the year 2021 (based on join and release dates)
SELECT '2021' AS Year,
    SUM(Salary) AS Total_Expenditure,
    COUNT(*) AS Employee_Count
FROM employee
WHERE (
        -- Employees who joined before or during 2021 and were still active
        (
            Join_Date <= '31-Dec-21'
            AND (
                Release_Date IS NULL
                OR Release_Date > '31-Dec-21'
            )
        )
        OR -- Employees who joined during 2021
        (
            Join_Date >= '01-Jan-21'
            AND Join_Date <= '31-Dec-21'
        )
    );
-- Alternative approach: Calculate monthly expenditure for 2021
SELECT '2021 Total' AS Period,
    SUM(Salary) AS Total_Expenditure
FROM employee
WHERE Join_Date <= '31-Dec-21'
    AND (
        Release_Date IS NULL
        OR Release_Date >= '01-Jan-21'
    );