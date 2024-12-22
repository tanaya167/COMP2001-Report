-- CREATE A NEW Trail_LocationPoint 

CREATE PROCEDURE CW2.CreateTrailLocationPoint
    @TrailID INT,
    @Location_Point INT,
    @Order_no INT
AS
BEGIN
    INSERT INTO CW2.Trail_LocationPoint (TrailID, Location_Point, Order_no)
    VALUES (@TrailID, @Location_Point, @Order_no);
END;



-- READ ALL Trail_LocationPoint DATA

CREATE PROCEDURE CW2.ReadTrailLocationPoints
AS
BEGIN
    SELECT * FROM CW2.Trail_LocationPoint;
END;



-- UPDATE A Trail_LocationPoint 

CREATE PROCEDURE CW2.UpdateTrailLocationPoint
    @TrailID INT,
    @Location_Point INT,
    @Order_no INT
AS
BEGIN
    UPDATE CW2.Trail_LocationPoint
    SET Order_no = @Order_no
    WHERE TrailID = @TrailID AND Location_Point = @Location_Point;
END;



-- DELETE A Trail_LocationPoint

CREATE PROCEDURE CW2.DeleteTrailLocationPoint
    @TrailID INT,
    @Location_Point INT
AS
BEGIN
    DELETE FROM CW2.Trail_LocationPoint WHERE TrailID = @TrailID AND Location_Point = @Location_Point;
END;
