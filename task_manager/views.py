from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.urls import reverse_lazy
from django.views import generic
from django.views.decorators.http import require_POST

from task_manager.forms import (
    TaskNameSearchForm,
    TaskForm,
    TaskTypeForm,
    TaskTypeNameSearchForm,
    WorkerNameSearchForm,
    TagForm,
    TagNameSearchForm
)
from task_manager.models import Task, TaskType, Worker, Tag


@login_required
def index(request):
    workers = Worker.objects.all()[1:6]
    tasks = Task.objects.all().filter(is_completed=False)[:5]
    num_workers = Worker.objects.count()
    num_tasks = Task.objects.count()
    context = {
        "tasks": tasks,
        "workers": workers,
        "num_workers": num_workers,
        "num_tasks": num_tasks
    }
    html_template = loader.get_template("home/index.html")
    return HttpResponse(html_template.render(context, request))


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    context_object_name = "task_list"
    template_name = "task_manager/task_list.html"
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TaskListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = TaskNameSearchForm(initial={"name": name})
        return context

    def get_queryset(self):
        form = TaskNameSearchForm(self.request.GET)
        if form.is_valid():
            return Task.objects.all().filter(
                name__icontains=form.cleaned_data["name"]
            )
        return Task.objects.all()


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("task_manager:task-list")


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("task_manager:task-list")


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy("task_manager:task-list")


class TaskTypeListView(LoginRequiredMixin, generic.ListView):
    model = TaskType
    context_object_name = "task_type_list"
    template_name = "task_manager/task_type_list.html"
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TaskTypeListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = TaskNameSearchForm(initial={"name": name})
        return context

    def get_queryset(self):
        form = TaskTypeNameSearchForm(self.request.GET)
        if form.is_valid():
            return TaskType.objects.all().filter(
                name__icontains=form.cleaned_data["name"]
            )
        return TaskType.objects.all()


class TaskTypeDetailView(LoginRequiredMixin, generic.DetailView):
    model = TaskType


class TaskTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = TaskType
    form_class = TaskTypeForm
    success_url = reverse_lazy("task_manager:task-type-list")


class TaskTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = TaskType
    success_url = reverse_lazy("task_manager:task-type-list")


class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = Worker
    context_object_name = "worker_list"
    template_name = "task_manager/worker_list.html"
    queryset = Worker.objects.all().select_related("position")
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(WorkerListView, self).get_context_data(**kwargs)
        first_name = self.request.GET.get("first_name", "")
        context["search_form"] = WorkerNameSearchForm(
            initial={"first_name": first_name}
        )
        return context

    def get_queryset(self):
        form = WorkerNameSearchForm(self.request.GET)
        if form.is_valid():
            return self.queryset.filter(
                first_name__icontains=form.cleaned_data["first_name"],
            )
        return self.queryset


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Worker
    queryset = Worker.objects.all().prefetch_related("tasks__task_type")


class TagListView(LoginRequiredMixin, generic.ListView):
    model = Tag
    context_object_name = "tag_list"
    template_name = "task_manager/tag_list.html"
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TagListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = TaskNameSearchForm(
            initial={"name": name}
        )
        return context

    def get_queryset(self):
        form = TagNameSearchForm(self.request.GET)
        if form.is_valid():
            return Tag.objects.all().filter(
                name__icontains=form.cleaned_data["name"],
            )
        return Tag.objects.all()


class TagCreateView(LoginRequiredMixin, generic.CreateView):
    model = Tag
    form_class = TagForm
    success_url = reverse_lazy("task_manager:tag-list")


class TagUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Tag
    form_class = TagForm
    success_url = reverse_lazy("task_manager:tag-list")


class TagDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Tag
    success_url = reverse_lazy("task_manager:tag-list")


@login_required
@require_POST
def toggle_task_completed(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.is_completed = not task.is_completed
    task.save()
    return redirect("task_manager:task-list")
