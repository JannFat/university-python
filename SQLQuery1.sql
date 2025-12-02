cursor.execute(""

IF OBJECT ID('students','U') IS NULL
CREATE TABLE students(
    id INT IDENTITY (1,1) PRIMARY KEY,
    name NVARCHAR(50),
    age INT,
    grade NVARCHAR(10)
    )
    "")
