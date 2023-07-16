from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Post
from .Serializers import PostSerializer

@api_view(['GET'])
def index(request):
    return Response({"success": "the setup was successful"})


@api_view(['GET'])
def GetAllPosts(request):
    get_posts = Post.objects.all()
    serializer = PostSerializer(get_posts, many=True)
    return Response(serializer.data)
    # many=true to get many items and not a single data


@api_view(['GET', 'POST'])
def CreatePost(request):
    data = request.data
    serializer = PostSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({"Success": "the post was created successfully"}, status=201)
    else:
        return Response(serializer.errors, status=400)


@api_view(['DELETE'])
def DeletePost(request):
    post_id = request.data.get('post_id')
    try:
        post = Post.objects.get(id=post_id)
        post.delete()
        return Response({"Success": "the post was successfully deleted"})
    except Post.DoesNotExist:
        return Response({"Error": "the post does not exist"}, status=400)


@api_view(['GET'])
def GetPost(request):
    post_id = request.data.get('post_id')
    try:
        post = Post.objects.get(id=post_id)
        serializer = PostSerializer(post)
        return Response(serializer.data)
    except Post.DoesNotExist:
        return Response({"Error": "the post does not exist"}, status=404)


@api_view(['PUT'])
def UpdatePost(request):
    post_id = request.data.get('post_id')
    new_title = request.data.get('new_title')
    new_content = request.data.get('new_content')

    try:
        post = Post.objects.get(id=post_id)

        if new_title:
            post.title = new_title
        if new_content:
            post.content = new_content

        post.save()
        return Response({"Success": "the post was successfully updated"}, status=200)

    except Post.DoesNotExist:
        return Response({"Error": "the post does not exist"}, status=404)
