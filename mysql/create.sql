CREATE TABLE file (
    id              BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    path            TEXT NOT NULL,
    password_hash   CHAR(40),
    password_salt   BINARY(16),
    download_limit  INT UNSIGNED NOT NULL DEFAULT 10,
    download_count  INT UNSIGNED NOT NULL DEFAULT 0
) ENGINE = INNODB;

CREATE TABLE message (
    id              BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    sender          TEXT NOT NULL,          
    receiver        TEXT NOT NULL,
    message         TEXT,
    time            TIMESTAMP NOT NULL
) ENGINE = INNODB;

CREATE TABLE message_attachment (
    message_id      BIGINT UNSIGNED NOT NULL,
    file_id         BIGINT UNSIGNED NOT NULL,
    PRIMARY KEY (message_id, file_id),
    FOREIGN KEY (message_id) REFERENCES message(id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (file_id) REFERENCES file(id)
        ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE = INNODB;

CREATE TABLE client (
    email           VARCHAR(254) NOT NULL PRIMARY KEY
) ENGINE = INNODB;
