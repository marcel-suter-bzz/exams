import json

from model.Person import Person


def main():
    peopledict = {}
    file = open('../files/MoodleUsers.json', encoding='UTF-8')
    users = json.load(file)
    for item in users[0]:
        if item['firstname'] != '' and item['lastname'] != '':
            role = 'student'
            if item['department'] == "Lehrer":
                role = 'teacher'
            key = item['email']
            person = Person(
                item['email'],
                item['firstname'],
                item['lastname'],
                role
            )
            peopledict[key] = person
    file.close()

    people_json = '['
    for key in peopledict:
        data = peopledict[key].to_json()
        people_json += data + ','
    people_json = people_json[:-1] + ']'
    file = open('../files/people.json', 'w', encoding='UTF-8')
    file.write(people_json)
    file.close()


if __name__ == '__main__':
    main()
