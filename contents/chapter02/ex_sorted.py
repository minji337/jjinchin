def sort_by_age(person):
    return person['age']

members = [{'name': '이현경', 'age': 31},
            {'name': '김민지', 'age': 26},
            {'name': '오민준', 'age': 29}]

sorted_members = sorted(members, key=sort_by_age, reverse=True)
print(sorted_members)
