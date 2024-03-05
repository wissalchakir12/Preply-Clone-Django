import os
from django.conf import settings
from django.shortcuts import redirect, render
from flask import app
import mysql.connector as sql
from django.core.files.storage import FileSystemStorage
from .models import Video  # Import your Video model here



em=None
pwd=None
def become_tutor(request):
    if request.method == 'POST':
        cnt=sql.connect(host="127.0.0.1", user="root", passwd="Said&10112001", database="prdb1")
        cursor=cnt.cursor()
        em = str(request.POST.get("email", "")).strip()
        pwd = str(request.POST.get("Password", "")).strip()
        rqt="select count(*) from tutor where Email='{}' ".format(em)
        cursor.execute(rqt)
        result = cursor.fetchone()
        if len(pwd) >= 7:
            if pwd.isdigit():
                ch_er = 1 #password all number
                context = {"Error" : "This password is too common. This password is entirely numeric.", "isError" : ch_er}
                cnt.commit()
                cnt.close()
                return render(request,'become_tutor.html', context)
            if result[0] > 0:
                rqt2="select check_info from tutor where Email='{}' and password_tr='{}'".format(em,pwd)
                cursor2=cnt.cursor()
                cursor2.execute(rqt2)
                result3 = cursor2.fetchone()
                if result3[0] == False:
                    request.session['tutor_signup'] = em.strip()
                    cnt.commit()
                    cnt.close()
                    return redirect('tutor_signup')
                else:
                    ch_er = 3 #user exists 
                    context = {"Error" : "A User with this email already exists.", "isError" : ch_er}
                    cnt.commit()
                    cnt.close()
                    return render(request,'become_tutor.html', context)
            else:
                rqt13="select count(*) from students where Email='{}' ".format(em)
                cursor2=cnt.cursor()
                cursor2.execute(rqt13)
                result33 = cursor2.fetchone()
                if result33[0] > 0:
                    ch_er = 3 #user exists
                    context = {"Error" : "A User with this email already exists.", "isError" : ch_er}
                    return render(request,'become_tutor.html', context)
                else:
                    request.session['tutor_signup'] = em.strip()  # Example user ID
                    c="insert into tutor(Email,password_tr) values ('{}','{}')".format(em,pwd)
                    cursor2=cnt.cursor()
                    cursor2.execute(c)
                    cnt.commit()
                    cnt.close()
                    return redirect('tutor_signup')
        else:
            ch_er = 2 #password short
            context = {"Error" : "This password is too short. It must contain at least 7 characters. This password is too common.", "isError" : ch_er}
            return render(request,'become_tutor.html', context)
    else:
        return render(request,'become_tutor.html')
    
    
fn_ = None   
ln_ = None
selected_country = None
lng = None

