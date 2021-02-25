from django.shortcuts import render,redirect,get_object_or_404
from. forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import CreateEvent,InvitedGuests,GuestRegistration
from .utils import render_to_pdf
from django.template.loader import get_template
from django.http import HttpResponse
import smtplib
from email.message import EmailMessage
from django.core.mail import send_mail
from django.conf import settings




#Print events list
def generate_pdf_events(request,*args,**kwargs):
        viewevents = CreateEvent.objects.all()
        template = get_template('Users/print_event_list.html')
        context = {'viewevents':viewevents}
        html = template.render(context)
        pdf = render_to_pdf('Users/print_event_list.html',context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Events_list.pdf" 
            content = "inline; filename='%s'" %(filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")

#Print guests list
def generate_pdf_guests(request,*args,**kwargs):
        viewguests = InvitedGuests.objects.all()
        template = get_template('Users/print_guest_list.html')
        context = {'viewguests':viewguests}
        html = template.render(context)
        pdf = render_to_pdf('Users/print_guest_list.html',context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Guests_list.pdf" 
            content = "inline; filename='%s'" %(filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")
# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f'Welcome {username}, Your account has succesfully been created')
            return redirect('login')
    else:
        form = RegistrationForm()

    return render(request, 'Users/register.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'Users/profile.html')

#Create an event
def create_event(request):
    form2 = CreateEventForm()
    viewevents = CreateEvent.objects.all()
    guests = InvitedGuests.objects.all()
    if request.method == 'POST':
        form2 = CreateEventForm(request.POST)

        if form2.is_valid():
            form2.save()
            messages.success(request,'Event successfully created')
            return redirect('view_event')

    return render(request,'Users/create_event.html',{'form2':form2})

#Guest Registration
def guest_registration(request):
    form4 = GuestRegistrationForm()
    subject = 'Registration for this event'
    content = 'Dear Sir/Madam,\n\nThank you.'
    #email = request.POST.get('id_email','')
    if request.method == 'POST':
        form4 = GuestRegistrationForm(request.POST)
        

        if form4.is_valid:
            form4.save()
            guestregister = GuestRegistration.objects.all()
            email = [obj.email for obj in guestregister]
            send_mail(subject, content, settings.EMAIL_HOST_USER,email, fail_silently=False)
            messages.success(request,'Success, you will receive a confirmation email')
            return redirect('guest_view_events')
            

    return render(request,'Users/Guests/guest_register.html', {'form4':form4})
#View events list
def view_event(request):
    viewevents = CreateEvent.objects.all()
    guests = InvitedGuests.objects.all()
    context = {'viewevents':viewevents,'guests':guests}

    return render(request, 'Users/view_event.html',context)

#Guest view upcoming events
def guest_view_events(request):
    viewevents = CreateEvent.objects.all()
    
    context = {'viewevents':viewevents}

    return render(request, 'Users/Guests/guest_view_events.html',context)

#Update events list
def update_event(request, pk):

	event = CreateEvent.objects.get(id=pk)
	form2 = CreateEventForm(instance=event)

	if request.method == 'POST':
		form2 = CreateEventForm(request.POST, instance=event)
		if form2.is_valid():
			form2.save()
			return redirect('view_event')

	context = {'form2':form2}
	return render(request, 'Users/update_event.html', context)

#Delete an event
def delete_event(request, pk):
	event = CreateEvent.objects.get(id=pk)
	if request.method == "POST":
		event.delete()
		return redirect('view_event')

	context = {'item':event}
	return render(request, 'Users/delete_event.html', context)

#Create a guests list
def create_guests_list(request):
    form3 = InvitedGuestsForm()
    if request.method == 'POST':
        form3 = InvitedGuestsForm(request.POST)
        if form3.is_valid():
            form3.save()
            messages.success(request, f'Guest added succesfully')
            return redirect('view_guests_list')
    else:
        form3 = InvitedGuestsForm()
    return render(request,'Users/create_guests_list.html', {'form3': form3})

#View guests list
def view_guests_list(request):
    viewguests = InvitedGuests.objects.all()
    context = {'viewguests':viewguests}

    return render(request, 'Users/view_guests_list.html',context)

#Update guests list
def update_guests_list(request, pk):

	guestlist = InvitedGuests.objects.get(id=pk)
	form3 = InvitedGuestsForm(instance=guestlist)

	if request.method == 'POST':
		form3 = InvitedGuestsForm(request.POST, instance=guestlist)
		if form3.is_valid():
			form3.save()
			return redirect('view_guests_list')

	context = {'form3':form3}
	return render(request, 'Users/update_guests_list.html', context)

#Delete guest
def delete_guests_list(request, pk):
	guestlist = InvitedGuests.objects.get(id=pk)
	if request.method == "POST":
		guestlist.delete()
		return redirect('view_guests_list')

	context = {'item':guestlist}
	return render(request, 'Users/delete_guests_list.html', context)

#Invite Guests
def invite_guests(request):
    viewguests = InvitedGuests.objects.all()
    context = {'viewguests':viewguests}

    return render(request, 'Users/invite_guests.html',context)

def save_invite_guests(request):
    if request.method == 'POST':
        if request.POST.get('guestname'):
            saveguestname = InvitedGuests()
            saveguestname.guestname = request.POST.get('guestname')
            saveguestname.save()
            return redirect('view_invited_guests')
    else:
        return render(request,'Users/invite_guests.html')

#Sending Mails
def sendmail(request,id):

    viewevent = get_object_or_404(CreateEvent,id=id)
    guests = viewevent.guests.all()
    recipients =[obj.email for obj in guests]
    msg = EmailMessage()
    msg['Subject']= f'Invitation to {viewevent.eventname} event'
    msg['From']= 'ezenfinancialsevents@gmail.com'
    viewguests = viewevent.guests.all()
    msg['To']= recipients
    msg.set_content(f'Hello Sir/Madam,\n\n\nI would like to invite you to {viewevent.eventname}.\n\nIt will be held in {viewevent.venue} on {viewevent.date}.\n\nDescription: {viewevent.description}.\n\nKindly confirm your attendance. \n\n\nThank you.')
    
    server = smtplib.SMTP_SSL('smtp.gmail.com',465)
    server.login('ezenfinancialsevents@gmail.com','eventsmanagement')
    server.send_message(msg)
    server.quit()
    messages.success(request, f'Invites Succesfully sent')
    return redirect('view_event')

#def guest_registration_email(request,id):
#    guestregistration = get_object_or_404(GuestRegistration,id=email)
#    recipients =[obj.email for obj in guestregistration]
#    msg = EmailMessage()
#    msg['Subject']= f'Registration for the event'
#    msg['From']= 'ezenfinancialsevents@gmail.com'
#   msg['To']= recipients
#    msg.set_content(f'Hello Sir/Madam,\n\n\nYour registration is succesful')
    
#    server = smtplib.SMTP_SSL('smtp.gmail.com',465)
#   server.login('ezenfinancialsevents@gmail.com','eventsmanagement')
#    server.send_message(msg)
#    server.quit()
#    messages.success(request, f'Registration email Succesfully sent')
#    return redirect('guest_view_events')
