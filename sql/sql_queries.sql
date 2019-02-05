use dwsports;
-- Testing table content
SELECT * FROM division;
SELECT * FROM player;
SELECT * FROM sports;
SELECT * FROM team;

-- To find how many players are on each team
SELECT t.team_id, t.team_name, COUNT(p.player_id) AS number_of_players
FROM player p, team t
WHERE p.team_id = t.team_id
GROUP BY t.team_id, t.team_name;

-- To see how many players there are per division
SELECT d.division_id, d.division_name, COUNT(p.player_id) AS number_of_players
FROM player p, division d
WHERE p.division_id = d.division_id
GROUP BY d.division_id, d.division_name;

-- To see how many players there are per sport
SELECT s.sport_id, s.sport_name, COUNT(p.player_id) AS number_of_players
FROM player p, sports s
WHERE p.sport_id = s.sport_id
GROUP BY s.sport_id, s.sport_name;

-- To count how many divisions each sport has
-- Currently has no relation
SELECT s.sport_id, s.sport_name, COUNT(d.division_id) AS number_of_division
FROM division d, sports s
WHERE d.sport_id = s.sport_id
GROUP BY s.sport_id, s.sport_name;

-- To count how many teams each division has
-- Currently has no relation
-- To count how many teams each sport has
-- Currently has no relation
SELECT s.sport_id, s.sport_name, COUNT(t.team_id) AS number_of_teams
FROM team t, sports s
WHERE t.sport_id = s.sport_id
GROUP BY s.sport_id, s.sport_name;