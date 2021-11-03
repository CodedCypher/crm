from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.core.mail import send_mail
from .models import Lead, Agent
from .forms import LeadForm, CustomUserCreationForm
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from agents.mixins import OrganizerandLoginRequiredMixin
#CRUD+L - Create, Retrive, Update, Delete + list 

class SignupView(generic.CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/signup.html'
    
    def get_success_url(self):
        return reverse('login')

class LandingPageView(generic.TemplateView):
    template_name = 'landing.html'


class LeadListView(LoginRequiredMixin, generic.ListView):
    template_name = 'leads/lead_list.html'
    context_object_name = "leads"
    
    def get_queryset(self):
        user = self.request.user
        #initial queryset of leads for the entire organization
        if user.is_organizer:
            queryset = Lead.objects.filter(organization=user.userprofile)
        elif user.is_agent:                              
            queryset = Lead.objects.filter(organization=user.agent.organization)
            #filter the agent that is logged in
            queryset = queryset.filter(agent__user=user)
        return queryset
        


class LeadDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = 'leads/lead_detail.html'
    context_object_name = 'lead'

    def get_queryset(self):
        user = self.request.user
        #initial queryset of leads for the entire organization
        if user.is_organizer:
            queryset = Lead.objects.filter(organization=user.userprofile)
        elif user.is_agent:                              
            queryset = Lead.objects.filter(organization=user.agent.organization)
            #filter the agent that is logged in
            queryset = queryset.filter(agent__user=user)
        return queryset

class LeadCreateView(OrganizerandLoginRequiredMixin, generic.CreateView):
    form_class = LeadForm
    template_name = 'leads/lead_create.html'
    
    def get_success_url(self):
        return reverse('leads:lead-list')

    def form_valid(self, form):
        send_mail(
            subject="A Lead has been created", 
            message="Go to the site to see the new lead",
            from_email="test@test.com",
            recipient_list=['test2@test.com'],
        )
        return super(LeadCreateView, self).form_valid(form)


class LeadUpdateView(OrganizerandLoginRequiredMixin, generic.UpdateView):
    template_name = 'leads/lead_update.html'
    form_class = LeadForm

    def get_queryset(self):
        user = self.request.user
        return Lead.objects.filter(organization=user.userprofile)

    def get_success_url(self):
        return reverse('leads:lead-list')


class LeadDeleteView(OrganizerandLoginRequiredMixin, generic.DeleteView):
    template_name = 'leads/lead_delete.html'
    queryset = Lead.objects.all()

    def get_queryset(self):
        user = self.request.user
        return Lead.objects.filter(organization=user.userprofile)

    def get_success_url(self):
        return reverse('leads:lead-list')

# def landing_page(request):
#     return render(request, 'landing.html')

# def lead_list(request):
#     leads = Lead.objects.all()
#     context = {
#         'leads': leads
#     }
#     return render(request, 'leads/lead_list.html', context)

# def lead_detail(request, pk, *args, **kwargs):
#     lead = get_object_or_404(Lead, id=pk)
#     context = {
#         'lead': lead,
#     }
#     return render(request, 'leads/lead_detail.html', context)

# def lead_create(request):
#     form = LeadForm(request.POST or None)
#     if form.is_valid():
#         form.save()
#         return redirect("/leads")            

#     context = {
#         'form': form
#     }
#     return render(request, 'leads/lead_create.html', context)

# def lead_update(request, pk):
#     lead = Lead.objects.get(id=pk)
#     form = LeadForm(instance=lead)
#     if request.method == "POST":
#         form = LeadForm(request.POST, instance=lead)
#         if form.is_valid():
#             form.save()
#             return redirect('/leads/')
#     context = {
#         'lead': lead,
#         'form': form,
#     }
#     return render(request, 'leads/lead_update.html', context)

# def lead_delete(request, pk):
#     lead = Lead.objects.get(id=pk)
#     if request.method == "POST":
#         lead.delete()
#         return redirect('/leads/')
#     context = {
#         'lead': lead
#     }
#     return render(request, 'leads/lead_delete.html', context)
    
