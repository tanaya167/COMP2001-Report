CREATE VIEW CW2.FullTrailView AS
SELECT
    CW2.Trail.TrailID,
    CW2.Trail.TrailName,
    CW2.Trail.TrailSummary,
    CW2.Trail.TrailDescription,
    CW2.Trail.Difficulty,
    CW2.Trail.Location AS TrailLocation,
    CW2.Trail.Length AS TrailLength,
    CW2.Trail.ElevationGain,
    CW2.Trail.RouteType,
    CW2.Trail.OwnerID,
    CW2.Trail_LocationPoint.Location_Point,
    CW2.Location_Point.Latitude,
    CW2.Location_Point.Longitude,
    CW2.Location_Point.Description AS LocationDescription,
    CW2.Feature.TrailFeatureID,
    CW2.Feature.TrailFeature,
    CW2.[User].UserID,
    CW2.[User].Email_Address AS UserEmail,
    CW2.[User].Role AS UserRole
FROM
    CW2.Trail
LEFT JOIN CW2.Trail_LocationPoint
    ON CW2.Trail.TrailID = CW2.Trail_LocationPoint.TrailID
LEFT JOIN CW2.Location_Point
    ON CW2.Trail_LocationPoint.Location_Point = CW2.Location_Point.Location_Point
LEFT JOIN CW2.Trail_Feature
    ON CW2.Trail.TrailID = CW2.Trail_Feature.TrailID
LEFT JOIN CW2.Feature
    ON CW2.Trail_Feature.TrailFeatureID = CW2.Feature.TrailFeatureID
LEFT JOIN CW2.[User]
    ON CW2.Trail.OwnerID = CW2.[User].UserID;
