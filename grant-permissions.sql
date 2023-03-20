CREATE USER 'cwlu'@'localhost' IDENTIFIED BY 'ilovegoogle';
CREATE USER 'thhuang'@'localhost' IDENTIFIED BY 'binglover123';
CREATE USER 'leetcodegrinder'@'localhost' IDENTIFIED BY 'iloveleetcode';
-- Can add more users or refine permissions
GRANT ALL PRIVILEGES ON shelterdb.* TO 'cwlu'@'localhost';
GRANT ALL PRIVILEGES ON shelterdb.* TO 'thhuang'@'localhost';
GRANT SELECT ON shelterdb.* TO 'leetcodegrinder'@'localhost';
FLUSH PRIVILEGES;