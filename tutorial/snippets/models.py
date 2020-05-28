from django.db import models
from pygments.lexers import get_all_lexers, get_lexer_by_name
from pygments.styles import get_all_styles
from pygments.formatters.html import HtmlFormatter
# Create your models here.

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0],item[0]) for item in LEXERS])
STYLE_CHOICES = sorted((item, item) for item in get_all_styles())

# model 类
class Snippet(models.Model):
    """
    外键 owner ，外联至 auth.User model， related_name 默认为当前的model类的小写， 主要用于反查 
    """
    owner1 = models.ForeignKey('auth.User',related_name='snippets',on_delete= models.CASCADE, default='')
    highlighted = models.TextField() 

    created = models.DateTimeField(auto_now_add=True) # 创建时间 自动生成
    title = models.CharField(max_length=100,blank=True,default='') # title 不传默认为 空字符串
    code = models.TextField() # 文字类型 不设长度
    linenos = models.BooleanField(default=False) # 布尔类型 默认为 false
    language = models.CharField(choices=LANGUAGE_CHOICES,default='python',max_length=100) # 语言类型 可选像为 list 
    style = models.CharField(choices=STYLE_CHOICES,default='friendly', max_length=100) # 样式 可选项较多

    # 添加 save 方法
    def save(self, *args, **kwargs):
        """
        使用`pygments`库创建一个高亮显示的HTML表示代码段。
        """ 
        lexer = get_lexer_by_name(self.language) # 这里通过计算获得 一个 lexer 值
        linenos = self.linenos and 'table' or False # 类似 js 中的 三目运行算符
        options = self.title and {'title': self.title} or {}  # 类似 js 中的 三目运算符
        formatter = HtmlFormatter(style=self.style, linenos=linenos,
                              full=True, **options)
        self.highlighted = highlight(self.code, lexer, formatter)

        super(Snippet, self).save(*args, **kwargs) # 由于覆盖了父类的save方法，这里重新执行父类的super().save, 


    class Meta:
        ordering = ['created'] # 根据 created 时间排序

