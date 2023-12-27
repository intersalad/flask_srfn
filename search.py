import requests
from database import Database

db = Database('personal_data.db')


def search_validate(prompt):
    return True


def prompt_into_category(prompt):
    prompt = str(prompt).lower()
    if prompt == 'видеограф':
        return 1488


def search(prompt):
    result = []
    a = {'видеограф': 1}
    print('Поиск по запросу ' + prompt)
    for i in a:
        if prompt == i:
            print("найден элемент", a[i])
            result.append(a[i])
            return result


def get_id(ses, prompt):
    print(ses['vk_token'])
    user_info = requests.get('https://api.vk.com/method/users.get?fields=&v=5.199&access_token=' + ses['vk_token']).json()
    user_id = user_info['response'][0]['id']
    print(user_id)
    access_token = '404203ae404203ae404203aed94351e15244042404203ae253ffb3aa2882118cd1bbdcb'  # Здесь нужно заменить на свой access token VK API
    api_version = '5.199'
    url = 'https://api.vk.com/method/friends.get?user_id=' + str(user_id) + '&fields=first_name&access_token=' + str(access_token) + '&v=5.199'
    try:
        response = requests.get(url)
        response.raise_for_status()
        friends_data = response.json()['response']
        friends_list = friends_data['items']
        ans = [user_id]
        for i in friends_list:
            #print('id: ', i['id'], '   name: ', i['first_name'], ' ', i['last_name'])
            friend_id = i['id']
            q = db.is_our_user(friend_id)
            if q is not None:
                ans.append(q)

        print('База, по которой ищем ', ans)
        print('Всего пользователей: ', len(friends_list))
        otvet = find_recs(ans, prompt)
        if otvet == 0:
            return "Ничего не нашли, сорян"
        else:
            return otvet

    except requests.exceptions.HTTPError as error:
        print(f'HTTP error occurred: {error}')
    except requests.exceptions.RequestException as error:
        print(f'Request exception occurred: {error}')
    except KeyError:
        print('Error: Unable to retrieve friends list.')


def find_recs(users_id_list, zapros):
    answer_list = []
    print(users_id_list)
    print('zapros ', zapros)
    zapros = prompt_into_category(zapros)
    print('category: ', zapros)
    print()
    for i in users_id_list:
        print(i, zapros)
        res = db.get_recs(i, zapros)
        if res:
            print('УРАА!')
            print('res ', res)
            answer_list.append(res)

    if answer_list:
        return answer_list

    else:
        return 0




