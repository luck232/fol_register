DROP PROCEDURE IF EXISTS sp_exist_user;

DELIMITER //

CREATE PROCEDURE sp_exist_user (IN in_username VARCHAR(253))
BEGIN

    DECLARE this_username_id INT;
    
    SELECT user_id INTO this_username_id FROM user WHERE username = in_username;

    IF this_username_id <> 0 THEN
        SELECT TRUE;
    ELSE
        SELECT FALSE;
    END IF;

END //

DELIMITER ;
