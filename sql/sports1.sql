CREATE SCHEMA IF NOT EXISTS sports1;

-- Ensure use of database
USE sports1;

-- Create database tables with table property information
DROP TABLE IF EXISTS sports;
CREATE TABLE sports (sport_id int primary key NOT NULL AUTO_INCREMENT,
        sport_name varchar(25) NOT NULL, sport_description varchar(80))
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
        team_name varchar(20) NOT NULL,
    division_id INT NOT NULL,
  CONSTRAINT team_fk_division
    FOREIGN KEY (division_id)
    REFERENCES division (division_id))
    AUTO_INCREMENT = 10;
    
DROP TABLE IF EXISTS player;
CREATE TABLE player (player_id int primary key NOT NULL AUTO_INCREMENT,
		sport_id INT NOT NULL,
        team_id INT NOT NULL,
        player_first_name varchar(20) NOT NULL,
        player_last_name varchar(20) NOT NULL, player_position varchar(20),
  CONSTRAINT player_fk_sports
	FOREIGN KEY (sport_id)
    REFERENCES sports (sport_id),
  CONSTRAINT player_fk_team
	FOREIGN KEY (team_id)
    REFERENCES team (team_id))
    AUTO_INCREMENT = 100;
    


    



