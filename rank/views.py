import json

from django.views import View
from django.http import (
    JsonResponse,
    HttpResponse
)

from .models import (
    GameUser,
    Comment
)
from user.utils import login_decorator

class CommentView(View):
    def get(self, request, user_id):
        try:
            if GameUser.objects.filter(access_id=user_id).exists():
                user     = GameUser.objects.get(access_id=user_id)
                comments = Comment.objects.filter(to_id=user).values()

                return JsonResponse({'comment' : list(comments)}, status=200)

            return JsonResponse({'Message' : 'INVALID_USER'}, status=400)

        except KeyError:
            return JsonResponse({'Message' : 'INVALID_KEYS'}, status=400)

    @login_decorator
    def post(self, request, user_id):
        try:
            data        = json.loads(request.body)
            from_user   = request.userinfo.game_user
            to_user     = GameUser.objects.get(access_id=user_id)

            Comment(
                comment = data['comment'],
                from_id = from_user,
                to_id   = to_user
            ).save()

            return HttpResponse(status=200)

        except KeyError:
            return JsonResponse({'Message' : 'INVALID_KEYS'}, status=400)
