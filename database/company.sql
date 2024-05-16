-- Hashed passsword from https://bcrypt-generator.com/: $2a$12$I7VzQeZtFDqu9CPCPEUDv.NG4dapERcTsTSNgkdqPxDv8Ik3QPTNC
-- epoch time from https://www.epochconverter.com/: 1715329042
-- UUID from https://www.uuidgenerator.net/: 568f046c-8f72-4212-9a79-fcf908fb8ca4

DROP TABLE IF EXISTS users;

CREATE TABLE users(
    user_pk                 TEXT,
    user_username           TEXT,
    user_first_name         TEXT,
    user_last_name          TEXT,
    user_email              TEXT,
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















