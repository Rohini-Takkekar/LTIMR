from flask import Flask, request,jsonify 
import psycopg2

app = Flask(__name__)

# Connect to PostgreSQLb 

conn = psycopg2.connect(
    database="API",
    user="postgres",
    password="postgres",
    host="localhost",
    port="5432")

cursor=conn.cursor()

def call_cursor():
    
    return cursor


#Create the books table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS books(
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    published_date TEXT,
    isbn TEXT,
    favorite BOOLEAN DEFAULT FALSE
)
''')


conn.commit()

@app.route('/books', methods=['POST'])
def add_book():  
    
    data = request.json    
    cursor.execute("INSERT INTO books (title, author, published_date, isbn, favorite) VALUES (%s, %s, %s, %s, %s)",
    (data['title'], data['author'], data.get('published_date'), data.get('isbn'), data.get('favorite', False)))
    conn.commit()   
    return jsonify({'message': 'Book added'})

def get_books():
    
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()    
    return jsonify(books)

@app.route('/books/<int:id>', methods=['PUT'])
def update_book(id): 
     
    cursor = call_cursor()
    data = request.json    
    cursor.execute("UPDATE books SET title=%s, author=%s, published_date=%s, isbn=%s, favorite=%s WHERE id=%s",
    (data['title'], data['author'], data.get('published_date'), data.get('isbn'), data.get('favorite', False), id))
    conn.commit()    
    return jsonify({'message': 'Book updated'})

@app.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id): 
    
    cursor.execute("DELETE FROM books WHERE id=%s", (id,))
    conn.commit()    
    return jsonify({'message': 'Book deleted'})

@app.route('/books/favorites', methods=['GET'])
def get_favorites():
    
    cursor.execute("SELECT * FROM books WHERE favorite = TRUE")
    books = cursor.fetchall()    
    return jsonify(books)

@app.route('/books/<int:id>/favorite', methods=['PATCH'])
def toggle_favorite(id):
    
    # Retrieve the current favorite status of the book
    cursor.execute("SELECT favorite FROM books WHERE id=%s", (id,))
    current_status = cursor.fetchone()

    if current_status is None:
        return jsonify({'message': 'Book not found'})
    new_status = not current_status[0]
    cursor.execute("UPDATE books SET favorite=%s WHERE id=%s", (new_status, id))
    conn.commit()

    return jsonify({'message': 'Favorite status updated', 'favorite': new_status})

if __name__ == "__main__":
    app.run(debug=True)
 