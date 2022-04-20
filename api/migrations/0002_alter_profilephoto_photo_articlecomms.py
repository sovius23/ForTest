# Generated by Django 4.0.3 on 2022-04-19 11:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profilephoto',
            name='photo',
            field=models.ImageField(upload_to='', verbose_name=models.Model),
        ),
        migrations.CreateModel(
            name='ArticleComms',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comments', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='api.article')),
            ],
        ),
    ]
