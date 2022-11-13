
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .forms import UploadFileForm
from .models import CurriculumVitae


def index(request):
    message = {"message" : "success"}
    return render(request, "index.html",message)

def cv_treatment(request):
    print("\nthis is your cv\n")
    return HttpResponse("""<html><script>window.location.replace('/');</script></html>""")


def upload_file(request):
    if request.method=='POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return HttpResponse("yayyyyyyyyyyy")
    else:
        form = UploadFileForm()
    return render(request, "index2.html", {"form": form})