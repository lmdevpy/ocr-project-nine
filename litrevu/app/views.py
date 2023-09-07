from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import authenticate, login
from django.views.generic import ListView
from django.views.generic import UpdateView
from django.views.generic.edit import FormView, CreateView
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django import forms
from .models import Ticket, User, Review, UserFollows
from .forms import TicketCreationForm, ReviewCreationForm, TicketAndReviewForm, FollowUserForm


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'


class CustomLogoutView(LogoutView):
    pass


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class CustomSignUpView(FormView):
    template_name = 'signup.html'
    form_class = SignUpForm

    def form_valid(self, form):
        user = form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(self.request, user)
            return redirect('login')  # Redirect to the login page after signing up
        return self.form_invalid(form)


class CustomLoginView(LoginView):
    template_name = 'login.html'


class CustomLoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)


class CustomFormView(FormView):
    template_name = 'login.html'
    form_class = CustomLoginForm

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(self.request, user)
            return redirect('home')
        return self.form_invalid(form)


class TicketCreateView(CreateView):
    model = Ticket
    form_class = TicketCreationForm
    template_name = 'create-ticket.html'
    # success_url = reverse_lazy('ticket-list')

    def get_success_url(self):
        return reverse_lazy('ticket-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TicketListView(ListView):
    model = Ticket
    template_name = 'ticket-list.html'
    context_object_name = 'tickets'


class TicketUpdateView(UpdateView):
    model = Ticket
    fields = ['title', 'description', 'image']
    template_name = 'ticket-update.html'

    def get_success_url(self):
        return reverse('ticket-list')


class ReviewCreateView(CreateView):
    model = Review
    form_class = ReviewCreationForm
    template_name = 'create-review.html'
    success_url = reverse_lazy('review-list')

    def dispatch(self, *args, **kwargs):
        if self.kwargs.get('ticket_id'):
            ticket_id = self.kwargs.get('ticket_id')
            self.ticket = get_object_or_404(Ticket, pk=ticket_id)
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.ticket:
            context['ticket'] = self.ticket
        return context

    def form_valid(self, form):
        if self.ticket:
            form.instance.ticket = self.ticket
        form.instance.user = self.request.user
        return super().form_valid(form)


class ReviewListView(ListView):
    model = Review
    template_name = 'review-list.html'
    context_object_name = 'reviews'


class ReviewUpdateView(UpdateView):
    model = Review
    fields = ['headline', 'rating', 'body']
    template_name = 'review-update.html'

    def get_success_url(self):
        return reverse('review-list')


class TicketAndReviewCreateView(CreateView):
    model = Ticket
    form_class = TicketAndReviewForm
    template_name = 'create-review-and-ticket.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class FollowUserView(FormView):
    form_class = FollowUserForm
    template_name = 'user-follow.html'
    success_url = reverse_lazy('user-follow')

    def form_valid(self, form):
        follow_username = form.cleaned_data['follow_username']
        user_to_follow = User.objects.get(username=follow_username)
        if user_to_follow:
            UserFollows.objects.create(user=self.request.user, followed_user=user_to_follow)
            return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class FollowedUsersView(ListView):
    template_name = 'user-follow.html'
    success_url = reverse_lazy('user-follow')
    model = UserFollows
    context_object_name = 'followed_users'


