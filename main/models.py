from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class AccountManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Необходим ввести адрес электронной почты')
        if not password:
            raise ValueError('Необходимо ввести пароль')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields['is_staff'] = True
        extra_fields['is_superuser'] = True
        return self._create_user(email, password, **extra_fields)


class Account(AbstractBaseUser, PermissionsMixin):
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'

    objects = AccountManager()

    email = models.EmailField(verbose_name='Email', unique=True)
    first_name = models.CharField(verbose_name='First name', blank=True, null=True, max_length=20)
    last_name = models.CharField(verbose_name='Last name', blank=True, null=True, max_length=20)
    middle_name = models.CharField(verbose_name='Middle name', blank=True, null=True, max_length=20)
    is_staff = models.BooleanField(verbose_name='Staff status', default=False)
    is_active = models.BooleanField(verbose_name='Active status', default=True)

    # reason I have added 'is_manager' filed
    # kpi-project users block has 3 types:
    # 1) managers - main user group, they have access only to own page and indicators;
    # 2) director - user has access to all indicators and manager pages but hasn't own kpi;
    # 3) director/manager - user has access to all indicators and manager pages and has own kpi and own page;
    # That is why i need additional field. It will look like (is_staff, is_manager):
    # 1gr - False, True
    # 2gr - True, False
    # 3gr - True, True
    is_manager = models.BooleanField(verbose_name='Manager status', default=True)

    def get_short_name(self):
        return '%s %s' % (self.first_name, self.middle_name)

    def get_full_name(self):
        return '%s %s %s' % (self.last_name, self.first_name, self.middle_name)

    def __unicode__(self):
        return self.email


class BaseTable(models.Model):
    """Base model class for two-rows db tables."""
    id = models.PositiveSmallIntegerField(verbose_name='ID', primary_key=True)
    name = models.CharField(verbose_name='Name', max_length=100)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return '%s' % self.name

    class Meta:
        abstract = True


class RowType(BaseTable):
    """Row types table (variable, fixed)."""
    pass


class RowGroup1(BaseTable):
    """1/3 group level table."""
    pass


class RowGroup2(BaseTable):
    """2/3 level level table."""
    pass


class RowGroup3(BaseTable):
    """3/3 level level table."""
    pass


class Organization(BaseTable):
    """Branches table."""
    pass


class DataType(BaseTable):
    """Data type table (actual, budget, RF1, RF2)."""
    pass


class Row(models.Model):
    """Main table with all row information."""
    id = models.PositiveSmallIntegerField(verbose_name='ID', primary_key=True)
    name = models.CharField(verbose_name='Name', max_length=100)
    row_type = models.ForeignKey(RowType, on_delete=models.PROTECT)
    row_group1 = models.ForeignKey(RowGroup1, on_delete=models.PROTECT)
    row_group2 = models.ForeignKey(RowGroup2, on_delete=models.PROTECT)
    row_group3 = models.ForeignKey(RowGroup3, on_delete=models.PROTECT)


class Data(models.Model):
    """Main table with all data values."""
    id = models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)
    org = models.ForeignKey(Organization, on_delete=models.PROTECT)
    row = models.ForeignKey(Row, on_delete=models.PROTECT)
    data_type = models.ForeignKey(DataType, on_delete=models.PROTECT)
    period = models.DateField(verbose_name='Period')
    value = models.FloatField(verbose_name='Value', default=0)


class IndicatorGroup(BaseTable):
    """Indicator group table (value, percent, turnover, variable)."""
    pass


class IndicatorEffect(BaseTable):
    """Indicator effect table (positive, negative)."""
    pass


class Indicator(models.Model):
    """Main table with all indicators information."""
    id = models.PositiveSmallIntegerField(verbose_name='ID', primary_key=True)
    name = models.CharField(verbose_name='Name', max_length=100)
    indicator_group = models.ForeignKey(IndicatorGroup, on_delete=models.PROTECT)
    indicator_effect = models.ForeignKey(IndicatorEffect, on_delete=models.PROTECT)
    slag = models.SlugField(verbose_name='Sort name', max_length=20)


class Report(models.Model):
    """Main table to create report structure."""
    id = models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)
    indicator = models.ForeignKey(Indicator, on_delete=models.PROTECT)
    row_code = models.PositiveSmallIntegerField(verbose_name='Row code', blank=True, null=True)
    row_position = models.PositiveSmallIntegerField(verbose_name='Row position', blank=True, null=True)
    org_code = models.PositiveSmallIntegerField(verbose_name='Organization code', blank=True, null=True)
    numerator = models.PositiveSmallIntegerField(verbose_name='Numerator', blank=True, null=True)
    denominator = models.PositiveSmallIntegerField(verbose_name='Denominator', blank=True, null=True)
    year = models.PositiveSmallIntegerField(verbose_name='Year')


class Scale(models.Model):
    """Main scale table."""
    id = models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)
    indicator = models.ForeignKey(Indicator, on_delete=models.PROTECT)
    row_position = models.PositiveSmallIntegerField(verbose_name='Row number')
    year = models.PositiveSmallIntegerField(verbose_name='Year')
    percent_min = models.FloatField(verbose_name='Minimum scale percent')
    percent_max = models.FloatField(verbose_name='Maximum scale percent')
    bonus_min = models.FloatField(verbose_name='Minimum bonus percent')
    bonus_max = models.FloatField(verbose_name='Maximum bonus percent')
    bonus_share = models.FloatField(verbose_name='Bonus share', default=0)
    account = models.ForeignKey(Account, on_delete=models.PROTECT)


class Target(models.Model):
    """Sub table with special indicator targets."""
    id = models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)
    indicator = models.ForeignKey(Indicator, on_delete=models.PROTECT)
    year = models.PositiveSmallIntegerField(verbose_name='Year')
    target = models.FloatField(verbose_name='Target', blank=True, null=True)


class CurrentPeriod(models.Model):
    """Current year period for dashboard current slice."""
    year = models.PositiveSmallIntegerField(verbose_name='Year', primary_key=True)
    period = models.DateField(verbose_name='Period')
