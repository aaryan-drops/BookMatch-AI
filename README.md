📚 BookMatch AI — Intelligent Book Recommendation System

Discover your next favorite book with BookMatch AI, an interactive book recommendation web application built with Python and Streamlit. Explore books, discover personalized recommendations, and rate books through a simple and user-friendly interface.

🚀 Live Demo

Try the application: "BookMatch AI" (https://bookmatch-ai-wqbnretfgkgvmcmhuxswgt.streamlit.app/)

GitHub Repository: "aaryan-drops/BookMatch-AI" (https://github.com/aaryan-drops/BookMatch-AI)

✨ Features

- Discover Books: Browse the available book collection.
- Search and Filter: Find books based on available information.
- AI-Powered Recommendations: Get book recommendations using content similarity.
- Personalized Recommendations: Explore recommendations based on your ratings, where supported by the application.
- Surprise Me: Discover a book through a random selection.
- Top-Rated Books: Explore highly rated books.
- Rate and Review: Submit ratings and reviews through the application.
- Persistent Storage: Store ratings and reviews using SQLite.

🧠 How It Works

BookMatch AI uses TF-IDF vectorization and cosine similarity to compare book information and identify similar books.

1. Book descriptions or other available text features are processed.
2. TF-IDF converts text into numerical feature vectors.
3. Cosine similarity measures how closely books match.
4. The system recommends books with similar content.

🛠️ Tech Stack

- Language: Python
- Frontend and Web App: Streamlit
- Data Processing: Pandas
- Recommendation Engine: Scikit-learn (TF-IDF and cosine similarity)
- Database: SQLite
- Version Control: Git and GitHub
- Deployment: Streamlit Community Cloud

📂 Project Structure

BookMatch-AI/
├── app.py
├── books.csv
├── README.md
├── requirements.txt
├── .gitignore
└── bookmatch.db        # Created locally when applicable

⚙️ Run Locally

1. Clone the repository

git clone https://github.com/aaryan-drops/BookMatch-AI.git
cd BookMatch-AI

2. Create a virtual environment

python -m venv venv

3. Activate the environment

Windows (Command Prompt):

venv\Scripts\activate

4. Install dependencies

pip install -r requirements.txt

5. Launch the application

streamlit run app.py

The application should open in your browser. If it does not, open the local URL displayed in the terminal.

🎯 Project Objective

The goal of BookMatch AI is to demonstrate how text-based recommendation techniques can be integrated into an interactive web application to make book discovery easier and more engaging.

👨‍💻 Author

Aaryan Mishra

- GitHub: "@aaryan-drops" (https://github.com/aaryan-drops)

---

If you enjoy the project, consider giving the repository a ⭐ on GitHub!
