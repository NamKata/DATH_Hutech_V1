# Generated by Django 3.0.4 on 2020-06-04 03:11

import ckeditor.fields
import ckeditor_uploader.fields
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CategoryName', models.CharField(max_length=150)),
                ('CategoryContent', models.CharField(max_length=500, null=True)),
                ('CategorySlug', models.SlugField()),
            ],
        ),
        migrations.CreateModel(
            name='Chap',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('SttChap', models.IntegerField(verbose_name='Chap ')),
                ('Title', models.CharField(max_length=200)),
                ('Content', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True)),
                ('Views', models.IntegerField(default=0)),
                ('StatusPost', models.BooleanField(default=False)),
                ('StatusEdit', models.BooleanField(default=False)),
                ('DateUp', models.DateTimeField()),
                ('DateEdit', models.DateTimeField()),
                ('CreateDate', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('StatusFollow', models.BooleanField(default=True)),
                ('CreateDate', models.DateTimeField(default=django.utils.timezone.now)),
                ('DateUnfollow', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Formality',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=100)),
                ('Content', models.CharField(max_length=250, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='LevelUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('LevelName', models.CharField(max_length=100)),
                ('CheckFollow', models.IntegerField()),
                ('CheckView', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Manga',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('MangaName', models.CharField(max_length=250)),
                ('OrtherName', models.CharField(max_length=250, null=True)),
                ('Slug', models.SlugField()),
                ('Image', models.ImageField(blank=True, max_length=150, null=True, upload_to='Manga')),
                ('Content', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('Author', models.CharField(blank=True, max_length=100, null=True)),
                ('Editor', models.CharField(blank=True, max_length=100, null=True)),
                ('StartDate', models.DateField(auto_now=True, null=True)),
                ('EndDate', models.DateField(auto_now=True, null=True)),
                ('Share', models.IntegerField(default=0)),
                ('StatusFinish', models.BooleanField(default=False)),
                ('StatusPost', models.BooleanField(default=False)),
                ('StatusDelete', models.BooleanField(default=False)),
                ('CreateDate', models.DateTimeField(default=django.utils.timezone.now)),
                ('Chapnow', models.IntegerField(default=0)),
                ('DateUpChap', models.DateTimeField(default=django.utils.timezone.now)),
                ('Formality', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DB.Formality')),
            ],
        ),
        migrations.CreateModel(
            name='MangaType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=150)),
                ('Slug', models.SlugField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Usergroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=50)),
                ('CreateDate', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='User_Comic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('UserName', models.CharField(max_length=100)),
                ('Email', models.EmailField(max_length=254)),
                ('Password', models.CharField(blank=True, max_length=25, null=True)),
                ('Birthday', models.DateField()),
                ('Address', models.CharField(blank=True, max_length=150, null=True)),
                ('Phone', models.CharField(blank=True, max_length=12, null=True)),
                ('Coins', models.IntegerField(default=0)),
                ('NickName', models.CharField(blank=True, max_length=100, null=True)),
                ('StatusEmail', models.BooleanField(default=False)),
                ('StatusDelete', models.BooleanField(default=False)),
                ('Image', models.ImageField(blank=True, max_length=150, null=True, upload_to='User')),
                ('Content', models.CharField(blank=True, max_length=150, null=True)),
                ('CreateDate', models.DateTimeField(default=django.utils.timezone.now)),
                ('StatusGender', models.BooleanField(default=False)),
                ('Group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DB.Usergroup')),
                ('LevelUser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DB.LevelUser')),
            ],
        ),
        migrations.CreateModel(
            name='Notifical',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Content', models.CharField(max_length=150, null=True)),
                ('CreateDate', models.DateTimeField(default=django.utils.timezone.now)),
                ('SetTime', models.DateTimeField()),
                ('StatusSet', models.BooleanField(default=False)),
                ('Follow', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DB.Follow')),
            ],
        ),
        migrations.CreateModel(
            name='MangaCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('StatusDelete', models.BooleanField(default=False)),
                ('CreateDate', models.DateTimeField(default=django.utils.timezone.now)),
                ('DeleteDate', models.DateTimeField()),
                ('Category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DB.Category')),
                ('Manga', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DB.Manga')),
            ],
        ),
        migrations.AddField(
            model_name='manga',
            name='MangaType',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DB.MangaType'),
        ),
        migrations.AddField(
            model_name='manga',
            name='User_Comic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DB.User_Comic'),
        ),
        migrations.AddField(
            model_name='follow',
            name='Manga',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DB.Manga'),
        ),
        migrations.AddField(
            model_name='follow',
            name='User_Comic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DB.User_Comic'),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Content', models.CharField(max_length=500, null=True)),
                ('Rating', models.IntegerField()),
                ('CreateDate', models.DateTimeField(default=django.utils.timezone.now)),
                ('Chap', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DB.Chap')),
                ('User_Comic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DB.User_Comic')),
            ],
        ),
        migrations.AddField(
            model_name='chap',
            name='Manga',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DB.Manga'),
        ),
    ]
