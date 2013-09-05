# Create your views here.

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