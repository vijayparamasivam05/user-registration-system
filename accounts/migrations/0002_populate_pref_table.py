from django.db import migrations


def populate_pref_table(apps, schema_editor):
    Pref = apps.get_model("accounts", "Pref")
    prefectures = [
        "Tokyo",
        "Osaka",
        "Kyoto",
        "Hokkaido",
        "Fukuoka",
        "Aichi",
        "Hyogo",
        "Okinawa",
        "Hiroshima",
        "Chiba",
        "Saitama",
        "Kanagawa",
        "Miyagi",
        "Shizuoka",
        "Ibaraki",
        "Niigata",
        "Kumamoto",
        "Nagasaki",
        "Yokohama",
        "Shiga",
    ]
    for pref in prefectures:
        Pref.objects.create(name=pref)


class Migration(migrations.Migration):
    dependencies = [
        (
            "accounts",
            "0001_initial",
        ),
    ]

    operations = [
        migrations.RunPython(populate_pref_table),
    ]
