from django.core.serializers import json
from django.db.models import Q
from django.shortcuts import render
from django.views.generic.base import View

from course.models import Course
from operation.models import UserFavorite
from organization.models import CourseOrg, CityDict, Teacher
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from .forms import UserAskForm
from django.http import HttpResponse
from django.contrib.auth import authenticate


class TeacherDetail(View):
    def get(self,request,teacher_id):
        # 获取讲师的数据
        teacher = Teacher.objects.get(id=int(teacher_id))

        # 通过老师的id从course外键中获取该老师教的教程
        relate_courses = Course.objects.filter(teacher = teacher_id)

        # 进入教师详情页面，该教师的点击数就自动增加点击次数
        teacher.click_nums += 1
        teacher.save()

        # 收藏逻辑
        has_teracher_fav = False
        has_org_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=teacher.id, fav_type=3):
                has_teracher_fav = True
            if UserFavorite.objects.filter(user=request.user, fav_id=teacher.org.id, fav_type=2):
                has_org_fav = True

        # 热门讲师排行榜逻辑
        golden_teachers = Teacher.objects.all().order_by('-click_nums')[:5]

        return render(request,'teacher-detail.html',{
            'teacher':teacher,
            'golden_teachers':golden_teachers,
            'relate_courses':relate_courses,
            'has_teacher_fav':has_teracher_fav,
            'has_org_fav':has_org_fav,
        })



class TeacherList(View):
    '''课程讲师列表页'''
    def get(self,request):
        all_teachers = Teacher.objects.all()

        # 页面中搜索栏的搜索功能
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            # 从所有课程中搜索, 使用__icontains就会相当于在数据库中使用like语句
            all_teachers = all_teachers.filter(Q(name__icontains=search_keywords) |
                                               Q(work_company__icontains=search_keywords)|
                                               Q(work_position__icontains=search_keywords))


        # 人气排行的逻辑
        sort = request.GET.get('sort', '')
        if sort:
            if sort == '':
                all_teachers = Teacher.objects.all().order_by('add_time')
            elif sort == 'hot':
                all_teachers = Teacher.objects.all().order_by('-click_nums')

        # 金牌讲师推荐逻辑
        golden_teachers = Teacher.objects.all().order_by('-click_nums')[:5]


        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # 第一个参数传需要做分页的列表，第二个参数是每页显示的列表数量，第三个固定为request
        p = Paginator(all_teachers, 6, request=request)
        teachers = p.page(page)

        return render(request,'teachers-list.html',{
            'all_teachers': teachers,
            'golden_teachers': golden_teachers,
            'sort':sort,
        })


class AddFavView(View):
    '''用户收藏功能'''
    def post(self, request):
        # 从前端获取收藏id和收藏类型
        fav_id = request.POST.get('fav_id', 0)
        fav_type = request.POST.get('fav_type', '')
        # 判断用户是否已经登录，如果没有登录
        if not request.user.is_authenticated:
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')

        exist_records = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))
        if exist_records:
            # 如果记录已经存在，则表示用户取消记录
            exist_records.delete()
            # 取消收藏同时也取消数据库中相对应的收藏数量
            if int(fav_type) == 1:
                course = Course.objects.get(id=int(fav_id))
                course.fav_nums -= 1
                # 当等于0的时候在减操作会出现负数，避免这个情况的解决方法
                if course.fav_nums < 0 :
                    course.fav_nums = 0
                course.save()

            elif int(fav_type) == 2:
                course_org = CourseOrg.objects.get(id=int(fav_id))
                course_org.fav_nums -= 1
                if course_org.fav_nums < 0 :
                    course_org.fav_nums = 0
                course_org.save()

            elif int(fav_type)== 3:
                teacher = Teacher.objects.get(id=int(fav_id))
                teacher.fav_nums -= 1
                if teacher.fav_nums < 0 :
                    teacher.fav_nums = 0
                teacher.save()
            return HttpResponse('{"status":"success", "msg":"收藏"}', content_type='application/json')
        else:
            # 如果没有收藏记录，实例化收藏的表
            user_fav = UserFavorite()
            # 判断2个参数必须大于0，并保存收藏结果，返回收藏成功
            if int(fav_id) > 0 and int(fav_type) > 0:
                user_fav.user = request.user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.save()
                # 收藏同时也取消数据库中相对应的收藏数量
                if int(fav_type) == 1:
                    course = Course.objects.get(id=int(fav_id))
                    course.fav_nums += 1
                    course.save()

                elif int(fav_type) == 2:
                    course_org = CourseOrg.objects.get(id=int(fav_id))
                    course_org.fav_nums += 1
                    course_org.save()

                elif int(fav_type) == 3:
                    teacher = Teacher.objects.get(id=int(fav_id))
                    teacher.fav_nums += 1
                    teacher.save()

                return HttpResponse('{"status":"success", "msg":"收藏成功"}', content_type='application/json')
            # 如果其他数据，返回收藏错误
            else:
                return HttpResponse('{"status":"fail", "msg":"收藏出错"}', content_type='application/json')


class OrgTeacherView(View):
    '''机构介绍页'''

    def get(self, request, org_id):
        # 用于返回前端，用于判断当前是那个页面
        current_page = 'teacher'
        course_org = CourseOrg.objects.get(id=int(org_id))
        # 判断用户是否已经收藏
        has_fav = False
        # 如果用户查询到数据库中已经有该数据，就返回True
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        # course_org下有一个外键指向course，django通过course_org的实例里面的course_set方法可以反向查找出对应的数据
        all_courses = course_org.course_set.all()
        all_teachers = course_org.teacher_set.all()
        return render(request, 'org-detail-teachers.html', {
            'all_courses': all_courses,
            'all_teachers': all_teachers,
            'course_org': course_org,
            'current_page': current_page,
            'has_fav':has_fav,
        })


