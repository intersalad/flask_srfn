from flask import Flask, redirect, url_for, session, render_template, request
import requests
from search import search_validate, get_id, rec_sort

from dotenv import load_dotenv
load_dotenv()

import os
from supabase import create_client

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
db = create_client(url, key)


# Создание экземпляра базы данных
#db = Database('personal_data.db')


app = Flask(__name__)
#app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:zwIx0bhW5XhRaBcw@db.ocalnnljxiorkuhmxihp.supabase.co:5432/postgres"
app.secret_key = '404203ae404203ae404203aed94351e15244042404203ae253ffb3aa2882118cd1bbdcb'


@app.route('/')
def index():
    return "hello"
    if 0 == 1:
        if 'vk_token' in session:
            return redirect(url_for('home'))
        return render_template('index.html')




@app.route('/search')
def search_page():
    q = request.args.get('q')
    print(q)
    if q is not None:
        ans = 'Вы искали ' + str(q)
        if search_validate(q):
            ans, user_id = get_id(session, q)
            #print(search(q))
            print('ans  !!!  ', ans)
            if ans is not None:
                after_sort = rec_sort(ans, user_id)
                result = db.rec_into_data(after_sort, q)
                print()
                print('result', result)
                return render_template('/search.html', answer=result)
            else:
                return render_template('/search.html', text='Ничего не найдено')

    else:
        ans = ''
        return render_template('/search.html')


@app.route('/home')
def home():
    print(session)
    print("good")
    fields = 'first_name,last_name,domain,sex,photo_400_orig,city,country,contacts,friends,followers_count,site,verified'
    user_info = requests.get(
        'https://api.vk.com/method/users.get?fields=' + fields + '&v=5.199&access_token=' + session['vk_token']).json()
    name = user_info['response'][0]['first_name']
    last_name = user_info['response'][0]['last_name']
    photo = user_info['response'][0]['photo_400_orig']
    city = user_info['response'][0]['city']['title']
    us_inf = {'vk_id': '-', 'first_name': '-', 'last_name': '-', 'domain': '-',
              'sex': '-', 'photo_400_orig': '-', 'city': '-', 'country': '-',
              'contacts': '-', 'friends': '-', 'followers_count': '-',
              'site': '-', 'verified': '-'}
    for i in user_info['response'][0]:
        us_inf[i] = user_info['response'][0][i]
        # print(i)

    vk_id = us_inf['id']
    print(vk_id)
    first_name = us_inf['first_name']
    last_name = us_inf['last_name']
    sex = us_inf['sex']
    domain = us_inf['domain']
    city = us_inf['city']['title']
    country = us_inf['country']['title']
    photo = us_inf['photo_400_orig']
    site = us_inf['site']

    db.insert_user(vk_id, first_name, last_name, sex, domain, city, country, photo, site)
    users = db.get_users()

    for user in users:
        print(user)
    print(1)
    print(session)
    return render_template('user.html', name=name, last_name=last_name, photo=photo, info=us_inf)





@app.route('/users')
def users():
    users_list = db.get_users()
    print(users_list)
    return render_template("users_list.html", a=users_list)

@app.route('/specs')
def specs():
    specs_list = db.get_specs()
    print(specs_list)
    return render_template("specs_list.html", a=specs_list)

@app.route('/login')
def login():
    return redirect('https://oauth.vk.com/authorize?client_id=51634940&redirect_uri=http://127.0.0.1:5000/oauth&scope=offline&response_type=code')


@app.route('/oauth')
def oauth():
    print(123)
    code = request.args.get('code')
    print(code)
    response = requests.get('https://oauth.vk.com/access_token?client_id=51634940&client_secret=30yTr5w9ufa57LYfghej&redirect_uri=http://127.0.0.1:5000/oauth&code=' + code).json()
    session['vk_token'] = response['access_token']
    print('user ID: https://vk.com/id', response['user_id'], sep='')
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run()
