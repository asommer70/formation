from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Form


class FormListView(LoginRequiredMixin, ListView):
    context_object_name = 'forms'
    model = Form
    paginate_by = 10
