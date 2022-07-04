import filecmp
import subprocess
import os

problemid=1

temp1='C:/Users/Ratin/Project/OJ/testcases/avaiv.cpp'
input='C:/Users/Ratin/Project/OJ/testcases/1.input.txt'
outputt='C:/Users/Ratin/Project/OJ/testcases/1.output.txt'
temp2 = r"C:\Users\Ratin\Project\OJ\Submissions\%s"%problemid + ".cpp"

avai=open(temp2,'w')

writes="#include<bits/stdc++.h>using namespace std; int main() {int n;cin>>n;while(n){int x,y;cin>>x>>y;cout<<x+y<<endl;n--;}return 0;}"

code=open(temp1,'wb+')

writes=bytes(writes,'utf-8')
code.write(writes)

expected_output=open(outputt,'r').read()


input_file=open(input,'r')


subprocess.run(["g++",temp1],shell=True)

print(code.read() )

process = subprocess.run('a.exe',stdin=input_file, shell=True, capture_output=True,text=True)
    
user_output = process.stdout.strip()

#print(temp2)

#print(expected_output)

if(expected_output==user_output):
  print("Nacho")
else:
  print("bedgarkh")

#print(user_output)