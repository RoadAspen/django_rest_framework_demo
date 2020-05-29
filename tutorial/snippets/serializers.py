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
使用 ModelSerializers , 可以通过 Meta 中的  model 和fields 快速的创建对应Model 的序列化器。field 字段在这里已经不需要了， 
并 默认简单实现的 create  和 update 。  get 方法是不需要特殊的字段验证
"""
# class SnippetSerializer(serializers.ModelSerializer):
#
#     """
#     source 控制用哪个属性填充字段，并且可以指向序列化十里山搞得任何属性,这里定义的属性必须在 fields中添加.
#     readonlyfield 只读，只能序列化表示，不能反序列化更新模型实例， 也可以使用 CharField（readonly = True）
#     """
#     owner = serializers.ReadOnlyField(source = 'owner.username')
#
#     class Meta:
#         model = Snippet
#         fields=('id', 'title', 'code', 'linenos', 'language', 'style', 'owner')
#
#
#
#
#
# class UserSerializer(serializers.ModelSerializer):
#     """
#     model 中不存在snippets 字段，这里通过反向关联查出，所以需要添加
#     """
#     snippets = serializers.PrimaryKeyRelatedField(many=True,queryset=Snippet.objects.all())
#
#     class Meta:
#         model = User
#         # fields 不一定填写 model中的字段，也可以填写不在model的字段，这些字段以及 serializer定义 在 执行 get 和 retrieve 操作时执行
#         fields = ('id', 'username', 'snippets')


"""
在实体之间使用超链接的方式 ，HyperlinkedModelSerializer 与 ModelSerializer 的 区别是 
HyperlinkedModelSerializer 默认不包含 'id' 字段。 它包含一个url字段，使用 HyperlinkedIdentityField
关联关系使用HyperlinkedRelatedField，而不是PrimaryKeyRelatedField
根据 url 的不同
"""


class SnippetSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    # 在 view_name 指向 url 为 snippet-highlight
    highlight = serializers.HyperlinkedIdentityField(view_name='snippet-highlight', format='html')

    # url 指向 model_name-detail
    class Meta:
        model = Snippet
        fields = ['url', 'id', 'highlight', 'owner',
                  'title', 'code', 'linenos', 'language', 'style']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    # 在 view_name 指向 url 指向 snippet-detail， 可以点击
    snippets = serializers.HyperlinkedRelatedField(many=True, view_name='snippet-detail', read_only=True)

    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'snippets']
