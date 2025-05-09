from .models import Relationship

def relationship_status(request):
    if request.user.is_authenticated:
        return {
            'is_following': lambda user: Relationship.objects.filter(
                follower=request.user,
                followed=user
            ).exists(),
            'is_friends': lambda user: Relationship.objects.filter(
                follower=request.user,
                followed=user,
                is_friends=True
            ).exists(),
            'friend_request_sent': lambda user: Relationship.objects.filter(
                follower=request.user,
                followed=user,
                is_friends=False
            ).exists()
        }
    return {}