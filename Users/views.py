from django.shortcuts import render,redirect,get_object_or_404
from. forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
from .utils import render_to_pdf
from django.template.loader import get_template
from django.http import HttpResponse,FileResponse
import smtplib
from email.message import EmailMessage
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt #for the ussd function
#from africastalking.AfricasTalkingGateway import AfricasTalkingGateway, AfricasTalkingGatewayException#for sms
import africastalking
from .filters import *
from django.core.paginator import Paginator

import io
import reportlab
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter,A4
#from reportlab.lib.units import inch
#from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph

username = 'sandbox'
api_key = '7e209952909369947e27cce5943f8219b359c4dbed11be2bed39f79e5016d75d'
africastalking.initialize(username, api_key)  
sms = africastalking.SMS 


# Create your views here.

def register(request):
    form = RegistrationForm()
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

                        #USER PROFILE


@login_required
#def profile(request):
#    profile_form2 = ProfileForm()
#    if request.method == 'POST':



def profile(request):
    #profile_form = ProfileForm()
    #user_form = UserUpdateForm()
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        user_form = UserUpdateForm(request.POST, instance=request.user)

        if profile_form.is_valid() and user_form.is_valid():
            profile_form.save()
            user_form.save()
            messages.success(request,'Your profile has been succesfully updated')
            return redirect('profile')
    else:
        profile_form = ProfileForm(instance=request.user.profile)
        user_form = UserUpdateForm( instance=request.user)

    return render(request, 'Users/profile.html',{'profile_form':profile_form,'user_form':user_form})



                            #CREATE AN EVENT views


#Create an event
@login_required
def create_event(request):
    user = request.user
    form2 = CreateEventForm(user = request.user)
    guests = InvitedGuests.objects.filter(created_by=user)
    if request.method == 'POST':
        form2 = CreateEventForm(request.POST,user = request.user)

        if form2.is_valid():
            new_form2 = form2.save(commit=False)
            new_form2.created_by = request.user
            new_form2.save()
            messages.success(request,'Event successfully created')
            return redirect('view_event')

    return render(request,'Users/create_event.html',{'form2':form2})

#View events list
@login_required
def view_event(request):
    user = request.user
    viewevents = CreateEvent.objects.filter(created_by=user)
    guests = InvitedGuests.objects.all()

    myFilter = CreateEventFilter(request.GET, queryset=viewevents)
    viewevents = myFilter.qs

    paginator = Paginator(viewevents, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'viewevents':viewevents,'guests':guests,'myFilter':myFilter,'page_obj':page_obj}

    return render(request, 'Users/view_event.html',context)

#Update events list
@login_required
def update_event(request, pk):

	event = CreateEvent.objects.get(id=pk)
	form2 = CreateEventForm(instance=event,user = request.user)

	if request.method == 'POST':
		form2 = CreateEventForm(request.POST, instance=event,user = request.user)
		if form2.is_valid():
			form2.save()
			return redirect('view_event')

	context = {'form2':form2}
	return render(request, 'Users/update_event.html', context)

#Delete an event
@login_required
def delete_event(request, pk):
	event = CreateEvent.objects.get(id=pk)
	if request.method == "POST":
		event.delete()
		return redirect('view_event')

	context = {'item':event}
	return render(request, 'Users/delete_event.html', context)

#Sending Mails
@login_required
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

                        #CREATING A GUESTS LIST views

#Create a guests list
@login_required
def create_guests_list(request):
    form3 = InvitedGuestsForm()
    if request.method == 'POST':
        form3 = InvitedGuestsForm(request.POST)
        if form3.is_valid():
            new_form3 = form3.save(commit=False)
            new_form3.created_by = request.user
            new_form3.save()
            messages.success(request, f'Guest added succesfully')
            return redirect('view_guests_list')
    else:
        form3 = InvitedGuestsForm()
    return render(request,'Users/create_guests_list.html', {'form3': form3})

#View guests list
@login_required
def view_guests_list(request):
    user = request.user
    viewguests = InvitedGuests.objects.filter(created_by=user)
    
    guestlistFilter = InvitedGuestsFilter(request.GET, queryset=viewguests)
    viewguests = guestlistFilter.qs

    paginator = Paginator(viewguests, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'viewguests':viewguests,'guestlistFilter':guestlistFilter,'page_obj':page_obj}
    return render(request, 'Users/view_guests_list.html',context)

#Update guests list
@login_required
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
@login_required
def delete_guests_list(request, pk):
	guestlist = InvitedGuests.objects.get(id=pk)
	if request.method == "POST":
		guestlist.delete()
		return redirect('view_guests_list')

	context = {'item':guestlist}
	return render(request, 'Users/delete_guests_list.html', context)

