from django.shortcuts import render
from game.models.turn import Turn


def index(request):
    turn = Turn()
    hello = "hello"
    return render(request, 'game/index.html', locals())





