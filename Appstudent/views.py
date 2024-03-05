from imp import NullImporter
from django.shortcuts import redirect, render
import mysql.connector as sql
fn=''
em=''
pwd=''
def signup(request):
    global fn,em,pwd
    if request.method == 'POST':
        cnt=sql.connect(host="127.0.0.1", user="root", passwd="Said&10112001", database="prdb1")
        cursor=cnt.cursor()
        d=request.POST
        for key, value in d.items():
            if key=="firstname":
                fn=value
            if key=="Email":
                em=value
            if key=="Password":
                pwd=value

        ch_er = 0

        if (fn == "" or fn is None):
            if (em is None or em == ""):
                if (pwd is None or pwd == ""):
                    ch_er = 1  #all input empty
                    context = {"Error" : "This field is required.", "isError" : ch_er}
                else:
                    ch_er = 2 # password full
                    context = {"Error" : "This field is required.", "isError" : ch_er}
            else:
                if (pwd is None or pwd == ""):
                    ch_er = 3 # email full password empty
                    context = {"Error" : "This field is required.", "isError" : ch_er}
                else:
                    ch_er = 4 # email full password full
                    context = {"Error" : "This field is required.", "isError" : ch_er}
        else:
            if (em is None or em == ""):
                if (pwd is None or pwd == ""):
                    ch_er = 5  #name full 
                    context = {"Error" : "This field is required.", "isError" : ch_er}
                else:
                    ch_er = 6 # name full password full
                    context = {"Error" : "This field is required.", "isError" : ch_er}
            else:
                if (pwd is None or pwd == ""):
                    ch_er = 7 # name full email full password empty
                    context = {"Error" : "This field is required.", "isError" : ch_er}
                else:
                    ch_er = 0 # name full email full password full
                    context = {"Error" : "This field is required.", "isError" : ch_er}
          
        if ch_er == 0:  
            if len(pwd) >= 7:
                if pwd.isdigit():
                    ch_er = 9 
                    context = {"Error" : "This password is too common. This password is entirely numeric.", "isError" : ch_er}
                    cnt.commit()
                    cnt.close()
                    return render(request,'signup.html', context)
                else:
                    rqt="select count(*) from prdb1.students where Email=%s"
                    cursor2=cnt.cursor()
                    cursor2.execute(rqt,(em,))
                    result = cursor2.fetchone()
                    if result[0] > 0:
                        ch_er = 10 
                        context = {"Error" : "A User with this email already exists.", "isError" : ch_er}
                        cnt.commit()
                        cnt.close()
                        return render(request,'signup.html', context)
                    else:
                        rqt1="select count(*) from tutor where Email=%s"
                        cursor3=cnt.cursor()
                        cursor3.execute(rqt1,(em,))
                        result2 = cursor2.fetchone()
                        if result2[0] > 0:
                            ch_er = 10 
                            context = {"Error" : "A User with this email already exists.", "isError" : ch_er}
                            cnt.commit()
                            cnt.close()
                            return render(request,'signup.html', context)
                        else:
                            c="insert into prdb1.students values('{}','{}','{}')".format(fn,em,pwd)
                            cursor.execute(c)
                            cnt.commit()
                            cnt.close()
                            return render(request,'findtutor.html')
            else :
                ch_er = 8
                context = {"Error" : "This password is too short. It must contain at least 7 characters. This password is too common.", "isError" : ch_er}
                cnt.commit()
                cnt.close()
                return render(request,'signup.html', context)
        else:
            return render(request, 'signup.html', context)
    else:
        return render(request,'signup.html')






l_em=None
l_pwd=None
rqt=None
def login(request):
    global l_em,l_pwd
    if request.method == 'POST':
        cnt=sql.connect(host="127.0.0.1", user="root", passwd="Said&10112001", database="prdb1")
        cursor=cnt.cursor()
        l_em = str(request.POST.get("Email", "")).strip()
        l_pwd = str(request.POST.get("Password", "")).strip()
        ch_er = 0

        if (l_em == "" or l_em is None):
            if (l_pwd is None or l_pwd == ""):
                ch_er = 1
                context = {"Error" : "This field is required.", "isError" : ch_er}
            else:
                ch_er = 3
                context = {"Error" : "This field is required.", "isError" : ch_er}
        else:
            if (l_pwd is None or l_pwd == ""):
                ch_er = 2
                context = {"Error" : "This field is required.", "isError" : ch_er}
            else:
                ch_er = 0
                context = {"Error" : "This field is required.", "isError" : ch_er}
          
        if (ch_er == 0):
            rqt = "SELECT COUNT(*) FROM students WHERE Email='{}' AND password_std='{}'".format(l_em, l_pwd)
            cursor.execute(rqt)
            result = cursor.fetchone()
            if result[0] > 0:
                request.session['student_login']= l_em
                cnt.commit()
                cnt.close()
                return redirect('findtutor')
            else:
                cursor2=cnt.cursor()
                rqt2="select count(*) from tutor where Email='{}' and password_tr='{}'".format(l_em,l_pwd)
                cursor2.execute(rqt2)
                result2 = cursor2.fetchone()
                if result2[0] > 0:
                    rqt3="select check_info from tutor where Email='{}' and password_tr='{}'".format(l_em,l_pwd)
                    cursor3=cnt.cursor()
                    cursor3.execute(rqt3)
                    result3 = cursor3.fetchone()
                    if result3[0] == False:
                        cnt.commit()
                        cnt.close()
                        return redirect('tutor_signup')
                    else :
                        request.session['tutor_login']= l_em
                        return redirect('home')

                    
                else:
                    ch_er = 5
                    context = {"Error" : "Please enter a correct username and password. Note that both fields may be case-sensitive.", "isError" : ch_er}
                    cnt.commit()
                    cnt.close()
                    return render(request,'login.html' ,context)
        else:
            return render(request, 'login.html', context)
    else:
        return render(request,'login.html')
    



