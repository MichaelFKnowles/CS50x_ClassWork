SELECT name FROM people, movies, stars WHERE people.id = stars.person_id AND movies.title = "Toy Story" AND stars.movie_id = movies.id;
