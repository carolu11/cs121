-- Given a user_id, returns the number of different genres of problems answered.
-- For example, if a user answered questions relating to linked lists, trees,
-- and databases, this function should return 3 total genres answered.
DROP FUNCTION IF EXISTS num_genres_answered;

DELIMITER !
CREATE FUNCTION num_genres_answered (user_id INT) 
    RETURNS INT DETERMINISTIC
BEGIN
    DECLARE genres_answered INT;

    SELECT COUNT(DISTINCT genre) INTO genres_answered
    FROM completed_problems c NATURAL JOIN genres
    WHERE c.user_id = user_id;

    RETURN genres_answered;
END !
DELIMITER ;


-- Given a username, returns the number of problems asked to the user.
DROP FUNCTION IF EXISTS num_problems_asked;

DELIMITER !
CREATE FUNCTION num_problems_asked (user_id INT)
    RETURNS INT DETERMINISTIC
BEGIN
    DECLARE problems_asked INT;

    SELECT COUNT(*) INTO problems_asked
    FROM asked_problems NATURAL JOIN users u
    WHERE u.user_id = user_id;

    RETURN problems_asked;
END !
DELIMITER ;


-- View that holds all of the distinct genres across all problems in the 
-- problem bank.
DROP VIEW IF EXISTS distinct_genres;

CREATE VIEW distinct_genres AS
    SELECT DISTINCT genre FROM genres ORDER BY genre;
    

-- The following procedure recalculates the number of problems a given user 
-- has completed that executes whenever a new problem is completed and inserted
-- into the completed_problems table.
DROP PROCEDURE IF EXISTS sp_update_completed_problems;

DELIMITER !
CREATE PROCEDURE sp_update_completed_problems (curr_user_id INT) 
BEGIN
    UPDATE users
    SET num_problems_answered = num_problems_answered + 1
    WHERE user_id = curr_user_id;
END !
DELIMITER ;

-- If a new row is inserted into the completed_problems table, then we need to 
-- update 
DROP TRIGGER IF EXISTS trg_recalc_completed;

DELIMITER !
CREATE TRIGGER trg_recalc_completed 
AFTER INSERT ON completed_problems FOR EACH ROW
BEGIN
    CALL sp_update_completed_problems (NEW.user_id);  
END !
DELIMITER ;