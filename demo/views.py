import json

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.template import RequestContext
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST

from django.contrib.sessions.models import Session

from demo.models import Task


def home(request):
    if not request.session.exists(request.session.session_key):
        request.session.create()
    
    return render(request, "homepage.html", {
        "tasks": Task.objects.filter(
            session__session_key=request.session.session_key
        ),
        "done_count": Task.objects.filter(
            session__session_key=request.session.session_key,
            done=True
        ).count()
    })


def complete_count_fragment(request):
    data = {
        "html": render_to_string(
            "_complete_count.html",
            RequestContext(request, {
                "done_count": Task.objects.filter(
                    done=True,
                    session__session_key=request.session.session_key
                ).count()
            })
        )
    }
    return HttpResponse(json.dumps(data), mimetype="application/json")


def _task_data(request, task):
    data = {
        "html": render_to_string(
            "_task.html",
            RequestContext(request, {
                "task": task
            })
        )
    }
    return data


@require_POST
def mark_done(request, pk):
    task = get_object_or_404(Task,
        session__session_key=request.session.session_key,
        pk=pk
    )
    task.done = True
    task.save()
    data = _task_data(request, task)
    return HttpResponse(json.dumps(data), mimetype="application/json")


@require_POST
def mark_undone(request, pk):
    task = get_object_or_404(Task,
        session__session_key=request.session.session_key,
        pk=pk
    )
    task.done = False
    task.save()
    data = _task_data(request, task)
    return HttpResponse(json.dumps(data), mimetype="application/json")


@require_POST
def add(request):
    session = Session.objects.get(session_key=request.session.session_key)
    task = Task.objects.create(
        session=session,
        label=request.POST.get("label")
    )
    data = _task_data(request, task)
    return HttpResponse(json.dumps(data), mimetype="application/json")


@require_POST
def delete(request, pk):
    task = get_object_or_404(Task,
        session__session_key=request.session.session_key,
        pk=pk
    )
    task.delete()
    data = {
        "html": ""
    }
    return HttpResponse(json.dumps(data), mimetype="application/json")
