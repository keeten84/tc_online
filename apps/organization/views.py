from django.core.serializers import json
from django.shortcuts import render
from django.views.generic.base import View
from organization.models import CourseOrg, CityDict
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from .forms import UserAskForm
from django.http import HttpResponse
from course.models import Course


class OrgHomeView(View):
    '''机构首页'''

    def get(self, request, org_id):
        course_org = CourseOrg.objects.get(id=int(org_id))
        # course_org下有一个外键指向course，django通过course_org的实例里面的course_set方法可以反向查找出对应的数据
        all_courses = course_org.course_set.all()[:3]
        all_teachers = course_org.teacher_set.all()[:1]
        return render(request, 'org-detail-homepage.html', {
            'all_courses': all_courses,
            'all_teachers': all_teachers,
            'course_org' : course_org,
        })


# 处理org/list页面下的"我要学习"的业务逻辑，比较合理的操作是异步的，不会对整个页面进行刷新。
# 如果有错误，显示错误。一种ajax的异步操作。因此我们此时不能直接render一个页面回来。应该是给前端返回json数据，而不是页面
# HttpResponse 类指明给用户返回哪种类型数据
class AddUserAskView(View):
    '''用户添加咨询'''

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


#


class OrgView(View):
    '''课程机构列表功能'''

    def get(self, request):
        # 获取所有课程机构，用于返回课程机构列表分页时候使用
        all_ogrs = CourseOrg.objects.all()
        # 热门授课机构排名逻辑
        hot_ogrs = all_ogrs.order_by('-click_nums')[:3]
        # 获取所有城市的列表，用于返回前端城市列表的时候使用
        all_citys = CityDict.objects.all()
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
