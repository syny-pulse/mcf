from dataclasses import fields
from msilib.schema import SelfReg
from typing import Self
from django.shortcuts import render
from django.shortcuts import render, redirect
from docx import Document
from .forms import Client_Form_Info, SearchForm
from .models import Client_Account, Client_Form_Info
from django.http import HttpResponse, FileResponse
import os
from django.urls import reverse
from django.shortcuts import redirect
from django import forms
from django.db import IntegrityError
from django.db import models
from django.contrib import messages  # for adding messages

def index(request):
    '''View function for home page of site.'''   
    return render(request, 'core/index.html')

def contact(request):
    """View function for contact page of site."""
    return render(request, 'core/contact.html')

def upload(request):
    """View function for upload page"""
    return render(request, 'core/upload.html')



def search_client(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            account_number = form.cleaned_data['account_number']
            try:
                client_account = Client_Account.objects.get(ACCTNUM=account_number)  # Removed unnecessary ACCTNUM__isnull=False

                # Redirect to the add_client_info view, passing the account_number
                return redirect(reverse('add_client_info', kwargs={'account_number': account_number}))

            except Client_Account.DoesNotExist:
                error_message = 'Client account not found.'
                return render(request, 'core/search_client.html', {'form': form, 'error_message': error_message})

    else:
        form = SearchForm()

    return render(request, 'core/search_client.html', {'form': form})






def add_client_info(request, account_number):
    context = {}

    try:
        client_account = Client_Account.objects.get(ACCTNUM=account_number)
        # Create form based on Client_Form_Info with fields
        Client_Info_Form = forms.modelform_factory(Client_Form_Info, fields='__all__')
        form = Client_Info_Form(initial={'ACCTNUM': Client_Account.objects.get(ACCTNUM=account_number)})
        form.fields['ACCTNUM'] = forms.CharField(disabled=True)
        if request.method == 'POST':
                form = Client_Info_Form(request.POST)
                if form.is_valid():
                    try:
                        form.save()  # Save the form data to the database
                        return redirect('success')  # Redirect to success page

                    except IntegrityError as e:
                    # Provide more specific error messages based on the error details
                        if 'duplicate' in str(e).lower():
                            context['error_message'] = 'A duplicate entry already exists for this information. Please check for conflicts and try again.'
                        else:
                            context['error_message'] = 'An error occurred while saving the information. Please try again.'

    except Client_Account.DoesNotExist:
        context['error_message'] = 'Client account not found.'
        return render(request, 'core/client_account_not_found.html', context)

    context = {
        'form': form,
        'header': f"Enter the following details for {client_account.ACCT_NAME}",
        'account_number': account_number,
        'client_account': client_account,
        'client_form_info': Client_Info_Form
    }

    return render(request, 'core/add_client_info.html', context)


def success_view(request):
    context = {'message': 'Your form has been submitted successfully!'}
    return render(request, 'core/success.html', context)


def generate(request):
    """View function for the generate page."""
    if request.method == 'POST':
        account_number = request.POST.get('account_number')
        accounts = Client_Account.objects.all()
        
        for account in accounts:
            try:
            # Query the database to get account data
                document = Document('template.docx')
                #account2 = Client_Form_Info.objects.get(ACCTNUM=account_number)
                for paragraph in document.paragraphs:
                    if "{{account_name}}" in paragraph.text:
                        paragraph.text = paragraph.text.replace("{{account_name}}",  str(account.ACCT_NAME))
                    if "{{dob}}" in paragraph.text:
                        paragraph.text = paragraph.text.replace("{{dob}}", str(account.CUST_DOB))
                    if "{{age}}" in paragraph.text:
                        paragraph.text = paragraph.text.replace("{{age}}", str(account.AGE))
                    if "{{disbursed_amount}}" in paragraph.text:
                        paragraph.text = paragraph.text.replace("{{disbursed_amount}}", str(account.DIS_AMT))
                    if "{{disbursement_date}}" in paragraph.text:
                        paragraph.text = paragraph.text.replace("{{disbursement_date}}", str(account.DIS_SHDL_DATE))
                    if "{{gender}}" in paragraph.text:
                        paragraph.text = paragraph.text.replace("{{gender}}", str(account.GENDER))
                    if "{{term}}" in paragraph.text:
                        paragraph.text = paragraph.text.replace("{{term}}", str(account.TERM))
                    if "{{claimed_amount}}" in paragraph.text:
                        paragraph.text = paragraph.text.replace("{{claimed_amount}}", str(account.AMOUNT_CLAIMED))
                    if "{{arrears}}" in paragraph.text:
                        paragraph.text = paragraph.text.replace("{{arrears}}",str(account.ARREARSDAYS))

                    output_filename = f"output_{account.ACCT_NAME}.docx"
                    document.save(output_filename)
                    return redirect('success')
           
            except Client_Account.DoesNotExist:
                return HttpResponse("Account number not found", status=404)

    

    return render(request, 'core/generate.html')
                    
                
               

"""# Find and replace placeholder with data
                    new_text = paragraph.text.replace (
                    "{{account_name}}", str(account.ACCT_NAME),
                    "{{dob}}",str(account.CUST_DOB),
                    "{{age}}",str(account.AGE),
                    "{{disbursed_amount}}",str(account.DIS_AMT),
                    "{{disbursement_date}}",str(account.DIS_SHDL_DATE),
                    "{{term}}",str(account.TERM),
                    "{{claimed_amount}}",str(account.AMOUNT_CLAIMED),
                    #"{{loan_purpose}}",str(account2.LOAN_PURPOSE),
                    "{{arrears}}",str(account.ARREARSDAYS),
                    "{{business_financed}}",str(account.BUSINESS_FINANCED),
                    #"{{group}}",str(account2.GROUP),
                    #"{{loan_application_date}}", str(account2.LOAN_APP_DATE),
                    #"{{cause_of_default}}",str(account2.REASON_FOR_DEFAULT),
                    "{{gender}}",str(account.GENDER),
                    #"{{address}}",str(account2.ADDRESS)
                    )
                    paragraph.text = new_text  # Update the text directly in the paragraph"""

        # Save the modified document
                    
    

"""account_data = {
            'account_number': account.ACCTNUM,
            'account_name': account.ACCT_NAME,
            'dob':account.CUST_DOB,
            'age':account.AGE,
            'disbursed_amount':account.DIS_AMT,
            'disbursement_date':account.DIS_SHDL_DATE,
            'term':account.TERM,
            'claimed_amount':account.AMOUNT_CLAIMED,
            'loan_purpose':account2.LOAN_PURPOSE,
            'business_financed':account.BUSINESS_FINANCED,
            'group':account2.GROUP,
            'loan_application_date': account2.LOAN_APP_DATE,
            'cause_of_default':account2.REASON_FOR_DEFAULT,
            'gender':account.GENDER,
            'address':account2.ADDRESS,
            # Add other fields as needed
        }"""

