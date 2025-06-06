# Generated by Django 5.1.4 on 2025-02-11 11:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_rename_student_user_delete_faq'),
    ]

    operations = [
        migrations.CreateModel(
            name='FAQ',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField()),
                ('answer', models.TextField(blank=True, null=True)),
                ('is_approved', models.BooleanField(default=False)),
                ('submitted_at', models.DateTimeField(auto_now_add=True)),
                ('submitted_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.user')),
            ],
        ),
    ]
