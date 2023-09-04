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
from app.views import HomeView, CustomFormView, CustomLogoutView, CustomSignUpView, TicketCreateView,\
    TicketListView, TicketUpdateView, ReviewCreateView, ReviewListView, ReviewUpdateView, TicketAndReviewCreateView, \
    FollowUserView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('login/', CustomFormView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('signup/', CustomSignUpView.as_view(), name='signup'),
    path('ticket/create', TicketCreateView.as_view(), name='create-ticket'),
    path('tickets/', TicketListView.as_view(), name='ticket-list'),
    path('ticket/<int:pk>/update/', TicketUpdateView.as_view(), name='ticket-update'),
    path('review/create/', TicketAndReviewCreateView.as_view(), name='create-review-and-ticket'),
    path('review/create/ticket/<int:ticket_id>/', ReviewCreateView.as_view(), name='create-review'),
    path('reviews/', ReviewListView.as_view(), name='review-list'),
    path('Review/<int:pk>/update/', ReviewUpdateView.as_view(), name='review-update'),
    path('follow/', FollowUserView.as_view(), name='user-follow'),

]
