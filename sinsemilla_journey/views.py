from django.http import HttpResponse

def index(request):
    return HttpResponse('''Sinsemilla Journey: A story of
        frustrasted ladies and their caretaker''')
