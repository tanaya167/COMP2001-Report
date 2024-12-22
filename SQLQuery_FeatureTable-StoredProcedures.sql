-- CREATE A NEW FEATURE

CREATE PROCEDURE CW2.CreateFeature
    @TrailFeature NVARCHAR(255)
AS
BEGIN
    INSERT INTO CW2.Feature (TrailFeature)
    VALUES (@TrailFeature);
END;



-- READ ALL FEATURES

CREATE PROCEDURE CW2.ReadFeatures
AS
BEGIN
    SELECT * FROM CW2.Feature;
END;



-- UPDATE A FEATURE

CREATE PROCEDURE CW2.UpdateFeature
    @TrailFeatureID INT,
    @TrailFeature NVARCHAR(255)
AS
BEGIN
    UPDATE CW2.Feature
    SET TrailFeature = @TrailFeature
    WHERE TrailFeatureID = @TrailFeatureID;
END;



-- DELETE A FEATURE

CREATE PROCEDURE CW2.DeleteFeature
    @TrailFeatureID INT
AS
BEGIN
    DELETE FROM CW2.Feature WHERE TrailFeatureID = @TrailFeatureID;
END;
