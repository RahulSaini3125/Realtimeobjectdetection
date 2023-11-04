from django.http import StreamingHttpResponse
from django.shortcuts import redirect, render
import cv2 as cv
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required



# *********************************************** landing python and views *************************************************
# ******* Views **********
def landing_page(request):
    if request.method == "POST":
        email = request.POST.get('useremail')
        password = request.POST.get('password')
        gets_user = authenticate(request,username = email, password = password)
        if gets_user is not None:
            login(request, gets_user)
            return redirect(home)
        else:
            return redirect(landing_page) 
            
    return render(request, 'app/index.html')


def Sign_in(request):
    return render(request, 'app/Sign_in.html') 

def sign_in_form(request):
    if request.method == "POST":
         first_name = request.POST.get('first_name')
         last_name = request.POST.get('last_name')
         email = request.POST.get('user_email')
         passwords = request.POST.get('user_password')
         set_user = User.objects.create_user(email,email,passwords)
         set_user.first_name = first_name
         set_user.last_name = last_name
         #gets_data = signin_form(username_signin = name, useremail_signin = email, userpassword_signin = password)
         set_user.save()
         return redirect(landing_page) 
    return render(request, 'app/Sign_in.html')  



# **************************************************************************************************************************



# *********************************************** Home python and views ****************************************************

# ******* Views **********
@login_required(login_url='landing_page')

def home(request):
    return render(request, 'app/home.html',{"name": request.user.get_full_name()})

# **************************************************************************************************************************



# *********************************************** Camera python and views **************************************************


def get_frame(video):
     cap = cv.VideoCapture()
     if video == "Video":
         cap = cv.VideoCapture(0);
     else:
         cap = cv.VideoCapture(); 
     while cap.isOpened :
          ret,frame = cap.read()
          if not ret:
              break;
          config_file = 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
          forzen_model = 'frozen_inference_graph.pb'
          model = cv.dnn_DetectionModel(forzen_model, config_file)
          classlabel = []
          file_name = 'classes.txt'
          with open(file_name, 'rt') as fpt:
               classlabel = fpt.read().rstrip('\n').split('\n')
               model.setInputSize(320,320)
               model.setInputScale(1.0/127.5)
               model.setInputMean((127.5,127.5,127.5))
               model.setInputSwapRB(True)
               classindex, confidece, bbox = model.detect(frame,confThreshold = 0.3)
               font_scale = 3
               font = cv.FONT_HERSHEY_PLAIN
               for classind, conf, boxes in zip(classindex.flatten(), confidece.flatten(), bbox):
                    cv.rectangle(frame,boxes,(255,0,0),2)
                    ret, Buffer = cv.imencode('.jpg', frame)
                    video_frame = Buffer.tobytes()
                    yield (b'--frame\r\n'
                         b'Content-Type: image/jpeg\r\n\r\n' + video_frame + b'\r\n')
                    
input = "None";
                 
def video_feed(request): 
    global change
    cam = change
    return StreamingHttpResponse(get_frame(cam),content_type="multipart/x-mixed-replace;boundary= frame")
            
            

# ******* Views **********
@login_required(login_url='landing_page')

def camera_site(request):
    global input 
    global change
    change = input;
    if request.method == "POST":
            change = request.POST.get('input')
    return render(request,'app/camera_site.html',{"name": request.user.get_full_name(), "input_value": change})

# **************************************************************************************************************************


# ********************************************** About Us python and views *************************************************

# ******* Views **********
@login_required(login_url='landing_page')

def about(request):
    titles = "About Us";
    return render(request, 'app/about.html', {"name": request.user.get_full_name()})

# **************************************************************************************************************************



# ********************************************** Services python and views *************************************************

# ******* Views **********
@login_required(login_url='landing_page')

def service(request):
    return render(request, 'app/service.html', {"name": request.user.get_full_name()})

# **************************************************************************************************************************

# ********************************************** contact python and views *************************************************

# ******* Views **********
@login_required(login_url='landing_page')

def contact(request):
    return render(request, 'app/contact.html', {"name": request.user.get_full_name()})

# **************************************************************************************************************************

def logout_user(request):
     logout(request)
     return redirect(landing_page)
