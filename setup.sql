-- clean up old tables;
-- must drop tables with foreign keys first
-- due to referential integrity constraints
DROP TABLE IF EXISTS asked_problems;
DROP TABLE IF EXISTS completed_problems;
DROP TABLE IF EXISTS solutions;
DROP TABLE IF EXISTS genres;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS problems;

-- Table that represents the users using the Leetcode Recommender, 
-- uniquely identified by user_id.
CREATE TABLE users (
    user_id INT AUTO_INCREMENT,
    username VARCHAR(30) NOT NULL UNIQUE,
    -- new users will have 0 questions answered
    num_problems_answered INT NOT NULL DEFAULT 0,
    -- 0 for false, 1 for true
    is_admin BOOLEAN NOT NULL,
    PRIMARY KEY (user_id)
);

-- Table containing all leetcode problems available, uniquely identified
-- by problem_id.
CREATE TABLE problems (
    problem_id INT,
    problem_name VARCHAR(200) NOT NULL,
    -- description of the problem
    problem_text TEXT,
    -- Easy, Medium, or Hard
    difficulty VARCHAR(10) NOT NULL,
    PRIMARY KEY (problem_id),
    CHECK (difficulty IN ('Easy', 'Medium', 'Hard'))
);

-- Table containing all leetcode solutions available, uniquely identified
-- by problem_id. Every problem will have a corresponding solution associated
-- with it.
CREATE TABLE solutions (
    problem_id INT NOT NULL,
    -- link to the solution's discussion post  
    link VARCHAR(1000) NOT NULL,
    -- solution to the associated problem_id in Python
    solution TEXT NOT NULL,
    -- username of the user who posted the solution
    username_posted VARCHAR(30),
    PRIMARY KEY (problem_id),
    FOREIGN KEY (problem_id) REFERENCES problems(problem_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

-- Table containing all leetcode genres for each problem, uniquely identified
-- by (problem_id, genre). Note that every problem_id will not have duplicate
-- genres, however each problem_id may have multiple genres associated with it.
-- Every problem_id will have at least one genre associated with it.
CREATE TABLE genres (
    problem_id INT, 
    genre VARCHAR(200) NOT NULL, 
    PRIMARY KEY (problem_id, genre),
    FOREIGN KEY (problem_id) REFERENCES problems(problem_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

-- Table containing all the asked problems to each user (represented by
-- user_id). 
CREATE TABLE asked_problems (
    user_id INT,
    problem_id INT,
    time_asked DATETIME DEFAULT (CURRENT_TIMESTAMP),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (problem_id) REFERENCES problems(problem_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

-- Table containing all the completed problems to each user (represented by
-- user_id).
CREATE TABLE completed_problems (
    user_id INT,
    problem_id INT,
    time_completed DATETIME DEFAULT (CURRENT_TIMESTAMP),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (problem_id) REFERENCES problems(problem_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

-- Create indexes for attributes that are frequently used
CREATE INDEX idx_users ON users (num_problems_answered);
CREATE INDEX idx_problems ON problems (problem_name, difficulty);