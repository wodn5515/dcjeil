from django.db import migrations


def reservation_time(apps, schema_editor):
    MyModel = apps.get_model("board", "Post")
    for obj in MyModel.objects.all():
        obj.reservation = obj.upload_date
        obj.save()


class Migration(migrations.Migration):

    dependencies = [
        ("board", "0011_post_reservation"),
    ]

    operations = [
        migrations.RunPython(reservation_time),
    ]