from users.models import Story

def stories(request):
    stories = Story.objects.all().order_by('-created_at')
    return {'stories': stories}