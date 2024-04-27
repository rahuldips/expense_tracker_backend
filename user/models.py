from django.db import models

# Create your models here.

class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100)
    phone_no = models.IntegerField()
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)  # Hashed password will be stored here
    is_active = models.BooleanField(default=True)  # True for active, False for inactive
    is_authenticated = models.BooleanField(default=False)  # True for authenticated via Google, False otherwise
    
    class Meta:
        managed = True
        db_table = 'user'

class UserLoginActivity(models.Model):
    la_id =  models.BigAutoField(primary_key=True)
    admin_user_id = models.BigIntegerField(blank=False,null=True)
    position_id = models.BigIntegerField(blank=False,null=True)
    login_time = models.DateTimeField(blank=False,null=True)
    logout_time = models.DateTimeField(blank=False,null=True)
    active_status = models.SmallIntegerField(default=1,blank=False,null=True)
    created_on = models.DateTimeField(blank=False,null=True)
    updated_on = models.DateTimeField(blank=False,null=True)
    class Meta:
        managed = True
        db_table = 'user_login_activity'

class UserToken(models.Model):
    token_id = models.BigAutoField(primary_key=True)
    user_id = models.BigIntegerField(blank=False,null=True)
    user_type = models.IntegerField(blank=False,null=True)
    token = models.CharField(max_length=255)
    updated_on = models.DateTimeField(blank=False,null=True)
    expiry_time = models.DateTimeField(blank=False,null=True)
    allow_flag = models.IntegerField(default=1,blank=False,null=True)

    class Meta:
        managed = True
        db_table = 'user_token'

class UserOtp(models.Model):
    otp_id = models.BigAutoField(primary_key=True)
    u_phone = models.CharField(max_length=45, blank=True, null=True)
    u_email = models.CharField(max_length=100, blank=True, null=True)
    otp = models.CharField(max_length=7,blank=False,null=True)
    created_on = models.DateTimeField(blank=False,null=True)
    updated_on = models.DateTimeField(blank=False,null=True)
    expire_time = models.DateTimeField(blank=False,null=True)
    
    class Meta:
        managed = True
        db_table = 'user_otp'

class ParameterMaster(models.Model):
    param_id = models.BigAutoField(primary_key=True)
    parameter_key = models.CharField(max_length=100,blank=False,null=True)
    parameter_value = models.CharField(max_length=600,blank=False,null=False)
    parameter_desc = models.CharField(max_length=255,blank=False,null=True)
    status = models.SmallIntegerField(default=1,blank=False,null=False)
    
    class Meta:
        managed = True
        db_table = 'parameter_master'