def tutor_signup (request):
    if request.method == 'POST':
        cnt=sql.connect(host="127.0.0.1", user="root", passwd="Said&10112001", database="prdb1")
        cursor6=cnt.cursor()

        #Country
        rqt6="select id_cnt , Name_cnt from country"
        cursor6.execute(rqt6)
        result = cursor6.fetchall()

        #Languages
        cursor7=cnt.cursor()
        rqt7="select Name_lng from Languages"
        cursor7.execute(rqt7)
        result2 = cursor7.fetchall()

        #Levels
        cursor8=cnt.cursor()
        rqt8="select Name_lvl from Levels"
        cursor8.execute(rqt8)
        result3 = cursor8.fetchall()

        #Subjects
        cursor9=cnt.cursor()
        rqt9="select id_sbj, Name_sbj from Subjects"
        cursor9.execute(rqt9)
        result4 = cursor9.fetchall()


        #Languages and levels
        
        cursor1=cnt.cursor()
        fn_ = str(request.POST.get("firstName", "")).strip()
        ln_ = str(request.POST.get("LastName", "")).strip()
        selected_country = request.POST.get('teachingExperience')

        lng = request.POST.getlist("language")
        list_lng=["English"]
        for item in lng:
            list_lng.append(item)

        lvl = request.POST.getlist("level")
        list_lvl=[]
        for item in lvl:
            list_lvl.append(item)

       

        
        
        
        sbj_ = request.POST.get('sbj_')

        phone_n = request.POST.get('phone_n')

        checkbox_ = request.POST.get('checkbox_')

        uploaded_file = request.FILES['uploaded_file']

        # Define the directory where you want to save the uploaded image
        save_directory = os.path.join(settings.MEDIA_ROOT, 'images')

        # Ensure the directory exists; create it if not
        os.makedirs(save_directory, exist_ok=True)

        # Build the complete path for the uploaded image
        image_path = os.path.join(save_directory, uploaded_file.name)

        # Save the uploaded image to the specified path
        with open(image_path, 'wb') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        video_file = request.FILES.get('video_tutor')

        if video_file:
            # Get the title from the form
            title = video_file.name

            # Save the uploaded video to the 'media' directory (configured in settings)
            media_root = settings.MEDIA_ROOT
            video_path = os.path.join(media_root, 'videos', video_file.name)

            with open(video_path, 'wb') as destination:
                for chunk in video_file.chunks():
                    destination.write(chunk)

        tutor_signup = request.session.get('tutor_signup')
        
        rqt11 = "update tutor set firstname = '{}' ,lastname = '{}' ,check_info = '{}' ,tr_cnt='{}' ,Subject_taugh='{}' ,phone_nbr = '{}' ,adult ='{}' ,Image = '{}', video_tutor = '{}' where Email = '{}'".format(fn_,ln_,1,selected_country,sbj_,phone_n,1,uploaded_file.name,video_file.name,tutor_signup)
        cursor1.execute(rqt11)

        for i in range(len(list_lng)):
            rqt12 = "insert into languages_spoken values('{}','{}','{}')".format(tutor_signup,list_lng[i],list_lvl[i])
            cursor1.execute(rqt12)

        del request.session['tutor_signup']
        
        context={'country' : result , 'Languages' : result2, 'Levels' : result3, 'Subjects' : result4, 'sbj_' : tutor_signup}

        cursor6.close()
        cnt.commit()
        cnt.close()
        return redirect('login') 
    
    else:
        cnt=sql.connect(host="127.0.0.1", user="root", passwd="Said&10112001", database="prdb1")
        cursor6=cnt.cursor()

        #Country
        rqt6="select id_cnt , Name_cnt from country"
        cursor6.execute(rqt6)
        result = cursor6.fetchall()

        #Languages
        cursor7=cnt.cursor()
        rqt7="select Name_lng from Languages"
        cursor7.execute(rqt7)
        result2 = cursor7.fetchall()

        #Levels
        cursor8=cnt.cursor()
        rqt8="select Name_lvl from Levels"
        cursor8.execute(rqt8)
        result3 = cursor8.fetchall()

        #Subjects
        cursor9=cnt.cursor()
        rqt9="select id_sbj, Name_sbj from Subjects"
        cursor9.execute(rqt9)
        result4 = cursor9.fetchall()

        context={'country' : result , 'Languages' : result2, 'Levels' : result3, 'Subjects' : result4}

        cursor6.close()
        cnt.commit()
        cnt.close()
        return render (request,'tutor_signup.html',context)

def logout_view(request):
    # Log the user out
    del request.session['tutor_signup']
    return redirect('become_tutor') 
  
def lessons(request):
    cnt=sql.connect(host="127.0.0.1", user="root", passwd="Said&10112001", database="prdb1")
    cursor = cnt.cursor()

    # Execute a SQL query to fetch video data
    query = "SELECT title, video_path, description FROM lessons"
    cursor.execute(query)

    # Fetch all video records
    video_data = cursor.fetchall()

    cursor.close()
    cnt.close()

    
    return render(request, 'lessons.html', {'videos': video_data})
        






def add_lessons(request):
    cnt=sql.connect(host="127.0.0.1", user="root", passwd="Said&10112001", database="prdb1")
    if request.method == 'POST':
        video_file = request.FILES.get('video')

        if video_file:
            # Get the title from the form
            title = video_file.name

            # Save the uploaded video to the 'media' directory (configured in settings)
            media_root = settings.MEDIA_ROOT
            video_path = os.path.join(media_root, 'videos', video_file.name)

            with open(video_path, 'wb') as destination:
                for chunk in video_file.chunks():
                    destination.write(chunk)

            cursor = cnt.cursor()
            name=str(request.POST.get("title", "")).strip()
            desc=str(request.POST.get("description", "")).strip()
            email = request.session.get('tutor_add_l')
            # Define the SQL query using .format() with placeholders
            insert_sql = "INSERT INTO lessons (title, description, email_tutor, video_path ) VALUES (%s, %s, %s, %s)"
            cursor.execute(insert_sql, (name, desc,  email,  title))
            cnt.commit()
            cursor.close()
            cnt.close()
            return redirect('lessons')

        return render(request, 'lessons.html')

    return render(request, 'add_lessons.html')
