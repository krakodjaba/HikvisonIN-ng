from flask import Flask, render_template
app = Flask(__name__)

# Чтение ссылок из файла
def read_urls():
    with open('urls.txt', 'r') as f:
        return [line.strip() for line in f.readlines()]

@app.route('/')
def index():
    urls = read_urls()
    urls = list(set(urls))  # Считываем ссылки из файла
    return render_template('index.html', urls=urls)  # Передаем их в HTML-шаблон

if __name__ == '__main__':
    app.run(debug=True)
