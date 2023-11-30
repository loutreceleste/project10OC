from datetime import date

from django.http import JsonResponse
from authentication.models import User
from authentication.serializers import UserSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED


@api_view(['GET', 'POST'])
def users_list(request):

        if request.method == 'GET':
                users = User.objects.all()
                serializer = UserSerializer(users, many=True)
                return Response(serializer.data)

        if request.method == 'POST':
                serializer = UserSerializer(data = request.data)
                if serializer.is_valid():
                        birthday = serializer.validated_data.get('birthday')
                        today = date.today()
                        age = today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))
                        if age >= 15:
                                serializer.save()
                                return Response(serializer.data, status=HTTP_201_CREATED)
                        else:
                                return Response({"message": "L'utilisateur doit avoir au moins 15 ans pour s'enregistrer."},
                                        status=status.HTTP_400_BAD_REQUEST)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def users_list_detail(request, id):

        try:
                user = User.objects.get(pk=id)
        except User.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
                serializer = UserSerializer(user)
                return Response(serializer.data)

        elif request.method == 'PUT':
                serializer = UserSerializer(user, data=request.data)
                if serializer.is_valid():
                        serializer.save()
                        return Response(serializer.data)
                return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
                user.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
