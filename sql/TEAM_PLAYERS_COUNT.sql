CREATE VIEW TEAM_PLAYERS_COUNT AS
SELECT t.team_id, t.team_name, COUNT(p.player_id) AS number_of_players
FROM player p, team t
WHERE p.team_id = t.team_id
GROUP BY t.team_id, t.team_name;
