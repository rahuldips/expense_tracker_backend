# Generated by Django 5.0.4 on 2024-04-29 19:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ParameterMaster',
            fields=[
                ('param_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('parameter_key', models.CharField(max_length=100, null=True)),
                ('parameter_value', models.CharField(max_length=600)),
                ('parameter_desc', models.CharField(max_length=255, null=True)),
                ('status', models.SmallIntegerField(default=1)),
            ],
            options={
                'db_table': 'parameter_master',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=100)),
                ('phone_no', models.IntegerField()),
                ('email', models.EmailField(max_length=100)),
                ('password', models.CharField(max_length=100)),
                ('is_active', models.BooleanField(default=True)),
                ('is_authenticated', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'user',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='UserLoginActivity',
            fields=[
                ('la_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('admin_user_id', models.BigIntegerField(null=True)),
                ('position_id', models.BigIntegerField(null=True)),
                ('login_time', models.DateTimeField(null=True)),
                ('logout_time', models.DateTimeField(null=True)),
                ('active_status', models.SmallIntegerField(default=1, null=True)),
                ('created_on', models.DateTimeField(null=True)),
                ('updated_on', models.DateTimeField(null=True)),
            ],
            options={
                'db_table': 'user_login_activity',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='UserOtp',
            fields=[
                ('otp_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('u_phone', models.CharField(blank=True, max_length=45, null=True)),
                ('u_email', models.CharField(blank=True, max_length=100, null=True)),
                ('otp', models.CharField(max_length=7, null=True)),
                ('created_on', models.DateTimeField(null=True)),
                ('updated_on', models.DateTimeField(null=True)),
                ('expire_time', models.DateTimeField(null=True)),
            ],
            options={
                'db_table': 'user_otp',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='UserToken',
            fields=[
                ('token_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('user_id', models.BigIntegerField(null=True)),
                ('user_type', models.IntegerField(null=True)),
                ('token', models.CharField(max_length=255)),
                ('updated_on', models.DateTimeField(null=True)),
                ('expiry_time', models.DateTimeField(null=True)),
                ('allow_flag', models.IntegerField(default=1, null=True)),
            ],
            options={
                'db_table': 'user_token',
                'managed': True,
            },
        ),
    ]
