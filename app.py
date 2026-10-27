import random
import sqlite3
from pathlib import Path

import pandas as pd
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

BASE_DIR = Path(__file__).resolve().parent
CSV_FILE = BASE_DIR / "books.csv"
DB_FILE = BASE_DIR / "bookmatch.db"

st.set_page_config(
    page_title="BookMatch AI",
    page_icon="📚",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #101827, #1c1533);
    color: #f8fafc;
}
h1, h2, h3, p, label {
    color: #f8fafc;
}
div[data-testid="stVerticalBlockBorderWrapper"] {
    border-color: #45405f;
    border-radius: 14px;
}
</style>
""", unsafe_allow_html=True)


# DATABASE
def setup_database():
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS ratings (
                book_id INTEGER PRIMARY KEY,
                stars INTEGER NOT NULL CHECK(stars BETWEEN 1 AND 5),
                review TEXT DEFAULT '',
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)


def save_rating(book_id, stars, review):
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("""
            INSERT INTO ratings (book_id, stars, review)
            VALUES (?, ?, ?)
            ON CONFLICT(book_id) DO UPDATE SET
                stars = excluded.stars,
                review = excluded.review,
                updated_at = CURRENT_TIMESTAMP
        """, (int(book_id), int(stars), review.strip()))


def get_ratings():
    with sqlite3.connect(DB_FILE) as conn:
        return pd.read_sql_query(
            "SELECT * FROM ratings", conn
        )


# LOAD BOOKS
@st.cache_data
def load_books():
    df = pd.read_csv(CSV_FILE)
    required = [
        "book_id", "title", "author", "genre", "description"
    ]

    if not set(required).issubset(df.columns):
        raise ValueError(
            "books.csv must contain: "
            + ", ".join(required)
        )

    df = df.dropna(subset=["title"]).copy()

    for col in ["title", "author", "genre", "description"]:
        df[col] = df[col].fillna("").astype(str)

    df["book_id"] = df["book_id"].astype(int)
    return df


# RECOMMENDATION ENGINE
def create_recommender(books):
    text = (
        books["genre"] + " "
        + books["title"] + " "
        + books["author"] + " "
        + books["description"]
    )

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2)
    )
    matrix = vectorizer.fit_transform(text)
    return cosine_similarity(matrix, matrix)


def recommend_books(books, similarity, book_id, count):
    matches = books.index[
        books["book_id"] == int(book_id)
    ].tolist()

    if not matches:
        return books.iloc[0:0].copy()

    index = matches[0]
    scores = list(enumerate(similarity[index]))
    scores.sort(key=lambda item: item[1], reverse=True)

    indices = [
        i for i, score in scores if i != index
    ][:count]

    result = books.iloc[indices].copy()
    result["similarity"] = [
        float(similarity[index][i]) for i in indices
    ]
    return result


setup_database()
books = load_books()
similarity = create_recommender(books)
ratings = get_ratings()

rating_map = (
    ratings.set_index("book_id")["stars"].to_dict()
    if not ratings.empty else {}
)

review_map = (
    ratings.set_index("book_id")["review"].to_dict()
    if not ratings.empty else {}
)


# SIDEBAR
st.sidebar.title("📚 BookMatch AI")
page = st.sidebar.radio(
    "Navigate",
    [
        "Discover Books",
        "AI Recommendations",
        "Top Rated Books",
        "My Ratings"
    ]
)
st.sidebar.divider()
st.sidebar.metric("Books in Library", len(books))
st.sidebar.metric("Books Rated", len(ratings))


# SEARCH AND FILTER
def filter_books(data, search, genre):
    filtered = data.copy()

    if search.strip():
        q = search.strip().casefold()
        mask = (
            filtered["title"].str.casefold().str.contains(q, regex=False)
            | filtered["author"].str.casefold().str.contains(q, regex=False)
            | filtered["genre"].str.casefold().str.contains(q, regex=False)
            | filtered["description"].str.casefold().str.contains(q, regex=False)
        )
        filtered = filtered[mask]

    if genre != "All":
        filtered = filtered[
            filtered["genre"].apply(
                lambda value: genre.casefold() in value.casefold()
            )
        ]

    return filtered


# BOOK CARD
def display_book(book):
    book_id = int(book["book_id"])

    with st.container(border=True):
        st.subheader("📖 " + str(book["title"]))
        st.caption(
            str(book["author"]) + " • " + str(book["genre"])
        )
        st.write(book["description"])

        if book_id in rating_map:
            st.write(f"⭐ Your rating: {rating_map[book_id]}/5")

        with st.expander("Rate this book / Write a review"):
            stars = st.select_slider(
                "Your rating",
                options=[1, 2, 3, 4, 5],
                value=int(rating_map.get(book_id, 5)),
                key=f"stars_{book_id}"
            )

            review = st.text_area(
                "Your review",
                value=str(review_map.get(book_id, "")),
                max_chars=1000,
                key=f"review_{book_id}"
            )

            if st.button("Save Rating", key=f"save_{book_id}"):
                save_rating(book_id, stars, review)
                st.success("Rating saved!")
                st.rerun()


def display_grid(data):
    if data.empty:
        st.info("No books found. Try another search or filter.")
        return

    st.caption(f"{len(data)} books found")

    for start in range(0, len(data), 2):
        cols = st.columns(2)
        for col, (_, book) in zip(
            cols, data.iloc[start:start + 2].iterrows()
        ):
            with col:
                display_book(book)


# HEADER
st.title("📚 BookMatch AI")
st.write(
    "Discover books, explore your interests, "
    "and find your next favourite read."
)


# DISCOVER BOOKS: SHOW ALL BOOKS
if page == "Discover Books":
    st.header("🔍 Discover All Books")

    search = st.text_input(
        "Search books",
        placeholder="Title, author, genre or description..."
    )

    genres = sorted(set(
        part.strip()
        for value in books["genre"]
        for part in value.split()
        if part.strip()
    ))
    genre = st.selectbox("Filter by genre", ["All"] + genres)

    filtered = filter_books(books, search, genre)

    display_grid(filtered)


# AI RECOMMENDATIONS
elif page == "AI Recommendations":
    st.header("🧠 AI Book Recommendations")
    st.write(
        "Explore the full library or find books similar "
        "to one you already like."
    )

    mode = st.radio(
        "Choose recommendation mode",
        [
            "All Books",
            "Personalized Recommendations",
            "Surprise Me"
        ],
        horizontal=True
    )

    if mode == "All Books":
        search = st.text_input(
            "Search all recommended books",
            key="all_search"
        )

        genres = sorted(set(
            part.strip()
            for value in books["genre"]
            for part in value.split()
            if part.strip()
        ))
        genre = st.selectbox(
            "Filter recommendations by genre",
            ["All"] + genres,
            key="all_genre"
        )

        display_grid(filter_books(books, search, genre))

    elif mode == "Personalized Recommendations":
        selected_title = st.selectbox(
            "Choose a book you like",
            books["title"].tolist()
        )

        selected_id = int(
            books.loc[
                books["title"] == selected_title, "book_id"
            ].iloc[0]
        )

        count = st.slider(
            "Number of similar books",
            min_value=1,
            max_value=max(1, len(books) - 1),
            value=min(10, len(books) - 1)
        )

        if st.button("✨ Recommend Books", type="primary"):
            results = recommend_books(
                books, similarity, selected_id, count
            )

            st.subheader("Books picked for you")

            for _, book in results.iterrows():
                st.caption(
                    "Content similarity: "
                    f"{book['similarity'] * 100:.1f}%"
                )
                display_book(book)

    else:
        st.write("Discover something new from the library.")

        if st.button("🎲 Surprise Me", type="primary"):
            count = min(5, len(books))
            picks = books.sample(
                n=count,
                random_state=random.randint(0, 1_000_000)
            )
            st.subheader("Your surprise book picks")
            display_grid(picks)


# TOP RATED BOOKS
elif page == "Top Rated Books":
    st.header("⭐ Top Rated Books")

    if ratings.empty:
        st.info(
            "No ratings yet. Rate some books to build the "
            "community rating list."
        )
    else:
        summary = ratings.groupby("book_id").agg(
            average_rating=("stars", "mean"),
            rating_count=("stars", "count")
        ).reset_index()

        summary = summary.merge(
            books, on="book_id", how="left"
        ).sort_values(
            ["average_rating", "rating_count"],
            ascending=[False, False]
        )

        st.caption(
            "Ratings currently come from this app's local database."
        )

        for _, row in summary.iterrows():
            st.write(
                f"⭐ **{row['average_rating']:.1f}/5** "
                f"({int(row['rating_count'])} rating)"
            )
            display_book(row)


# MY RATINGS
elif page == "My Ratings":
    st.header("⭐ My Ratings & Reviews")

    if ratings.empty:
        st.info(
            "You have not rated any books yet. "
            "Visit Discover Books to get started."
        )
    else:
        summary = ratings.merge(
            books[["book_id", "title", "author"]],
            on="book_id",
            how="left"
        )

        st.metric(
            "Your Average Rating",
            f"{summary['stars'].mean():.1f} / 5"
        )

        for _, row in summary.iterrows():
            with st.container(border=True):
                st.subheader(row["title"])
                st.caption(row["author"])
                st.write(f"⭐ {row['stars']} / 5")
                st.write(row["review"] or "No written review.")