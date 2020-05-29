from django.urls import path
from snippets import views
"""
类视图必须要调用 as_view 方法 ，因为视图只接收函数，不接受类， as_view 方法会将类的方法打包进一个函数中然后返回
"""
urlpatterns = [
    path('snippets/', views.snippet_list), # 走 函数 view
    path('snippets/<int:pk>/', views.snippet_detail), # 走 函数 view
    path('snippetsclass/', views.SnippetListView.as_view()), # 走 类 view 
    path('snippetsclass/<int:pk>/', views.SnippetDetailView.as_view()), # 走 类 view
    path('snippetsmixinclass/', views.SnippetGenericMixinListAPIView.as_view()), # 走 类 view
    path('snippetsmixinclass/<int:pk>/', views.SnippetGenericMixinDetailRetrieveAPIView.as_view()), # 走 类 view
    path('users/',views.UserList.as_view()),
    path('users/<int:pk>/',views.UserDetail.as_view()),
]

