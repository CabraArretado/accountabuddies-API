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
from accountabuddiesAPI.models import Group, Task



class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task

        fields = ('id', 'title', 'created_by', 'created_at', 'group', 'description', 'due', 'done')
        depth = 1

class Tasks(ViewSet):



    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized ForumPost instance
        """
        created_by = User.objects.get(pk=request.auth.user.id)
        group = Group.objects.get(pk=request.data["group"])

        task = Task.objects.create(
            title = request.data["title"],
            description = request.data["description"],
            due = request.data["due"],
            created_by = created_by,
            group = group
        )

        serializer = TaskSerializer(task, context={'request': request})
        return Response(serializer.data, content_type='application/json')



    def retrieve(self, request, pk=None):
        """Handle GET requests

        Returns:
            Response -- JSON serialized instance
        """
        try:
            task = Task.objects.get(pk=pk)
            serializer = TaskSerializer(task, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)



    def update(self, request, pk=None):
        """Handle PUT requests

        Returns:
            Response -- Empty body with 204 status code
        """
        task = Task.objects.get(pk=pk)
        task.title = request.data["title"]
        task.description = request.data["description"]
        task.due =request.data["due"]
        task.done =request.data["done"]
        task.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)



    def destroy(self, request, pk=None):
        """Handle DELETE requests

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            task = Task.objects.get(pk=pk)
            serializer = TaskSerializer(task, context={'request': request})

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Task.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



    def list(self, request):
        """Handle GET requests to product resource

        If no query parameters on request return all forum posts without distinctions, otherwise
        return the all forum posts with the keyword provided in the title

        Returns:
            Response -- JSON serialized list of products

        """

        tasks = Task.objects.all()

        group = self.request.query_params.get('group', None)

        if group is not None:
            tasks = tasks.filter(group=group)

        serializer = TaskSerializer(tasks, many=True, context={'request': request})

        return Response(serializer.data)