from django.shortcuts import render
from django.http import HttpResponse ,Http404
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view,APIView
from rest_framework.response import Response
from rest_framework import status
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer,UserSerializer
from rest_framework import mixins , generics 
from django.contrib.auth.models import User
# Create your views here.

"""
1、对list 的操作 为 get 和 post
2、对defail 的操作为 get、put、delete
"""

# # 创建 解析工具
# class JSONResponse(HttpResponse):
#     """
#     An HttpResponse that renders its content into JSON.
#     """
#     def __init__(self,data,**kwargs):
#         content = JSONRenderer().render(data)
#         kwargs['content_type'] = 'application/json'
#         super(JSONResponse,self).__init__(content, **kwargs)


# @csrf_exempt
# def snippet_list(request): 
#     """
#         列出所有的snippet或者创建一个新的snippet ， list 操作 
#     """
#     if request.method == 'GET': # get请求 取数据列表，然后返回
#         snippet = Snippet.objects.all()
#         serializer = SnippetSerializer(snippet,many=True)
#         return JSONResponse(serializer.data)

#     elif request.method == 'POST': # post 请求  
#         # 首先解析 请求中的data，然后序列化，判断序列化是否成功，成功就 调用save方法
#         data = JSONParser().parse(request)
#         serializer = SnippetSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JSONResponse(serializer.data,status = 201) # 返回json，且 状态码为 201 
#         return JSONResponse(serializer.errors,status = 400) # 如果数据不合法，则返回序列化的错误信息


# @csrf_exempt
# def snippet_detail(request,pk):
#     """
#         获取，更新或删除一个 code snippet。 单个操作
#     """
#     try:
#         snippet = Snippet.objects.get(pk=pk) # 先根据 pk 获取到一个 确定的数据
#     except Snippet.DoesNotExist:
#         return HttpResponse(status=404)
    
#     if request.method == 'GET':
#         serializer = SnippetSerializer(snippet)
#         return JSONResponse(serializer.data)

#     elif request.method == 'PUT':
#         data = JSONParser().parse(request)
#         serializer = SnippetSerializer(snippet, data=data)
        
#         if serializer.is_valid():
#             serializer.save()
#             return JSONResponse(serializer.data)
#         return JSONResponse(serializer.errors, status=400)

#     elif request.method == 'DELETE': # delete 请求
#         snippet.delete()
#         return JSONResponse(status=204)


"""
    rest_framework 提供两个可用于编写API视图的包装器 ，可以将 多个方法的视图 集合到同一个函数或者类中
    用于 函数 的  @api_view 装饰器
    用于 类的  APIView 类
"""

