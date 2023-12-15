
-- Tables Creations
CREATE EXTENSION IF NOT EXISTS "uuid-ossp"; -- Important import this extension to UUIDs

CREATE TABLE Users(
    id UUID PRIMARY KEY DEFAULT uuid_generate_v1(),
    username VARCHAR NOT NULL,
    name VARCHAR NOT NULL,
	surname VARCHAR NOT NULL, 
	email VARCHAR NOT NULL,
    hashed_password VARCHAR NOT NULL,
	is_active bool default false
);


-- Selects 
SELECT * FROM Users;
							
							
-- Scripts:
DROP TABLE Users;							
