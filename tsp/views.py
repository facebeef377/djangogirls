from django.shortcuts import render
from django.utils import timezone
from .models import Task, Instance
from django.http import JsonResponse
import json
from django.http import HttpResponse
from rest_framework import routers, serializers, viewsets
import ctypes as ct
import subprocess as sp
from rest_framework import generics
from .serializers import *

# Create your views here.

def task_run(request):
    return render(request, 'task_run.html',  {})

def start(self):
    test("test")
    return JsonResponse({'status':'OK'})

def get_data(self):
    tasks = Task.objects.order_by('created_date')
    return JsonResponse(serializers.serialize('json', tasks), safe=False)

def test(tmp):
    exe = sp.Popen(['mpirun', '-n', '4', '--hosts', 'master,slave2', './home/mpiuser/cloud/cpi'  ])
    exe.communicate()
    print (tmp)

def check_tasks(self):
    tasks = Task.objects.all()
    for task in tasks:
    	if(task.status != "100"):
            print("Rozpoczynam problem o nazwie: " + task.title)
            instance_id = 3; #instance_id = task.instance_id
            ins = Instance.objects.get(id=instance_id)
            file=open("dane.txt",'w')
            file.write(str(ins.cityCount) + "\n") #instance_id
            file.write(str(task.population) + "\n")
            file.write(str(task.generations) + "\n")
            file.write(str(task.wpz) + "\n")
            file.close()
            file=open("graph.txt",'w')
            file.write(ins.graph)
            file.close()
            #exe = sp.Popen(['mpirun -np 4 --hosts master3,slave4 TSP_moj/BBC'],stdout=sp.PIPE,shell=True)
            print ("mpirun -np " + task.proc + " --hosts master3,slave4 ./TSP" )
            running = 1
            while(running):
                file=open("status.txt",'r')
                stat=file.read()
                task.status = stat
                task.save()
                file.close()
                if(exe.poll() == 0):
                    running = 0
                    print("Koniec tego!")
                time.sleep(1)
            #Put to history
            #exe.communicate()
            #Sebek cioto mozesz jeszcze to porownac po statusie z pliku xD
    return JsonResponse({'status':'OK'})



class CreateView(generics.ListCreateAPIView):
    """This class defines the create behavior of our rest api."""
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def perform_create(self, serializer):
        """Save the post data when creating a new bucketlist."""
        serializer.save()

class DetailsView(generics.RetrieveUpdateDestroyAPIView):
    """This class handles the http GET, PUT and DELETE requests."""

    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class UserTaskList(generics.ListAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        username = self.kwargs['owner_id']
        return Task.objects.filter(owner_id=username)





class CreateView_Instance(generics.ListCreateAPIView):
    queryset = Instance.objects.all()
    serializer_class = InstanceSerializer

    def perform_create(self, serializer):
        serializer.save()

class DetailsView_Instance(generics.RetrieveUpdateDestroyAPIView):
    queryset = Instance.objects.all()
    serializer_class = InstanceSerializer

class UserTaskList_Instance(generics.ListAPIView):
    serializer_class = InstanceSerializer

    def get_queryset(self):
        username = self.kwargs['owner_id']
        return Instance.objects.filter(owner_id=username)




class CreateView_History(generics.ListCreateAPIView):
    queryset = History.objects.all()
    serializer_class = HistorySerializer

    def perform_create(self, serializer):
        serializer.save()

class DetailsView_History(generics.RetrieveUpdateDestroyAPIView):
    queryset = History.objects.all()
    serializer_class = HistorySerializer

class UserTaskList_History(generics.ListAPIView):
    serializer_class = HistorySerializer

    def get_queryset(self):
        username = self.kwargs['owner_id']
        return History.objects.filter(owner_id=username)
