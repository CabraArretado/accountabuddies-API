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
from accountabuddiesAPI.models import Group, ForumPost, GroupUser
from .group_user import GroupUserSerializer




class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'

class Groups(ViewSet):



    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized User instance
        """
        user = User.objects.get(pk=request.user.id)

        group = Group.objects.create(
            title=request.data["title"],
            description=request.data["description"],
            size=request.data["size"],
            created_by=user,
            population=1
        )
        group_user = GroupUser.objects.create(
            user=user,
            group = group,
            is_adm = True
        )

        serializer = GroupSerializer(group, context={'request': request})
        return Response(serializer.data, content_type='application/json')



    def retrieve(self, request, pk=None):
        """Handle GET requests

        Returns:
            Response -- JSON serialized park area instance
        """
        try:
            group = Group.objects.get(pk=pk)
            serializer = GroupSerializer(group, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)



    def update(self, request, pk=None):
        """Handle PUT requests

        Returns:
            Response -- Empty body with 204 status code
        """

        group = Group.objects.get(pk=pk)
        group.title = request.data["title"],
        group.description = request.data["description"],
        group.size=request.data["size"],
        group.population = request.data["population"]

        group.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)



    def destroy(self, request, pk=None):
        """Handle DELETE requests

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            group = Group.objects.get(pk=pk)
            group.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Group.DoesNotExist as ex:
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
        # Custom Queries
        search = self.request.query_params.get('search', None)
        my_groups = self.request.query_params.get('my_groups', None)
        sort = self.request.query_params.get('sort', None)

        # groups = Group.objects.all()
        current_user = User.objects.get(pk=request.auth.user.id)

        groups = GroupUser.objects.filter(user=current_user).prefetch_related("group")

        if my_groups is not None:
            groups = Group.objects.filter(groupuser__user=request.auth.user)
        if search is not None:
            # All the groups the user is not in with the key word
            mygroups = Group.objects.filter(groupuser__user=request.auth.user)
            groups = Group.objects.filter(title__contains=search)
            groups = groups.difference(mygroups)

        
        serializer = GroupSerializer(groups, many=True, context={'request': request})
        return Response(serializer.data)