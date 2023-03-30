from flask import Flask, render_template, request, redirect, url_for
import os
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'

RESULTS_DIR = './results'

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'admin' and password == 'password':
            return redirect(url_for('tests'))
        else:
            return render_template('login.html', error=True)
    else:
        return render_template('login.html', error=False)

@app.route('/tests', methods=['GET', 'POST'])
def tests():
    if request.method == 'POST':
        data = request.get_json()
        section_name = data['section_name']
        test_results = data['test_results']

        results_path = os.path.join(RESULTS_DIR, f'{section_name}.json')
        with open(results_path, 'w') as f:
            json.dump(test_results, f)

        return 'success'
    else:
        return render_template('tests.html')

@app.route('/results')
def results():
    results = {}
    for filename in os.listdir(RESULTS_DIR):
        with open(os.path.join(RESULTS_DIR, filename)) as f:
            section_results = json.load(f)
            results[filename.split('.')[0]] = section_results

    average_results = {}
    for section_name, section_results in results.items():
        section_average = sum(section_results) / len(section_results)
        average_results[section_name] = round(section_average, 2)

    return render_template('results.html', results=results, average_results=average_results)

if __name__ == '__main__':
    app.run(debug=True)