class OrgDescView(View):
    '''机构介绍页'''

    def get(self, request, org_id):
        # 用于返回前端，用于判断当前是那个页面
        current_page = 'desc'
        course_org = CourseOrg.objects.get(id=int(org_id))
        # 判断用户是否已经收藏
        has_fav = False
        # 如果用户查询到数据库中已经有该数据，就返回True
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        # course_org下有一个外键指向course，django通过course_org的实例里面的course_set方法可以反向查找出对应的数据
        all_courses = course_org.course_set.all()
        return render(request, 'org-detail-desc.html', {
            'all_courses': all_courses,
            'course_org': course_org,
            'current_page': current_page,
            'has_fav':has_fav
        })


class OrgCourseView(View):
    '''机构课程列表页'''

    def get(self, request, org_id):
        # 用于返回前端，用于判断当前是那个页面
        current_page = 'course'
        course_org = CourseOrg.objects.get(id=int(org_id))
        # 判断用户是否已经收藏
        has_fav = False
        # 如果用户查询到数据库中已经有该数据，就返回True
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        # course_org下有一个外键指向course，django通过course_org的实例里面的course_set方法可以反向查找出对应的数据
        all_courses = course_org.course_set.all()
        return render(request, 'org-detail-course.html', {
            'all_courses': all_courses,
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav,
        })


class OrgHomeView(View):
    '''机构首页'''

    def get(self, request, org_id):
        current_page = 'home'
        course_org = CourseOrg.objects.get(id=int(org_id))

        # 点击进入课程点击率加1
        course_org.click_nums += 1
        course_org.save()

        # 判断用户是否已经收藏
        has_fav = False
        # 如果用户查询到数据库中已经有该数据，就返回True
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        # course_org下有一个外键指向course，django通过course_org的实例里面的course_set方法可以反向查找出对应的数据
        all_courses = course_org.course_set.all()[:3]
        all_teachers = course_org.teacher_set.all()[:1]
        return render(request, 'org-detail-homepage.html', {
            'all_courses': all_courses,
            'all_teachers': all_teachers,
            'course_org': course_org,
            'current_page': current_page,
            'has_fav' : has_fav,
        })


# 用户添加咨询
class AddUserAskView(View):
    '''
    处理org/list页面下的"我要学习"的业务逻辑，比较合理的操作是异步的，不会对整个页面进行刷新。
    如果有错误，显示错误。一种ajax的异步操作。因此我们此时不能直接render一个页面回来。应该是给前端返回json数据，而不是页面
    HttpResponse 类指明给用户返回哪种类型数据
    '''

    # 由于是提交表单，所以只需要重写post请求，另外前端页面记得在表单前写{% crsf_token %},否则无法提交表单
    def post(self, request):
        userask_form = UserAskForm(request.POST)
        ret = {'status': True, 'error': None, 'data': None}
        # 判断该form是否有效
        if userask_form.is_valid():
            # 这里是modelform和form的区别，当保存当时候需要添加commit为true进行真正保存，这样就不需要把一个一个字段取出来然后存到model的对象中之后save
            user_ask = userask_form.save(commit=True)
            # 如果保存成功,返回json字符串,后面content type是告诉浏览器的用什么格式当数据
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            # 如果保存失败，返回json字符串,并将form的报错信息通过msg传递到前端
            return HttpResponse('{"status":"fail", "msg":"添加出错"}', content_type='application/json')


class OrgView(View):
    '''课程机构列表功能'''

    def get(self, request):
        # 获取所有课程机构，用于返回课程机构列表分页时候使用
        all_ogrs = CourseOrg.objects.all()
        # 热门授课机构排名逻辑
        hot_ogrs = all_ogrs.order_by('-click_nums')[:3]
        # 获取所有城市的列表，用于返回前端城市列表的时候使用
        all_citys = CityDict.objects.all()

        # 页面中搜索栏的搜索功能
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            # 从所有课程中搜索, 使用__icontains就会相当于在数据库中使用like语句
            all_ogrs = all_ogrs.filter(Q(name__icontains=search_keywords) | Q(desc__icontains=search_keywords))



        # 从前端获取city字段的id值，用于根据点击前端页面城市列表时候返回该城市的培训机构的列表
        city_id = request.GET.get('city', '')
        # 从数据库中根据前端的city_id去数据库中匹配所有符合的数据，并用于返回到列表分页
        if city_id:
            all_ogrs = all_ogrs.filter(city_id=int(city_id))

        # 类别筛选逻辑
        category = request.GET.get('ct', '')
        if category:
            all_ogrs = all_ogrs.filter(category=category)

        # 排序功能的逻辑
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'students':
                all_ogrs = all_ogrs.order_by('-students')
            elif sort == 'courses':
                all_ogrs = all_ogrs.order_by('-course_nums')

        # 全部筛选逻辑后再获取机构的总数量，待页面返回的时候使用
        org_nums = all_ogrs.count()

        # 对课程机构列利用第三方包pure-pagination进行分页，详细用法参考该git里面的使用教程
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # 第一个参数传需要做分页的列表，第二个参数是每页显示的列表数量，第三个固定为request
        p = Paginator(all_ogrs, 4, request=request)
        orgs = p.page(page)
        # 将数据返回到前端页面
        return render(request, 'org-list.html', {
            'all_orgs': orgs,
            'all_citys': all_citys,
            'org_nums': org_nums,
            'city_id': city_id,
            'category': category,
            'hot_orgs': hot_ogrs,
            'sort': sort,

        })

    def post(self, request):
        pass
