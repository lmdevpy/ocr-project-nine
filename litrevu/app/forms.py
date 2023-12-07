from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import Ticket, Review, User, UserFollows


class TicketCreationForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']


class ReviewCreationForm(forms.ModelForm):
    RATING_CHOICES = [(str(i), f"{i}") for i in range(6)]
    rating = forms.ChoiceField(choices=RATING_CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = Review
        fields = ['headline', 'rating', 'body']


class TicketAndReviewForm(forms.ModelForm):
    RATING_CHOICES = [(str(i), f"{i}") for i in range(6)]
    review_headline = forms.CharField(required=True)
    review_rating = forms.ChoiceField(choices=RATING_CHOICES, widget=forms.RadioSelect)
    review_body = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Ticket
        fields = ["title", "description", "image"]

    def save(self, *args, **kwargs):
        ticket = super().save(commit=True)
        review = Review.objects.create(
            ticket=ticket,
            user=ticket.user,
            headline=self.cleaned_data['review_headline'],
            rating=self.cleaned_data['review_rating'],
            body=self.cleaned_data["review_body"],
        )
        return ticket


class FollowUserForm(forms.Form):
    follow_username = forms.CharField(max_length=150, required=True)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def clean_follow_username(self):
        username = self.cleaned_data['follow_username']
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError(f'user {username} does not exist')
        if UserFollows.objects.filter(user=self.user, followed_user__username=username).exists():
            raise forms.ValidationError('user already followed')
        if self.user.username == username:
            raise forms.ValidationError("u can't follow yourself")
        return username
