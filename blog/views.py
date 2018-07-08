from django.shortcuts import render, HttpResponse, redirect
from blog import forms
from django.contrib import auth
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


# 登录
def login(request):
    form_obj = forms.LoginForm()
    if request.method == "POST":
        ret = {"code": 0}
        username = request.POST.get("username")
        password = request.POST.get("password")
        v_code = request.POST.get("v_code", "")

        if v_code.upper() == request.session.get("v_code", ""):
            # 验证码正确,再验证用户输入的有效性
            user = auth.authenticate(username=username, password=password)
            if user:
                # 用户名密码正确
                auth.login(request, user)
                ret["data"] = "/index/"
            else:
                # 用户名或密码错误
                ret["code"] = 1
                ret["data"] = "用户名或密码错误"
        else:
            # 验证码错误
            ret["code"] = 1
            ret["data"] = "验证码错误"
        return JsonResponse(ret)
    return render(request, "login.html", {"form_obj": form_obj})


from PIL import Image, ImageDraw, ImageFont
import random
from . import models


# 图片验证码
def v_code(request):
    # 定义一个生成随机颜色代码的内部函数
    def get_color():
        return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)

    # 生成一个图片对象
    img_obj = Image.new(
        "RGB",
        (250, 35),
        color=get_color()
    )

    # 在图片中加文字
    # 生成一个画笔对象
    draw_obj = ImageDraw.Draw(img_obj)
    # 加载字体文件
    font_obj = ImageFont.truetype("static/courbi.ttf", size=28)
    # 写字
    # draw_obj.text(
    #     (0, 0),  # 位置
    #     "A",  # 内容
    #     (0,0,0),  # 颜色
    #     font=font_obj
    # )

    # for循环5次，每次写一个随机的字符
    tmp_list = []
    for i in range(5):
        n = str(random.randint(0, 9))
        l = chr(random.randint(97, 122))
        u = chr(random.randint(65, 90))
        r = random.choice([n, l, u])
        tmp_list.append(r)
        draw_obj.text(
            (i * 48 + 20, 0),  # 位置
            r,  # 内容
            get_color(),  # 颜色
            font=font_obj
        )
    # 得到生成的随机
    v_code_str = "".join(tmp_list)
    # 注意： 不能使用全局变量保存验证码，会被覆盖
    request.session["v_code"] = v_code_str.upper()

    # 加干扰线
    width = 250  # 图片宽度（防止越界）
    height = 35
    for i in range(5):
        x1 = random.randint(0, width)
        x2 = random.randint(0, width)
        y1 = random.randint(0, height)
        y2 = random.randint(0, height)
        draw_obj.line((x1, y1, x2, y2), fill=get_color())

    # 加干扰点
    for i in range(5):
        draw_obj.point([random.randint(0, width), random.randint(0, height)], fill=get_color())
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw_obj.arc((x, y, x + 4, y + 4), 0, 90, fill=get_color())

    # 第一版： 将生成的图片保存到文件中
    # with open("xx.png", "wb") as f:
    #     img_obj.save(f, "png")
    # print("图片已经生成！")
    # with open("xx.png", "rb") as f:
    #     return HttpResponse(data, content_type="image/png")

    # 第二版：直接将图片在内存中保存
    from io import BytesIO
    tmp = BytesIO()  # 生成一个io对象
    img_obj.save(tmp, "png")

    data = tmp.getvalue()
    return HttpResponse(data, content_type="image/png")


# 首页
def index(request):
    article_list = models.Article.objects.all()
    total_num = article_list.count()
    current_page = request.GET.get("page")
    from utils import my_pagination
    url_prefix = request.path_info.strip('/')  # 去掉路由前缀两边的"/"
    page_obj = my_pagination.Pagination(total_num, current_page, url_prefix, per_page_data_num=2)
    article_list = article_list[page_obj.data_start:page_obj.data_end]
    page_html = page_obj.page_tool_html()
    return render(
        request,
        "index.html",
        {
            "article_list": article_list,
            "page_html": page_html
        }
    )


# 注册
def register(request):
    if request.method == "POST":
        ret = {"code": 0}
        form_obj = forms.RegisterForm(request.POST)
        if form_obj.is_valid():
            # 用户数据经过校验，没问题
            # 进一步获取头像数据
            avatar_obj = request.FILES.get("avatar")
            print(avatar_obj)
            # 创建用户
            form_obj.cleaned_data.pop("re_password", "")
            models.UserInfo.objects.create_user(
                avatar=avatar_obj,
                **form_obj.cleaned_data
            )
            # 创建用户成功后，跳转登陆页面
            ret["data"] = "/login/"
        else:
            # 用户数据校验失败
            ret["code"] = 1
            ret["data"] = form_obj.errors
        return JsonResponse(ret)

    form_obj = forms.RegisterForm()
    return render(request, "register.html", {"forms_obj": form_obj})


# 注销
def logout(request):
    auth.logout(request)
    return redirect("/login/")


