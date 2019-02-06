DROP SCHEMA IF EXISTS dwsports;
CREATE SCHEMA dwsports;
USE dwsports;

CREATE TABLE team (team_id int primary key NOT NULL,
        team_name varchar(20) NOT NULL);
    
CREATE TABLE division (division_id int primary key NOT NULL,
        division_name varchar(60) NOT NULL);

CREATE TABLE sports (sport_id int primary key NOT NULL,
        sport_name varchar(25) NOT NULL, 
        sport_description varchar(80));

CREATE TABLE player (
		team_id INT NOT NULL,
        division_id INT NOT NULL,
        sport_id INT NOT NULL,
        player_id INT NOT NULL,
        player_name varchar(50) NOT NULL,
        player_position varchar(20),
                
        CONSTRAINT team_fk FOREIGN KEY(team_id)
        REFERENCES team(team_id) ON DELETE NO ACTION ON UPDATE NO ACTION,
        
        CONSTRAINT division_fk FOREIGN KEY(division_id)
        REFERENCES division(division_id) ON DELETE NO ACTION ON UPDATE NO ACTION,
        
        CONSTRAINT sports_fk FOREIGN KEY(sport_id)
        REFERENCES sports(sport_id) ON DELETE NO ACTION ON UPDATE NO ACTION        
);

INSERT INTO dwsports.team SELECT team_id, team_name FROM sports.team;
INSERT INTO dwsports.division SELECT division_id, division_name FROM sports.division;
INSERT INTO dwsports.sports SELECT sport_id, sport_name, sport_description FROM sports.sports;
INSERT INTO dwsports.player 
	 (team_id, division_id, sport_id, player_id, player_name, player_position)
    SELECT a.team_id, b.division_id, c.sport_id, d.player_id,
    concat( trim(d.player_first_name), ' ', trim(d.player_last_name)),
    d.player_position
	FROM sports.team a, sports.division b, sports.sports c, sports.player d, sports.team_members e
    WHERE a.division_id = b.division_id AND a.team_id = e.team_id  AND e.player_id = d.player_id AND a.sport_id = c.sport_id;


