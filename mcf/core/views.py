from dataclasses import fields
from msilib.schema import SelfReg
from typing import Self
from django.shortcuts import render

# Create your views here.
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



"""from django.shortcuts import render, redirect
from django.contrib import messages  # for adding messages
from django.core.exceptions import IntegrityError
from .forms import ClientInfoForm, SearchForm  # Assuming forms are in the same directory

import psycopg2  # Import psycopg2


def add_client_info(request, account_number):
  context = {}  # Initialize context dictionary

  try:
    # Connect to the PostgreSQL database using psycopg2
    conn = psycopg2.connect(
        database="mcfyaw",  # Replace with your database name
        user="postgres",  # Replace with your database username
        password="Byaruhanga12",  # Replace with your database password
        host="localhost",  # Replace with your database host (localhost if local)
        # Add port if needed (default is 5432)
    )

    cursor = conn.cursor()

    # Get client account using raw SQL (assuming no complex filtering needed)
    cursor.execute(f"SELECT * FROM core_client_account WHERE ACCTNUM = %s", (account_number,))
    client_account = cursor.fetchone()

    if not client_account:
        context['error_message'] = 'Client account not found.'
        return render(request, 'core/client_account_not_found.html', context)

    client_name = client_account[3]  # Assuming field order (index 1)

    # **Improved Field Type Mapping:**
    data_type_map = {
        9: forms.DateInput,  # Date
        12: forms.CharField,  # Character
        14: forms.CharField,  # Character
        15: forms.IntegerField,  # Integer
        17: forms.IntegerField,  # Integer
        # ... (add mappings for other data types in your table)
    }

    # Get fields with null values
    null_fields = [field for field in client_account[2:] if field is None]

    # Dynamically generate form fields based on null_fields
    fields = {}
    for field_name in null_fields:
      # Assuming field data starts from index 2, adjust if different
      field_type_index = client_account[4:].index(field_name)

      try:
        field_type = data_type_map[client_account[2 + field_type_index]]  # Use data_type_map
      except KeyError:
        field_type = forms.CharField  # Placeholder for unsupported types

      fields[field_name] = field_type(label=field_name, required=False)  # Adjust label as needed

    # Create the form using modelform_factory (commented out as we're using raw SQL)
    # ClientInfoForm = modelform_factory(Client_Account, fields=fields, exclude=None)

    form = ClientInfoForm(request.POST or None, initial={'client_name': client_name})  # Pre-populate client name

    if request.method == 'POST':
      if form.is_valid():
        try:
          # Update client account using raw SQL
          update_query = f***
          #UPDATE core_client_account
          #SET {', '.join(f"{field_name} = %s" for field_name in form.cleaned_data.keys() if field_name != 'ACCTNUM')}
          #WHERE ACCTNUM = %s
          
          values = [value for field_name, value in form.cleaned_data.items() if field_name != 'ACCTNUM'] + [account_number]
          cursor.execute(update_query, values)
          conn.commit()  # Commit changes to the database

          messages.success(request, 'Client information updated successfully!')
          return redirect('success')  # Redirect to success page

        except IntegrityError as e:
          # Provide more specific error messages based on the error details
          if 'duplicate' in str(e).lower():
            context['error_message'] = 'A duplicate entry already exists for this information. Please check for conflicts and try again.'
          else:
            context['error_message'] = 'An error occurred while saving the information. Please try again.'
            # Consider logging the full error details for debugging

      else:
          # Handle form validation errors (e.g., display error messages in the context)"""




def success_view(request):
    context = {'message': 'Your form has been submitted successfully!'}
    return render(request, 'core/success.html', context)

