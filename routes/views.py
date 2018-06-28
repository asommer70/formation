from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
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
from forms.models import Form


User = get_user_model()


class RouteListView(LoginRequiredMixin, ListView):
    context_object_name = 'routes'
    model = Route
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['forms'] = Form.objects.all()
        return context


class RouteDetailView(LoginRequiredMixin, DetailView):
    model = Route


class RouteCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    fields = ['form', 'user', 'group']
    model = Route
    success_url = reverse_lazy('routes:list')
    success_message = "Route created."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.all()
        context['groups'] = Group.objects.all()
        return context


class RouteUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    fields = ['form', 'user', 'group']
    model = Route
    success_message = "Route updated."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.all()
        context['groups'] = Group.objects.all()
        print('RouteUpdateView context:', context)
        return context


class RouteDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Route
    success_url = reverse_lazy('routes:list')
    success_message = "Route deleted."
