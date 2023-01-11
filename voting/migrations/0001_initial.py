# Generated by Django 4.1.4 on 2022-12-15 21:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Candidate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=20)),
                ('lastname', models.CharField(max_length=20)),
                ('mat_no', models.CharField(max_length=15)),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/candidate')),
                ('votes', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Positions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('session', models.CharField(max_length=20)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.department')),
                ('faculty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.faculty')),
            ],
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_votes', models.IntegerField()),
                ('winning_vote', models.IntegerField(blank=True, null=True)),
                ('position', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='voting.positions')),
                ('winner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='voting.candidate')),
            ],
        ),
        migrations.AddField(
            model_name='candidate',
            name='position',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='voting.positions'),
        ),
    ]
