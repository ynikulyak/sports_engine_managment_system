-- Create database if it is not already created
CREATE SCHEMA IF NOT EXISTS sports;

-- Ensure use of database
USE sports;

-- Create database tables with table property information
DROP TABLE IF EXISTS sports;
CREATE TABLE sports (sport_id int primary key NOT NULL AUTO_INCREMENT,
        sport_name varchar(20) NOT NULL, sport_description varchar(80))
    AUTO_INCREMENT = 1;
    
DROP TABLE IF EXISTS division;
CREATE TABLE division (division_id int primary key NOT NULL AUTO_INCREMENT,
        division_name varchar(60) NOT NULL, sport_id INT NOT NULL,
  CONSTRAINT division_fk_sports
    FOREIGN KEY (sport_id)
    REFERENCES sports (sport_id))
    AUTO_INCREMENT = 1000;
    
DROP TABLE IF EXISTS team;
CREATE TABLE team (team_id int primary key NOT NULL AUTO_INCREMENT,
        team_name varchar(20) NOT NULL, sport_id INT NOT NULL,
    division_id INT NOT NULL,
  CONSTRAINT team_fk_sports
    FOREIGN KEY (sport_id)
    REFERENCES sports (sport_id),
  CONSTRAINT team_fk_division
    FOREIGN KEY (division_id)
    REFERENCES division (division_id))
    AUTO_INCREMENT = 10;
    
DROP TABLE IF EXISTS player;
CREATE TABLE player (player_id int primary key NOT NULL AUTO_INCREMENT,
        player_first_name varchar(20) NOT NULL,
        player_last_name varchar(20) NOT NULL, player_position varchar(20))
    AUTO_INCREMENT = 100;
    
DROP TABLE IF EXISTS team_members;
CREATE TABLE team_members (team_id int not null, player_id int not null,
	CONSTRAINT team_members_fk_team
		FOREIGN KEY (team_id)
        REFERENCES team (team_id),
	CONSTRAINT team_members_fk_player
		FOREIGN KEY (player_id)
        REFERENCES player (player_id));
    

    
DROP TABLE IF EXISTS admin;
CREATE TABLE admin (admin_id int primary key NOT NULL AUTO_INCREMENT,
        admin_first_name varchar(20) NOT NULL, admin_last_name varchar(20) NOT NULL,
    admin_user_name varchar(40) NOT NULL UNIQUE, admin_password varchar(80) NOT NULL)
    AUTO_INCREMENT = 10000;

-- Insert sport table data
INSERT INTO sports VALUES (DEFAULT,'Soccer', 'Soccer description.');
INSERT INTO sports VALUES (DEFAULT,'Baseball', 'Baseball description.');

INSERT INTO division VALUES (default,'Major League Baseball', 2);
INSERT INTO division VALUES (default,'Major League Soccer', 1);

-- Insert team table data
INSERT INTO team VALUES (default,'Boston Red Sox', 2, 1000);
INSERT INTO team VALUES (default, 'Los Angelos Dodgers', 2, 1000);
INSERT INTO team VALUES (default, 'Atlanta United', 1, 1001);

-- Inserting baseball players
INSERT INTO player VALUES (100, 'Mookie', 'Betts', 'Right fielder');
INSERT INTO player VALUES (101, 'Chris', 'Sale', 'Pitcher');
INSERT INTO player VALUES (102, 'J.D.', 'Martinez', 'Right fielder');
INSERT INTO player VALUES (103, 'Andrew', 'Benintendi', 'Left fielder');
INSERT INTO player VALUES (104, 'Dustin', 'Pedroia', 'Second baseman');
INSERT INTO player VALUES (105, 'Clayton', 'Kershaw', 'Pitcher');
INSERT INTO player VALUES (106, 'Cody', 'Bellinger', 'First baseman');
INSERT INTO player VALUES (107, 'Justin', 'Turner', 'Third baseman');
INSERT INTO player VALUES (108, 'Corey', 'Seager', 'Shortstop');
INSERT INTO player VALUES (109, 'Enrique', 'Hernandez', 'Center fielder');

-- Inserting soccer players
INSERT INTO player VALUES (110, 'Josef', 'Martinez','Forward');
INSERT INTO player VALUES (111, 'Miguel', 'Almiron', 'Midfielder');
INSERT INTO player VALUES (112, 'Brad', 'Guzan', 'Goalkeeper');
INSERT INTO player VALUES (113, 'Michael', 'Parkhurst', 'Defender');
INSERT INTO player VALUES (114, 'Ezequiel', 'Barco', 'Midfielder');
INSERT INTO player VALUES (115, 'Aaron', 'Long', 'Defender');
INSERT INTO player VALUES (116, 'Vincent', 'Bezecourt', 'Midfielder');
INSERT INTO player VALUES (117, 'Ben', 'Mines', 'Forward');
INSERT INTO player VALUES (118, 'Evan', 'Louro', 'Goalkeeper');
INSERT INTO player VALUES (119, 'Hassan', 'Ndam', 'Defender');

-- Insert team members
INSERT INTO team_members VALUES (10, 100);
INSERT INTO team_members VALUES (10, 101); 
INSERT INTO team_members VALUES (10, 102); 
INSERT INTO team_members VALUES (10, 103); 
INSERT INTO team_members VALUES (10, 104); 
INSERT INTO team_members VALUES (11, 100); 
INSERT INTO team_members VALUES (11, 101); 
INSERT INTO team_members VALUES (11, 105); 
INSERT INTO team_members VALUES (10, 106); 
INSERT INTO team_members VALUES (10, 107); 
INSERT INTO team_members VALUES (10, 108); 
INSERT INTO team_members VALUES (10, 109); 

INSERT INTO team_members VALUES (12, 110); 
INSERT INTO team_members VALUES (12, 111); 
INSERT INTO team_members VALUES (12, 112); 
INSERT INTO team_members VALUES (12, 113); 
INSERT INTO team_members VALUES (12, 114); 
INSERT INTO team_members VALUES (12, 115); 
INSERT INTO team_members VALUES (12, 116); 
INSERT INTO team_members VALUES (12, 117); 
INSERT INTO team_members VALUES (12, 118);
INSERT INTO team_members VALUES (12, 119); 
 
 
INSERT INTO admin VALUES (10000, 'first', 'user', 'admin', SHA1('admin'));