# 个人主页
def home(request, username, *args):
    """
    点击文章作者名，跳转至个人主页
    :param request: 请求对象
    :param username: 用户名
    :return:
    """
    # 去数据库中，根据用户名去找所有文章
    user_obj = models.UserInfo.objects.filter(username=username).first()  # QuerySet()对象转化为对象

    if not user_obj:
        # 无此用户
        return HttpResponse("无此用户")
    else:
        # 找到合法用户
        # 找到该用户的博客属性:提取博客标题，博客主题
        blog = user_obj.blog

    # 左侧面板数据

    # # 分类筛选
    # # category_list = models.Category.objects.filter(blog=blog)
    # # 进一步找到该分类中的文章数目
    # from django.db.models import Count
    # category_list = models.Category.objects.filter(blog=blog).annotate(
    #     num=Count("article")).values("title", "num")
    #
    # # 标签分类
    # tag_list = models.Tag.objects.filter(blog=blog).annotate(
    #     num=Count("article")).values("title", "num")
    #
    # # 日期分类
    # archive = models.Article.objects.filter(user=user_obj).extra(
    #     select={
    #         "year_month": "DATE_FORMAT(create_time,'%%Y-%%m')"}).values(
    #     "year_month").annotate(num=Count("nid")).values("year_month","num")

    # 按分类筛选取数据
    if not args:
        # 找到此用户博客中的所有文章
        article_list = models.Article.objects.filter(user__username=username)
    else:

        if args[0] == "category":
            article_list = models.Article.objects.filter(category__title=args[1])
        elif args[0] == "tag":
            article_list = models.Article.objects.filter(tags__title=args[1])
        else:
            year, month = args[1].split("-")
            article_list = models.Article.objects.filter(create_time__year=year, create_time__month=month)

    total_num = article_list.count()
    current_page = request.GET.get("page")
    from utils import my_pagination
    url_prefix = request.path_info.strip('/')  # 去掉路由前缀两边的"/"
    page_obj = my_pagination.Pagination(total_num, current_page, url_prefix, per_page_data_num=1)
    article_list = article_list[page_obj.data_start:page_obj.data_end]
    page_html = page_obj.page_tool_html()

    return render(
        request,
        "home.html",
        {
            "username": username,
            "blog": blog,
            "article_list": article_list,
            "page_html": page_html
        }
    )


# 文章详情
def article_detail(request, username, article_nid):
    """
    文章详情视图
    :param request: 请求对象
    :param username: 用户名
    :param article_nid: 文章唯一ID值
    :return:
    """
    user_obj = models.UserInfo.objects.filter(username=username).first()
    if not user_obj:
        return HttpResponse(404)
    article_obj = models.Article.objects.filter(user=user_obj, nid=article_nid).first()
    blog = user_obj.blog

    # 评论列表返回
    comment_list = models.Comment.objects.filter(article__nid=article_nid)

    return render(
        request,
        "article_detail.html",
        {
            "username": username,
            "blog": blog,
            "article": article_obj,
            "comment_list": comment_list
        }
    )


# 点赞/踩灭
def updown(request):
    ret = {"code": 0}  # 0 正常操作 1 有误操作
    is_up = request.POST.get("is_up")
    article_id = request.POST.get("article_id")
    user_id = request.POST.get("user_id")
    # 数据库中is_up为布尔型，而从请求体中取到的值为字符串，故需要转换类型
    is_up = True if is_up.upper() == "TRUE" else False
    print(is_up, article_id, user_id)

    is_author = models.Article.objects.filter(user_id=user_id, nid=article_id)
    if is_author:
        # 文章作者不可以操作点赞/踩灭
        ret["code"] = 1
        ret["tip"] = "不可以给自己的内容点赞" if is_up else "不可以给自己的内容踩灭"

    else:
        is_exist = models.ArticleUpDown.objects.filter(
            user_id=user_id,
            article_id=article_id
        ).first()
        if is_exist:
            # 已经操作过一次的用户不能继续操作
            ret["code"] = 1
            ret["tip"] = "你已经点赞过" if is_exist.is_up else "你已经踩灭过"
        else:
            from django.db.models import F
            from django.db import transaction

            try:
                with transaction.atomic():
                    # 1、创建一条点赞/踩灭记录
                    models.ArticleUpDown.objects.create(
                        is_up=is_up,
                        article_id=article_id,
                        user_id=user_id
                    )

                    # 2、更新文章表中相对应的数据
                    if is_up:
                        models.Article.objects.filter(nid=article_id).update(up_count=F("up_count") + 1)
                    else:
                        models.Article.objects.filter(nid=article_id).update(up_count=F("down_count") + 1)

                    # 3、点赞/踩灭反馈信息，tip
                    ret["tip"] = "点赞！" if is_up else "反对！"
            except Exception as e:
                print(str(e))
    return JsonResponse(ret)


# 提交评论
def comment_commit(request):
    ret = {"code": 0}
    floor_num = request.POST.get("floor_num", "")
    username = request.POST.get("username", "")
    article_id = request.POST.get("article_id", "")
    user_id = request.POST.get("user_id", "")
    content = request.POST.get("content", "")

    # 创建一条新评论记录
    models.Comment.objects.create(
        article_id=article_id,
        user_id=user_id,
        content=content
    )

    cur_comment_obj = models.Comment.objects.last()

    from utils import comment_generator
    comment_obj = comment_generator.CommentGenerator(
        floor_num=floor_num,
        username=username,
        create_time=cur_comment_obj.create_time.strftime('%Y-%m-%d %X'),
        content=content,
        parent_comment=cur_comment_obj.parent_comment
    )
    if comment_obj:
        coment_html = comment_obj.page_html()
        ret["code"] = 1
        ret["comment_html"] = coment_html
    return JsonResponse(ret)
