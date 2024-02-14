from django.shortcuts import render,redirect
from .models import *
from django.template.loader import render_to_string
import pdfkit
from django.http import HttpResponse
# from django.template import loader
# Create your views here.
def number_to_words(n):
    if n < 0:
        return "Negative numbers are not supported."
    if n == 0:
        return 'Zero'

    def words_under_100(number):
        units = ["", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine"]
        teens = ["Ten", "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen", "Seventeen", "Eighteen", "Nineteen"]
        tens = ["", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"]

        if number < 10:
            return units[number]
        elif 10 <= number < 20:
            return teens[number - 10]
        else:
            return tens[number // 10] + (" " + units[number % 10] if number % 10 != 0 else "")

    def words_under_1000(number):
        if number < 100:
            return words_under_100(number)
        else:
            return words_under_100(number // 100) + " Hundred" + (" " + words_under_100(number % 100) if number % 100 != 0 else "")

    parts = []
    if n >= 100000:
        parts.append(words_under_100(n // 100000) + " Lakh")
        n %= 100000
    if n >= 1000:
        parts.append(words_under_1000(n // 1000) + " Thousand")
        n %= 1000
    if n > 0:
        parts.append(words_under_1000(n))

    return ' '.join(parts)



def createBank(request):
    print('here-->')
    if request.method=='POST':
        bank_name=request.POST.get('bank')
        bank=Bank.objects.create(bank_name=bank_name)
        return render(request,'create_bank.html',{'data':'saved'})    

    return render(request,'create_bank.html',{'data':''})


def createDept(request):
    if request.method=='POST':
        dept_name=request.POST.get('dept')
        return render(request,'create_dept.html',{'data':'saved'})    

    return render(request,'create_dept.html',{})


def createEmployee(request):
    if request.method=='POST':
        data=request.POST
        dept=Department.objects.get(id=data['department'])
        bank=Bank.objects.get(id=data.get('bank_name'))
        conv=data.get('conv')
        special_allowance=data.get('special_allowance')
        pf=data.get('pf')
        if conv is '':
            conv=0
        if special_allowance is '':
            special_allowance=0
        if pf is '':
            pf=0
        
        emp=Employee.objects.create(name=data['name'],department=dept,designation=data['designation'],joining_date=data.get('joining_date'),account_number=data.get('account_number'),ifsc=data.get('ifsc'),bank_name=bank,pf_number=data.get('pf_number'),uan_no=data.get('uan_no'),pan_no=data.get('pan_no'),basic_salary=data.get('basic_salary'),hra=data.get('hra'),conv=conv,special_allowance=special_allowance,pf=pf,email=data.get('email'))
        print(emp)
        
        return render(request,'create_payslip.html',{})
    depts=Department.objects.all()
    banks=Bank.objects.all()
    print(depts)
    return render(request,'create_employee.html',{'depts':depts,'banks':banks})

def createPayslip(request):
    if request.method=='POST':
        data=request.POST
        basic_salary=data.get('basic_salary')
        hra=data.get('hra')
        conv=data.get('conv')
        special_allowance=data.get('special_allowance')
        pf=data.get('pf')
        employee=Employee.objects.get(email=data.get('email'))
        if basic_salary is '':
            basic_salary=employee.basic_salary
        if hra is '':
            hra=employee.hra
        if conv  is '':
            conv=employee.conv
        if special_allowance is '':
            special_allowance=employee.special_allowance
        if pf is '':
            pf=employee.pf

        payslip=Payslip.objects.create(employee=employee,basic_salary=basic_salary,hra=hra,conv=conv,special_allowance=special_allowance,pf=pf,year=data.get('year'),month=data.get('month'))
        
        total_heads=int(employee.basic_salary)+int(employee.hra)+int(employee.conv)+int(employee.special_allowance)
        salary=int(payslip.basic_salary)+int(payslip.hra)+int(payslip.conv)+int(payslip.special_allowance)
        net_salary=salary-int(payslip.pf)
        net_salary_words=number_to_words(net_salary)+' Rupees only '
        formatted_salary=str(net_salary)
        if len(formatted_salary)>5:
            one=formatted_salary[-1:-4:-1]
            two=formatted_salary[-4:-6:-1]
            three=formatted_salary[-6::-1]
            formatted_salary=three[::-1]+','+two[::-1]+','+one[::-1]
            print(formatted_salary)
        elif len(formatted_salary)>3:
            one=formatted_salary[-1:-4:-1]
            three=formatted_salary[-4::-1]
            formatted_salary=three[::-1]+','+one[::-1]
        template=render_to_string('payslips.html',{'employee':employee,'payslip':payslip,'heads':total_heads,'salary':salary,'net_sal':formatted_salary,'net_salary_words':net_salary_words})
        options={
        'page-size':'Letter',
        'encoding':"ÜTF-8",
        }
        html=pdfkit.from_string(template,False,options=options)
        # result=html.write_pdf()
        response=HttpResponse(html,content_type='application/pdf')
        response['Content-Disposition']='attachment; filename="report.pdf"'
        return response

        return render(request,'payslip.html',{'employee':employee,'payslip':payslip,'heads':total_heads,'salary':salary,'net_sal':formatted_salary,'net_salary_words':net_salary_words})

    return render(request,'create_payslip.html',{})