SELECT SUM(rating) / COUNT(rating) FROM ratings JOIN movies ON ratings.movie_id = movies.id WHERE ratings.rating <> 0 AND  movies.year = 2012;
