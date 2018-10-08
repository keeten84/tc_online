from django.db.models import Q
from django.http import HttpResponse
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.views.generic.base import View
from course.models import Course, Video, CourseResource
from operation.models import UserFavorite, CourseComments, UserCourse
from utils.mixin_utils import LoginRequiredMixin


# 视频播放页面
class VideoPlayView(LoginRequiredMixin,View):
    def get(self, request, video_id):
        video = Video.objects.get(id=int(video_id))
        course = video.lesson.course
        all_resources = CourseResource.objects.filter(course=course)

        # 查询用户点击开始学习之后就绑定课程，关联了以后以便在推荐课程中返回已绑定课程
        user_courses = UserCourse.objects.filter(course=course)
        if not user_courses:
            user_course = UserCourse(user=request.user,course=course)
            user_course.save()

        # 页面中'该同学还学过其他什么课程'的业务逻辑流程如下
        # 第一，查找出学过这门课程的同学有哪些
        user_courses = UserCourse.objects.filter(course=course)
        # 第二，通过上面查找出来的数据，然后从数据中获取出学过这门课程的用户ID
        user_ids = [user_course.user.id for user_course in user_courses]
        # 第三，根据上面遍历出来的用户id，查找出每一个用户学过的所有课程，user_id__in的意思是传进入一个列表
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 第四，根据查找出来的课程，遍历出所有课程的ID
        course_ids = [user_course.user.id for user_course in all_user_courses]
        # 第五，获取学过该用户学过的其他所有课程里面的前5个
        relate_courses = Course.objects.filter(id__in = course_ids).order_by('-click_nums')[:5]

        return render(request, 'course-play.html', {
            'course': course,
            'course_resources':all_resources,
            'relate_courses':relate_courses,
            'video': video,

        })



# 添加课程评论，继承utils里面的LoginRequiredMixin类，继承之后提前对用户登录做验证，没有登录的跳转到登录页面
class AddCommentsView(View):
    def post(self,request):
        if not request.user.is_authenticated:
            # 判断用户登录情况
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')

        course_id = request.POST.get('course_id',0)
        comments = request.POST.get('comments','')
        if int(course_id) > 0 and comments:
            course_comments = CourseComments()
            course = Course.objects.get(id = int(course_id))
            course_comments.user = request.user
            course_comments.course = course
            course_comments.comment = comments

            course_comments.save()
            return HttpResponse('{"status":"success", "msg":"添加成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"添加失败"}', content_type='application/json')


# 课程评论页面，继承utils里面的LoginRequiredMixin类，继承之后提前对用户登录做验证，没有登录的跳转到登录页面
class CourseCommentView(LoginRequiredMixin,View):
    def get(self,request,course_id):
        course = Course.objects.get(id=int(course_id))
        all_resources = CourseResource.objects.filter(course=course)
        all_comments = CourseComments.objects.filter(course = course)

        # 页面中'该同学还学过其他什么课程'的业务逻辑流程如下
        # 第一，查找出学过这门课程的同学有哪些
        user_courses = UserCourse.objects.filter(course=course)
        # 第二，通过上面查找出来的数据，然后从数据中获取出学过这门课程的用户ID
        user_ids = [user_course.user.id for user_course in user_courses]
        # 第三，根据上面遍历出来的用户id，查找出每一个用户学过的所有课程，user_id__in的意思是传进入一个列表
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 第四，根据查找出来的课程，遍历出所有课程的ID
        course_ids = [user_course.user.id for user_course in all_user_courses]
        # 第五，获取学过该用户学过的其他所有课程里面的前5个
        relate_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:5]


        return render(request,'course-comment.html',{
            'course':course,
            'course_resources':all_resources,
            'all_comments':all_comments,
            'relate_courses': relate_courses,
        })


# 课程视频详情页
class CourseInfoView(LoginRequiredMixin,View):
    def get(self, request, course_id):
        # 先查找出该课程的数据
        course = Course.objects.get(id=int(course_id))
        course.students += 1
        course.save()
        # 查询用户点击开始学习之后就绑定课程，关联了以后以便在推荐课程中返回已绑定课程
        user_courses = UserCourse.objects.filter(course=course)
        if not user_courses:
            user_course = UserCourse(user=request.user,course=course)
            user_course.save()


        # 页面中'该同学还学过其他什么课程'的业务逻辑流程如下
        # 第一，查找出学过这门课程的同学有哪些
        user_courses = UserCourse.objects.filter(course=course)
        # 第二，通过上面查找出来的数据，然后从数据中获取出学过这门课程的用户ID
        user_ids = [user_course.user.id for user_course in user_courses]
        # 第三，根据上面遍历出来的用户id，查找出每一个用户学过的所有课程，user_id__in的意思是传进入一个列表
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 第四，根据查找出来的课程，遍历出所有课程的ID
        course_ids = [user_course.user.id for user_course in all_user_courses]
        # 第五，获取学过该用户学过的其他所有课程里面的前5个
        relate_courses = Course.objects.filter(id__in = course_ids).order_by('-click_nums')[:5]


        # 获取下载资源列表用于展示课程下载资源
        all_resources = CourseResource.objects.filter(course = course)
        return render(request, 'course-video.html', {
            'course': course,
            'course_resources':all_resources,
            'relate_courses':relate_courses,

        })


# 课程详情页
class CourseDetailView(View):
    def get(self, request, course_id):
        # 提出课程数据
        course = Course.objects.get(id=int(course_id))
        # 增加课程的点击数，只要点击进入课程详情页，就自动添加一次
        course.click_nums += 1
        course.save()

        # 收藏功能，将数据返回前端展示是否已经收藏课程或者机构
        has_fav_course = False
        has_fav_org = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_id, fav_type=1):
                has_fav_course = True

            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                has_fav_org = True

        tag = course.tag
        if tag:
            relate_courses = Course.objects.filter(tag=tag)[:1]
        else:
            relate_courses = []

        return render(request, 'course-detail.html', {
            'course': course,
            'relate_courses': relate_courses,
            'has_fav_course': has_fav_course,
            'has_fav_org': has_fav_org,

        })


# 课程列表页
class CourseListView(View):
    def get(self, request):
        current_nav = 'course'
        all_course = Course.objects.all().order_by('-add_time')

        hot_course = all_course.order_by('-click_nums')[:3]
        course_nums = all_course.count()

        # 页面中搜索栏的搜索功能
        search_keywords = request.GET.get('keywords','')
        if search_keywords:
            # 从所有课程中搜索, 使用__icontains就会相当于在数据库中使用like语句
            all_course = all_course.filter(Q(name__icontains=search_keywords)|Q(desc__icontains=search_keywords)|Q(detail__icontains=search_keywords))



        # 课程排序功能的逻辑
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'students':
                all_course = all_course.order_by('-students')
            elif sort == 'hot':
                all_course = all_course.order_by('-click_nums')

        # 课程分页功能的逻辑代码
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_course, 6, request=request)
        courses = p.page(page)

        return render(request, 'course-list.html', {
            'all_course': courses,
            'course_nums': course_nums,
            'sort': sort,
            'hot_course': hot_course,
            'current_nav':current_nav,
        })
