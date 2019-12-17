from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class UserProfile(models.Model):
    """用户信息表"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # 关联Django的用户验证表
    name = models.CharField(max_length=32, verbose_name="full name")
    role = models.ManyToManyField('Role')

    def __str__(self):  # _unicode
        return self.name


class Role(models.Model):
    """角色表"""
    name = models.CharField(max_length=64, unique=True)
    menus = models.ManyToManyField('Menus', blank=True)

    def __str__(self):
        return self.name


class CustomerInfo(models.Model):
    """客户信息表"""
    name = models.CharField(max_length=64, default=None)
    phone = models.CharField(max_length=32, unique=True)
    address = models.TextField(verbose_name='邮寄地址')
    wechat_or_other = models.CharField(max_length=64, blank=True, null=True)
    source_choices = (
        (0, '转介绍'),
        (1, 'Google'),
        (2, 'Facebook'),
        (3, 'Twitter'),
        (4, 'Wechat'),
        (5, 'Other'),
    )
    source = models.SmallIntegerField(choices=source_choices, verbose_name='客户来源')
    referral_from = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE)
    consult_course = models.ManyToManyField('Course', verbose_name='咨询课程')
    consult_Details = models.TextField(verbose_name='咨询详情')
    cunsultant = models.ForeignKey('UserProfile', verbose_name='咨询顾问', on_delete=models.CASCADE)
    status_choices = (
        (0, '未报名'),
        (1, '待咨询'),
        (2, '待确认'),
        (3, '已报名'),
        (4, '已退费'),
        (5, '已退费'),
    )
    status = models.SmallIntegerField(choices=status_choices, verbose_name='报名状态')
    date = models.DateTimeField(auto_now_add=True, verbose_name='录入时间')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = '客户信息表：CustomerInfo'
        verbose_name = '客户信息表：CustomerInfo'


class Student(models.Model):
    """学院表"""
    customer = models.OneToOneField('CustomerInfo', on_delete=models.CASCADE)
    class_grades = models.ManyToManyField('ClassList')

    def __str__(self):
        return self.customer


class CustomerFollowUp(models.Model):
    """客户跟踪记录表"""
    customer = models.ForeignKey('CustomerInfo', on_delete=models.CASCADE)
    content = models.TextField(verbose_name='跟踪内容')
    user = models.ForeignKey('UserProfile', verbose_name='跟踪客户', on_delete=models.CASCADE)
    status_choices = (
        (0, '无报名几乎'),
        (1, '近期报名'),
        (2, '今年内报名'),
        (0, '还需考虑'),
        (0, '已报名'),
        (0, '不准备报名'),
    )
    status = models.SmallIntegerField(choices=status_choices, verbose_name='报名状态')

    def __str__(self):
        return self.content


class Course(models.Model):
    """课程表"""
    name = models.CharField(max_length=64, unique=True, verbose_name='课程名称')
    price = models.PositiveIntegerField(verbose_name='课程价格')
    period = models.PositiveSmallIntegerField(verbose_name='周期(月)', default=5)
    outline = models.TextField(verbose_name='课程大纲')

    def __str__(self):
        return self.name


class ClassList(models.Model):
    """班级列表"""
    branch = models.ForeignKey('Branch', on_delete=models.CASCADE)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    class_type_choices = (
        (0, '平日班'),
        (1, '周末班'),
        (2, '网络班'),
    )
    class_type = models.SmallIntegerField(choices=class_type_choices, default=1)
    semester = models.PositiveSmallIntegerField(verbose_name='学期')
    branch = models.ForeignKey('Branch', on_delete=models.CASCADE)
    contract_template = models.ForeignKey('ContractTemplate', on_delete=models.CASCADE, blank=True, null=True)
    Teacher = models.ManyToManyField('UserProfile')
    start_date = models.DateField(verbose_name=u'开课日期')
    graduate_date = models.DateField(blank=True, null=True, verbose_name='毕业日期')

    def __str__(self):
        return '{}{}期'.format(self.course, self.semester)

    class Meta:
        unique_together = ('course', 'semester', 'branch', 'class_type')


class CourseRecord(models.Model):
    """上课记录"""
    class_grade = models.ForeignKey('ClassList', on_delete=models.CASCADE, verbose_name='记录班级')
    day_number = models.PositiveSmallIntegerField(verbose_name='课程节次')
    teacher = models.ForeignKey('UserProfile', on_delete=models.CASCADE, verbose_name='讲师')
    title = models.CharField(max_length=64, verbose_name='本节课主题')
    content = models.TextField(verbose_name='课程内容')
    has_home = models.BooleanField(verbose_name='是否有作业', default=False)
    homework = models.TextField(verbose_name='作业')
    date = models.DateTimeField(auto_now_add=True, verbose_name='上课时间')

    def __str__(self):
        return '%s第(%s)节'.format(self.class_grade, self.day_number)

    class Meta:
        unique_together = ('class_grade', 'day_number')


class StudyRecord(models.Model):
    """学习记录"""
    course_record = models.ForeignKey('CourseRecord', on_delete=models.CASCADE, verbose_name='课程记录')
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    score_choices = (
        (100, 'A+'),
        (95, 'A'),
        (90, 'B+'),
        (85, 'B'),
        (80, 'A-'),
        (75, 'C+'),
        (70, 'C'),
        (60, 'C-'),
        (0, 'D'),
        (-50, 'E'),
        (-100, 'F'),
    )
    score = models.SmallIntegerField(choices=score_choices, default=0, verbose_name='分数')
    show_status_choices = (
        (0, '缺勤'),
        (1, '已签到'),
        (2, '迟到'),
        (3, '早退'),
    )
    show_status = models.SmallIntegerField(choices=show_status_choices, default=1, verbose_name='出勤情况')
    note = models.TextField(verbose_name='备注')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}{}{}'.format(self.course_record, self.student, self.score)


class Branch(models.Model):
    """分机构校区"""
    name = models.CharField(max_length=64, verbose_name='校区', unique=True)
    phone = models.CharField(max_length=64, verbose_name='联系电话', blank=True, null=True)
    address = models.CharField(max_length=128, verbose_name='地址')

    def __str__(self):
        return self.name


class Menus(models.Model):
    name = models.CharField(max_length=64)
    url_type_choices = (
        (0, 'absolute'),
        (1, 'dynamic'),
    )
    url_type = models.SmallIntegerField(choices=url_type_choices, verbose_name='URL类型', default=0)
    url = models.CharField(max_length=128)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('name', 'url')
        verbose_name_plural = '目录表  Menus'


class ContractTemplate(models.Model):
    """合同模板存储表"""
    name = models.CharField(max_length=64)
    content = models.TextField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


class StudentEnrollment(models.Model):
    """学生报名表"""
    customer = models.ForeignKey('CustomerInfo', on_delete=models.CASCADE)
    consulant = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
    class_grade = models.ForeignKey('ClassList', on_delete=models.CASCADE)
    contract_agreed = models.BooleanField(default=False)
    contract_sign_date = models.DateTimeField(blank=True, null=True, verbose_name='合同签署时间')
    contract_approved = models.BooleanField(default=False)
    approved_date = models.DateTimeField(blank=True, null=True, verbose_name='合同审核时间')

    def __str__(self):
        return self.customer

class PaymentRecord(models.Model):
    """缴费记录表"""
    enrollment = models.ForeignKey('StudentEnrollment',on_delete=models.CASCADE)
    payment_type_choices = ((0,'报名费'),(1,'学费'),(2,'退费'))
    payment_type = models.IntegerField(choices=payment_type_choices,default=0)
    consultant = models.ForeignKey('UserProfile',on_delete=models.CASCADE)
    amount = models.IntegerField(verbose_name='费用',default=500)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.amount