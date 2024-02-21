# Generated by Django 4.2.10 on 2024-02-21 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flat_applications', '0004_remove_lazyrenter_lazy_profile_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='landlord',
            name='landlord_type',
            field=models.CharField(choices=[('private', 'Private'), ('company', 'Company'), ('agent', 'Agent')], default='private', max_length=50),
        ),
    ]
