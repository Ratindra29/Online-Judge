from django.shortcuts import get_object_or_404,render
from django.http import HttpResponse,Http404
from django.utils import timezone
import subprocess,os,sys
import filecmp
import docker

import os.path

from .models import Problem,Testcase,Submission,User

#creating a Docker client to perform docker operations using Docker SDK for python

client = docker.from_env()

#creating a docker image for C++
docker_img_cpp = 'gcc:11.2.0'






def index(request):
    Problem_list = Problem.objects.order_by('problemid')
    context = {'Problem_list': Problem_list}
    return render(request, 'practice/index.html', context)




def detail(request, problemid):
    problem = get_object_or_404(Problem, pk=problemid)
    return render(request, 'practice/detail.html', {'problem': problem})

def results(request, problemid):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % problemid)

def submit(request, problemid):

    input=Testcase.objects.get(pk=problemid).inputdoc
    output=Testcase.objects.get(pk=problemid).outputdoc
  
   #We can Store the submitted file in this path with dynamic name (problemid)
    temp =r"C:\Users\Ratin\Project\OJ\Submissions\%s"%problemid + ".cpp" 

   #This is the file where we store useroutput to compare with expected output
    tester=r"C:\Users\Ratin\Project\OJ\tester.txt"
    
    #creating the submission file
    code_file=open(temp,'wb+') 


    code=request.POST.get('code')


    #we need to convert the code that we get from form to bytes to use the write command
    code=bytes(code,'utf-8')
    code_file.write(code)
    
    #now in the submission file the text is copied from code , we need to convert it to bytes to allow subprocess to run it
    code_file=bytes(temp,'utf-8')

    

    #---------------------------------------------------------------------------------------------------------------------------------------
    #----------------------------------------DOCKER USED HERE-------------------------------------------------------------------------------
    #---------------------------------------------------------------------------------------------------------------------------------------


    #if due to Mallicious code the container gets killed , we start a new container 
    try :
         container= client.containers.get("OJcpp")
         if(container.status!='running'):
                 container.start()
    except docker.errors.NotFound:
        container = client.containers.run(docker_img_cpp,detach=True,tty=True,name="OJcpp")
      
    

    #copying the user code and testcase input in container files 

    subprocess.run(['docker','cp',temp,container.id+':a.cpp'],shell=True)
    subprocess.run(['docker','cp',input,container.id+':input.txt'],shell=True)


    compile=subprocess.run(['docker','exec',container.id,'bash','-c',"g++ a.cpp"],shell=True)
    
    #if there is a problem while compiling we set the verdict as compilation error

    verdict=""
    if(compile.returncode!=0):
        verdict="Compilation Error"
   
    
    #the compiled code is run and output is saved in output.txt file in container

    process=subprocess.run(['docker','exec',container.id,'bash','-c',"./a.out <input.txt>output.txt"],shell=True)
    subprocess.run(['docker','cp',container.id+':output.txt',tester],shell=True)

    #-------------------------DOCKER USE FINISHED-------------------------------------------------------------------------------------------------------------------------------------------
    


    expected_output=open(output,'r').read()
    user_output=open(tester,'r').read().strip()


    # we need to check if there was a problem in compiling the submitted code as even after compilation error there might be previous "a.exe" file of previous code available in the system
    if(process.returncode!=0 ):
        verdict="Runtime Error"
    elif(expected_output==user_output and verdict!="Compilation Error"):
        verdict="Answer Correct"
    elif(verdict!="Compilation Error"):
        verdict="Wrong answer"
    


    #saving the submission

    submission=Submission()
    temp=str(temp)

    submission.problemid=Problem.objects.get(pk=problemid)
    submission.answercode=temp
    submission.verdict=verdict
    submission.save()

    
    return HttpResponse("Your Anwer verdict is %s." % verdict)



    
    
    


    
