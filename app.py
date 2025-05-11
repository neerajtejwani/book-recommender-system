from flask import Flask, render_template, request
import pickle
import numpy as np

# Load data
popular_df = pickle.load(open('templates/popular.pkl', 'rb'))
pt = pickle.load(open('pt.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl', 'rb'))

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html',
                           book_name=popular_df['Book-Title'].values,
                           author=popular_df['Book-Author'].values,
                           image=popular_df['Image-URL-M'].values,
                           votes=popular_df['num_ratings'].values,
                           rating=popular_df['avg_rating'].values)


@app.route('/recommend')
def recommend_ui():  # Changed function name to avoid conflict
    return render_template('recommend.html')


@app.route('/recommend_books', methods=['POST'])
def recommend_books():  # Different function name
    user_input = request.form.get('user_input')

    try:
        index = np.where(pt.index == user_input)[0][0]
        similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:6]
        data = []
        for i in similar_items:
            item = []
            temp_df = books[books['Book-Title'] == pt.index[i[0]]]
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
            data.append(item)
        return render_template('recommend.html', data=data)
    except IndexError:
        return render_template('recommend.html', data=[], error="Book not found. Please enter an exact match.")


if __name__ == '__main__':
    app.run(debug=True)
