from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import Context, Template
from . import map_marker as mm
import os

def UploadView(request):
    if request.method == "POST": # I have given up on smart approach
        c = 1
        name= []
        for img in request.FILES.getlist('upload'):
            img = img.read()
            f = open(f"{c}.jpg","wb")
            f.write(img)
            f.close()
            name.append(f"{c}.jpg")
            c += 1
        m = mm.get_map(name)
        f = open("./mark/templates/mark/map.html","w")
        f.write(m)
        f.close()
        for n in name:
            os.remove(n)
            if os.path.exists(n + ".temp"):
                os.remove(n + ".temp")
        return render(request,"./mark/map.html")
    else:
        return render(request,"./mark/upload.html")