from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Task
from .forms import TaskForm


class TaskListView(ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'


class TaskCompleteView(View):
    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        task.completed = True
        task.save()
        return redirect('tasks:task-list')


class TaskDetailView(DetailView):
    model = Task
    template_name = 'tasks/task_detail.html'


class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'


class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'


class TaskDeleteView(DeleteView):
    model = Task
    template_name = 'tasks/task_confirm_delete.html'
    success_url = reverse_lazy('tasks:task-list')
