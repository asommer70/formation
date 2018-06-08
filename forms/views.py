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
    fields = ['name', 'public']
    model = Form
    success_url = reverse_lazy('forms:list')
    success_message = "Form created."


class FormUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    fields = ['name', 'public']
    model = Form
    # success_url = reverse_lazy('forms:detail')
    success_message = "Form updated."

    # def get_success_url(self):
    #    reverse_lazy('forms:detail', kwarks={'pk': self.object.pk})


class FormDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Form
    success_url = reverse_lazy('forms:list')
    success_message = "Form deleted."
