from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/process_urls/', methods=['POST'])
def process_urls():
    if request.method == 'POST':
        print("121")
        urls = request.form.get('url').split(',')
        print(urls)

        # Отправляем запрос на бэкенд
        backend_url = 'http://localhost:8012/process_urls/'
        response = requests.post(backend_url, json={"urls": urls})

        # Парсим JSON-ответ
        results = response.json()

        print(results)

        return render_template('index.html', results=results)


if __name__ == '__main__':
    app.run(debug=True, port=8011)
