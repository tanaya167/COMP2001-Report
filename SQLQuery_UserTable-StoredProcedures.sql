-- CREATE A NEW USER

CREATE PROCEDURE CW2.CreateUser
    @Email_Address NVARCHAR(255),
    @Role NVARCHAR(50)
AS
BEGIN
    INSERT INTO CW2.[User] (Email_Address, Role)
    VALUES (@Email_Address, @Role);
END;



-- READ ALL USERS

CREATE PROCEDURE CW2.ReadUsers
AS
BEGIN
    SELECT * FROM CW2.[User];
END;



-- UPDATE A USER

CREATE PROCEDURE CW2.UpdateUser
    @UserID INT,
    @Email_Address NVARCHAR(255),
    @Role NVARCHAR(50)
AS
BEGIN
    UPDATE CW2.[User]
    SET Email_Address = @Email_Address,
        Role = @Role
    WHERE UserID = @UserID;
END;



-- DELETE A USER

CREATE PROCEDURE CW2.DeleteUser
    @UserID INT
AS
BEGIN
    DELETE FROM CW2.[User] WHERE UserID = @UserID;
END;
