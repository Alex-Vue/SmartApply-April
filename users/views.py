import json, os
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, JsonResponse, Http404, HttpResponse
from users.models import User, Calendar, Document
from django.conf import settings
from django import forms
from users.forms import DocumentForm
from django.urls import reverse

#######################################################
from django.db.models import Count
import datetime


#######################################################


#
# currently working on uploading a file w/ https://simpleisbetterthancomplex.com/tutorial/2016/08/01/how-to-upload-files-with-django.html
#
#


def app_org(request):
    return render(request, 'users/appOrg.html')


#########################################################
def ajax_resv_list(request):
    # POST 요청일 때
    if request.method == 'POST':
        data = json.loads(request.body)
        resv_list = list(Calendar.objects.filter(event_date__icontains=data).values())
        context = {
            'resv_list': resv_list
        }
        return JsonResponse(context)


def index(request):
    msg = 'My Message'
    user_id = request.session.get('user_id')
    if user_id:

        if request.method == "POST":
            title = request.POST['resv_title']
            user_name = User.objects.filter(id=user_id)[0].User_name
            body = request.POST['resv_body']
            time = request.POST['onlydatetime']
            if title and user_name and body and time:
                cal = Calendar(title=title,
                               body=body,
                               event_date=time,
                               user_name=user_name,
                               is_active=True)
                cal.save()
                return redirect('/')
            # Calendar.objects.create(title=title, body=body, event_date=time, user_name=user_name, is_active=True)
            # print(Calendar.objects.all())
        # user = User.objects.get(id=user_id)
        # messages.success(request, user.User_name)
        context = {
            'cal_list': Calendar.objects.all(),
        }

        return render(request, "home/home.html", context)

        # return render(request, 'calendar/calendar.html')
    return render(request, 'index.html')


#########################################################

def home(View):
    def get(self, request):
        user = request.session["User_name"]
        return render(request, "home/home.html", {"user": user})


#################################### 20220418
def ajax_resv_cnt(request):
    # POST 요청일 때
    if request.method == 'POST':
        data = json.loads(request.body)
        user_id = request.session.get('user_id')
        user = User.objects.get(id=user_id)

        year = int(data['year'])
        month = int(data['month'])
        first_day = datetime.date(year, month, 1)

        if month == 12:
            last_day = datetime.date(year + 1, 1, 1) - datetime.timedelta(days=1)
        else:
            last_day = datetime.date(year, month + 1, 1) - datetime.timedelta(days=1)

        query = Calendar.objects.filter(user_name=user.User_name,
                                        event_date__range=(first_day, last_day)).values('event_date')

        resv_date_cnt_list = dict()

        for q in query:
            d = q['event_date'].day
            if d not in resv_date_cnt_list:
                resv_date_cnt_list[d] = 1
            else:
                resv_date_cnt_list[d] += 1
        context = {
            'resv_date_cnt_list': resv_date_cnt_list,
        }
        return JsonResponse(context)


################################### 20220418

def cal(request):
    # model = Calendar
    # template_name = 'cal/calendar.html'

    # context = super().get_context_data(**kwargs)
    user_id = request.session.get('user_id')
    if user_id:

        if request.method == "POST":
            title = request.POST['resv_title']
            user_name = User.objects.filter(id=user_id)[0].User_name
            body = request.POST['resv_body']
            time = request.POST['onlydatetime']
            if title and user_name and body and time:
                cal = Calendar(title=title,
                               body=body,
                               event_date=time,
                               user_name=user_name,
                               is_active=True)
                cal.save()
                return redirect('/cal')
        ############################################## 20220418
        user = User.objects.get(id=user_id)
        year = request.GET.get('year', datetime.datetime.today().year)
        month = request.GET.get('month', datetime.datetime.today().month)
        first_day = datetime.date(year, month, 1)

        if month == 12:
            last_day = datetime.date(year + 1, 1, 1) - datetime.timedelta(days=1)
        else:
            last_day = datetime.date(year, month + 1, 1) - datetime.timedelta(days=1)

        query = Calendar.objects.filter(user_name=user.User_name,
                                        event_date__range=(first_day, last_day)).values('event_date')

        resv_date_cnt_list = dict()

        for q in query:
            d = q['event_date'].day
            if d not in resv_date_cnt_list:
                resv_date_cnt_list[d] = 1
            else:
                resv_date_cnt_list[d] += 1

        context = {
            'cal_list': Calendar.objects.all(),
            'resv_date_cnt_list': resv_date_cnt_list,
        }
        ############################################## 20220418
        return render(request, "calendar/calendar.html", context)
    # use today's date for the calendar

    # Instantiate our calendar class with today's year and date
    # cal = Calendar(d.year, d.month)

    # Call the formatmonth method, which returns our calendar as a table
    # html_cal = cal.formatmonth(withyear=True)
    # context['calendar'] = mark_safe(html_cal)
    return render(request, 'calendar/calendar.html')


def logout_view(request):
    user_id = request.session.get('user_id')
    if user_id:
        request.session["user_id"] = None
        return redirect('/')


def profile_view(request):
    user_id = request.session.get('user_id')

    if user_id:
        user = User.objects.get(id=user_id)
        messages.success(request, user.User_name)
        return render(request, 'users/profile.html', {})


def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        first_name = request.POST['firstname']
        # middle_name = request.POST['middlename']
        last_name = request.POST['lastname']
        # gender = request.POST['gender']
        # date_of_birth = request.POST['birthday']

        user = User.objects.filter(User_name=username)
        if user:
            messages.warning(request, "Sign-Up Failed")
        else:
            User.objects.create(First_name=first_name, Last_name=last_name, User_name=username, password=password)
            messages.warning(request, "Membership Was Successful")
            HttpResponseRedirect("/")
    return render(request, 'users/signUp.html', {})


def signin_view(request):
    if request.session.get('user_id'):
        messages.warning(request, "already logged in")
        return redirect("/")
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if username and password:
            print(request.POST['username'], request.POST['password'])
            user = User.objects.filter(User_name=username, password=password).first()
            print(user)
            if user:
                request.session["user_id"] = user.id
                request.session["user"] = User.objects.filter(User_name=username, password=password).values()[0]
            return redirect("/")

            # HttpResponseRedirect("/")
        else:
            messages.warning(request, "fail")
    return render(request, 'users/signIn.html', {})


def files(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'home/importantFiles.html', {
                'uploads': Document.objects.all()
            })
    else:
        form = DocumentForm()
    return render(request, 'home/importantFiles.html', {
        'form': form,
        'uploads': Document.objects.all()
    })

def download(request, path):
    file_path = "documents/" + path;
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404

def deleteFile(request, document):
  if os.path.exists(document):
    os.remove(document)
    
  file_to_be_deleted = Document.objects.get(document=document)
  file_to_be_deleted.delete()
  #match doc with os to delete file path
  
  
  return HttpResponseRedirect(reverse('importantfiles'))
    

def applications(request):
    return render(request, 'home/processOfApp.html')
