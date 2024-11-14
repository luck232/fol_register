DROP PROCEDURE IF EXISTS sp_create_user;
DELIMITER //

CREATE PROCEDURE sp_create_user (IN in_username VARCHAR(253), IN in_shapass VARCHAR(60))
BEGIN

    INSERT IGNORE INTO user (username, shapass) 
    VALUES (in_username, in_shapass);

    IF row_count() > 0 THEN
        SELECT TRUE;
    ELSE
        SELECT FALSE;
    END IF;
END //

DELIMITER ;
