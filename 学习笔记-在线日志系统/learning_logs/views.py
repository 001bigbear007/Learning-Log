# -*- coding:utf-8 -*-
# author:bigbear
# software: PyCharm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse

from .forms import TopicForm, EntryForm
from .models import Topic, Entry  # 从当前文件所在文件夹中的模型模块modes中导入数据关联模型Topic、Entry


# 核实主题关联到的用户是否为当前登录用户
def check_topic_owner(topic, request):
    if topic.owner != request.user:
        raise Http404  # 非主题关联用户访问返回404响应


# Create your views here.（在这里创建视图）

def index(request):
    """学习笔记的主页视图"""
    # render()根据视图提供的数据渲染响应，参数：原始请求对象、可用于创建网页的模板
    return render(request, 'learning_logs/index.html')


@login_required  # 调用函数login_required()，检查用户是否已登录：已登录运行下列函数代码；未登录重定向到登录页面
def topics(request):
    """学习笔记的主题页视图"""
    # 获取主题：查询数据库，通过filter()过滤当前用户的Topics对象，并按属性date_added排序，并将返回的查询集存储到变量topics中
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    # 定义上下文字典：键-访问数据的名称，值-发送给模板的数据
    context = {'topics': topics}
    # render()根据视图提供的数据渲染响应，参数：原始请求对象、可用于创建网页的模板、发送给模板的数据
    return render(request, 'learning_logs/topics.html', context)


@login_required  # 调用函数login_required()，检查用户是否已登录：已登录运行下列函数代码；未登录重定向到登录页面
def topic(request, topic_id):
    """学习笔记的特定主题页视图"""
    # 获取特定主题：通过topic_id查询数据库，请求单个Topic对象，并将返回的查询集存储到变量topic中
    topic = Topic.objects.get(id=topic_id)
    # 确定请求的主题属于当前用户
    check_topic_owner(topic, request)
    # 获取特定主题的条目：查询数据库，请求提供特定主题的entries对象，并按属性date_added排序，并将返回的查询集存储到变量entries中
    entries = topic.entry_set.order_by('date_added')
    # 定义上下文字典：键-访问数据的名称，值-发送给模板的数据
    context = {'topic': topic, 'entries': entries}
    # render()根据视图提供的数据渲染响应，参数：原始请求对象、可用于创建网页的模板
    return render(request, 'learning_logs/topic.html', context)


@login_required  # 调用函数login_required()，检查用户是否已登录：已登录运行下列函数代码；未登录重定向到登录页面
def new_topic(request):
    """学习笔记的主题新增页视图"""
    # 判断请求方法：GET请求是进入主题新增页，需要一个空表单；即便是其他类型请求，返回一个空表单也无妨
    if request.method != 'POST':
        # 未提交数据：创建一个新表单
        form = TopicForm()  # 创建TopicForm()实例，并将其存储到变量form中
    # 而POST请求是用户填写完表单提交，需要保存表单，并将表单内容添加到主题页中显示
    else:
        # POST提交的数据，对数据进行处理
        form = TopicForm(request.POST)  # 使用request.POST中存储的用户输入数据，创建TopicForm()实例
        if form.is_valid():  # 自动验证用户填写了所有必不可少的字典，且输入数据与要求字段类型一致（如：字段text少于200个字符）
            new_topic = form.save(commit=False)  # 通过验证后的数据先不提交到数据库，暂时保存到变量new_entry中
            new_topic.owner = request.user  # 设置属性topic为从数据库中获取的主题
            new_topic.save()  # 将条目对象保存到数据库，并与正确的主题相关联
            # HttpResponseRedirect()：将用户重定向到主题页中
            return HttpResponseRedirect(reverse('learning_logs:topics'))  # reverse()根据指定的URL模型确定URL
    # 将空表单添加到上下文字典中
    context = {'form': form}
    # render()根据视图提供的数据渲染响应，参数：原始请求对象、可用于创建网页的模板
    return render(request, 'learning_logs/new_topic.html', context)


