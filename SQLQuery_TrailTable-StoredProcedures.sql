-- CREATE A NEW TRAIL

CREATE PROCEDURE CW2.CreateTrail
    @TrailName NVARCHAR(255),
    @TrailSummary NVARCHAR(MAX),
    @TrailDescription NVARCHAR(MAX),
    @Difficulty NVARCHAR(50),
    @Location NVARCHAR(255),
    @Length FLOAT,
    @ElevationGain FLOAT,
    @RouteType NVARCHAR(50),
    @OwnerID INT
AS
BEGIN
    INSERT INTO CW2.TRAIL (TrailName, TrailSummary, TrailDescription, Difficulty, Location, Length, ElevationGain, RouteType, OwnerID)
    VALUES (@TrailName, @TrailSummary, @TrailDescription, @Difficulty, @Location, @Length, @ElevationGain, @RouteType, @OwnerID);
END;



-- SELECT/READ A TRAIL

CREATE PROCEDURE CW2.ReadTrails
AS
BEGIN
    SELECT * FROM CW2.TRAIL;
END;



-- UPDATE A TRAIL

CREATE PROCEDURE CW2.UpdateTrail
    @TrailID INT,
    @TrailName NVARCHAR(255),
    @TrailSummary NVARCHAR(MAX),
    @TrailDescription NVARCHAR(MAX),
    @Difficulty NVARCHAR(50),
    @Location NVARCHAR(255),
    @Length FLOAT,
    @ElevationGain FLOAT,
    @RouteType NVARCHAR(50),
    @OwnerID INT
AS
BEGIN
    UPDATE CW2.TRAIL
    SET TrailName = @TrailName,
        TrailSummary = @TrailSummary,
        TrailDescription = @TrailDescription,
        Difficulty = @Difficulty,
        Location = @Location,
        Length = @Length,
        ElevationGain = @ElevationGain,
        RouteType = @RouteType,
        OwnerID = @OwnerID
    WHERE TrailID = @TrailID;
END;



-- DELETE A TRAIL

CREATE PROCEDURE CW2.DeleteTrail
    @TrailID INT
AS
BEGIN
    DELETE FROM CW2.TRAIL WHERE TrailID = @TrailID;
END;
