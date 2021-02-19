from flask import Flask, render_template

app = Flask(__name__)
app.config['SECRET_KEY'] = '43a7b1952644a1bce603a93c30abc4d6'

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
