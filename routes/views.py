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
from .models import Route


class RouteListView(LoginRequiredMixin, ListView):
    context_object_name = 'routes'
    model = Route
    paginate_by = 10


class RouteDetailView(LoginRequiredMixin, DetailView):
    model = Route


class RouteCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    fields = ['form', 'user', 'group']
    model = Route
    success_url = reverse_lazy('routes:list')
    success_message = "Route created."


class RouteUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    fields = ['form', 'user', 'group']
    model = Route
    success_message = "Route updated."


class RouteDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Route
    success_url = reverse_lazy('routes:list')
    success_message = "Route deleted."
