import random
from datacenter.models import Schoolkid
from datacenter.models import Mark
from datacenter.models import Chastisement
from datacenter.models import Lesson
from datacenter.models import Commendation
from datacenter.models import Subject


def get_schoolkid(schoolkid_name):
    schoolkid = Schoolkid.objects.get(full_name__contains=schoolkid_name)
    return schoolkid


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
    subjects = Subject.objects.filter(year_of_study=schoolkid.year_of_study)
    return random.choice(subjects).title


def fix_marks(schoolkid):
    schoolkid_marks = Mark.objects.filter(schoolkid=schoolkid, points__in=['2', '3'])
    for mark in schoolkid_marks:
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
    random_lesson = random.choice(lessons)
    Commendation.objects.create(
        text=get_random_commendation(),
        created=random_lesson.date,
        schoolkid=schoolkid,
        subject=random_lesson.subject,
        teacher=random_lesson.teacher
    )


def start_hack():
    input_name = input("Введите свое ФИО полностью: ")
    try:
        schoolkid = get_schoolkid(input_name)
        print("Успешно!")
    except Schoolkid.DoesNotExist:
        raise SystemExit("Такого ученика в базе нет")
    except Schoolkid.MultipleObjectsReturned:
        raise SystemExit("В базе найдено несколько учеников с введенными данными")
    fix_marks(schoolkid)
    remove_castisement(schoolkid)
    create_commendation(schoolkid)


start_hack()