@login_required  # 调用函数login_required()，检查用户是否已登录：已登录运行下列函数代码；未登录重定向到登录页面
def edit_topic(request, topic_id):
    """学习笔记的特定主题编辑页视图"""
    # 获取需修改的主题
    topic = Topic.objects.get(id=topic_id)
    # 确定请求的主题属于当前用户
    check_topic_owner(topic, request)
    # 判断请求方法：GET请求是进入特定条目编辑页，使用当前条目填充表单；即便是其他类型请求，返回一个同样的表单也无妨
    if request.method != 'POST':
        # 未提交数据：仅使用当前条目填充表单
        form = TopicForm(instance=topic)  # 使用instance=topic创建TopicForm()实例，并将其存储到变量form中
    # 而POST请求是用户填写完表单提交，需要保存表单，并将表单内容添加到主题页中显示
    else:
        # POST提交的数据，对数据进行处理
        form = TopicForm(instance=topic, data=request.POST)  # 使用instance=topic创建TopicForm()实例，再使用request.POST中的相关数据进行修改
        if form.is_valid():  # 自动验证用户填写了所有必不可少的字典，且输入数据与要求字段类型一致
            form.save()  # 将已修改号的条目对象保存到数据库
            # HttpResponseRedirect()：将用户重定向到主题页中
            return HttpResponseRedirect(reverse('learning_logs:topics'))  # reverse()根据指定的URL模型确定URL
    # 将原主题表单添加到上下文字典中
    context = {'topic': topic, 'form': form}
    # render()根据视图提供的数据渲染响应，参数：原始请求对象、可用于创建网页的模板
    return render(request, 'learning_logs/edit_topic.html', context)


@login_required  # 调用函数login_required()，检查用户是否已登录：已登录运行下列函数代码；未登录重定向到登录页面
def new_entry(request, topic_id):
    """学习笔记的特定主题条目新增页视图"""
    # 获取渲染页面以及处理表单数据的主题
    topic = Topic.objects.get(id=topic_id)
    # 确定请求的主题属于当前用户
    check_topic_owner(topic, request)
    # 判断请求方法：GET请求是进入特定主题的条目新增页，需要一个空表单；即便是其他类型请求，返回一个空表单也无妨
    if request.method != 'POST':
        # 未提交数据：创建一个新表单
        form = EntryForm()  # 创建EntryForm()实例，并将其存储到变量form中
    # 而POST请求是用户填写完表单提交，需要保存表单，并将表单内容添加到特定主题的条目页中显示
    else:
        # POST提交的数据，对数据进行处理
        form = EntryForm(data=request.POST)  # 使用request.POST中存储的用户输入数据，创建EntryForm()实例
        if form.is_valid():  # 自动验证用户填写了所有必不可少的字典，且输入数据与要求字段类型一致
            new_entry = form.save(commit=False)  # 通过验证后的数据先不提交到数据库，暂时保存到变量new_entry中
            new_entry.topic = topic  # 设置属性topic为从数据库中获取的主题
            new_entry.save()  # 将条目对象保存到数据库，并与正确的主题相关联
            # HttpResponseRedirect()：将用户重定向到特定主题条目页中
            return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic_id]))  # reverse()根据指定的URL模型确定URL
    # 将空表单添加到上下文字典中
    context = {'topic': topic, 'form': form}
    # render()根据视图提供的数据渲染响应，参数：原始请求对象、可用于创建网页的模板
    return render(request, 'learning_logs/new_entry.html', context)


@login_required  # 调用函数login_required()，检查用户是否已登录：已登录运行下列函数代码；未登录重定向到登录页面
def edit_entry(request, entry_id):
    """学习笔记的特定条目编辑页视图"""
    # 获取需修改的条目以及关联的主题
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    # 确定请求的主题属于当前用户
    check_topic_owner(topic, request)
    # 判断请求方法：GET请求是进入特定条目编辑页，使用当前条目填充表单；即便是其他类型请求，返回一个同样的表单也无妨
    if request.method != 'POST':
        # 未提交数据：仅使用当前条目填充表单
        form = EntryForm(instance=entry)  # 使用instance=entry创建EntryForm()实例，并将其存储到变量form中
    # 而POST请求是用户填写完表单提交，需要保存表单，并将表单内容添加到特定主题的条目页中显示
    else:
        # POST提交的数据，对数据进行处理
        form = EntryForm(instance=entry, data=request.POST)  # 使用instance=entry创建EntryForm()实例，再使用request.POST中的相关数据进行修改
        if form.is_valid():  # 自动验证用户填写了所有必不可少的字典，且输入数据与要求字段类型一致
            form.save()  # 将已修改号的条目对象保存到数据库
            # HttpResponseRedirect()：将用户重定向到特定主题条目页中
            return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic.id]))  # reverse()根据指定的URL模型确定URL
    # 将原条目表单添加到上下文字典中
    context = {'entry': entry, 'topic': topic, 'form': form}
    # render()根据视图提供的数据渲染响应，参数：原始请求对象、可用于创建网页的模板
    return render(request, 'learning_logs/edit_entry.html', context)
