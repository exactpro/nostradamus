from django.db import migrations

from apps.authentication.models import Team


def create_nostradamus_team(apps, schema_editor):
    Team.objects.create(name="Nostradamus")


def create_qa_role(apps, schema_editor):
    qa_table = apps.get_model("authentication", "Role")
    qa_table.objects.create(name="QA")


class Migration(migrations.Migration):

    dependencies = [("settings", "0001_initial")]
    operations = [
        migrations.RunPython(
            create_nostradamus_team,
        ),
        migrations.RunPython(
            create_qa_role,
        ),
    ]
