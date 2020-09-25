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



class ForumCommentarySerializer(serializers.ModelSerializer):
    class Meta:
        model = ForumCommentary
        fields = ('id', 'user', 'created_at', 'title',  'group', 'content', "post")
        depth = 1




class ForumCommentaries(ViewSet):



    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized ForumPost instance
        """
        user = User.objects.get(pk=request.auth.user.id)
        group = Group.objects.get(pk=request.data["group"])
        post = ForumPost.objects.get(pk=request.data["post"])
        

        forum_commentary = ForumCommentary.objects.create(
            title = request.data["title"],
            content = request.data["content"],
            post = post,
            user = user,
            group = group
        )

        serializer = ForumCommentarySerializer(forum_commentary, context={'request': request})
        return Response(serializer.data, content_type='application/json')



    def retrieve(self, request, pk=None):
        """Handle GET requests

        Returns:
            Response -- JSON serialized park area instance
        """
        try:
            forum_commentary = ForumCommentary.objects.get(pk=pk)
            serializer = ForumCommentarySerializer(forum_commentary, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)



    def update(self, request, pk=None):
        """Handle PUT requests

        Returns:
            Response -- Empty body with 204 status code
        """
        forum_commentary = ForumCommentary.objects.get(pk=pk)
        forum_commentary.title = request.data["title"]
        forum_commentary.content = request.data["content"]
        forum_commentary.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)



    def destroy(self, request, pk=None):
        """Handle DELETE requests

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            forum_commentary = ForumCommentary.objects.get(pk=pk)
            forum_commentary.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except ForumCommentary.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



    def list(self, request):
        """Handle GET requests to product resource

        If no query parameters on request return all forum posts without distinctions, otherwise
        return the all forum posts with the keyword provided in the title

        Returns:
            Response -- JSON serialized list of commentaries

        """
        forum_commentaries = ForumCommentary.objects.all()

        # Get all the commentaries of specific post 
        post = self.request.query_params.get('post', None)

        if post is not None:
            forum_commentaries = forum_commentaries.filter(post=post)



        # search = self.request.query_params.get('search', None)
        # sort = self.request.query_params.get('sort', None)
        # if sort is not None:
        #     groups = groups.order_by(sort)
        # if search is not None:
        #     groups = groups.filter(title__contains=search)

        serializer = ForumCommentarySerializer(forum_commentaries, many=True, context={'request': request})

        return Response(serializer.data)