"""
自定义权限
"""

from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    可以被任何人看到，但是只有创建代码片段的用户才能更新或删除
    """

    def has_object_permission(self,request,view,obj):
        # 读权限 为 任意请求
        # 如果 请求的方法 是 安全的方法，即幂等的。
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # 其他非安全请求，如 put， delete则只有 snippet 的owner才能执行
        return obj.owner == request.user 
