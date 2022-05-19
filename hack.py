import random
from datacenter.models import Schoolkid
from datacenter.models import Mark
from datacenter.models import Chastisement
from datacenter.models import Lesson
from datacenter.models import Commendation
from datacenter.models import Subject


def get_schoolkid_id():
    input_name = input("Введите свою фамилию: ")
    schoolkids = Schoolkid.objects.filter(full_name__contains=input_name)
    if schoolkids:
        for index, schoolkid in enumerate(schoolkids):
            print(index + 1, schoolkid.full_name, schoolkid.year_of_study, schoolkid.group_letter)
        print("Найдите себя в списке учеников и введите свой номер из списка")
        input_index = input('Введите свой номер: ')
        schoolkid_id = schoolkids[int(input_index)-1].id
    else:
        print("Такого ученика не нашлось в базе,попробуйте еще раз")
        get_schoolkid_id()
    return schoolkid_id


def get_random_commendation():
    commendations = [
        'Молодец',
        'Отлично!',
        'Хорошо!',
        'Гораздо лучше, чем я ожидал',
        'Ты меня приятно удивил!',
        'Великолепно!',
        'Прекрасно!',
        'Ты меня очень обрадовал!',
        'Именно этого я давно ждал от тебя!',
        'Сказано здорово – просто и ясно!',
        'Ты, как всегда, точен!',
        'Очень хороший ответ!',
        'Талантливо!',
        'Ты сегодня прыгнул выше головы!',
        'Я поражен!',
        'Иван - обманщик!Срочно обратитесь в школу',
        'Потрясающе!',
        'Замечательно!',
        'Прекрасное начало!',
        'Так держать!',
        'Ты на верном пути!',
        'Здорово!',
        'Это как раз то, что нужно!',
        'Я тобой горжусь!',
        'С каждым разом у тебя получается всё лучше!',
        'Мы с тобой не зря поработали!',
        'Я вижу, как ты стараешься!',
        'Ты растешь над собой!',
        'Ты многое сделал, я это вижу!',
        'Теперь у тебя точно все получится!',
    ]
    return random.choice(commendations)


def get_random_subject(schoolkid):
    subject = Subject.objects.filter(year_of_study=schoolkid.year_of_study)
    random_subject_index = random.randint(0, len(subject))
    return str(subject[random_subject_index].title)


def fix_marks(schoolkid):
    schoolkid_marks = Mark.objects.filter(schoolkid=schoolkid, points__in=['2', '3'])
    for index, mark in enumerate(schoolkid_marks):
        mark = schoolkid_marks[index]
        mark.points = '5'
        mark.save()


def remove_castisement(schoolkid):
    schoolkid_chastisement = Chastisement.objects.filter(schoolkid=schoolkid)
    schoolkid_chastisement.delete()


def create_commendation(schoolkid):
    random_subject = get_random_subject(schoolkid)
    lessons = Lesson.objects.filter(
        subject__title=random_subject,
        year_of_study=schoolkid.year_of_study,
        group_letter=schoolkid.group_letter,
    )
    random_lesson = random.randint(0, len(lessons))
    lesson = lessons[random_lesson]
    Commendation.objects.create(
        text=get_random_commendation(),
        created=lesson.date,
        schoolkid=schoolkid,
        subject=lesson.subject,
        teacher=lesson.teacher
    )


def start_hack():
    pupil = Schoolkid.objects.get(id=get_schoolkid_id())
    fix_marks(pupil)
    remove_castisement(pupil)
    create_commendation(pupil)


start_hack()
