from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView, View
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib.messages.views import SuccessMessageMixin
from . models import *
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required
def task_home(request):
    task = Task.objects.all().order_by('-created')


    search_query = request.GET.get('search',  '')
    #if search_query:
        #tasks =Task.objects.filter(Q(depart__icontains=search_query))
    template_name = 'task/app-todo.html'
    context = {'Task':task}

    return render(request, template_name, context)

@login_required
def task_detail(request, slug):
    task = get_object_or_404(Task, slug=slug)
    #products = Product.objects.all()

    template_name = 'task/task_details.html'
    context = {'task':task}
    return render(request, template_name, context)



class add_task(SuccessMessageMixin, CreateView):
    model = Task
    template_name = 'task/forms/add_task.html'
    fields = '__all__'
    exclude = ('slug',)
    success_url = reverse_lazy('task:task-home')
    success_message = 'The Task have been successfully Created'

    def form_valid(self, form):
        print('form valid')
        print(form.cleaned_data)
        return super().form_valid(form)
class edit_task(SuccessMessageMixin, UpdateView):
    model = Task
    template_name = 'task/forms/edit_task.html'
    fields = [ 'employee', 'comments', 'priority', 'state', 'expiry_date']
    exclude = ('slug',)
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('task:task-home')
    success_message = 'The Task have been successfully Edited'
 