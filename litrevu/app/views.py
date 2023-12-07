from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import authenticate, login
from django.views.generic import ListView, UpdateView, DeleteView, FormView, CreateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Value, CharField, Q
from .models import Ticket, User, Review, UserFollows
from .forms import TicketCreationForm, ReviewCreationForm, TicketAndReviewForm, FollowUserForm
from itertools import chain


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


class TicketCreateView(LoginRequiredMixin, CreateView):
    model = Ticket
    form_class = TicketCreationForm
    template_name = 'create-ticket.html'
    success_url = reverse_lazy('ticket-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TicketListView(LoginRequiredMixin, ListView):
    model = Ticket
    template_name = 'ticket-list.html'
    context_object_name = 'tickets'


class TicketUpdateView(LoginRequiredMixin, UpdateView):
    model = Ticket
    fields = ['title', 'description', 'image']
    template_name = 'ticket-update.html'

    def get_success_url(self):
        return reverse('ticket-list')


class ReviewCreateView(LoginRequiredMixin, CreateView):
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


class ReviewListView(LoginRequiredMixin, ListView):
    model = Review
    template_name = 'review-list.html'
    context_object_name = 'reviews'


class ReviewUpdateView(LoginRequiredMixin, UpdateView):
    model = Review
    fields = ['headline', 'rating', 'body']
    template_name = 'review-update.html'

    def get_success_url(self):
        return reverse('review-list')


class ReviewDeleteView(LoginRequiredMixin, DeleteView):
    model = Review
    template_name = 'review-delete.html'
    success_url = reverse_lazy('posts')


class TicketAndReviewCreateView(LoginRequiredMixin, CreateView):
    model = Ticket
    form_class = TicketAndReviewForm
    template_name = 'create-review-and-ticket.html'
    success_url = reverse_lazy('feeds')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TicketDeleteView(LoginRequiredMixin, DeleteView):
    model = Ticket
    template_name = 'ticket-delete.html'
    success_url = reverse_lazy('posts')


class FollowView(LoginRequiredMixin, FormView):
    form_class = FollowUserForm
    template_name = 'user-follow.html'
    success_url = reverse_lazy('user-follow')
    model = UserFollows
    context_object_name = 'follow_data'

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

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        followed_users = UserFollows.objects.filter(user=self.request.user)
        users_following = UserFollows.objects.filter(followed_user=self.request.user)
        context['followed_users'] = followed_users
        context['users_following'] = users_following

        return context


class UnfollowView(LoginRequiredMixin, DeleteView):
    model = UserFollows
    template_name = 'user-unfollow.html'
    success_url = reverse_lazy('user-follow')


class PostView(LoginRequiredMixin, TemplateView):
    template_name = 'posts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reviews = Review.objects.filter(user=self.request.user)\
            .annotate(content_type=Value('REVIEW', CharField()))
        tickets = Ticket.objects.filter(user=self.request.user)\
            .annotate(content_type=Value('TICKET', CharField()))

        posts = sorted(
            chain(reviews, tickets),
            key=lambda post: post.time_created,
            reverse=True
        )

        context['posts'] = posts

        return context


class FeedView(LoginRequiredMixin, TemplateView):
    template_name = 'feeds.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        followed_users = UserFollows.objects.filter(
            user=self.request.user
            ).values_list('followed_user', flat=True)

        reviews = Review.objects.filter(
            Q(user__in=followed_users) |
            Q(user=self.request.user) |
            Q(ticket__user=self.request.user)
            ).annotate(content_type=Value('REVIEW', CharField()))

        tickets = Ticket.objects.filter(
            Q(user__in=followed_users) |
            Q(user=self.request.user)
            ).annotate(content_type=Value('TICKET', CharField()))

        feeds = sorted(
            chain(reviews, tickets),
            key=lambda feed: feed.time_created,
            reverse=True
        )

        context['feeds'] = feeds
        print(feeds)

        return context
