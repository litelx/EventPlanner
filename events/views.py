import datetime

import geocoder
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse_lazy, reverse
from django.db.models import Sum
from django.shortcuts import redirect
from django.utils.encoding import escape_uri_path
from django.views.generic import View
from django.views.generic.edit import CreateView, FormView, UpdateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from . import forms
from . import models
# Create your views here.
from django.http import HttpResponse


class LoginView(FormView):
    form_class = forms.LoginForm
    template_name = "login.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect('events:home')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])

        if user is not None and user.is_active:
            login(self.request, user)
            if self.request.GET.get('from'):
                return redirect(
                    self.request.GET['from'])  # SECURITY: check path
            return redirect('events:home')

        form.add_error(None, "Invalid user name or password")
        return self.form_invalid(form)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("login")


class LoggedInMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            url = reverse("login") + "?from=" + escape_uri_path(request.path)
            return redirect(url)
        return super().dispatch(request, *args, **kwargs)


class EventMixin:
    model = models.Event
    template = "events/event_form.html"
    fields = (
        'title',
        'start',
        'end',
        'description',
        'price',
        'status',
        'location',
    )
    success_url = reverse_lazy('events:home')

    def get_initial(self):
        return super().get_initial()

    def form_valid(self, form):
        # assert False, self.request.user.username
        form.instance.longitude = geocoder.google(form.instance.location).latlng[0]
        form.instance.latitude = geocoder.google(form.instance.location).latlng[1]

        form.instance.host = self.request.user
        return super().form_valid(form)


class CreateEventView(LoggedInMixin, EventMixin, CreateView):
    page_title = "Add New events"


class UpdateEventView(LoggedInMixin, EventMixin, UpdateView):
    page_title = "Edit events"


class DetialsEventView(DetailView):
    page_title = "event's Details"
    model = models.Event
    success_url = reverse_lazy('events:update')

    def get_context_data(self, **kwargs):
        context = super(DetialsEventView, self).get_context_data(**kwargs)
        return context


class EventListView(LoggedInMixin, ListView):
    page_title = "Home"
    model = models.Event


class GuestListView(LoggedInMixin, ListView):
    page_title = "Home"
    model = models.Event.host

# def get_queryset(self):
#     return super().get_queryset().filter(user=self.request.user)

# user = authenticate(username=form.cleaned_data['username'],
#                     password=form.cleaned_data['password'])
#
# if user is not None and user.is_active:
#     login(self.request, user)
#     if self.request.GET.get('from'):
#         return redirect(
#             self.request.GET['from'])  # SECURITY: check path
#     return redirect('events:home')
#
# form.add_error(None, "Invalid user name or password")
# return self.form_invalid(form)