# 基于函数的视图  format = None 即 不解析后边的format
@csrf_exempt
@api_view(['GET','POST'])
def snippet_list(request,format = None):
    """
    列出所有的snippets，或者创建一个新的snippet
    """
    if request.method == 'GET':
        snippet = Snippet.objects.all()
        serializer = SnippetSerializer(snippet,many = True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = SnippetSerializer(data = request.data)

        if serializer.is_valid(): # 如果传过来的参数时序列化之后是合法的，则执行save，返回 201 created
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['GET','PUT','DELETE'])
def snippet_detail(request, pk, format = None):
    """
    获取、更新、删除一个pk索引的snippets,先获取资源，如果获取失败直接返回 Not Found
    """
    try:
        snippet = Snippet.objects.get(pk=pk)
    except expression as identifier:
        return Response(status = status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET': # get请求  序列化之后直接返回
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    elif request.method == 'PUT':

        serializer = SnippetSerializer(snippet,data = request.data)

        if serializer.is_valid(): # 如果 传过来的值都是合法的
            serializer.save()
            return Response(serializer.data, status = status.HTTP_200_OK)
        
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE': # 如果是删除
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# 基于类的视图 , 继承自 APIView

# list  有 get 和 post 方法
class SnippetListView(APIView):
    """
    列出所有的snippets，或者创建一个新的snippet，使用 class view 必须在 url中调用 as_view() 方法
    """
    def get(self,request,format=None): # 基于类，所以 第一个参数为 self

        snippet = Snippet.objects.all()
        serializer = SnippetSerializer(snippet,many = True)

        return Response(serializer.data)
    
    def post(self,request,format=None):
        serializer = SnippetSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status = status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
     
# detail 有 get put delete 方法
class SnippetDetailView(APIView):
    """
    获取、更新、删除一个pk索引的snippets,先获取资源，如果获取失败直接返回 Not Found，使用 class view 必须在 url中调用 as_view() 方法
    """
    # 由于 detail 是基于一条已有的数据 做一些 改变，所以需要先定义获取数据的 func
    def get_object(self,pk):  # 该方法可用 generics.get_object_or_404 来 代替
        try:
            return Snippet.objects.get(pk = pk)
        except expression as identifier:
            raise Http404
            

    def get(self, request ,pk ,format=None):
        snippet = self.get_object(pk)
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request,pk,format=None):
        snippet = self.get_object(pk)
        serializer = SnippetSerializer(snippet, data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def delete(self, request,pk,format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

   
"""
基于类视图的最大优势之一是它可以轻松地创建可复用的行为。基于模型的api视图都是可以复用的， rest framework 在 mixins 实现  
"""
# 基于 mixins 的 类视图  list 支持  get post 
class SnippetMixinListView(mixins.ListModelMixin,
                            mixins.CreateModelMixin,
                            generics.GenericAPIView):
    """
    list 视图 ，具有  list 和 create api ，分别对应 get 和 post 方法。 类 View 则 继承自 GenericAPIView
    GenericAPIView 内置了 get_object, get_queryset, 且 必须设置 self.queryset,除非 覆写 get_object 和 get_queryset
    ListModelMixin 提供了 list 方法， 代替 SnippetSerializer(snippet,many=True)
    CreateModelMixin 提供了 create 方法， 代替 SnippetSerializer(data = request.data) 和 is_valid 以及save 操作.
    mixins 类 必须 依赖于 GenericAPIView 类提供的方法
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer # serializer class

    def get(self,request,*args,**kwargs):
        # 直接调用 ListModelMixin 内置的list 方法
        return self.list(request,*args,**kwargs)
    
    def post(self,request,*args,**kwargs):
        # 直接调用 CreateModelMixin 内置的create 方法
        return self.create(request,*args,**kwargs)


# 基于 mixins 的 类视图  defail 支持  get put delete 
class SnippetMixinDetailView(mixins.RetrieveModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.DestroyModelMixin,
                            generics.GenericAPIView):
    """
    detail 视图 ，具有  retrieve 和 update destroy api ，分别对应 get 和 put、delete 方法。 类 View 则 继承自 GenericAPIView 。
    GenericAPIView 内置了 get_object, get_queryset, 且 必须设置 self.queryset,除非 覆写 get_object 和 get_queryset
    RetrieveModelMixin 提供了 retrieve 方法， 代替 SnippetSerializer(snippet)
    UpdateModelMixin 提供了 update 方法， 代替 SnippetSerializer(snippet，data = request.data) 和 is_valid 以及save 操作.
    DestroyModelMixin 提供了 destroy 方法， 代替  snippet.delete() 操作.
    mixins 类 必须 依赖于 GenericAPIView 类提供的方法
    为什么 mixins 类提供的方法不是 get ，post ，delete 而是 retrieve、create、update 的原因。->
    主要是 在我们的类中需要自定义 get、post、update 等方法，如果 mixins提供的方法名是http方法，则会被我们写的方法 覆盖。
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer # serializer class

    def get(self,request,*args,**kwargs):
        # 直接调用 RetrieveModelMixin 内置的 retrieve 方法
        return self.retrieve(request,*args,**kwargs)
    
    def put(self,request,*args,**kwargs):
        # 直接调用 UpdateModelMixin 内置的 update 方法
        return self.update(request,*args,**kwargs)

    def delete(self,request,*args,**kwargs):
        # 直接调用 DestroyModelMixin 内置的 destory 方法
        return self.destroy(request,*args,**kwargs)



"""
我们通过 组合 mixins的类和 generics 提供的GenericAPIView ，可以减少代码量，但是 还是要写 基础的http方法。
generics 提供了一系列 mixins 和 提供的GenericAPIView 组合起来的 APIView，这样 get，post 等 http 方法也不需要写了。

ListAPIView 等同于 ListModelMixin 和 GenericAPIView 的组合，且 内置实现了 get 方法。
CreateAPIView 等同于 CreateModelMixin 和 GenericAPIView 的组合，且 内置实现了 post 方法。
ListCreateAPIView 等同于 ListModelMixin,CreateModelMixin 和 GenericAPIView 的组合，且 内置实现了get, post 方法。
RetrieveAPIView 等同于 RetrieveModelMixin 和 GenericAPIView 的组合，且 内置实现了get 方法。
DestroyAPIView 等同于 DestroyModelMixin 和 GenericAPIView 的组合，且 内置实现了delete 方法,在delete中调用 destory方法。
其他等同
"""

class SnippetGenericMixinListAPIView(generics.ListAPIView):
    """
    ListAPIView 等同于 ListModelMixin 和 GenericAPIView 的组合，且 内置实现了 get 方法。
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer # serializer class

class SnippetGenericMixinCreateAPIView(generics.CreateAPIView):
    """
    CreateAPIView 等同于 CreateModelMixin 和 GenericAPIView 的组合，且 内置实现了 post 方法。
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer # serializer class

class SnippetGenericMixinListCreateAPIView(generics.ListCreateAPIView):
    """
    ListCreateAPIView 等同于 ListModelMixin,CreateModelMixin 和 GenericAPIView 的组合，且 内置实现了get, post 方法。
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer # serializer class

class SnippetGenericMixinDetailRetrieveAPIView(generics.RetrieveAPIView):
    """
    RetrieveAPIView 等同于 RetrieveModelMixin 和 GenericAPIView 的组合，且 内置实现了 get 方法。并在get内部执行 retrieve 方法
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer # serializer class



# 添加 user 视图

class UserList(generics.ListAPIView): # 获取user
    """
    获取user 的list, ListAPIView 提供了 get 方法 ，然后调用了 ListModelMixin 的 list 方法
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer



class UserDetail(generics.RetrieveAPIView): #  update新的
    """
    getuser， RetrieveAPIView 提供了 get 方法 ，然后调用了 RetrieveModelMixin 的 retrieve 方法.并获取了uri传参
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer