-- CREATE A NEW Trail_Feature 

CREATE PROCEDURE CW2.CreateTrailFeature
    @TrailID INT,
    @TrailFeatureID INT
AS
BEGIN
    INSERT INTO CW2.Trail_Feature (TrailID, TrailFeatureID)
    VALUES (@TrailID, @TrailFeatureID);
END;



-- READ ALL Trail_Feature DATA

CREATE PROCEDURE CW2.ReadTrailFeatures
AS
BEGIN
    SELECT * FROM CW2.Trail_Feature;
END;



-- UPDATE A Trail_Feature 

CREATE PROCEDURE CW2.UpdateTrailFeature
    @TrailID INT,
    @TrailFeatureID INT
AS
BEGIN
    UPDATE CW2.Trail_Feature
    SET TrailFeatureID = @TrailFeatureID
    WHERE TrailID = @TrailID;
END;



-- DELETE A Trail_Feature 

CREATE PROCEDURE CW2.DeleteTrailFeature
    @TrailID INT,
    @TrailFeatureID INT
AS
BEGIN
    DELETE FROM CW2.Trail_Feature WHERE TrailID = @TrailID AND TrailFeatureID = @TrailFeatureID;
END;