"""def generate(request):
    View function for the generate page.
    if request.method == 'POST':
        account_number = request.POST.get('account_number')
        try:
            # Query the database to get account data
            account = Client_Account.objects.get(ACCTNUM=account_number)
        except Client_Account.DoesNotExist:
            return HttpResponse("Account number not found", status=404)

        # Convert account data to a dictionary for compatibility with existing functions
        account_data = {
            'account_number': account.ACCTNUM,
            'account_name': account.ACCT_NAME,
            # Add other fields as needed
        }

        try:
            document = Document('template.docx')
            if populate_document(document, account_data):
                output_filename = f"output_{account_number}.docx"
                document.save(output_filename)
                # Check if additional information is needed
                if additional(account_data):
                    # Save account_number in session to pass to the second form
                    request.session['account_number'] = account_number
                    return redirect('form')  # Redirect to the second form
                else:
                    # Serve the file for download
                    file_path = os.path.join(os.path.dirname(__file__), output_filename)
                    if os.path.exists(file_path):
                        with open(file_path, 'rb') as f:
                            response = FileResponse(f)
                            response['Content-Disposition'] = f'attachment; filename="{output_filename}"'
                            return response
                    else:
                        return HttpResponse("File not found", status=404)
            else:
                return HttpResponse("Failed to generate document", status=500)
        except Exception as e:
            return HttpResponse(f"An error occurred: {e}", status=500)
    else:
        return render(request, 'core/generate.html') """

"""def my_view(request, client_account_id):
    # Retrieve client_account object
    client_account = Client_Account.objects.get(id=client_account_id)

    if request.method == 'POST':
        form = ClientInfoForm(client_account, request.POST)
        if form.is_valid():
            # Update model directly with empty values for null fields
            for field_name, field_value in form.cleaned_data.items():
                setattr(client_account, field_name, field_value or None)  # Set empty values to None
            client_account.save()  # Save the model instance
            return redirect('success')  # Redirect to a success page
    else:
        form = ClientInfoForm(client_account)

    return render(request, 'template.html', {'form': form})"""
    

"""def find_account_data(account_number, account_name):
  Find account data in the mcfyaw database.
  try:
    # Connect to the PostgreSQL database
    conn = psycopg2.connect(database="mcfyaw")
    cur = conn.cursor()

    # Convert account number to integer for comparison
    account_number = int(account_number)

    # Execute a query to find the account data
    #sql = SELECT * FROM core_client_account WHERE ACCTNUM = %s
    cur.execute(sql, (account_number))

    # Fetch the first row (assuming there's only one account with that number)
    row = cur.fetchone()

    # Close the cursor and connection
    cur.close()
    conn.close()

    # Return the row data if account number is found
    return row
  except Exception as e:
    print(f"Error finding account data: {e}")
  return None  # Return None if account number is not found"""

"""def populate_database(request):
    View function for the loan form page.
    if request.method == 'POST':
        form = add_client_info(request.POST)
        if form.is_valid():
            # Extract form data
            account_number = form.cleaned_data.get('account_number')
            account_name = form.cleaned_data.get('account_name')
            # Create or update the Client_Account object in the database
            client_account, created = Client_Account.objects.update_or_create(
                ACCTNUM=account_number,
                defaults={'account_name': account_name}
            )
            # Redirect to success page
            return redirect('success')
        else:
            # If form is not valid, render the form again with errors
            return render(request, 'core/add_.client-info.html', {'form': form})
    else:
        # If it's a GET request, display the form
        account_number = request.GET.get('account')
        if account_number:
            account = find_account_data(account_number)
            if account:
                account_name = account[3]
                form = add_client_info(initial={'account_number': account_number})
                return render(request, 'core/add_client_info.html', {'form': form, 'account_name': account_name})
            else:
                error_message = "Account not found. Please enter a valid account number."
                return render(request, 'core/error.html', {'error_message': error_message})
        else:
            form = add_client_info()
            return render(request, 'core/search_client.html', {'form': form})"""






def generate(request):
    """View function for the generate page."""
    if request.method == 'POST':
        account_number = request.POST.get('account_number')
        account = Client_Account.objects.get(ACCTNUM=account_number)
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

