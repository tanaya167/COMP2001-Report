CREATE TABLE CW2.Owner (
    OwnerID INT NOT NULL PRIMARY KEY,
    OwnerName VARCHAR(255) NOT NULL
);

CREATE TABLE CW2.Trail (
    TrailID INT NOT NULL PRIMARY KEY,
    TrailName VARCHAR(255) NOT NULL,
    TrailSummary TEXT,
    TrailDescription TEXT,
    Difficulty VARCHAR(50),
    Location VARCHAR(255),
    Length DECIMAL(10, 2),
    ElevationGain INT,
    RouteType VARCHAR(100),
    OwnerID INT,
    CONSTRAINT FK_Owner FOREIGN KEY (OwnerID) REFERENCES CW2.Owner(OwnerID)
);

CREATE TABLE CW2.Location_point(
    Location_point INT NOT NULL PRIMARY KEY,
    Latitude DECIMAL (10, 7) NOT NULL,
    Longitude DECIMAL (10, 7) NOT NULL,
    Description TEXT
);

CREATE TABLE CW2.Feature(
    TrailFeatureID INT NOT NULL PRIMARY KEY,
    TrailFeature VARCHAR(255) NOT NULL
);

CREATE TABLE CW2.Trail_LocationPoint (
    TrailID INT NOT NULL, 
    Location_Point INT NOT NULL, 
    Order_no INT NOT NULL, 
    CONSTRAINT PK_Trail_Location_Point PRIMARY KEY (TrailID, Location_Point), 
    CONSTRAINT FK_Trail FOREIGN KEY (TrailID) REFERENCES CW2.TRAIL(TrailID), 
    CONSTRAINT FK_Location_Point FOREIGN KEY (Location_Point) REFERENCES CW2.Location_Point(Location_Point) 
);

CREATE TABLE CW2.Trail_Feature (
    TrailID INT NOT NULL, 
    TrailFeatureID INT NOT NULL, 
    CONSTRAINT PK_Trail_Feature PRIMARY KEY (TrailID, TrailFeatureID), 
    CONSTRAINT FK_Trail_Feature_Trail FOREIGN KEY (TrailID) REFERENCES CW2.TRAIL(TrailID), 
    CONSTRAINT FK_Trail_Feature_Feature FOREIGN KEY (TrailFeatureID) REFERENCES CW2.Feature(TrailFeatureID) 
);

CREATE TABLE CW2.[User] (
    UserID INT NOT NULL PRIMARY KEY, 
    Email_Address VARCHAR(255) NOT NULL UNIQUE, 
    Role VARCHAR(50) NOT NULL 
);
