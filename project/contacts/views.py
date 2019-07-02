from django.shortcuts import render, redirect
from django.views.generic import UpdateView
from django.urls import reverse
from .models import Contact
from .forms import SearchForm, ContactForm
from django.http import HttpResponseRedirect

# Create your views here.

def home(request):
    if request.method == 'GET':
        form =  SearchForm(request.GET)
        if form.is_valid():
            search = form.cleaned_data.get('search')    
            qs = Contact.objects.filter().search(search)           
            request.session['search_url'] =  request.build_absolute_uri()        
            return render(request, 'home.html', {'qs': qs, 'form':form}) 
        else:
            form =SearchForm()
        return render(request, 'home.html', {'form': form})

class ContactUpdateView(UpdateView):
    model = Contact
    form_class = ContactForm
    template_name = 'edit_contact.html'
    context_object_name = 'contact'
   
    def form_valid(self, form):
        post = form.save(commit=False)

        post.save()
        return HttpResponseRedirect(self.request.session.get('search_url'))
  
