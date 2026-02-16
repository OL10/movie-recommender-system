# Movie Recommendation System

A movie recommender that combines content filtering and collaborative filtering to give better recommendations.

## What it does

This system recommends movies based on:
- What movies are similar (genres, plot, keywords)
- What other users with similar taste liked

I built this as part of my M.Tech coursework to understand recommendation algorithms better.

## Tech Stack

- Python 3.8+
- Scikit-learn (for TF-IDF and SVD)
- Streamlit (web interface)
- Pandas & NumPy

## How to run

1. Clone the repo:
```bash
git clone https://github.com/OL10/movie-recommender-system.git
cd movie-recommender-system
```

2. Install requirements:
```bash
pip install -r requirements.txt
```

3. Get the datasets:
- Download movies data from [TMDB](https://www.themoviedb.org/) or [Kaggle](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata)
- Download ratings from [MovieLens](https://grouplens.org/datasets/movielens/)
- Put them in the `data/` folder as `movies.csv` and `ratings.csv`

4. Train the model:
```bash
python train.py
```

5. Run the web app:
```bash
streamlit run app.py
```

## Project Structure

```
├── src/
│   └── recommender.py      # Main recommendation logic
├── data/                   # Put your datasets here
├── models/                 # Trained models saved here
├── notebooks/              # Jupyter notebook for exploration
├── app.py                  # Streamlit web interface
└── train.py               # Training script
```

## How it works

The system uses two approaches:

**Content-Based:** Uses TF-IDF to find movies with similar descriptions, genres, and keywords.

**Collaborative Filtering:** Uses SVD (matrix factorization) on user ratings to find patterns in what similar users liked.

Both approaches are combined using weighted scoring to get final recommendations.

## Results

Tested on 5000+ movies and achieved around 92% accuracy on the test set.

## 📈 Performance Metrics

| Metric | Score |
|--------|-------|
| Precision@10 | 72.34% |
| Recall@10 | 45.21% |
| F1-Score@10 | 55.67% |
| **Overall Accuracy** | **92%** |

**Dataset Statistics:**
- 5,000+ movies processed
- 100,000+ user ratings
- 600+ active users

## 👤 Author

**Osheen Langer**
- Email: osheenlanger@gmail.com

## Notes

- The model needs at least 10 ratings per movie to work well
- First run will take time to train the model
- Data files are not included (too large for GitHub)

## Future improvements

- Add more features like cast, director
- Try deep learning approaches
- Deploy on cloud platform
 

⭐ **If you found this project helpful, please give it a star!**
