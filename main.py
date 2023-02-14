import json
from os.path import join
from flask import Flask, render_template, redirect
from answer import AnswerForm
from login import LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hertysss_secret_key'
DIR_IMG = '/static/img'

@app.route('/<title>')
@app.route('/index/<title>')
def index(title):
    return render_template('base.html', title=title)


@app.route('/list_prof/<list>')
def list_prof(list):
    professions = ['инженер-исследователь', 'пилот', 'строитель', 'экзобиолог',
                 'врач', 'инженер по терраформированию', 'климатолог', 'специалист по радиационной защите',
                 'астрогеолог', 'гляциолог', 'инженер жизнеобеспечения', 'метеоролог',
                 'оператор марсохода', 'киберинженер', 'штурман', 'пилот дронов']
    return render_template('list_prof.html', type_list=list, professions=professions)


@app.route('/answer', methods=['GET', 'POST'])
def answer():
    form = AnswerForm()
    if form.validate_on_submit():
        print(1)
        data = {
            'lastname': form.lastname.data,
            'firstname': form.firstname.data,
            'education': form.education.data,
            'profession': form.profession.data,
            'sex': form.sex.data,
            'motivation': form.motivation.data,
            'ready': form.ready.data
        }
        return redirect(f'/auto_answer/{json.dumps(data)}')
    return render_template('answer.html', title='Авторизация', form=form)


@app.route('/auto_answer/<data>')
def auto_answer(data):
    return render_template('auto_answer.html',
                           data=json.loads(data))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect('/success')
    return render_template('login.html', title='Аварийный доступ', form=form)


@app.route('/distribution', methods=['GET'])
def distribution():
    user_list = ['Ридли Скотт', 'Энди Уир', 'Марк Уотни', 'Венката Капур', 'Тедди Сандрес', 'Шон Бин']
    return render_template('distribution.html', title='По каютам!', user_list=user_list)


@app.route('/table/<sex>/<int:age>')
def table(sex, age):
    data = {'title': 'Цвет каюты'}
    if age < 21:
        file_age = 'child.jpg' #'adult.jpg'
        data['url_age'] = join(DIR_IMG, file_age)
        print(data['url_age'])
        file_sex = 'child_female.jpg' if sex == 'female' else 'child_male.jpg'
        data['url_sex'] = join(DIR_IMG, file_sex)
    else:
        file_age = 'adult.jpg'
        data['url_age'] = join(DIR_IMG, file_age)
        file_sex = 'adult_female.jpg' if sex == 'female' else 'adult_male.jpg'
        data['url_sex'] = join(DIR_IMG, file_sex)
    return render_template('table.html', data=data)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1', debug=True)
