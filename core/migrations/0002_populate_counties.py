from django.db import migrations

def populate_counties(apps, schema_editor):
    County = apps.get_model('core', 'County')
    counties = [
        ('Baringo', '01'),
        ('Bomet', '02'),
        ('Bungoma', '03'),
        ('Busia', '04'),
        ('Elgeyo-Marakwet', '05'),
        ('Embu', '06'),
        ('Garissa', '07'),
        ('Homa Bay', '08'),
        ('Isiolo', '09'),
        ('Kajiado', '10'),
        ('Kakamega', '11'),
        ('Kericho', '12'),
        ('Kiambu', '13'),
        ('Kilifi', '14'),
        ('Kirinyaga', '15'),
        ('Kisii', '16'),
        ('Kisumu', '17'),
        ('Kitui', '18'),
        ('Kwale', '19'),
        ('Laikipia', '20'),
        ('Lamu', '21'),
        ('Machakos', '22'),
        ('Makueni', '23'),
        ('Mandera', '24'),
        ('Marsabit', '25'),
        ('Meru', '26'),
        ('Migori', '27'),
        ('Mombasa', '28'),
        ("Murang'a", '29'),
        ('Nairobi', '30'),
        ('Nakuru', '31'),
        ('Nandi', '32'),
        ('Narok', '33'),
        ('Nyamira', '34'),
        ('Nyandarua', '35'),
        ('Nyeri', '36'),
        ('Samburu', '37'),
        ('Siaya', '38'),
        ('Taita-Taveta', '39'),
        ('Tana River', '40'),
        ('Tharaka-Nithi', '41'),
        ('Trans-Nzoia', '42'),
        ('Turkana', '43'),
        ('Uasin Gishu', '44'),
        ('Vihiga', '45'),
        ('Wajir', '46'),
        ('West Pokot', '47'),
    ]
    
    for name, code in counties:
        County.objects.create(name=name, code=code)

def reverse_counties(apps, schema_editor):
    County = apps.get_model('core', 'County')
    County.objects.all().delete()

class Migration(migrations.Migration):
    dependencies = [
        ('core', '0001_initial'),
    ]
    operations = [
        migrations.RunPython(populate_counties, reverse_counties),
    ]
