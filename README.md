# CS121 Final Project
Names: Carolyn Lu, Teresa Huang
Emails: cwlu@caltech.edu, thhuang@caltech.edu

Our data comes from: <br/>
https://www.kaggle.com/datasets/jacobhds/leetcode-solutions-and-content-kpis?resource=download <br/>
https://www.kaggle.com/datasets/manthansolanki/leetcode-questions <br/>
We combined both datasets to create our desired schema. 

To load the data from the command-line into MySQL run the following commands: <br/>
$ cd folder: <br/>
$ mysql --local-infile=1 -u root -p <br/>
mysql> source setup.sql; <br/>
mysql> source load-data.sql; <br/>
mysql> source setup-passwords.sql; <br/>
mysql> source setup-routines.sql; <br/>
mysql> source grant-permissions.sql; <br/>
mysql> source queries.sql; (for queries) <br/>
mysql> quit; <br/>
$ python3 app-admin.py <br/>
OR <br/>
$ python3 app-client.py <br/>

Depending on whether you are in the admin or client profile you will have the
following options: 

For admin: <br/>
(l) - Login <br/>
(a) - Create and add new users <br/>
(q) - Quit <br/>

For client: <br/>
(l) - Login <br/>
(i) - Get genres of problems answered so far <br/>
(ii) - Get number of problems completed <br/>
(iii) - Get number of problems asked <br/>
(g) - Find a problem with a certain genre to practice <br/>
(p) - Enter a password to unlock admin responsibilities <br/>
(q) - Quit <br/>

Note that if we had more time, we would've added more admin functionalities 
such as inserting/updating/deleting problems, and also giving them the option 
to access all the user information if desired.