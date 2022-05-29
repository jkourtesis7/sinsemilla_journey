from django.http import HttpResponse

def index(request):
    return HttpResponse('''Sinsemilla Journey: A story of
        frustrated ladies and their caretaker''')
