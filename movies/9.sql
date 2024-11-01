SELECT DISTINCT name FROM people, movies, stars WHERE people.id = stars.person_id AND movies.year = 2004 AND stars.movie_id = movies.id ORDER BY people.birth;
