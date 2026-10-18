import streamlit as st
from recommender import load_data, build_model, recommend

st.set_page_config(page_title="Movie Recommendation System", page_icon="🎬")

st.title("🎬 Movie Recommendation System")
st.write("Content-based recommendations using TF-IDF and cosine similarity.")

@st.cache_resource
def load_model():
    data = load_data()
    return build_model(data)

df, vectorizer, matrix, similarity = load_model()

st.sidebar.header("Choose a movie")
movie = st.sidebar.selectbox("Movie", df["title"].tolist())
count = st.sidebar.slider("Number of recommendations", 3, 10, 5)

if st.button("Recommend"):
    results = recommend(movie, df, similarity, count)
    st.subheader(f"Recommendations for: {movie}")
    for title, score in results:
        st.write(f"**{title}** — similarity: {score:.4f}")
