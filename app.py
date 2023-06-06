from flask import Flask ,render_template,request
import pickle
import pandas as pd
import numpy as np






pickle_off = open('popular.pkl',"rb")
popular_df = pd.read_pickle(pickle_off)

pt1 = open('pt.pkl',"rb")
pt = pd.read_pickle(pt1)
books1 = open('books.pkl',"rb")
books = pd.read_pickle(books1)
sim = open('similarity_score.pkl',"rb")
similarity = pd.read_pickle(sim)

app=Flask(__name__,template_folder='template')

@app.route('/')
def index():
    return render_template('index.html',
                           book_name=list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           votes=list(popular_df['num_rating'].values),
                           rating=list(popular_df['avg_rating'].values)
                           )

@app.route('/recommend')
def recommend_ui():
    return render_template('Recommend.html',methods=['post'])

@app.route('/recommend_books',methods=['post'])
def recommend():
    user_input=request.form.get('user-input')
    index = np.where(pt.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity[index])), key=lambda x: x[1], reverse=True)[1:5]

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(item)

    print(data)

    return render_template('recommend.html', data=data)


if __name__== '__main__':
    app.run(debug=True)
