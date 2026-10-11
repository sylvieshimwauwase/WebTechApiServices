from django.http import HttpResponse
from django.shortcuts import render
from Blog.views import Blog_Dashboard

def home(request):
    #return HttpResponse("Hello Guys! What's Up?")
    # return render(request, 'home.html')
    return Blog_Dashboard(request)

def course(request, course_id):
    return HttpResponse(f'This is the python Course ID: {course_id}')

def courseName(request, course_name):
    return HttpResponse(f'This is the course Name: {course_name}')

def courseBlog(request, course_blog_title):
    return HttpResponse(f'This is the Python Blog: {course_blog_title}')

def studentMarks(request):

    # student_marks = {
    #     'name':['David','John','Mohamed','Alex'],
    #     'regno':[20001,20002,20003,20004],
    #     'marks':[20,23,45,57]
    # }
    # student_marks = zip(student_marks['name'],student_marks['regno'],student_marks['marks'])

    # return render(request, "studentMarks.html", {'student_marks':student_marks})

    json_data = [
        {
            "name":"David",
            "regno":20001,
            "marks":68
        },
        {
            "name":"John",
            "regno":20002,
            "marks":75
        },
        {
            "name":"Mohamed",
            "regno":20003,
            "marks":82
        },
        {
            "name":"Alex",
            "regno":20004,
            "marks":45
        }
    ]
    return render(request, "studentMarks.html",{'json_data':json_data})