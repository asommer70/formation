from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from itertools import chain
from operator import attrgetter
from .models import Input, Approval, Attachment
from .mixins import InputHolderMixin

User = get_user_model()


class InputListView(LoginRequiredMixin, ListView):
    context_object_name = 'inputs'
    model = Input
    # paginate_by = 10 # Might look into a better way to do this later...
    table_pagination = False

    def get_queryset(self, *args, **kwargs):
        if ('search' in self.request.GET):
            # Use a raw query to process the search in order to use the
            # PostgreSQL jsonb_each_text function for searching Input.data values.
            qs = Input.objects.raw('''
               select count(*) as num_rows, * from inputs_input 
               join jsonb_each_text(inputs_input.data) e on true 
               join auth_user on (inputs_input.user_id = auth_user.id)
               where e.value like %s and
                     (inputs_input.user_id = %s or
                     inputs_input.route_holder_id = %s)
               group by e.key, inputs_input.id, e.value, auth_user.id;
            ''', ['%' + self.request.GET['search'] + '%',
                  self.request.user.id, self.request.user.id])

            # Add the row count.
            qs.num_rows = sum(1 for q in qs)
        else:
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
        # context['input'].data['dyns'] = ''

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


class ApprovalListView(LoginRequiredMixin, ListView):
    context_object_name = 'approvals'
    model = Approval
    paginate_by = 6

    def get_queryset(self, *args, **kwargs):
        qs = super(ApprovalListView, self).get_queryset(*args, **kwargs).filter(
            user=self.request.user
        )
        return qs
    

@login_required()
def add_attachment(request, pk):
    if request.method == 'POST':
        print('request.POST:', request.POST)
        input = Input.objects.get(pk=pk)
        user = User.objects.get(pk=request.POST['user_id'])
        attachment = Attachment.objects.create(input=input, upload=request.FILES['file'], user=user)
        return HttpResponseRedirect(reverse('inbox:detail', args=[pk]))
    else: 
        return HttpResponseRedirect(reverse('inbox:detail', args=[pk]))