#Event Organizer view of public event guests
@login_required
def view_applications(request):
    user = request.user
    viewapplications = GuestRegistration.objects.filter(event_organizer= user)

    publicFilter = GuestRegistrationFilter(request.GET, queryset=viewapplications)
    viewapplications = publicFilter.qs

    paginator = Paginator(viewapplications, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'viewapplications':viewapplications,'publicFilter':publicFilter,'page_obj':page_obj}

    return render(request,'Users/event_applications.html',context)

#Event Organizer view of invites only applications
@login_required
def view_invites_only_applications(request):
    user = request.user
    viewinvitesapplications = InvitesOnlyRegistration.objects.filter(event_organizer=user)

    invitesFilter = InvitesOnlyRegistrationFilter(request.GET, queryset=viewinvitesapplications)
    viewinvitesapplications = invitesFilter.qs

    paginator = Paginator(viewinvitesapplications, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'viewinvitesapplications':viewinvitesapplications,'invitesFilter': invitesFilter,'page_obj':page_obj}

    return render(request,'Users/invites_only_applications.html',context)

#Reject a public event application
@login_required
def reject_application(request, pk):
	application = GuestRegistration.objects.get(id=pk)
	if request.method == "POST":
		application.delete()
		return redirect('view_applications')

	context = {'item':application}
	return render(request, 'Users/reject_application.html', context)

#Reject Invites Only application
@login_required
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
        #sms.send(f'Dear {viewinvitesapplications.firstname}, Your application for the event has been declined.\nThank you.',[f'{viewinvitesapplications.phonenumber}'], callback = reject_invites_only_application)
        return redirect('view_invites_only_applications')
        
    context = {'item':viewinvitesapplications}
    return render(request, 'Users/reject_invites_only_application.html', context)

#Sending Emails to succesful applicants
@login_required
def succesful_application(request,id):
    viewinvitesapplications = get_object_or_404(InvitesOnlyRegistration,id=id)
    applications = viewinvitesapplications.email
    recipient =[applications]
    subject = 'Succesful Application'
    content = f'Hello {viewinvitesapplications.firstname},\n\nYour application  has been approved.\n\nThank you.'
    send_mail(subject, content, settings.EMAIL_HOST_USER,recipient, fail_silently=False)
    messages.success(request, f'Approval email Succesfully sent')
    return redirect('view_invites_only_applications')


                        #GUEST ACTIONS views


#Guest view upcoming events
def guest_view_events(request):
    viewevents = CreateEvent.objects.all()
    

    guestsFilter = GuestViewEventFilter(request.GET, queryset=viewevents)
    viewevents = guestsFilter.qs

    paginator = Paginator(viewevents, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'viewevents':viewevents,'guestsFilter':guestsFilter,'page_obj':page_obj}

    return render(request, 'Users/Guests/guest_view_events.html',context)

#Guest Registration For Public Events
def guest_registration(request,id):
    form4 = GuestRegistrationForm()
    viewevent = get_object_or_404(CreateEvent,id=id)
    if request.method == 'POST':
        form4 = GuestRegistrationForm(request.POST)
        
        if form4.is_valid:
            new_form4 = form4.save(commit=False)
            new_form4.event_organizer = viewevent.created_by
            new_form4.event_applied_for = viewevent.eventname
            new_form4.save()
            name = form4.cleaned_data.get('firstname')
            email =  form4.cleaned_data.get('email')
            phone_number = form4.cleaned_data.get('phonenumber')
            recipient = [email]
            subject = f'Registration for the {viewevent.eventname} event'
            content = f'Dear {name},\n\nYou have succesfully enrolled for the {viewevent.eventname} event that is to be held on {viewevent.date} in {viewevent.venue}.\n\nDescription: {viewevent.description}.\n\nFor more enquiries, email us at ezenfinancialsevents@gmail.com\n\nSee you there.'
            send_mail(subject, content, settings.EMAIL_HOST_USER,recipient, fail_silently=False)
            messages.success(request,'Success, you will receive a confirmation email')
            #sms.send(f'Dear {name},You have succesfully enrolled for the {viewevent.eventname} event that is to be held on {viewevent.date} in {viewevent.venue}. Check your mail for more details',[f'{phone_number}'], callback = guest_registration)
            return redirect('guest_view_events')
           
    return render(request,'Users/Guests/guest_register.html', {'form4':form4})

