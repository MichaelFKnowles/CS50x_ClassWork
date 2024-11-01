SELECT SUM(energy) / COUNT(name) FROM songs WHERE artist_id = (SELECT id FROM artists WHERE name = "Drake");
