from flask import Flask, render_template, request, redirect, url_for, flash, get_flashed_messages
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Список избирателей
voters = []
# Итоги голосования
results = {}

# Загрузка данных из избирателей (на практике это может быть база данных или файл)
def load_voters():
    global voters
    try:
        with open('voters.json', 'r') as file:
            voters = json.load(file)
    except FileNotFoundError:
        # Если файл не найден, начинаем с пустого списка
        voters = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        voter_id = request.form['voter_id']
        # Проверяем, зарегистрирован ли избиратель
        if voter_id in voters:
            flash('Избиратель уже зарегистрирован!')  # Сообщение при повторной регистрации
        else:
            voters.append(voter_id)  # Добавляем избирателя в список
            # Сохраняем данные в файл
            with open('voters.json', 'w') as file:
                json.dump(voters, file)
            return redirect(url_for('ballot'))
    
    return render_template('register.html')

@app.route('/ballot', methods=['GET', 'POST'])
def ballot():
    if request.method == 'POST':
        candidate = request.form['candidate']
        # Подсчет голосов
        if candidate in results:
            results[candidate] += 1
        else:
            results[candidate] = 1
        return redirect(url_for('show_results'))

    return render_template('ballot.html')

@app.route('/results', methods=['GET'])
def show_results():
    # Передаем результаты в шаблон
    return render_template('results.html', results=results) 

if __name__ == '__main__':
    load_voters()  # Загружаем избирателей при старте
    app.run(debug=True)