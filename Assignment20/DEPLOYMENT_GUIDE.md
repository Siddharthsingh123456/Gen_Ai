# GitHub + Render Deployment

## GitHub
1. Create a new GitHub repository.
2. Upload all files from this folder.
3. Commit and push.
4. Copy the repository URL into the submission notes.

## Render
1. Create a Render account.
2. Select **New Web Service**.
3. Connect GitHub.
4. Select the recommendation-system repository.
5. Runtime: Python.
6. Build command:
   `pip install -r requirements.txt`
7. Start command:
   `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
8. Deploy.
9. Open the generated Render URL.
10. Test at least three movies and record the URL in `MY_RUN_NOTES.txt`.

## Before final submission
If the tutor requires the full 4,803-row Kaggle file to be physically included, run:
`python download_kaggle_dataset.py`
and include `data/tmdb_5000_movies.csv` in the final repository/ZIP.
