def search_validate(prompt):
    return True


def search(prompt):
    result = []
    a = {'семен': 'олег'}
    print('Поиск по запросу ' + prompt)
    for i in a:
        if prompt == i:
            print("найден элемент", a[i])
            result.append(a[i])
            return result

