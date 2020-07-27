# Generated by Django 3.0.8 on 2020-07-27 06:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('pledge_text', models.CharField(max_length=512)),
                ('co2_formula', models.CharField(blank=True, max_length=128, null=True)),
                ('water_formula', models.CharField(blank=True, max_length=128, null=True)),
                ('waste_formula', models.CharField(blank=True, max_length=128, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_id', models.SlugField()),
                ('answer_input_type', models.CharField(choices=[('numeric', 'numeric'), ('select', 'select')], max_length=32)),
                ('answer_input_type_options', models.CharField(blank=True, help_text='Add additional input options used to further constrain allowed input values.', max_length=128, null=True)),
                ('action', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pledges.Action')),
            ],
            options={
                'unique_together': {('action', 'question_id')},
            },
        ),
        migrations.CreateModel(
            name='SelectAnswerFormulaValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_value', models.CharField(max_length=64)),
                ('formula_value', models.FloatField()),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pledges.Question')),
            ],
        ),
        migrations.CreateModel(
            name='Pledge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(blank=True, max_length=512, null=True)),
                ('action', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pledges.Action')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'action')},
            },
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_value', models.CharField(max_length=64)),
                ('formula_value', models.FloatField(blank=True)),
                ('pledge', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pledges.Pledge')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pledges.Question')),
            ],
            options={
                'unique_together': {('pledge', 'question')},
            },
        ),
    ]
