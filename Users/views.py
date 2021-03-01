from django.shortcuts import render,redirect,get_object_or_404
from. forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
from .utils import render_to_pdf
from django.template.loader import get_template
from django.http import HttpResponse
import smtplib
from email.message import EmailMessage
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt #for the ussd function




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

#Print Applicants list
def generate_pdf_applicants(request,*args,**kwargs):
        viewapplications = GuestRegistration.objects.all()
        template = get_template('Users/print_applicants_list.html')
        context = {'viewapplications':viewapplications}
        html = template.render(context)
        pdf = render_to_pdf('Users/print_applicants_list.html',context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Applicants_list.pdf" 
            content = "inline; filename='%s'" %(filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")

#Print invites only list
def generate_pdf_invites_only_applicants(request,*args,**kwargs):
        viewinvitesapplications = InvitesOnlyRegistration.objects.all()
        template = get_template('Users/print_invites_applications.html')
        context = {'viewinvitesapplications':viewinvitesapplications}
        html = template.render(context)
        pdf = render_to_pdf('Users/print_invites_applications.html',context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Applicants_list.pdf" 
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
def guest_registration(request,id):
    form4 = GuestRegistrationForm()
    viewevent = get_object_or_404(CreateEvent,id=id)
    if request.method == 'POST':
        form4 = GuestRegistrationForm(request.POST)
        

        if form4.is_valid:
            form4.save()
            name = form4.cleaned_data.get('firstname')
            email =  form4.cleaned_data.get('email')
            recipient = [email]
            subject = f'Registration for the {viewevent.eventname} event'
            content = f'Dear {name},\n\nYou have succesfully enrolled for the {viewevent.eventname} event that is to be held on {viewevent.date} in {viewevent.venue}.\n\nDescription: {viewevent.description}.\n\nFor more enquiries, email us at ezenfinancialsevents@gmail.com\n\nSee you there.'
            send_mail(subject, content, settings.EMAIL_HOST_USER,recipient, fail_silently=False)
            messages.success(request,'Success, you will receive a confirmation email')
            return redirect('guest_view_events')
            

    return render(request,'Users/Guests/guest_register.html', {'form4':form4})

#Invites Only Event Application
def invites_only_application(request,id):
    form5 = InvitesOnlyRegistrationForm()
    viewevent = get_object_or_404(CreateEvent,id=id)
    
    if request.method == 'POST':
        form5 = InvitesOnlyRegistrationForm(request.POST)
        

        if form5.is_valid:
            form5.save()
            name = form5.cleaned_data.get('firstname')
            email =  form5.cleaned_data.get('email')
            recipient = [email]
            subject = f'Registration for the {viewevent.eventname} event'
            content = f'Dear {name},\n\nYour application for the {viewevent.eventname} event has been succesfully received. You will receive a confirmation email.\n\nThank you.'
            send_mail(subject, content, settings.EMAIL_HOST_USER,recipient, fail_silently=False)
            messages.success(request,'Your application has been received. You will be notified if it\'s succesful')
            return redirect('guest_view_events')
            

    return render(request,'Users/Guests/invites_only_registration.html', {'form5':form5})
#View events list
def view_event(request):
    viewevents = CreateEvent.objects.all()
    guests = InvitedGuests.objects.all()
    context = {'viewevents':viewevents,'guests':guests}

    return render(request, 'Users/view_event.html',context)

#Event Organizer view of public event guests
def view_applications(request):
    viewapplications = GuestRegistration.objects.all()
    context = {'viewapplications':viewapplications}

    return render(request,'Users/event_applications.html',context)

#Event Organizer view of invites only applications
def view_invites_only_applications(request):
    viewinvitesapplications = InvitesOnlyRegistration.objects.all()
    context = {'viewinvitesapplications':viewinvitesapplications}

    return render(request,'Users/invites_only_applications.html',context)
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

#Reject a public event application
def reject_application(request, pk):
	application = GuestRegistration.objects.get(id=pk)
	if request.method == "POST":
		application.delete()
		return redirect('view_applications')

	context = {'item':application}
	return render(request, 'Users/reject_application.html', context)

#Reject Invites Only application
def reject_invites_only_application(request, id):
    viewinvitesapplications = get_object_or_404(InvitesOnlyRegistration,id=id)
    if request.method == "POST":
        applications = viewinvitesapplications.email
        recipient =[applications]
        subject = 'Unsuccesful Application'
        content = f'Hello {viewinvitesapplications.firstname},\n\nYour application for the event has been declined.\n\nThank you.'
        send_mail(subject, content, settings.EMAIL_HOST_USER,recipient, fail_silently=False)
        messages.success(request, f'Denial email Succesfully sent')
        viewinvitesapplications.delete()
        return redirect('view_invites_only_applications')
        
    context = {'item':viewinvitesapplications}
    return render(request, 'Users/reject_invites_only_application.html', context)


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
    msg['From']= 'otieno.samuel@ezenfinancials.com'
    viewguests = viewevent.guests.all()
    msg['To']= recipients
    msg.set_content(f'Hello {guest.guestname},\n\n\nI would like to invite you to {viewevent.eventname}.\n\nIt will be held in {viewevent.venue} on {viewevent.date}.\n\nDescription: {viewevent.description}.\n\nKindly confirm your attendance. \n\n\nThank you.')
    
    server = smtplib.SMTP_SSL('mail.ezenfinancials.com',587)
    server.login('otieno.samuel@ezenfinancials.com','@Sillykbian1')
    server.send_message(msg)
    server.quit()
    messages.success(request, f'Invites Succesfully sent')
    return redirect('view_event')

#Sending Emails to succesful applicants
def succesful_application(request,id):
    viewinvitesapplications = get_object_or_404(InvitesOnlyRegistration,id=id)
    applications = viewinvitesapplications.email
    recipient =[applications]
    subject = 'Succesful Application'
    content = f'Hello {viewinvitesapplications.firstname},\n\nYour application  has been approved.\n\nThank you.'
    send_mail(subject, content, settings.EMAIL_HOST_USER,recipient, fail_silently=False)
    messages.success(request, f'Approval email Succesfully sent')
    return redirect('view_invites_only_applications')

def unsuccesful_application(request,id):
    viewinvitesapplications = get_object_or_404(InvitesOnlyRegistration,id=id)
    
    return redirect('view_invites_only_applications')
#def succesful_application(request,id):
#    viewinvitesapplications = get_object_or_404(InvitesOnlyRegistration,id=id)
#    applications = InvitesOnlyRegistration.objects.all()
#    recipients =[obj.email for obj in applications]
#    msg = EmailMessage()
#    msg['Subject']= 'Succesful Application'
#    msg['From']= 'otieno.samuel@ezenfinancials.com'
#    msg['To']= recipients
#    msg.set_content(f'Hello {viewinvitesapplications.firstname},\n\nYour application  has been approved.\n\nThank you.')
    
#    server = smtplib.SMTP_SSL('mail.ezenfinancials.com',587)
#    server.login('otieno.samuel@ezenfinancials.com','@Sillykbian1')
#    server.send_message(msg)
#    server.quit()
#    messages.success(request, f'Approval email Succesfully sent')
#    return redirect('invites_only_application')

@csrf_exempt
def ussd_callback(request):
    viewevents = CreateEvent.objects.all()
    if request.method == 'POST':
        session_id = request.POST.get("sessionId")
        service_code = request.POST.get("serviceCode")
        phone_number = request.POST.get("phoneNumber")
        text = request.POST.get("text")
        
        response = ''
        
        if text == '':
            response = "CON What event type would you want to attend? \n"
            response += "1. Public \n"
            response += "2. Invites Only"
        elif text == '1':
            response = "CON Choose public event: \n "
            response += "1. Get Together Mombasa \n"
            response += "2. Get Together Nairobi \n"
            response += "3. Get Together Kisumu \n"
            response += "4. Get Together Nakuru \n"
            response += "5. Get Together Naivasha \n"
            response += "6. Get Together Kilifi "
        elif text == "1*1":
            response = "CON 1. Attend\n"
            response += "2. Go Back\n"
            response +=  "3. Exit"
        
        elif text == "1*1*1":
            response = "CON Enter Your Full Names:"
        elif text == "1*1*1":
            response = "CON Enter Your ID Number:"
        elif text == "1*1*3":
            response = "END Thank you for using our service"
        elif text == "1*2":
            response = "CON 1. Attend\n"
            response += "2. Go Back\n"
            response +=  "3. Exit"
        elif text == "1*2*1":
            response = "CON Enter Your Full Names:"
        elif text == "1*2*3":
            response = "END Thank you for using our service"
        elif text == "1*3":
            response = "CON 1. Attend\n"
            response += "2. Go Back\n"
            response +=  "3. Exit"
        elif text == "1*3*1":
            response = "CON Enter Your Full Names:"
        elif text == "1*3*3":
            response = "END Thank you for using our service"
        elif text == "1*4":
            response = "CON 1. Attend\n"
            response += "2. Go Back\n"
            response +=  "3. Exit"
        elif text == "1*4*1":
            response = "CON Enter Your Full Names:"
        elif text == "1*4*3":
            response = "END Thank you for using our service"
        elif text == "1*5":
            response = "CON 1. Attend\n"
            response += "2. Go Back\n"
            response +=  "3. Exit"
        elif text == "1*5*1":
            response = "CON Enter Your Full Names:"
        elif text == "1*5*3":
            response = "END Thank you for using our service"
        elif text == "1*6":response +=  "3. Exit"
        elif text == "1*6*1":
            response = "CON Enter Your Full Names:"
        elif text == "1*6*3":
            response = "END Thank you for using our service"
        elif text == "2":
            response = "CON Enter special code:"
            
        return HttpResponse(response)
    