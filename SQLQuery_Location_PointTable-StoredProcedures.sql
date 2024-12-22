-- CREATE A NEW LOCATION POINT

CREATE PROCEDURE CW2.CreateLocationPoint
    @Latitude DECIMAL(10, 7),
    @Longitude DECIMAL(10, 7),
    @Description NVARCHAR(MAX)
AS
BEGIN
    INSERT INTO CW2.Location_Point (Latitude, Longitude, Description)
    VALUES (@Latitude, @Longitude, @Description);
END;



-- READ ALL LOCATION POINTS

CREATE PROCEDURE CW2.ReadLocationPoints
AS
BEGIN
    SELECT * FROM CW2.Location_Point;
END;



-- UPDATE A LOCATION POINT

CREATE PROCEDURE CW2.UpdateLocationPoint
    @Location_Point INT,
    @Latitude DECIMAL(10, 7),
    @Longitude DECIMAL(10, 7),
    @Description NVARCHAR(MAX)
AS
BEGIN
    UPDATE CW2.Location_Point
    SET Latitude = @Latitude,
        Longitude = @Longitude,
        Description = @Description
    WHERE Location_Point = @Location_Point;
END;



-- DELETE A LOCATION POINT

CREATE PROCEDURE CW2.DeleteLocationPoint
    @Location_Point INT
AS
BEGIN
    DELETE FROM CW2.Location_Point WHERE Location_Point = @Location_Point;
END;
