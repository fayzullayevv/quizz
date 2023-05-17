from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Test,Question,CheckQuestion,CheckTest
from django.contrib.auth.decorators import login_required
from django.utils import timezone

def HomePage(request):
    tests = Test.objects.all()
    return render(request,'home.html',{'tests':tests})

def Sign_up(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    return render(request,'registration/signup.html',{'form':form})



def Ready_to_test(request,test_id):
    test = get_object_or_404(Test,id=test_id)
    return render(request,'ready_to_test.html',{'test':test})



def TestView(request,test_id):
    test = get_object_or_404(Test,id=test_id)
    test1 = Test.objects.all()
    attemps = CheckTest.objects.filter(student = request.user,test=test).count()
    if (timezone.now()>=test.start_date and timezone.now()<=test.end_date) and attemps<test.maximum_attemps:
      questions = Question.objects.filter(test=test)
      if request.method == 'POST':
          checktest = CheckTest.objects.create(student=request.user,test=test)
          for question in questions:
              given_answer =request.POST[str(question.id)]
              CheckQuestion.objects.create(checktest=checktest,question=question,given_answer=given_answer,true_answer=question.true_answer,)
          checktest.save()
          return redirect('checktest',checktest.id)
      context = {'test':test,'questions':questions,'test1':test1}
      return render(request,'test.html',context)
    else:
        return HttpResponse('Test no found!')
    

@login_required(login_url='login')
def CheckTestView(request,checktest_id):
    checktest = get_object_or_404(CheckTest,id=checktest_id,student=request.user)
    return render(request,'checktest.html',{'checktest':checktest})