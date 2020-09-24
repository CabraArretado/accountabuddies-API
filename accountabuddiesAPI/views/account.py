import json
from django.http import HttpResponse
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from accountabuddiesAPI.models import Account

# class AccountSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Account
#         url = serializers.HyperlinkedIdentityField(
#             view_name='account',
#             lookup_field='id'
#         )
#         fields = ('id', 'user')
#         depth = 1
class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'
        depth = 2



class Accounts(ViewSet):

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized User instance
        """

        user = User.objects.create_user(
            first_name=request.data["first_name"],
            last_name=request.data["last_name"],
            password=request.data["password"],
            # username is equal to email
            username=request.data["email"],
            email=request.data["email"]
        )

        account = Account.objects.create(
            user=user
        )

        token = Token.objects.create(user=user)

        data = json.dumps({"token": token.key})
        return HttpResponse(data, content_type='application/json')

    def retrieve(self, request, pk=None):
        """Handle GET requests

        Returns:
            Response -- JSON serialized park area instance
        """
        try:
            account = Account.objects.get(pk=pk)
            serializer = AccountSerializer(
                account, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests

        Returns:
            Response -- Empty body with 204 status code
        """

        account = Account.objects.get(pk=pk)

        user = User.objects.get(pk=account.user.id)
        user.first_name = request.data["first_name"]
        user.last_name = request.data["last_name"]
        user.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            user = User.objects.get(pk=pk)
            user.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Account.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):

        myself = self.request.query_params.get('myself', None)

        # myself true makes just the current profile be sent back

        if myself:
            account = Account.objects.filter(user=request.user.id)
        else:
            account = Account.objects.all()

        serializer = AccountSerializer(account, many=True, context={'request': request})

        return Response(serializer.data)