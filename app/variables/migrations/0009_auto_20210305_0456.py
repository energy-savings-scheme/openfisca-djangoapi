# Generated by Django 3.1.7 on 2021-03-05 04:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('variables', '0008_auto_20210305_0400'),
    ]

    operations = [
        migrations.AddField(
            model_name='variable',
            name='parents',
            field=models.ManyToManyField(blank=True, related_name='children_set', to='variables.Variable'),
        ),
        migrations.AlterField(
            model_name='variable',
            name='children',
            field=models.ManyToManyField(blank=True, related_name='parent_set', to='variables.Variable'),
        ),
    ]
