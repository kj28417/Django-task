from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from .forms import TaskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators  import login_required


def home(request):
    return render(request, "home.html")

@login_required
def tareas(request):
    tareas = Task.objects.filter(usuario=request.user, completada__isnull=True)
    return render(request, "tareas.html", {
        "tareas": tareas
    })


def registro(request):
    if request.method == "GET":
        return render(request, "singup.html", {
            "formulario": UserCreationForm
        })
    else:
        if request.POST["password1"] == request.POST["password2"]:
            try:
                Usuario = User.objects.create_user(
                    username=request.POST["username"], password=request.POST["password1"])
                Usuario.save()
                login(request, Usuario)
                return redirect("tareas")
            except:
                return render(request, "singup.html", {
                    "formulario": UserCreationForm,
                    "error": "El usuario ya existe"
                })
        return render(request, "singup.html", {
            "formulario": UserCreationForm,
            "error": "Contraseña invalida"
        })

@login_required
def cerrarSesion(request):
    logout(request)
    return redirect("/")


def iniciarSesion(request):
    if request.method == "GET":
        return render(request, "singin.html", {
            "form": AuthenticationForm
        })
    else:
        Usuario = authenticate(
            request, username=request.POST["username"], password=request.POST["password"])
        if Usuario is None:
            return render(request, "singin.html", {
                "form": AuthenticationForm,
                "error": "La contraseña y el usuario no coinsiden"
            })
        else:
            login(request, Usuario)
            return redirect("tareas")

@login_required
def crearTarea(request):
    if request.method == "GET":
        return render(request, "crear_tarea.html", {
            "form": TaskForm
        })
    else:
        form = TaskForm(request.POST)
        nuevaTarea = form.save(commit=False)
        nuevaTarea.usuario = request.user
        nuevaTarea.save()
        return redirect("tareas")

@login_required
def detalles(request, task_id):
    task = get_object_or_404(Task, pk=task_id, usuario=request.user)
    form = TaskForm(instance=task)
    if request.method == "GET":
        return render(request, "detalles_de_tareas.html", {
            "task": task,
            "form": form
        })
    else:
        try:
            task = get_object_or_404(Task, pk=task_id, usuario=request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect("tareas")
        except:
            return render(request, "detalles_de_tareas.html", {
                "task": task,
                "form": form,
                "error": "ha ocurrido un error"
                })

@login_required
def completada(request, task_id):
    task = get_object_or_404(Task, pk=task_id, usuario=request.user)
    if request.method == "POST":
        task.completada = timezone.now()
        task.save()
        return redirect("tareas")
    
@login_required    
def borrar(request, task_id):
    task = get_object_or_404(Task, pk=task_id, usuario=request.user)
    if request.method == "POST":
        task.delete()
        return redirect("tareas")
    
@login_required    
def tareaCompleta(request):
    tareas = Task.objects.filter(usuario=request.user, completada__isnull=False)
    return render(request, "tareas.html", {
        "tareas": tareas
    })