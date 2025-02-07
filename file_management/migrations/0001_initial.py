# Generated by Django 4.2.16 on 2024-11-08 17:51

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference_number', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('file_name', models.CharField(max_length=100)),
                ('file_data', models.FileField(upload_to='uploaded_files/')),
                ('file_type', models.CharField(max_length=50)),
                ('priority', models.CharField(choices=[('Normal', 'Normal'), ('Urgent', 'Urgent')], max_length=10)),
                ('purpose', models.TextField()),
                ('file_source', models.CharField(max_length=100)),
                ('subject', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('status', models.CharField(default='Pending', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('from_department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_files', to='file_management.department')),
                ('to_department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_files', to='file_management.department')),
            ],
        ),
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action_taken', models.CharField(max_length=100)),
                ('action_taken_at', models.DateTimeField(auto_now_add=True)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='file_management.department')),
                ('file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='file_management.file')),
            ],
        ),
    ]
