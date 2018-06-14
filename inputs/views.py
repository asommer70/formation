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
from .models import Input


class InputListView(LoginRequiredMixin, ListView):
    context_object_name = 'inputs'
    model = Input
    paginate_by = 10


class InputCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    fields = ['data', 'form']
    model = Input
    success_url = reverse_lazy('inbox')


class InputDetailView(LoginRequiredMixin, DetailView):
    model = Input


class InputUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    fields = ['data']
    model = Input
    success_message = "Update successful."


class InputDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Input
    success_url = reverse_lazy('inbox:list')
    success_message = "Deletion complete."
