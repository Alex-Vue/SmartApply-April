from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Calendar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_date', models.DateTimeField(null=True)),
                ('user_name', models.TextField()),
                ('title', models.TextField()),
                ('body', models.TextField(null=True)),
                ('is_active', models.BooleanField()),
            ],
        ),
    ]