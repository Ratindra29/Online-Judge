from django.shortcuts import get_object_or_404,render
from django.http import HttpResponse,Http404
from django.utils import timezone
import subprocess,os,sys
import filecmp
import shutil

import os.path




from .models import Problem,Testcase,Submission,User



def index(request):
    Problem_list = Problem.objects.order_by('problemid')
    context = {'Problem_list': Problem_list}
    return render(request, 'practice/index.html', context)
# Leave the rest of the views (detail, results, vote) unchanged



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
    
    #creating the submission file
    code_file=open(temp,'wb+') 


    code=request.POST.get('code')
    #we need to convert the code that we get from form to bytes to use the write command
    code=bytes(code,'utf-8')
    code_file.write(code)
    
    #now in the submission file the text is copied from code , we need to convert it to bytes to allow subprocess to run it
    code_file=bytes(temp,'utf-8')
    
    
    #if there is a problem while compiling we set the verdict as compilation error
    compile=subprocess.run(["g++",temp],shell=True)
    verdict=""

    if(compile.returncode!=0):
        verdict="Compilation Error"

    expected_output=open(output,'r').read()

    input_file=open(input,'r')

    process = subprocess.run('a.exe', stdin=input_file,shell=True, capture_output=True,text=True)
     
    
    user_output= process.stdout.strip()


    # we need to check if there was a problem in compiling the submitted code as even after compilation error there might be previous "a.exe" file of previous code available in the system
    if(process.returncode!=0 ):
        verdict="Compilation Error"
    elif(expected_output==user_output and verdict!="Compilation Error"):
        verdict="Answer Correct"
    elif(verdict!="Compilation Error"):
        verdict="Wrong answer"
    
    submission=Submission()
    temp=str(temp)

    submission.problemid=Problem.objects.get(pk=problemid)
    submission.answercode=temp
    submission.verdict=verdict
    submission.save()

    
    return HttpResponse("Your Anwer verdict is %s." % verdict)



    
    
    


    
