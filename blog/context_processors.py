# blog/context_processors.py
from . import models

def base_context(request):
    topics = models.Post.objects.get_topics()[:10]
    return {'topics': topics}
