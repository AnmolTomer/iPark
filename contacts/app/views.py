# For class based views
from django.views.generic import ListView, DetailView

from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
#   For complex query search
from django.db.models import Q
from .models import Contact,Car

from .Main import imgRead
from django.utils.timezone import datetime
import os

from django.views.generic.edit import CreateView,UpdateView,DeleteView

# IDEA: we can create new user from our template
from django.contrib.auth.forms import UserCreationForm

# IDEA: FOR CLASS BASED VIEWS WE CAN WRITE THIS
from django.contrib.auth.mixins import LoginRequiredMixin

# IDEA: FOR FUNCTION BASED VIEW WE NEED This:
from django.contrib.auth.decorators import login_required

from django.urls import reverse_lazy
#   we'll use generic class based view provided by django
#   to Create an obj from frontend
# Create your views here.

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#   IDEA: It must inherit from ListViews
#   IDEA: But this ListView contains the getQuerySet()
#   IDEA: which returns all the contacts so we need to override it
#   IDEA: so that it'll display only the required contacts
class HomePageView(LoginRequiredMixin,ListView):
    #   what template we want to render this content
    template_name = 'index.html'
    #   mention the model from where we are going to show the list of objects
    model = Contact
    #   we have configured our homepage by giving it an name contacts
    #   to all the fetched contact object so have to tell Django to
    #   call all those objects in our contact models
    context_object_name = 'contacts'
    def get_queryset(self):
        """
        we'll create all the contact obj that would have sent to us when we try
        to visit the home page when we visit the get_queryset() method
        """
        contacts = super().get_queryset()
        cars = Car.objects.all()
        # response  = imgRead()
        # response = "HR26DK8337"
        # response = "TN21IY8405"
        response = None 
        if response != None:
            print(response)
            # print(contacts)
            # print(cars)
            '''for contact in contacts:
                if contact.number_plate == None:
                    print(contact)'''
            adarsh = []
            print("--------------Initial Vaule---------------")
            print(adarsh)
            registered = []
            print("----------------------------------------") 
            for car in cars:
                # print(car)
                registered.append(car.number_plate)
                if(car.sl_no != None):
                    adarsh.append(str(car.number_plate))
                    # print(str(car.sl_no))
            print(adarsh)
            print(registered)
            if response not in registered:
                adarsh.append(response)
                print("-------------------Unregistered-------------------")
                for contact in contacts:
                    if contact.number_plate == None:
                        sl_no = Contact.objects.get(sl_no=contact.sl_no)
                        # print("Hey")
                        p = Car(number_plate=response,entry_time=str(datetime.now()),service_used=0,status='Allowed',sl_no=sl_no,name=None,email=None,phone=None)
                        # print(p)
                        p.save()
                        sl_no = Contact.objects.filter(sl_no=contact.sl_no)
                        sl_no.update(number_plate=p,avalibility="occupied") 
                        break
            else:
                #   Present in parking area !
                #   So remove it
                print("-------------------Present -> Removing-------------------")
                if response in adarsh:
                    #   get number_plate obj
                    n = Car.objects.get(number_plate=response)
                    # print('------------'+str(n)+'----------------')
                    # print(n.number_plate)
                    p = Contact.objects.filter(sl_no=n.sl_no)
                    p.update(number_plate=None,avalibility="empty")
                    n = Car.objects.filter(number_plate=response)
                    n.update(sl_no=None)
                    print(p)
                    print(adarsh)
                    adarsh.remove(response)
                    print(adarsh)
                    print("HI")
                else:
                    #   Not present in parking area !
                    print("-------------------Not Present -> Adding-------------------")
                    for contact in contacts:
                        adarsh.append(response)
                        if contact.number_plate == None:
                            sl_num = Contact.objects.get(sl_no=contact.sl_no)
                            p = Car.objects.get(number_plate=response)
                            p.name_plate = response
                            p.entry_time = str(datetime.now())
                            p.service_used += 1
                            p.sl_no=sl_num 
                            
                            p.save()       
                            sl_num = Contact.objects.filter(sl_no=contact.sl_no)
                            sl_num.update(number_plate=p,avalibility="occupied") 
                            break
            print("--------------Final Vaule---------------")
            print(adarsh)
            print("----------------------------------------")       
            # print(BASE_DIR)
        # IDEA: NOW WE'LL filter -> it takes the name of model field and
        # IDEA: set it's value to current login user
        return contacts.filter(manager = self.request.user)
# Similarly, we make the contact detailview
class ContactDetailView(LoginRequiredMixin,DetailView):
    template_name = 'detail.html'
    # model = Contact
    context_object_name = 'contact'
    queryset = Contact.objects.all()
    def get_context_data(self, **kwargs):
        context = super(ContactDetailView, self).get_context_data(**kwargs)
        context['car'] = Car.objects.all()
        # And so on for more models
        print(context)
        return context
    
# function based view needs a "request" argument and here,
# we have to return a template
@login_required
def search(request):
    if request.GET:
            #variable = name of input tag
        search_term = request.GET['search_term']
        search_results = Contact.objects.filter(
            Q(sl_no__icontains = search_term) |
            Q(info__icontains = search_term) |
            Q(avalibility__iexact = search_term)
        )
        context = {
        #we are assiging its value as the variable search_term
            'search_term' : search_term ,
            'contacts' : search_results
                # after adding this , we make the changes
                # in the value accordingly
        }
        return render(request , 'search.html' , context)
    else:
        return redirect('home')
#    this CreateView contains all the function req to
#   Create an obj from the frontend
class ContactCreateView(LoginRequiredMixin,CreateView):
    model = Contact
    template_name = 'create.html'
    #list of values that will include the form input that will be there in the template
    fields = ['sl_no','number_plate','avalibility','info' , 'image']
    
    # success_url = '/'

    # we have the form argument
    # we are saving all the form values
    # in the instance variable
    def form_valid(self,form):
        # we don't want it to be saved to the database isntead
        # we want it to be saved it into our instance variable
        # for it we set commit = False and the follwing next line
        instance = form.save(commit=False)
        # we can set the manager model field
        instance.manager = self.request.user
        # now we can save the instance variables
        instance.save()
        # we want it to redirect the home page
        return redirect('home')


class ContactUpdateView(LoginRequiredMixin,UpdateView):
    model = Contact
    template_name = 'update.html'
    #list of values that will include the form input that will be there in the template
    fields = ['sl_no','number_plate','avalibility','info' , 'image']
    #   This was taking us to the home page but we want to
    #   go to the detail page so :: success_url = '/'

    def form_valid(self,form):
        #   we have to create an instance that will have the
        #   contact object that we are trying to update
        instance = form.save()
        return redirect('detail',instance.pk)

class ContactDeleteView(LoginRequiredMixin,DeleteView):
    model = Contact
    template_name = 'delete.html'
    success_url = '/'

class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('home')
