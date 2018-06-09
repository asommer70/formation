from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Form


class FormListView(LoginRequiredMixin, ListView):
    context_object_name = 'forms'
    model = Form
    paginate_by = 10


class FormDetailView(LoginRequiredMixin, DetailView):
    model = Form


class FormCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    fields = ['name', 'content', 'public']
    model = Form
    success_url = reverse_lazy('forms:list')
    success_message = "Form created."


class FormUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    fields = ['name', 'content', 'public']
    model = Form
    success_message = "Form updated."


class FormDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Form
    success_url = reverse_lazy('forms:list')
    success_message = "Form deleted."
