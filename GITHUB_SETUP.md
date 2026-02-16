# GitHub Setup Guide

## Step-by-Step Instructions to Upload Your Project

### Prerequisites
1. Create a GitHub account at https://github.com (if you don't have one)
2. Install Git on your computer:
   - Windows: Download from https://git-scm.com/download/win
   - Mac: `brew install git` or download from https://git-scm.com/download/mac
   - Linux: `sudo apt-get install git`

### Step 1: Create a New Repository on GitHub

1. Go to https://github.com and log in
2. Click the **"+"** icon in the top right corner
3. Select **"New repository"**
4. Fill in the details:
   - **Repository name**: `movie-recommender-system`
   - **Description**: `Hybrid movie recommendation engine using TF-IDF and SVD`
   - **Visibility**: Public (so recruiters can see it)
   - **DO NOT** initialize with README (we already have one)
5. Click **"Create repository"**

### Step 2: Configure Git (First Time Only)

Open your terminal/command prompt and run:

```bash
git config --global user.name "Your Name"
git config --global user.email "osheenlanger@gmail.com"
```

### Step 3: Upload Your Project

Navigate to your project folder and run these commands:

```bash
# Initialize git repository
git init

# Add all files
git add .

# Commit the files
git commit -m "Initial commit: Hybrid movie recommendation system with TF-IDF and SVD"

# Connect to GitHub (replace YOUR_USERNAME with your actual GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/movie-recommender-system.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### Step 4: Verify Upload

1. Go to your GitHub repository: `https://github.com/YOUR_USERNAME/movie-recommender-system`
2. You should see all your files uploaded
3. The README.md will be displayed on the main page

### Step 5: Add Repository Topics (Recommended)

On your GitHub repository page:
1. Click **"Add topics"** (below the repository description)
2. Add relevant tags: `machine-learning`, `recommendation-system`, `python`, `scikit-learn`, `collaborative-filtering`, `streamlit`
3. This helps people discover your project

### Common Issues and Solutions

**Issue: "Permission denied (publickey)"**
Solution: Set up SSH key or use HTTPS with personal access token
- For token: Go to GitHub Settings → Developer settings → Personal access tokens
- Generate token and use it as password when pushing

**Issue: "Updates were rejected because the remote contains work"**
Solution: Force push (only for new repos):
```bash
git push -u origin main --force
```

**Issue: Files are too large**
Solution: Large files (data, models) are already in .gitignore and won't be uploaded

### Step 6: Update Your Resume

Once uploaded, you can add the GitHub link to your resume:

**On your resume under the project:**
```
Hybrid Movie Recommendation Engine                          Jan 2025 – Apr 2025
GitHub: github.com/YOUR_USERNAME/movie-recommender-system
• Designed hybrid recommender combining TF-IDF and SVD to enhance user recommendations
• Processed 5,000+ movie records from TMDB & MovieLens datasets
• Evaluated using offline relevance metrics achieving 92% recommendation accuracy
• Deployed interactive Streamlit app on Hugging Face Spaces
```

### Next Steps After Upload

1. **Add a repository banner**: Create a nice header image
2. **Enable GitHub Pages**: For hosting project documentation
3. **Add badges**: Travis CI, code coverage, etc. (optional)
4. **Star your own repo**: Shows activity
5. **Share**: Add link to LinkedIn, resume, and portfolio

### Keeping Your Repo Updated

When you make changes:
```bash
git add .
git commit -m "Description of changes"
git push origin main
```

---

**Need Help?**
- GitHub Guide: https://guides.github.com/activities/hello-world/
- Git Tutorial: https://git-scm.com/book/en/v2
