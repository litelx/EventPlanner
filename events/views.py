import datetime

import geocoder
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse_lazy, reverse
from django.shortcuts import redirect, get_object_or_404
from django.utils.encoding import escape_uri_path
from django.views.generic import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, FormView, UpdateView
from django.views.generic.list import ListView
from django.contrib import messages

from . import forms
from . import models
# Create your views here.


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

        form.instance.latitude = geocoder.google(form.instance.location).latlng[0]
        form.instance.longitude = geocoder.google(form.instance.location).latlng[1]

        form.instance.host = self.request.user
        return super().form_valid(form)


class CreateEventView(LoggedInMixin, EventMixin, CreateView):
    def title(self):
        return "Add New event"


class UpdateEventView(LoggedInMixin, EventMixin, UpdateView):
    def title(self):
        return self.object.title


class DetialsEventView(DetailView):

    def title(self):
        return self.object.title
    model = models.Event
    success_url = reverse_lazy('events:update')

    def get_context_data(self, **kwargs):
        context = super(DetialsEventView, self).get_context_data(**kwargs)
        return context


class EventListView(LoggedInMixin, ListView):
    def title(self):
        return "Home"
    model = models.Event


class GuestListView(LoggedInMixin, ListView):
    page_title = "Home"
    # model = models.

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


class GuestResponseView(FormView):
    form_class = forms.GuestReponseForm
    template_name = "events/guest_reponse.html"

    def title(self):
        return "RSVP"

    def get_context_data(self, **kwargs):
        d = super().get_context_data(**kwargs)
        d['guest'] = get_object_or_404(models.Guest.objects, secret_code= self.kwargs['secret'])
        d['statuses'] = models.Guest.Status.choices
        return d

    def form_valid(self, form):
        # assert False, dir(form)
        guest = get_object_or_404(models.Guest.objects, secret_code= self.kwargs['secret'])
        guest.status = form.data['guest_response']
        # form.instance.date = datetime.date.today()
        o = guest.save()
        messages.success(self.request, 'Your response has been recorded')
        return redirect('events:details', pk=guest.event_id)