#Invites Only Event Application
def invites_only_application(request,id):
    form5 = InvitesOnlyRegistrationForm()
    viewevent = get_object_or_404(CreateEvent,id=id)
    
    if request.method == 'POST':
        form5 = InvitesOnlyRegistrationForm(request.POST)
        
        if form5.is_valid:
            new_form5 = form5.save(commit=False)
            new_form5.event_organizer = viewevent.created_by
            new_form5.event_applied_for = viewevent.eventname
            new_form5.save()
            name = form5.cleaned_data.get('firstname')
            email =  form5.cleaned_data.get('email')
            phone_number = form5.cleaned_data.get('phonenumber')
            recipient = [email]
            subject = f'Registration for the {viewevent.eventname} event'
            content = f'Dear {name},\n\nYour application for the {viewevent.eventname} event has been succesfully received. You will receive a confirmation email.\n\nThank you.'
            send_mail(subject, content, settings.EMAIL_HOST_USER,recipient, fail_silently=False)
            messages.success(request,'Your application has been received. You will be notified if it\'s succesful')
            #sms.send(f'Dear {name}, Your application for the {viewevent.eventname} event has been succesfully received. You will receive a confirmation email.\nThank you.',[f'{phone_number}'], callback = invites_only_application)
            return redirect('guest_view_events')
            
    return render(request,'Users/Guests/invites_only_registration.html', {'form5':form5})



                            #USSD CALLBACK View


@csrf_exempt
def ussd_callback(request):
    viewevents = CreateEvent.objects.all()
    if request.method == 'POST':
        session_id = request.POST.get("sessionId")
        service_code = request.POST.get("serviceCode")
        phone_number = request.POST.get("phoneNumber")
        text = request.POST.get("text")
        
        response = ''
        mobilenumber = ''
        username = ''
        
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
            response += "6. Get Together Lamu \n"
            response += "7. Get Together Kwale \n"
            response += "98. MORE "
        elif text == '1*98':
            response += "CON 8. Get Together Kakamega \n"
            response += "9. Get Together Busia \n"
            response += "10. Get Together Mandera \n"
            response += "11. Get Together Eldoret \n"
            response += "12. Get Together Wajir \n"
            response += "13. Get Together Uasin Gishu \n"
            response += "00. Exit "
        elif text == '1*98*00':
            response = "END Thank you for using our service"
        elif text == "1*1":
            response = "CON 1. Attend\n"
            response += "2. Go Back\n"
            response +=  "3. Exit"
        
        elif text == "1*1*1":
            response = "CON Enter Your Mobile Number:"
            mobilenumber = text
        elif text == f"{mobilenumber}":
            response = "CON Enter Your Full Names:"
        elif text == f"1*1*1*{username}":
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


                            # GENERATING PDFs

                            
#Print events list
@login_required
def generate_pdf_events(request,*args,**kwargs):
        user = request.user
        viewevents = CreateEvent.objects.filter(created_by=user)
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
@login_required
def generate_pdf_guests(request,*args,**kwargs):
        user = request.user
        viewguests = InvitedGuests.objects.filter(created_by=user)
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
@login_required
def generate_pdf_applicants(request,*args,**kwargs):
        user = request.user
        viewapplications = GuestRegistration.objects.filter(event_organizer=user)
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
@login_required
def generate_pdf_invites_only_applicants(request,*args,**kwargs):
        user = request.user
        viewinvitesapplications = InvitesOnlyRegistration.objects.filter(event_organizer=user)
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
 
#Printing Reports using reportlab
def event_report(request):
    

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=Events_List.pdf'
    for viewevent in viewevents:
        data = [['Event Type','Event Name','Venue','Description','Date','Guests'],
            [f'{viewevent.eventtype}',f'{viewevent.eventname}',f'{viewevent.venue}',f'{viewevent.description}',f'{viewevent.date}',f'{viewevent.guests}',]
            ]
        t = Table(data,style = [
            ('GRID',(0,0),(-1,-1),1,colors.black),
            ('BACKGROUND',(0,0),(5,0),colors.yellow),
        ])
        return response


def events_report(request):
    user = request.user
    viewevents = CreateEvent.objects.filter(created_by=user)

    
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer,pagesize=A4)
    width, height = A4

    for viewevent in viewevents:
        data=[['Event Type','Event Name','Venue','Description','Date','Guests'],
             [viewevent.eventtype,viewevent.eventname,viewevent.venue,viewevent.description,viewevent.date,viewevent.guests],
             [viewevent.eventtype,2,3,4,5,6]]


    #t=Table(data,colWidths=[100 for i in range(1,6)],rowHeights=[20 for i in range(1,4)])
    t=Table(data,colWidths=None, rowHeights=None)
    tstyle=TableStyle([("BOX",(0,0),(-1,-1),1,colors.red),
                    ("GRID",(0,0),(-1,-1),1,colors.black),
                    ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
                    ("ALIGN",(0,0),(5,0),"CENTER"),
                    ('BACKGROUND',(0,0),(5,0),colors.yellow),
                    ('FONTSIZE',(0,0),(5,0),12),])
    t.setStyle(tstyle)
    t.wrapOn(p, width, height)
    t.wrapOn(p, width, height)
    
    t.drawOn(p,20,600)

    p.showPage()
    p.save()

    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='Events_list.pdf')