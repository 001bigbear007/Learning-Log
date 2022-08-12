# -*- coding:utf-8 -*-
# author:bigbear
# software: PyCharm
from django.contrib.auth.models import User
from django.db import models


# Create your models here.（在这里创建模型：模型告诉Django如何处理应用程序中存储的数据）

# 创建Topic类，继承了Django中的Model类（定义了模块基本功能）
class Topic(models.Model):
    """用户学习的主题（创建时分配一个外键或ID）"""
    # CharField：由字符或文本组成的数据，且必须指定预留空间max_length（定长存储）
    text = models.CharField(max_length=200)  # 可存储少量文本，如名称、标题、城市等
    # DateTimeField：记录日期和时间的数据；auto_now_add：自动设置成当前日期和时间
    date_added = models.DateTimeField(auto_now_add=True)  # 按创建顺序呈现主题，并在每个主题旁边放置时间戳
    # 通过外键将主题类与模型User关联
    # 解决django.db.utils.OperationalError: no such column: learning_logs_topic.owner_id方法：添加db_column='owner'再次运行迁移命令即可
    owner = models.ForeignKey(User, default='1', db_column='owner', on_delete=models.CASCADE)

    def __str__(self):
        """"返回模型的字符串表示，来显示有关主题的信息"""
        return self.text


# 创建Entry类，继承了Django基类Model
class Entry(models.Model):
    """学到的有关某个主题的具体知识"""
    """
    ForeignKey：外键，引用了数据库中的另一条记录，且必须设置on_delete：
    （1）CASCADE（默认设置此项）：删除级联，当父表的记录删除时，子表中与其相关联的记录也会删除。
    （2）PROTECT：子表记录所关联的父表记录被删除时，会报ProtectedError异常。
    （3）SET_NULL：子表记录所关联的父表记录被删除时，将子表记录中的关联字段设为NULL，注意：需要允许数据表的该字段为NULL。
    （4）SET_DEFAULT：子表记录所关联的父表记录被删除时，将子表记录中的关联字段设为一个给定的默认值。
    （5）DO_NOTHING：子表记录所关联的父表记录被删除时，什么也不做。
    （6）SET()：设置为一个传递给SET()的值或者一个回调函数的返回值，该参数用得相对较少。
    """
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)  # ForeignKey实例：将每个条目关联到特定的主题
    # TextField：由字符或文本组成的数据，但无长度限制（变长存储）
    text = models.TextField()  # TextField实例：存储条目
    # DateTimeField：记录日期和时间的数据；auto_now_add：自动设置成当前日期和时间
    date_added = models.DateTimeField(auto_now_add=True)  # 按创建顺序呈现条目，并在每个条目旁边放置时间戳

    # 嵌套Meta类
    class Meta:
        """存储用于管理模型的额外信息"""
        # 让Django在需要时使用Entries来表示多个条目；若无该类，则使用Entrys来表示多个条目
        verbose_name_plural = "entries"

    def __str__(self):
        """返回模型的字符串表示，来显示有关条目的部分信息"""
        if len(self.text) > 50:
            return self.text[:50] + "..."
        else:
            return self.text
