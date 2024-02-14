from django.db import models
import enum
from datetime import timedelta
# Create your models here.
class Department(models.Model):
    dept_name=models.CharField(max_length=256,unique=True)
    def __str__(self) -> str:
        return self.dept_name

class Bank(models.Model):
    bank_name=models.CharField(max_length=256,unique=True)
    def __str__(self) -> str:
        return self.bank_name


class Employee(models.Model):
    name=models.CharField(max_length=256)
    email=models.EmailField(max_length=256,unique=True,default='abc@gmail.com')
    company_code=models.CharField(max_length=256,default='SPCPE',null=True,blank=True)
    employee_id=models.BigIntegerField(unique=True,null=True,blank=True)
    department=models.ForeignKey(Department,on_delete=models.CASCADE)
    designation=models.CharField(max_length=256) #map
    joining_date=models.DateField()
    account_number=models.CharField(max_length=256,unique=True)
    ifsc=models.CharField(max_length=256)
    bank_name=models.ForeignKey(Bank,on_delete=models.CASCADE) #map
    pf_number=models.CharField(max_length=256,null=True,blank=True)
    uan_no=models.CharField(max_length=256,null=True,blank=True)
    pan_no=models.CharField(max_length=256,unique=True)
    basic_salary=models.IntegerField()
    hra=models.IntegerField()
    conv=models.IntegerField(default=0)
    special_allowance=models.IntegerField(default=0)
    isActive=models.BooleanField(default=True)
    pf=models.IntegerField(default=0)
    def __str__(self) -> str:
        return self.name
    def save(self, *args, **kwargs):
        if not self.employee_id:
            last_id = Employee.objects.all().order_by('employee_id').last()
            if not last_id:
                # This is the first entry
                self.employee_id = 100001
            else:
                # Increment the last id
                self.employee_id = last_id.employee_id + 1
            self.company_code='SPCPE'
        super(Employee, self).save(*args, **kwargs)
    
class Months(enum.Enum):
    January='Jan'
    February='Feb'
    MARCH='MAR'
    APRIL='APR'
    MAY='MAY'
    JUNE='JUNE'
    JULY='JULY'
    AUGUST='AUG'
    SEPTEMBER='SEPT'
    OCTOBER='OCT'
    NOVEMBER='NOV'
    DECEMBER='DEC'
    @classmethod
    def choices(cls):
        return [(key.value,key.name) for key in cls]
class Payslip(models.Model):
    employee=models.ForeignKey(Employee,on_delete=models.CASCADE)
    basic_salary=models.IntegerField(null=True,blank=True)
    hra=models.IntegerField(null=True,blank=True)
    conv=models.IntegerField(null=True,blank=True)
    special_allowance=models.IntegerField(null=True,blank=True)
    pf=models.IntegerField(null=True,blank=True)
    month=models.CharField(max_length=256,choices=Months.choices(),default=Months.January)
    year=models.IntegerField(default=2024)

    def __str__(self) -> str:
        return self.employee.name if self.employee else ''
    
    def save(self,*args,**kwargs):
        if self.basic_salary is None or self.basic_salary==0 :
            self.basic_salary=self.employee.basic_salary
        if self.hra is None or self.hra==0:
            self.hra=self.employee.hra
        if self.conv is None or self.conv==0:
            self.conv=self.employee.conv
        if self.special_allowance is None or self.special_allowance==0:
            self.special_allowance=self.employee.special_allowance
        if self.pf is None or self.pf==0:
            self.pf=self.employee.pf
        if int(self.year)<2023:
            self.year=2024
        super(Payslip,self).save(*args,**kwargs)

        
        
        



