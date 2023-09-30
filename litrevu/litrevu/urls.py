"""
URL configuration for litrevu project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app.views import CustomLogoutView, CustomSignUpView, TicketCreateView,\
    TicketListView, TicketUpdateView, ReviewCreateView, ReviewListView, ReviewUpdateView, TicketAndReviewCreateView, \
    FollowView, PostView, UnfollowView, CustomLoginView, ReviewDeleteView, TicketDeleteView, FeedView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', FeedView.as_view(), name='feeds'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('signup/', CustomSignUpView.as_view(), name='signup'),
    path('ticket/create', TicketCreateView.as_view(), name='create-ticket'),
    path('tickets/', TicketListView.as_view(), name='ticket-list'),
    path('ticket/<int:pk>/update/', TicketUpdateView.as_view(), name='ticket-update'),
    path('ticket/<int:pk>/delete/', TicketDeleteView.as_view(), name='ticket-delete'),
    path('review/create/', TicketAndReviewCreateView.as_view(), name='create-review-and-ticket'),
    path('review/create/ticket/<int:ticket_id>/', ReviewCreateView.as_view(), name='create-review'),
    path('reviews/', ReviewListView.as_view(), name='review-list'),
    path('review/<int:pk>/update/', ReviewUpdateView.as_view(), name='review-update'),
    path('review/<int:pk>/delete/', ReviewDeleteView.as_view(), name='review-delete'),
    path('follow/', FollowView.as_view(), name='user-follow'),
    path('unfollow/<int:pk>', UnfollowView.as_view(), name='user-unfollow'),
    path('posts/', PostView.as_view(), name='posts'),
    path('feeds/', FeedView.as_view(), name='feeds'),


]
