CREATE VIEW SPORT_PLAYERS_COUNT AS
SELECT s.sport_id, s.sport_name, COUNT(p.player_id) AS number_of_players
FROM player p, sports s
WHERE p.sport_id = s.sport_id
GROUP BY s.sport_id, s.sport_name;



