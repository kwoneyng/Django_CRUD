from django.shortcuts import render
from .models import Job
from faker import Faker


def index(request):
    return render(request, 'jobs/index.html')


def past_job(request):
    name = request.POST.get('name')

    # 데이터 베이스에 name 으로 저장된 전생직업 있는지 확인
    job = Job.objects.filter(name=name).first()

    # 없다면, 새로 만든다.
    if job == None:
        fake = Faker('ko-KR')
        job = Job(name=name, past_job=fake.job())
        job.save()
        
    # 있다면, 그냥 보여준다.
    context = {'job': job}

    return render(request, 'jobs/past_life.html', context)
