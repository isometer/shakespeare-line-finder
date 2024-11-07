from flask import Flask, render_template, request, url_for, redirect


app = Flask(__name__)
from search.search import search_bp
app.register_blueprint(search_bp, url_prefix="/search")

@app.route('/')
def home():
    return redirect(url_for('search_bp.start'))

if __name__ == '__main__':
  app.run(debug=True)
