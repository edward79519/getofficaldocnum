from django.db import models
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords

# Create your models here.
# 更改內建使用者(User Model)預設顯示方式
User.__str__ = lambda user_instance: "{}{}".format(user_instance.last_name, user_instance.first_name)


class Company(models.Model):
    fullname = models.CharField(max_length=40)
    shortname = models.CharField(max_length=10)
    addtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)
    valid = models.BooleanField(default=True)
    plmsn = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.fullname

    class Meta:
        ordering = ['plmsn']


class Department(models.Model):
    fullname = models.CharField(max_length=10)
    shortname = models.CharField(max_length=10)
    addtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)
    valid = models.BooleanField(default=True)

    def __str__(self):
        return self.fullname


class OfficalDoc(models.Model):
    comp = models.ForeignKey(
        Company,
        on_delete=models.PROTECT,
        related_name="officaldocs",
    )
    dept = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        related_name="officaldocs",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="officaldocs",
    )
    sn = models.CharField(
        max_length=10,
    )
    fullsn = models.CharField(
        max_length=30,
    )
    pubdate = models.DateField()
    title = models.CharField(max_length=300)
    addtime = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [['comp', 'dept', 'sn']]

    def __str__(self):
        return self.fullsn


class ReceiveDoc(models.Model):
    sn = models.CharField(max_length=10)
    fullsn = models.CharField(max_length=30, unique=True)
    senddept = models.CharField(max_length=100)
    sendsn = models.CharField(max_length=100, unique=True)
    senddate = models.DateField()
    abstract = models.CharField(max_length=500)
    rcvcomp = models.ForeignKey(
        Company,
        on_delete=models.PROTECT,
        related_name='receivedocs',
    )
    addtime = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='receivedocs',
    )

    def __str__(self):
        return self.fullsn


class BaseModel(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='%(app_label)s_%(class)s_author')
    changed_by = models.ForeignKey('auth.User', on_delete=models.PROTECT)
    is_valid = models.BooleanField(default=True)
    add_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    history = HistoricalRecords(inherit=True)

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    class Meta:
        abstract = True


class ContractCate(BaseModel):
    sn = models.IntegerField(unique=True, primary_key=True)
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return "{}_{}".format(str(self.sn).zfill(2), self.name)


class ContractStatus(models.Model):
    order = models.IntegerField(unique=True)
    name = models.CharField(max_length=20, unique=True)
    is_valid = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['order']


class ContractTaxStatus(models.Model):
    order = models.IntegerField(unique=True)
    name = models.CharField(max_length=20, unique=True)
    is_valid = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['order']


class Project(BaseModel):
    order = models.IntegerField(unique=True)
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Contract(BaseModel):
    sn = models.CharField(max_length=17, unique=True)
    status = models.ForeignKey(
        ContractStatus,
        on_delete=models.PROTECT,
        related_name='contracts',
    )
    comp = models.ForeignKey(
        Company,
        on_delete=models.PROTECT,
        related_name='contracts',
    )
    category = models.ForeignKey(
        ContractCate,
        on_delete=models.PROTECT,
        related_name='contracts',
    )
    sign_date = models.DateField(null=True, blank=True)
    length = models.IntegerField(null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    counterparty = models.CharField(max_length=100)
    counter_dept = models.CharField(max_length=50)
    counter_contact = models.CharField(max_length=50)
    total_price = models.DecimalField(max_digits=15, decimal_places=2)
    tax_status = models.ForeignKey(
        ContractTaxStatus,
        on_delete=models.PROTECT,
        related_name='contracts',
    )
    tax = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    payment = models.CharField(max_length=100, null=True, blank=True)
    content = models.CharField(max_length=500)
    manage_dept = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        related_name='contracts',
        null=True,
        blank=True,
    )
    manager = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='contracts',
        null=True,
        blank=True,
    )
    location = models.CharField(max_length=50, null=True, blank=True)
    project = models.ForeignKey(
        Project,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    remark = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return "{}-{}-{}".format(self.sn, self.comp, self.category, self.counterparty)

    class Meta:
        ordering = ['-add_time']
