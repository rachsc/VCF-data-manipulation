# Generated by Django 4.0 on 2022-01-01 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='VcfRow',
            fields=[
                ('CHROM', models.CharField(max_length=100)),
                ('POS', models.PositiveIntegerField()),
                ('ID', models.CharField(max_length=100)),
                ('REF', models.CharField(max_length=100)),
                ('ALT', models.CharField(max_length=100)),
                ('my_pk', models.PositiveIntegerField(primary_key=True, serialize=False)),
            ],
        ),
    ]
