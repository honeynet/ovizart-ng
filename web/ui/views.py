# Create your views here.

from django import forms
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
import os
import time

@login_required
def index(request):
    analysisList = request.user.ovizart.getAnalysis()
    for a in analysisList:
        a['id'] = a['_id']
        del a['_id']

        ts = a['startTime']
        a['startTime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(ts))

        for f in a['files']:
            f['filename'] = os.path.basename(f['filename'])

    return render_to_response('index.html', {'analysisList': analysisList, 'username': request.user.username})


def login(request):
    # Check for credentials
    data = {}
    form_elements = ['username', 'password', 'protocol', 'host', 'port']
    isParametersValid = True
    for element in form_elements:
        if element in request.POST:
            from django.utils.html import escape
            data[element] = escape(request.POST[element])
            print '#', element, data[element]
        else:
            isParametersValid = False
            break

    if isParametersValid:
        from django.contrib.auth import authenticate, login
        user = authenticate(username=data['username'], password=data['password'], protocol=data['protocol'],
                            host=data['host'], port=data['port'])
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return render_to_response('login.html', {'error_msg': 'Invalid credentials'})
    else:
        return render_to_response('login.html', RequestContext(request, {}))


def logout(request):
    import django
    django.contrib.auth.logout(request)
    return redirect('/login')


class UploadFileForm(forms.Form):
    #title = forms.CharField(max_length=50)
    file = forms.FileField()


def handle_uploaded_file(f):
    uploaded_file = '/tmp/uploaded.bin'
    with open(uploaded_file, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    #with open(uploaded_file, 'r') as destination:
    import sys
    sys.path.append('../')
    sys.path.append('../../')
    from core.ovizart_proxy import OvizartProxy
    op = OvizartProxy(protocol='https')
    op.login('ggercek', '123456')
    response = op.uploadFile(uploaded_file)
    # TODO: Do something with the result


# @login_required
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return HttpResponse("OK")
    else:
        form = UploadFileForm()
    return render_to_response('upload.html',  RequestContext(request,  {'form': form}))
