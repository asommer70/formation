from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from itertools import chain
from operator import attrgetter
from .models import Input, Approval
from .mixins import InputHolderMixin

User = get_user_model()


class InputListView(LoginRequiredMixin, ListView):
    context_object_name = 'inputs'
    model = Input
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        qs = super(InputListView, self).get_queryset(*args, **kwargs).filter(
            Q(user=self.request.user) | Q(route_holder=self.request.user)
        ).exclude(status='archived')
        return qs


class InputCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    fields = ['data', 'form']
    model = Input
    success_url = reverse_lazy('inbox')


class InputDetailView(LoginRequiredMixin, InputHolderMixin, DetailView):
    model = Input

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Add a next_user attribute to the Input.data in order to send
        # the Input to the next user, also add a blank comment attribute.
        context['input'].data['next_user'] = ''
        context['input'].data['comment'] = ''
        context['input'].data['attachment'] = ''

        # Used for deciding which user to send the Input to.
        context['users'] = User.objects.all()
        return context


class InputUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    fields = ['data']
    model = Input
    success_message = "Update successful."


class InputDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Input
    success_url = reverse_lazy('inbox:list')
    success_message = "Deletion complete."


class ArchiveListView(LoginRequiredMixin, ListView):
    context_object_name = 'inputs'
    model = Input
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        qs = super(ArchiveListView, self).get_queryset(*args, **kwargs).filter(
            Q(user=self.request.user), Q(status='archived')
        )
        return qs

    def get_context_data(self,  *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['approvals'] = Approval.objects.filter(
            user=self.request.user
        ).order_by(
            'input_id',
            '-created_at').distinct('input_id')
        return context

