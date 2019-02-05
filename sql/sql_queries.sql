use dwsports;
-- Testing table content
SELECT * FROM division;
SELECT * FROM player;
SELECT * FROM sports;
SELECT * FROM team;
-- 1
-- To find how many players are on each team, execute:
SELECT t.team_id, t.team_name, COUNT(p.player_id) AS number_of_players
FROM player p, team t
WHERE p.team_id = t.team_id
GROUP BY t.team_id, t.team_name;

-- 2
-- To see how many players there are per division, execute:
SELECT d.division_id, d.division_name, COUNT(p.player_id) AS number_of_players
FROM player p, division d
WHERE p.division_id = d.division_id
GROUP BY d.division_id, d.division_name;

-- 3
-- To see how many players there are per sport,execute:
SELECT s.sport_id, s.sport_name, COUNT(p.player_id) AS number_of_players
FROM player p, sports s
WHERE p.sport_id = s.sport_id
GROUP BY s.sport_id, s.sport_name;

-- 4
-- To count how many divisions each sport has, execute:
-- Currently has no relation
SELECT s.sport_id, s.sport_name, COUNT(d.division_id) AS number_of_divisions
FROM division d, sports s
WHERE d.sport_id = s.sport_id
GROUP BY s.sport_id, s.sport_name;

-- 5
-- To count how many teams each division has, execute:
-- Currently has no relation
SELECT d.division_id, d.division_name, COUNT(t.team_id) AS number_of_teams
FROM division d, team t
WHERE t.division_id = d.division_id
GROUP BY d.division_id, d.division_name;

-- 6
-- To count how many teams each sport has, execute:
-- Currently has no relation
SELECT s.sport_id, s.sport_name, COUNT(t.team_id) AS number_of_teams
FROM team t, sports s
WHERE t.sport_id = s.sport_id
GROUP BY s.sport_id, s.sport_name;