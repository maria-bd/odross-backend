from django.http import JsonResponse
from .models import Users
from .serializers import UsersSerializer

def user_list(request):
    if request.method == 'GET':
        users = Users.objects.all()
        serializer = UsersSerializer(users, many=True)
        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)
