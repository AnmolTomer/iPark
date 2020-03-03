from django.urls import path
from . import views

urlpatterns = [
    #   Old version : path('',views.home,name = 'home'),
    path('',views.HomePageView.as_view(),name = 'home'),
    #   Old version :   path('detail/<int:id>' , views.detail , name = "detail") ,
    #   change it -> pk
    path('detail/<int:pk>' , views.ContactDetailView.as_view() , name = "detail") ,
    #   we are catching a primary key on the url pattern and
    #   that will be used automatically used by our class based views to get
    #   the object of contact model class that matches that primary key

    path('search/', views.search , name = 'search'),

    #for the creating of contacts link
    path('contacts/create' , views.ContactCreateView.as_view(), name="create"),

    path('contacts/update/<int:pk>' , views.ContactUpdateView.as_view(), name="update" ),

    path('contacts/delete/<int:pk>' , views.ContactDeleteView.as_view(), name="delete" ),

    path('signup/', views.SignUpView.as_view(), name="signup"),
]
