📚 BookMatch AI

Discover your next favourite book with intelligent recommendations.

BookMatch AI is a Python-based book discovery and recommendation web application built with Streamlit. It helps readers explore books, discover similar titles, rate books, and write reviews.

✨ Features

- 📖 Discover Books: Browse the complete book library.
- 🔍 Search & Filter: Search by title, author, genre, or description.
- 🧠 Content-Based Recommendations: Discover similar books using TF-IDF and cosine similarity.
- 🎲 Surprise Me: Discover random books from the library.
- ⭐ Ratings & Reviews: Rate books and save personal reviews.
- 🏆 Top Rated Books: Explore books ranked by saved ratings.
- 💾 SQLite Database: Store ratings and reviews locally.

🛠️ Tech Stack

- Python
- Streamlit
- Pandas
- Scikit-learn
- SQLite
- TF-IDF and Cosine Similarity

🚀 Getting Started

1. Clone the repository

git clone YOUR_GITHUB_REPOSITORY_URL
cd BookMatch

2. Create a virtual environment

python -m venv venv

The virtual environment will be created inside the project directory under the "venv" folder.

3. Activate the environment

Windows Command Prompt:

venv\Scripts\activate.bat

4. Install dependencies

pip install streamlit pandas scikit-learn

5. Run the application

streamlit run app.py

📂 Project Structure

BookMatch/
├── app.py
├── books.csv
├── README.md
└── requirements.txt

The SQLite database is created automatically when the application runs.

🧠 How Recommendations Work

BookMatch AI uses TF-IDF to represent book titles, authors, genres, and descriptions as numerical vectors. Cosine similarity compares these vectors to identify books with similar content.

🔮 Future Improvements

- Integrate a public book API for a larger catalogue.
- Add book cover images.
- Introduce user accounts and personalized reading lists.
- Deploy the application online.
- Add more advanced recommendation methods.

⚠️ Note

The current version uses a local book dataset. Ratings and reviews are stored in a local SQLite database, and the recommendation engine is content-based rather than a generative AI model.

👨‍💻 Author

Created as a learning and portfolio project.