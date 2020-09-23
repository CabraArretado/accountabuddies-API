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
from accountabuddiesAPI.models import Group, ForumPost, ForumCommentary



class ForumPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForumPost
        fields = ('id', 'created_by', 'created_at', 'title',  'group', 'content')
        depth = 1

class ForumPosts(ViewSet):



    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized ForumPost instance
        """
        print(request.data)
        user = User.objects.get(pk=request.auth.user.id)
        group = Group.objects.get(pk=request.data["group"])

        forum_post = ForumPost.objects.create(
            title=request.data["title"],
            content=request.data["content"],
            group=group,
            created_by=user,

        )

        serializer = ForumPostSerializer(forum_post, context={'request': request})
        return Response(serializer.data, content_type='application/json')



    def retrieve(self, request, pk=None):
        """Handle GET requests

        Returns:
            Response -- JSON serialized park area instance
        """
        try:
            forum_post = ForumPost.objects.get(pk=pk)
            serializer = ForumPostSerializer(forum_post, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)



    def update(self, request, pk=None):
        """Handle PUT requests

        Returns:
            Response -- Empty body with 204 status code
        """
        pass
        # forum_post = ForumPost.objects.get(pk=pk)
        # forum_post.title = request.data["title"]
        # forum_post.content = request.data["content"]
        # forum_post.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)



    def destroy(self, request, pk=None):
        """Handle DELETE requests

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            forum_post = ForumPost.objects.get(pk=pk)
            forum_post.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except ForumPost.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



    def list(self, request):
        """Handle GET requests to product resource

        If no query parameters on request return all forum posts without distinctions, otherwise
        return the all forum posts with the keyword provided in the title

        Returns:
            Response -- JSON serialized list of posts

        """

        forum_posts = ForumPost.objects.all()

        group = self.request.query_params.get('group', None)
        search = self.request.query_params.get('search', None)
        post = self.request.query_params.get('post', None)

        if post is not None:
            forum_posts = forum_posts.filter(group=group)
        if group is not None:
            forum_posts = forum_posts.filter(group=group)
        if search is not None:
            forum_posts = forum_posts.filter(group=group).filter(title__contains=search)

        serializer = ForumPostSerializer(forum_posts, many=True, context={'request': request})

        return Response(serializer.data)