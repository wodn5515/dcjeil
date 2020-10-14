from django.db import migrations, models

def populate_email(apps, schema_editor):
    MyModel = apps.get_model('member', 'User')
    for user in MyModel.objects.all():
        user.email = user.uid + "@example.com"
        user.save()
        
class Migration(migrations.Migration):
    
    dependencies = [
        ('member', '0001_initial'),
    ]
    
    operations = [
        migrations.RunPython(populate_email),
    ]