from django.db import models
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords

# Create your models here.


class Company(models.Model):
    fullname = models.CharField(max_length=40)
    shortname = models.CharField(max_length=10)
    addtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)
    valid = models.BooleanField(default=True)

    def __str__(self):
        return self.fullname


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
    changed_by = models.ForeignKey('auth.User', on_delete=models.PROTECT)
    is_valid = models.BooleanField(default=True)
    add_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    class Meta:
        abstract = True


class ContractCate(BaseModel):
    sn = models.IntegerField(max_length=3, unique=True, primary_key=True)
    name = models.CharField(max_length=50, unique=True)


