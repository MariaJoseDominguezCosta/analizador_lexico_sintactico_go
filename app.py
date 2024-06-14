# app.py

from flask import Flask, request, render_template
from lexer import tokenize
from parser_1 import parse
from semantico import errores

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result_lex = []
    result_syntax = ''
    if request.method == 'POST':
        code = request.form['code']
        result_lex = tokenize(code)
        result_syntax = parse(code)
    return render_template('index.html', tokens=result_lex, syntax=result_syntax, mensaje3=errores)

if __name__ == '__main__':
    app.run(debug=True)