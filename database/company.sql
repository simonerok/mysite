-- Hashed passsword from https://bcrypt-generator.com/: $2a$12$I7VzQeZtFDqu9CPCPEUDv.NG4dapERcTsTSNgkdqPxDv8Ik3QPTNC
-- epoch time from https://www.epochconverter.com/: 1715329042
-- UUID from https://www.uuidgenerator.net/: 568f046c-8f72-4212-9a79-fcf908fb8ca4


/*  USERS */
DROP TABLE IF EXISTS users;

CREATE TABLE users(
    user_pk                 TEXT,
    user_username           TEXT,
    user_first_name         TEXT,
    user_last_name          TEXT,
    user_email              TEXT UNIQUE,
    user_password           TEXT,
    user_role               TEXT,
    user_created_at         INTEGER,
    user_updated_at         INTEGER,
    user_is_verified        INTEGER,
    user_is_blocked         INTEGER,
    user_deleted_at         INTEGER,
    PRIMARY KEY(user_pk)
) WITHOUT ROWID;

INSERT INTO users VALUES(
    "568f046c-8f72-4212-9a79-fcf908fb8ca4",
    "johndoe",
    "Jhon",
    "Doe",
    "admin@company.com",
    "password",
    "admin",
    1715329042,
    0,
    1,
    0,
    0
);

SELECT * FROM users;


/* used for developing */
UPDATE users SET user_role = "admin" WHERE user_username = "adminSofia";
UPDATE users SET user_email = "ss@ss.dk" WHERE user_username = "adminSofia";
DELETE FROM users WHERE user_is_verified = 0;



/* ITEMS */
DROP TABLE IF EXISTS items;

CREATE TABLE items(
    item_pk                 TEXT,
    item_owner_fk           TEXT,
    item_name               TEXT,
    item_splash_image       TEXT,
    item_lat                REAL,  
    item_lon                REAL,  
    item_stars              REAL,
    item_price_per_night    REAL,
    item_created_at         INTEGER,
    item_updated_at         INTEGER,
    item_blocked_at         INTEGER,
    FOREIGN KEY (item_owner_fk) REFERENCES users(user_pk),
    PRIMARY KEY(item_pk)
) WITHOUT ROWID;

-- #Setting the owner to be partner with id: df9d6ede859048398d592fc43a8fb772
SELECT items.*, users.user_username AS owner_name
FROM items
JOIN users ON items.item_owner_fk = users.user_pk


INSERT INTO items VALUES
("5dbce622fa2b4f22a6f6957d07ff4951", "df9d6ede859048398d592fc43a8fb772","Serenity Stay", "photo-1523217582562-09d0def993a6.avif", 55.6761, -3.9410, 4.8, 2541, 1, 0, 0),
("5dbce622fa2b4f22a6f6957d07ff4952", "df9d6ede859048398d592fc43a8fb772", "Coastal Charm", "photo-1564013799919-ab600027ffc6.avif", 55.7539, 37.6208, 4.6, 985, 2, 0, 0),
("5dbce622fa2b4f22a6f6957d07ff4953", "df9d6ede859048398d592fc43a8fb772", "Sunset Villa", "photo-1568605114967-8130f3a36994.avif", 55.0330, -115.6226, 3.9, 429, 3, 0, 0),
("5dbce622fa2b4f22a6f6957d07ff4954", "df9d6ede859048398d592fc43a8fb772", "Breezy Bungalow", "photo-1575517111478-7f6afd0973db.avif", 55.3122, -160.4914, 4.2, 862, 4, 0, 0),
("5dbce622fa2b4f22a6f6957d07ff4955", "df9d6ede859048398d592fc43a8fb772", "Mountain Retreat", "photo-1577915589301-09000ae0d072.avif", 55.9486, -3.1999, 3.5, 1200, 5, 0, 0),
("5dbce622fa2b4f22a6f6957d07ff4956", "df9d6ede859048398d592fc43a8fb772", "Seaside Sanctuary", "photo-1582063289852-62e3ba2747f8.avif", 55.7576, 37.6156, 4.1, 1965, 6, 0, 0),
("5dbce622fa2b4f22a6f6957d07ff4957", "df9d6ede859048398d592fc43a8fb772", "Rustic Ridge", "photo-1589129140837-67287c22521b.avif", 55.8657, -4.2576, 3.8, 1700, 7, 0, 0),
("5dbce622fa2b4f22a6f6957d07ff4958", "df9d6ede859048398d592fc43a8fb772", "Urban Nest", "photo-1602075432748-82d264e2b463.avif", 55.9533, 9.1194, 4.9, 2100, 8, 0, 0),
("5dbce622fa2b4f22a6f6957d07ff4959", "df9d6ede859048398d592fc43a8fb772", "Haven Hideaway", "photo-1613977257365-aaae5a9817ff.avif", 55.1947, 30.2188, 4.5, 985, 9, 0, 0),
("5dbce622fa2b4f22a6f6957d07ff4910", "df9d6ede859048398d592fc43a8fb772", "Forest Haven", "premium_photo-1661883964999-c1bcb57a7357.avif", 55.7047, 13.1910, 4.3, 1200, 10, 0, 0);


SELECT * FROM items;    









