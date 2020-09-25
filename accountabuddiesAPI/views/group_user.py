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
from django.contrib.auth.models import User
from accountabuddiesAPI.models import Group, ForumPost, GroupUser




class GroupUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupUser
        fields = ('user', 'group', 'is_adm',  'created_at')
        depth = 1

class GroupUsers(ViewSet):

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized User instance
        """
        user = User.objects.get(pk=request.user.id)

        group = Group.objects.get(pk=request.data["group"])

        group_user = GroupUser.objects.create(
            group = group,
            user = user
        )

        serializer = GroupUserSerializer(group_user, context={'request': request})
        return Response(serializer.data, content_type='application/json')



    def retrieve(self, request, pk=None):
        """Handle GET requests

        Returns:
            Response -- JSON serialized park area instance
        """
        try:
            group_user = GroupUser.objects.get(pk=pk)
            serializer = GroupUserSerializer(group_user, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)



    def update(self, request, pk=None):
        """Handle PUT requests
        Just changes the the is_adm property 

        Returns:
            Response -- Empty body with 204 status code
        """

        group_user = GroupUser.objects.get(pk=pk)

        group_user.is_adm = request.data["is_adm"]

        group_user.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)



    def destroy(self, request, pk=None):
        """Handle DELETE requests

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            group_user = GroupUser.objects.get(pk=pk)
            group_user.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except GroupUser.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



    def list(self, request):
        """Handle GET requests to product resource

        If no query parameters on request return all items without distinctions, otherwise
        return the all items with the kewword provided in the title

        Returns:
            Response -- JSON serialized list of products

        """
        user_groups = GroupUser.objects.all()

        # has to send my_groups as true to send back all the relaitons
        my_groups = self.request.query_params.get('my_groups', None)
        leave_group = self.request.query_params.get('leave_group', None)

        if my_groups is not None:
            user_groups = request.auth.user.groupuser_set.all()


        serializer = GroupUserSerializer(user_groups, many=True, context={'request': request})
        return Response(serializer.data)