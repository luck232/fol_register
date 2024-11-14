DROP TABLE IF EXISTS user;
CREATE TABLE user(
    user_id INT NOT NULL AUTO_INCREMENT,
    username VARCHAR(253) UNIQUE,
    shapass VARCHAR(60),
    PRIMARY KEY (user_id)
);

