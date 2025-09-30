from django.db import migrations, models
import django.db.models.deletion
import uuid

class Migration(migrations.Migration):

    dependencies = [
        ('Invoice', '0008_alter_category_currency'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserLoginHistory',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('login_datetime', models.DateTimeField(auto_now_add=True)),
                ('ip_address', models.GenericIPAddressField()),
                ('user_agent', models.TextField()),
                ('device_type', models.CharField(max_length=50)),
                ('browser', models.CharField(max_length=50)),
                ('os', models.CharField(max_length=50)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='login_history', to='Invoice.user')),
            ],
            options={
                'ordering': ['-login_datetime'],
            },
        ),
    ]
