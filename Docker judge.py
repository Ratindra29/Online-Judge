import docker
import subprocess
import filecmp
import os


client = docker.from_env()


inputfile=r"C:\Users\Ratin\Project\OJ\testcases\1.input.txt"
tester=r"C:\Users\Ratin\Project\OJ\tester.txt"

code=open(inputfile,'r')

container=client.containers.get("OJcpp")
process=subprocess.run(['docker','cp','test.cpp',container.id+':a.cpp'],shell=True)
process=subprocess.run(['docker','cp',inputfile,container.id+':input'],shell=True)

print("yaha tak1")

subprocess.run(['docker','exec',container.id,'bash','-c',"g++ a.cpp"],shell=True)

print("yaha tak 2")
process=subprocess.run(['docker','exec',container.id,'bash','-c',"./a.out <input>output.txt"],shell=True)
process=subprocess.run(['docker','cp',container.id+':output.txt',tester],shell=True)

outputpath=r"C:\Users\Ratin\Project\OJ\testcases\1.output.txt"
expected=open(outputpath,'r').read()




print("yaha tak 3")

uoutput= open(tester,'r').read().strip()




print(process.returncode)
print("yaha tak 4")

print(uoutput==expected)


#print(filecmp("tester.txt",outputpath))

print("yaha tak 5")



