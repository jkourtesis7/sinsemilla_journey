"""
First view for Sinsemilla Journey
"""
from django.http import HttpResponse

def index(request):
    """
    Index request
    """
    return HttpResponse('''Sinsemilla Journey: A story of
        frustrated ladies and their caretaker''')
