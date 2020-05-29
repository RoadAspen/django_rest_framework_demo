from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Snippet, STYLE_CHOICES, LANGUAGE_CHOICES

# serializers 主要是为了 序列化输入 和  输出， serializers.Serializer 是最基本的 序列化基类
# class SnippetSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True) # 只读
#     title = serializers.CharField(read_only=False,allow_blank = True, max_length=100) # 可读写
#     code = serializers.CharField(style={'base_template': 'textarea.html'})
#     linenos = serializers.BooleanField(required=True) # 必传
#     language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python') # choice 默认为 python
#     style = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly') 

#     # 新增时
#     def create(self,validated_date):
#         """
#             根据提供的验证过的数据创建并返回一个新的 Snippet 实例
#         """
#         return Snippet.objects.create(**validated_date)

#     # 更新时 validated_date
#     def update(self, instance, validated_date):
#         """
#             根据提供的验证过的数据更新并返回一个已存在的 Snippet 实例
#         """
#         instance.title = validated_date.get('title',instance.title) # 如果传入title就取title，否则取实例的原始title
#         instance.code = validated_data.get('code', instance.code)
#         instance.linenos = validated_data.get('linenos', instance.linenos)
#         instance.language = validated_data.get('language', instance.language)
#         instance.style = validated_data.get('style', instance.style)

#         instance.save() # 最后一定要调用 save 方法 
#         return instance


"""
使用 ModelSerializers , 可以通过 Meta 中的  model 和fields 快速的创建对应Model 的序列化器
并 默认简单实现的 create  和 update 。  get 方法是不需要特殊的字段验证
"""
class SnippetSerializer(serializers.ModelSerializer):


    class Meta:
        model = Snippet
        fields=('id', 'title', 'code', 'linenos', 'language', 'style')





class UserSerializer(serializers.ModelSerializer):
    """
    model 中不存在snippets 字段，这里通过反向关联查出，所以需要添加
    """
    snippets = serializers.PrimaryKeyRelatedField(many=True,queryset=Snippet.objects.all())
    
    class Meta:
        model = User
        fields = ('id', 'username', 'snippets')
