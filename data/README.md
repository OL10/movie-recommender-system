# Data Directory

This folder should contain your movie datasets.

## Required Files

1. **movies.csv** - Movie metadata
   - Columns: `movieId`, `title`, `genres`, `overview`, `keywords` (optional)
   - Source: TMDB Dataset

2. **ratings.csv** - User ratings
   - Columns: `userId`, `movieId`, `rating`, `timestamp`
   - Source: MovieLens Dataset

## Download Instructions

### TMDB Movies Dataset
1. Visit [TMDB](https://www.themoviedb.org/) or [Kaggle TMDB Dataset](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata)
2. Download the movie metadata CSV
3. Rename to `movies.csv` and place here

### MovieLens Dataset
1. Visit [MovieLens](https://grouplens.org/datasets/movielens/)
2. Download MovieLens 100K or 1M dataset
3. Extract `ratings.csv` and place here

## Sample Data Format

**movies.csv:**
```csv
movieId,title,genres,overview,keywords
1,Toy Story,Animation|Comedy|Family,"Led by Woody, Andy's toys live happily...",jealousy|toy|boy
2,Jumanji,Adventure|Fantasy|Family,"When siblings Judy and Peter discover...",board game|magic
```

**ratings.csv:**
```csv
userId,movieId,rating,timestamp
1,1,4.0,964982703
1,3,4.0,964981247
2,1,5.0,835355493
```

## Note

These files are not included in the repository due to size constraints. Please download them separately.
