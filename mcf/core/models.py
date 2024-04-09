from django.db import models
def get_age_category(age):
  if age < 20:
    return "Below 20 years"
  elif age < 26:
    return "20 - 25 years"
  elif age < 31:
    return "26 - 30 years"
  elif age < 36:
    return "31 - 35 years"
  else:
    return "Above 35 years"
def get_claim_status(arrears_days):
    if arrears_days < 270:
        return "ACTIVE"
    else:
        return "WRITTEN OFF"
# Create your models here.
class Client_Account(models.Model):
    SOL_ID = models.CharField(max_length=50)
    CIF_ID = models.CharField(max_length=50, null=True)
    ACCT_MGR_USER_ID = models.CharField(max_length=50)
    ACCTNUM = models.CharField(max_length=50, unique=True, primary_key=True)
    ACCT_NAME = models.CharField(max_length=100)
    ARREARSDAYS = models.IntegerField()
    LCYBALANCE = models.DecimalField(max_digits=20, decimal_places=2)
    MAT_DATE = models.DateField()
    TERM = models.CharField(max_length=50)
    FLOW_AMT = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    DIS_AMT = models.DecimalField(max_digits=20, decimal_places=2)
    DIS_SHDL_DATE = models.DateField()
    PRINCIPLE_BALANCE = models.DecimalField(max_digits=20, decimal_places=2)
    AMOUNT_CLAIMED = models.DecimalField(max_digits=20, decimal_places=2)
    LOAN_CYCLE = models.CharField(max_length=50, default=1)
    DATE_ARREARS_START = models.DateField()
    GENDER = models.CharField(max_length=50, null=True)
    CUST_DOB = models.DateField(null=True)
    AGE = models.IntegerField()     # Date of Birth
    NATIONAL_ID_REG_NUMBER = models.CharField(max_length=50, null=True)
    BUSINESS_FINANCED = models.CharField(max_length=150, null=True, blank=True)
    INDUSTRY_SECTOR = models.CharField(max_length=50, null=True, blank=True)
    MODE_OF_ENGAGEMENT = models.CharField(max_length=50, default="DIRECT")
    AGE_CATEGORY = models.CharField(max_length=100, default=get_age_category(0))
    LOAN_CYCLE = models.CharField(max_length=50)
    

    app_label = 'core'
    
  


class Client_Form_Info(models.Model):
    ACCTNUM = models.CharField(max_length=50, unique=True,primary_key=True)
    LOAN_APP_DATE = models.DateField(blank=True)
    ADDRESS = models.CharField(max_length=255, blank=True)
    LOAN_PURPOSE = models.CharField(max_length=255, blank=True)
    GROUP = models.CharField(max_length=100, blank=True)
    REASON_FOR_DEFAULT = models.CharField(max_length=255, blank=True)
    CONTACT = models.CharField(max_length=50, blank=True)
    

class Excel_Report(models.Model):
    ACCTNUM = models.CharField(max_length=50, unique=True, primary_key=True)
    ACCT_NAME = models.CharField(max_length=100)
    LOAN_BALANCE = models.DecimalField(max_digits=20, decimal_places=2)
    DISBURSED_AMOUNT = models.DecimalField(max_digits=20, decimal_places=2)
    DATE_OF_DISBURSEMENT = models.DateField()
    AMOUNT_CLAIMED = models.DecimalField(max_digits=20, decimal_places=2)
    LOAN_CYCLE = models.CharField(max_length=50, default=1)
    DATE_OF_DEFAULT = models.DateField()
    GENDER = models.CharField(max_length=50, null=True)
    AGE = models.IntegerField()     # Date of Birth
    SECTOR_OF_VALUE_CHAIN = models.CharField(max_length=50, null=True, blank=True)
    MODE_OF_ENGAGEMENT = models.CharField(max_length=50, default="DIRECT")
    LOAN_CYCLE = models.CharField(max_length=50)
    REASON_FOR_DEFAULT = models.CharField(max_length=255, blank=True)
    CONTACT = models.CharField(max_length=50)
    
    
  

