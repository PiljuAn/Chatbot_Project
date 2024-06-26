# Generated by Django 5.0 on 2024-06-11 05:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Label_0_answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'label_0_answer',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='save_data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('user_input', models.CharField(max_length=255, null=True)),
                ('chatting_output', models.CharField(blank=True, max_length=255, null=True)),
                ('keyword', models.CharField(blank=True, max_length=255, null=True)),
                ('concept_code', models.CharField(blank=True, max_length=2200, null=True)),
                ('example_code', models.CharField(blank=True, max_length=2200, null=True)),
                ('code_output', models.CharField(blank=True, max_length=2200, null=True)),
                ('doc_url', models.CharField(blank=True, max_length=255, null=True)),
                ('classification_label', models.CharField(blank=True, max_length=10, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'django_io',
            },
        ),
    ]
