from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)


# Create your models here.
class UserProfileManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            name=name,
        )
        user.is_admin = True
        user.is_active = True
        user.save(using=self._db)
        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=32, help_text="add update")
    password = models.CharField(_('password'), max_length=128, help_text=mark_safe("<a href='password/'>密码修改</a>"))
    roles = models.ManyToManyField('Role', blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class Customer(models.Model):
    """
    客户表
    max_length=32 为字节单位，utf8格式的中文，一个汉字为3个字节，所以最多存储10个汉字
    blank=True 用于Django_admin中可以为空
    """
    name = models.CharField(max_length=32, null=True, blank=True)
    qq = models.CharField(max_length=64, null=False, unique=True)
    qq_name = models.CharField(max_length=64, null=True, blank=True)
    phone = models.CharField(max_length=64, null=True, blank=True)
    source_choices = (
        (0, "转介绍"),
        (1, 'QQ群'),
        (2, '官网'),
        (3, '百度推广'),
        (4, '51CTO'),
        (5, '知乎'),
        (6, '市场推广')
    )
    source = models.SmallIntegerField(choices=source_choices)
    referral_from = models.CharField(max_length=64, verbose_name="转介绍人", null=True, blank=True)
    consult_course = models.ForeignKey("Course", verbose_name="咨询的课程")
    content = models.TextField(verbose_name="咨询记录")
    tag = models.ManyToManyField("Tag", blank=True)  # 一个用户有多个标签，一个标签属于多个人 多对多
    consultant = models.ForeignKey('UserProfile', verbose_name="课程顾问")
    memo = models.TextField(null=True, blank=True, verbose_name="备注")
    date = models.DateTimeField(auto_now_add=True)
    status_choices = ((0, '已报名'), (1, '未报名'), (2, '已退学'))
    status = models.SmallIntegerField(choices=status_choices)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = verbose_name = "客户表"
        ordering = ['id']


class Tag(models.Model):
    """
    用户标签表
    """
    name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = verbose_name = "标签"
        ordering = ['id']


class CustomerFollowUp(models.Model):
    """
    客户信息跟进表
    """
    customer = models.ForeignKey('Customer', verbose_name="跟进的客户")
    content = models.TextField(verbose_name="跟进的内容")
    consultant = models.ForeignKey('UserProfile', verbose_name="谁跟进的")
    date = models.DateTimeField(auto_now_add=True)
    intention_choices = (
        (0, '两周内'),
        (1, '一个月内'),
        (2, '近期无意向'),
        (3, '已在其他机构报名'),
        (4, '已报名'),
        (5, '已拉黑'),
    )
    intention = models.SmallIntegerField(choices=intention_choices)

    def __str__(self):
        return "%s" % self.customer

    class Meta:
        verbose_name_plural = verbose_name = "客户跟进记录"
        ordering = ['id']


class Course(models.Model):
    """
    课程
    """
    name = models.CharField(max_length=64, unique=True)
    price = models.PositiveSmallIntegerField(verbose_name="学费(+)")
    period = models.PositiveSmallIntegerField(verbose_name="周期(month)")
    outline = models.TextField(verbose_name="课程大纲")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = verbose_name = "课程"
        ordering = ['id']


class Branch(models.Model):
    """
    校区
    """
    name = models.CharField(max_length=128, unique=True)
    addr = models.CharField(max_length=256)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = verbose_name = "校区"
        ordering = ['id']


class ClassList(models.Model):
    """
    班级表
    """
    branch = models.ForeignKey("Branch", verbose_name="分校")
    course = models.ForeignKey('Course')
    class_type_choices = (
        (0, '面授(脱产)'),
        (1, '面授(周末)'),
        (2, '网络班'),
    )
    class_type = models.SmallIntegerField(choices=class_type_choices, verbose_name="班级类型")
    semester = models.PositiveSmallIntegerField(verbose_name="学期")
    teachers = models.ManyToManyField("UserProfile")
    start_data = models.DateField(verbose_name="开班时间")
    end_data = models.DateField(verbose_name="结业日期", null=True, blank=True)

    class Meta:
        unique_together = ('branch', 'course', 'semester')
        verbose_name_plural = verbose_name = "班级"
        ordering = ['id']

    def __str__(self):
        return "%s %s %s" % (self.branch, self.course, self.semester)


class CourseRecord(models.Model):
    """
    上课记录表，与班级一对多
    """
    from_class = models.ForeignKey('ClassList')
    day_number = models.PositiveSmallIntegerField(verbose_name="第几节课")
    teacher = models.ForeignKey("UserProfile")
    has_homework = models.BooleanField(default=True, verbose_name="是否有作业")
    homework_title = models.CharField(max_length=128, blank=True, null=True)
    homework_content = models.TextField(blank=True, null=True)
    outline = models.TextField(verbose_name="课程大纲")
    date = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('from_class', 'day_number')
        verbose_name_plural = verbose_name = "上课记录"
        ordering = ['id']

    def __str__(self):
        return "%s %s" % (self.from_class, self.day_number)


class StudyRecord(models.Model):
    """
    学习记录表
    """
    student = models.ForeignKey("Enrollment")
    course_record = models.ForeignKey('CourseRecord')
    attendance_choices = (
        (0, '已签到'),
        (1, '迟到'),
        (2, '缺勤'),
        (3, '早退')
    )
    attendance = models.SmallIntegerField(choices=attendance_choices, default=0, verbose_name="出勤记录")
    score_choices = (
        (100, 'A+'),
        (90, 'A'),
        (85, 'B+'),
        (80, 'B'),
        (75, 'B-'),
        (70, 'C+'),
        (60, 'C'),
        (40, 'C-'),
        (-50, 'D'),
        (0, 'N/A'),  # NOT Available
    )
    score = models.SmallIntegerField(choices=score_choices)
    memo = models.TextField(null=True, blank=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return '%s %s %s' % (self.student, self.course_record, self.score)

    class Meta:
        unique_together = ('student', 'course_record')
        verbose_name_plural = verbose_name = "学习记录"
        ordering = ['id']


class Enrollment(models.Model):
    """
    报名表
    """
    customer = models.ForeignKey("Customer")
    enrolled_class = models.ForeignKey("ClassList", verbose_name='报名的班级')
    consultant = models.ForeignKey("UserProfile", verbose_name="课程顾问")
    contract_agreed = models.BooleanField(default=False, verbose_name='学员统一合同条款')
    contract_approved = models.BooleanField(default=False, verbose_name='销售已经审核合同条款')
    data = models.DateTimeField(verbose_name="报名日期")

    def __str__(self):
        return "%s %s" % (self.customer, self.enrolled_class)

    class Meta:
        unique_together = ('customer', 'enrolled_class')
        verbose_name_plural = verbose_name = "报名"
        ordering = ['id']


class Payment(models.Model):
    """
    缴费记录
    """
    customer = models.ForeignKey("Customer")
    course = models.ForeignKey("Course", verbose_name="报名课程")
    amount = models.PositiveIntegerField(verbose_name="缴费数额", default=500)
    consultant = models.ForeignKey("UserProfile", verbose_name="办理人")
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s %s" % (self.customer, self.amount)

    class Meta:
        verbose_name_plural = verbose_name = "缴费"
        ordering = ['id']


'''
class UserProfile(models.Model):
    """
    用户账号表
    """
    user = models.OneToOneField(User)
    name = models.CharField(max_length=32)
    roles = models.ManyToManyField('Role', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = verbose_name = "用户账号"
        ordering = ['id']
'''


class Role(models.Model):
    """
    角色表
    """
    name = models.CharField(max_length=32, unique=True)
    menus = models.ManyToManyField('Menu', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = verbose_name = "角色"
        ordering = ['id']


class Menu(models.Model):
    """
    菜单
    """
    name = models.CharField(max_length=32)
    url_name = models.CharField(max_length=64)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = verbose_name = "菜单"
        ordering = ['id']
