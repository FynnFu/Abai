import pymorphy2 as pymorphy2
from django.shortcuts import render, redirect
from django.http import HttpResponse
from function.models import *

interface_words_ru = {"find": 'Найти',
                      "word_search": 'Поиск слова',
                      "home": 'Главная',
                      "word": 'Слово...',
                      "words_of_edification": 'Слова назидания',
                      "code_of_humanity": 'Кодекс человечности',
                      "number_of_uses_of_the_word": 'Количество использований слова',
                      "line_1_404": 'Тут пока ничего нет, но возможно в будущем будет)',
                      "line_2_404": 'А пока можете поддержать проект донатом',
                      "line_3_404": 'Вот ссылочка(нажмите на картинку):'}
interface_words_kz = {"find": 'Іздеу',
                      "word_search": 'Сөзді іздеу',
                      "home": 'Басты бет',
                      "word": 'Сөз...',
                      "words_of_edification": 'Қара сөз',
                      "code_of_humanity": 'Адамгершілік кодекс',
                      "number_of_uses_of_the_word": 'Қолданған сөздер саны',
                      "line_1_404": 'Бұл жерде әлі ештеңе жоқ, бірақ болашақта болуы мүмкін)',
                      "line_2_404": 'Әзірше жобаны қайырымдылық арқылы қолдауға болады',
                      "line_3_404": 'Мұнда сілтеме (суретті басыңыз): '}


def index(request, ln='ru'):
    ln = request.COOKIES.get('ln')
    if ln is not None:
        return redirect(home, ln)
    else:
        ln = 'ru'
        html = redirect(home, ln)
        html.set_cookie('ln', ln)
        return html


def home(request, ln):
    woe_text = []
    title_list = []
    word_str = request.POST.get('word_str', None)
    word_str = word_str.strip()
    if word_str is None or word_str == '':
        return redirect('woe', ln=ln)
    else:
        woes = WOE.objects.all()
        word_list = morphy(word_str)
        for woe in woes:
            if ln == 'ru':
                lens = woe.text
                title = woe.title
            else:
                lens = woe.text_kz
                title = woe.title_kz
            for word_one in word_list:
                endings = [' ', '.', '!', ',', '?']
                words = [word_one, word_one.title()]
                for word in words:
                    for ending in endings:
                        if lens.find(' ' + word + ending) > -1:
                            lens = lens.replace(' ' + word + ending, '<strong>' + ' ' + word + ending + '</strong>')
                            if not (title in title_list):
                                title_list.append(title)
            if title in title_list:
                woe_text.append('<h2>' + title + '</h2>' + '<br>' + '<p>' + lens + '</p>' + '<br>')
        i = 0
        for woe in woe_text:
            i += woe.count('</strong>')
        data = {"woes": woe_text, "amount": i, "word": word_str, "ln": ln, "interface_words": get_interface_words(ln)}
        return render(request, 'word_list.html', data)


def get_all_woe(request, ln):
    woes = WOE.objects.all()
    woe_text = []
    for woe in woes:
        if ln == 'ru':
            lens = woe.text
            title = woe.title
        else:
            lens = woe.text_kz
            title = woe.title_kz
        woe_text.append('<h2>' + title + '</h2>' + '<br>' + '<p>' + lens + '</p>' + '<br>')
    data = {"woes": woe_text, "ln": ln, "interface_words": get_interface_words(ln)}
    html = render(request, 'word_list.html', data)
    html.set_cookie('ln', ln)
    return html


def get_all_ch(request, ln):
    chs = CH.objects.all()
    ch_text = []
    for ch in chs:
        if ln == 'ru':
            lens = ch.text
        else:
            lens = ch.text_kz
        ch_text.append('<h2>' + str(ch.id) + '</h2>' + '<br>' + '<p>' + lens + '</p>' + '<br>')
    data = {"woes": ch_text, "ln": ln, "interface_words": get_interface_words(ln)}
    html = render(request, 'word_list.html', data)
    html.set_cookie('ln', ln)
    return html


def morphy(word):
    all_lexeme = []
    morph = pymorphy2.MorphAnalyzer()
    p = morph.parse(word)[0]
    for x in p.lexeme:
        all_lexeme.append(x.word)
    return all_lexeme


def page_not_found(request, exception):
    ln = request.COOKIES.get('ln')
    if ln is not None:
        data = {"ln": ln, "interface_words": get_interface_words(ln)}
        return render(request, '404.html', data)
    else:
        ln = 'ru'
        data = {"ln": ln, "interface_words": get_interface_words(ln)}
        html = render(request, '404.html', data)
        html.set_cookie('ln', ln)
        return html


def get_interface_words(languages):
    if languages == 'ru':
        return interface_words_ru
    elif languages == 'kz':
        return interface_words_kz
    else:
        return interface_words_ru
