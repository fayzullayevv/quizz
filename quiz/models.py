from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import pre_save

class Category(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name
    
class Test(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    title  = models.CharField(max_length=200)
    maximum_attemps = models.PositiveBigIntegerField()
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(default=(timezone.now()+timezone.timedelta(days=10)))
    pass_percentage = models.PositiveBigIntegerField()

    def __str__(self):
        return self.title
    

class Question(models.Model):
    test = models.ForeignKey(Test,on_delete=models.CASCADE)
    question = models.CharField(max_length=300)
    a = models.CharField(max_length=150)
    b = models.CharField(max_length=150)
    c = models.CharField(max_length=150)
    d = models.CharField(max_length=150)
    true_answer = models.CharField(max_length=150,help_text='E.x: a ')

    def _str__(self):
        return self.question
    

class CheckTest(models.Model):
    student = models.ForeignKey(User,on_delete=models.CASCADE)
    test = models.ForeignKey(Test,on_delete=models.CASCADE)
    finded_questions = models.PositiveBigIntegerField(default=0)
    user_passed = models.BooleanField(default=False)
    percentage = models.PositiveBigIntegerField(default=0)

    def __str__(self):
        return 'Test of '+str(self.student.username)
    
class CheckQuestion(models.Model):
    checktest = models.ForeignKey(CheckTest,on_delete=models.CASCADE)
    question = models.ForeignKey(Question,on_delete=models.CASCADE)
    given_answer = models.CharField(max_length=1,help_text='E.x: a ')
    true_answer = models.CharField(max_length=1,help_text='E.x: a ')
    is_true = models.BooleanField(default=False)






@receiver(pre_save,sender = CheckQuestion)
def check_answer(sender,instance,*args, **kwargs):
    if instance.given_answer == instance.true_answer:
        instance.is_true = True



@receiver(pre_save,sender = CheckTest)
def check_test(sender,instance,*args, **kwargs):
    checktest = instance
    checktest.finded_questions = CheckQuestion.objects.filter(checktest=checktest,is_true=True).count()
    try:
        checktest.percentage = int(checktest.finded_questions)*100//CheckQuestion.objects.filter(checktest=checktest).count()
        if checktest.test.pass_percentage <= checktest.percentage:
            checktest.user_passed = True
    except:
        pass