def logout(request):
    del request.session['tutor_login']
    return redirect('home')

def logout_student(request):
    del request.session['student_login']
    return redirect('home')


def home(request):
    cnt=sql.connect(host="127.0.0.1", user="root", passwd="Said&10112001", database="prdb1")
    if request.session.get('tutor_login'):
        request.session['tutor_add_l'] = request.session.get('tutor_login')
        context = {"home": "tutor_login"}
    else:
        cursor=cnt.cursor()
        rqt5 = "select count(*) from tutor"
        rqt6 = "select count(*) from subjects"
        rqt7 = "select COUNT(DISTINCT tr_cnt) from tutor"
        cursor.execute(rqt5)
        result5 = cursor.fetchone()
        cursor.execute(rqt6)
        result6 = cursor.fetchone()
        cursor.execute(rqt7)
        result7 = cursor.fetchone()
        context = {"home": "home_login",  "number_tutor" : result5[0], "number_subject" : result6[0], "number_country" : result7[0]}
    return render(request, 'home.html', context)


        

   


def findtutor(request):
    cnt=sql.connect(host="127.0.0.1", user="root", passwd="Said&10112001", database="prdb1")
    if request.method == 'POST':
        x = request.POST.get("subjects","")
        cursor=cnt.cursor()
        rqt = "select * from tutor where Subject_taugh = '{}' and check_info = True".format(x)
        rqt2 = "select * from subjects "
        rqt3 = "select * from country"
        rqt4 = "select * from languages_spoken"
        cursor.execute(rqt)
        result = cursor.fetchall()
        cursor.execute(rqt2)
        result2 = cursor.fetchall()
        cursor.execute(rqt3)
        result3 = cursor.fetchall()
        cursor.execute(rqt4)
        result4 = cursor.fetchall()
        rqt5 = "select count(*) from tutor"
        rqt6 = "select count(*) from subjects"
        rqt7 = "select COUNT(DISTINCT tr_cnt) from tutor"
        cursor.execute(rqt5)
        result5 = cursor.fetchone()
        cursor.execute(rqt6)
        result6 = cursor.fetchone()
        cursor.execute(rqt7)
        result7 = cursor.fetchone()

        context = {"tutors" : result, "subjects" :result2, "countries" : result3, "languages_spoken" : result4,  "number_tutor" : result5[0], "number_subject" : result6[0], "number_country" : result7[0] }
        return render(request,'findtutor.html',context)

    else:
        cursor=cnt.cursor()
        rqt = "select id_sbj, Name_sbj from Subjects"
        rqt2 = "select * from tutor where check_info = True"
        rqt3 = "select * from country"
        rqt4 = "select * from languages_spoken"
        cursor.execute(rqt)
        result = cursor.fetchall()
        cursor.execute(rqt2)
        result2 = cursor.fetchall()
        cursor.execute(rqt3)
        result3 = cursor.fetchall()
        cursor.execute(rqt4)
        result4 = cursor.fetchall()

        rqt5 = "select count(*) from tutor"
        rqt6 = "select count(*) from subjects"
        rqt7 = "select COUNT(DISTINCT tr_cnt) from tutor"
        cursor.execute(rqt5)
        result5 = cursor.fetchone()
        cursor.execute(rqt6)
        result6 = cursor.fetchone()
        cursor.execute(rqt7)
        result7 = cursor.fetchone()

        cnt.commit()
        cursor.close()
        cnt.close()
        context={"subjects" : result, "tutors" : result2, "countries" : result3, "languages_spoken" : result4, "number_tutor" : result5[0], "number_subject" : result6[0], "number_country" : result7[0] }
        return render(request,'findtutor.html',context)

def tutor_video(request, email):
    cnt=sql.connect(host="127.0.0.1", user="root", passwd="Said&10112001", database="prdb1")
    var1 = str(email).strip()
    cursor=cnt.cursor()
    rqt = "select * from tutor where Email ='{}'".format(var1)
    cursor.execute(rqt)
    result = cursor.fetchone()
    rqt1 = "select id_sbj, Name_sbj from Subjects"
    cursor.execute(rqt1)
    result1 = cursor.fetchall()
    rqt2 = "select * from country"
    cursor.execute(rqt2)
    result2 = cursor.fetchall()


    context = {"tutor" : result, "subjects" : result1, "countries" : result2}
    cursor.close()
    cnt.close()

    return render(request, "tutor_video.html", context)

