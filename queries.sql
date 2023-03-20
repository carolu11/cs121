-- Finds the number of questions answered for each genre for a specific user.
-- For example, if a user answered 3 questions relating to linked lists, and 2
-- relating to trees, then this query result should contain 3 for linked lists
-- and 2 for trees. Corresponds to RA #1.
SELECT genre, COUNT(problem_id) AS num_answered 
FROM genres NATURAL JOIN completed_problems
WHERE user_id = '1'
GROUP BY genre 
ORDER BY genre;

-- Finds the number of different genres of problems answered for user_id 1.
-- For example, if a user answered questions relating to linked lists, trees,
-- and databases, this function should return 3 total genres answered.
SELECT COUNT(DISTINCT genre) INTO genres_answered
FROM completed_problems c NATURAL JOIN genres
WHERE user_id = '1';

-- Finds remaining problems with their corresponding information (i.e. 
-- problem_id, name, description, difficulty, genre, and solution) to ask the
-- given user under the "Tree" genre.
-- Note that this does not include problems that have already been asked to a
-- given user or a user has already completed. 
-- Corresponds to RA #2.
SELECT problem_id, problem_name, problem_text, difficulty, genre, solution
FROM genres NATURAL JOIN problems NATURAL JOIN solutions
WHERE genre = 'Tree' AND (problem_id NOT IN 
    (SELECT problem_id 
    FROM asked_problems NATURAL JOIN completed_problems
    WHERE user_id='1'))
ORDER BY problem_id;

-- Finds the corresponding user_id of a username
SELECT user_id FROM users WHERE username='cwlu';

-- Finds all distinct problem genres
SELECT DISTINCT genre FROM genres ORDER BY genre;

-- Finds the number of problems user_id 1 answered.
SELECT num_problems_answered FROM users WHERE user_id='1';


-- Finds remaining problems with their corresponding information (i.e. 
-- problem_id, name, description, difficulty, genre, and solution) to ask the
-- given user under the "easy" difficulty.
-- Note that this does not include problems that have already been asked to a
-- given user or a user has already completed. Difficulties are
-- case-insensitive.
SELECT problem_id, problem_name, problem_text, difficulty, genre, solution
FROM genres NATURAL JOIN problems NATURAL JOIN solutions
WHERE UPPER(difficulty) = UPPER('easy') AND (problem_id NOT IN 
    (SELECT problem_id 
    FROM asked_problems NATURAL JOIN completed_problems
    WHERE user_id='1'))
ORDER BY problem_id;

-- Finds the user with the most number of problems answered.
SELECT * FROM users 
WHERE num_problems_answered = (SELECT MAX(num_problems_answered) FROM users);