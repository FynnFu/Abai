from django.shortcuts import render, redirect
from django.http import HttpResponse
from function.models import *


def index(request):
    return redirect('home')


def home(request):
    woe_text = []
    i = 0
    word_str = request.POST.get('word_str', None)
    if word_str is None:
        return get_all_woe(request)
    elif word_str == "снупдог":
        return render(request, 'abai.html')
    else:
        woes = WOE.objects.all()
        for woe in woes:
            if woe.text.find(' ' + word_str) > -1:
                lens = woe.text.replace(word_str, '<strong>' + word_str + '</strong>')
                woe_text.append('<h2>' + woe.title + '</h2>' + '<br>' + '<p>' + lens + '</p>' + '<br>')
                i += 1
        data = {"woes": woe_text, "amount": i, "word": word_str}
        return render(request, 'word_list.html', data)


def get_all_woe(request):
    woes = WOE.objects.all()
    woe_text = []
    word_str = ''
    for woe in woes:
        if woe.text.find(' ' + word_str) > -1:
            lens = woe.text.replace(word_str, '<strong>' + word_str + '</strong>')
            woe_text.append('<h2>' + woe.title + '</h2>' + '<br>' + '<p>' + lens + '</p>' + '<br>')
    data = {"woes": woe_text}
    return render(request, 'word_list.html', data)


def get_all_ch(request):
    chs = CH.objects.all()
    ch_text = []
    word_str = ''
    for ch in chs:
        if ch.text.find(' ' + word_str) > -1:
            lens = ch.text.replace(word_str, '<strong>' + word_str + '</strong>')
            ch_text.append('<h2>' + str(ch.id) + '</h2>' + '<br>' + '<p>' + lens + '</p>' + '<br>')
    print(ch_text)
    data = {"woes": ch_text}
    return render(request, 'word_list.html', data)
