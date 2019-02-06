use dwsports;
-- Testing table content
SELECT * FROM division;
SELECT * FROM player;
SELECT * FROM sports;
SELECT * FROM team;
-- View 1
-- Number of players for each team
CREATE VIEW TEAM_PLAYERS_COUNT AS
SELECT t.team_id, t.team_name, COUNT(p.player_id) AS number_of_players
FROM player p, team t
WHERE p.team_id = t.team_id
GROUP BY t.team_id, t.team_name;

-- View 2
-- Number of players for each sport
CREATE VIEW SPORT_PLAYERS_COUNT AS
SELECT s.sport_id, s.sport_name, COUNT(p.player_id) AS number_of_players
FROM player p, sports s
WHERE p.sport_id = s.sport_id
GROUP BY s.sport_id, s.sport_name;

-- View 3
-- Number of players for each division
CREATE VIEW DIVISION_PLAYERS_COUNT AS
SELECT d.division_id, d.division_name, COUNT(p.player_id) AS number_of_players
FROM player p, division d
WHERE p.division_id = d.division_id
GROUP BY d.division_id, d.division_name;

-- 1
-- To find how many players are on each team, execute:
SELECT t.team_id, t.team_name, COUNT(p.player_id) AS number_of_players
FROM player p, team t
WHERE p.team_id = t.team_id
GROUP BY t.team_id, t.team_name;

-- OR simply use View:
SELECT * FROM TEAM_PLAYERS_COUNT;

-- Find players only in specified team using view
SELECT * FROM TEAM_PLAYERS_COUNT
WHERE team_name = "Los Angelos Dodgers";

-- 2
-- To see how many players there are per division, execute:
SELECT d.division_id, d.division_name, COUNT(p.player_id) AS number_of_players
FROM player p, division d
WHERE p.division_id = d.division_id
GROUP BY d.division_id, d.division_name;

-- OR simply use View:
SELECT * FROM DIVISION_PLAYERS_COUNT;

-- Find the number of players in the specified division
SELECT * FROM division_players_count
WHERE division_name = "Major League Baseball";

-- 3
-- To see how many players there are per sport,execute:
SELECT s.sport_id, s.sport_name, COUNT(p.player_id) AS number_of_players
FROM player p, sports s
WHERE p.sport_id = s.sport_id
GROUP BY s.sport_id, s.sport_name;

-- OR simply use View:
SELECT * FROM SPORT_PLAYERS_COUNT;

-- 4
-- To count how many Right fielders each sport has, execute:
SELECT s.sport_id, s.sport_name, COUNT(p.player_position) AS number_of_right_fielders
FROM player p, sports s
WHERE p.sport_id = s.sport_id AND p.player_position="Right fielder"
GROUP BY s.sport_id, s.sport_name;

-- 5
-- To count how many Pitchers each team has, execute:
SELECT t.team_id, t.team_name, COUNT(p.player_position) AS number_of_pitchers
FROM player p, team t
WHERE p.team_id = t.team_id AND p.player_position="Pitcher"
GROUP BY t.team_id, t.team_name;

-- 6
-- To count how many Forward each team has, execute:
SELECT t.team_id, t.team_name, COUNT(p.player_position) AS number_of_forwards
FROM player p, team t
WHERE p.team_id = t.team_id AND p.player_position="Forward"
GROUP BY t.team_id, t.team_name;

-- 7
-- To count how many Goalies each division has, execute:
SELECT d.division_id, d.division_name, COUNT(p.player_position) AS number_of_goalies
FROM player p, division d
WHERE p.division_id = d.division_id AND p.player_position="Goalkeeper"
GROUP BY d.division_id, d.division_name;

