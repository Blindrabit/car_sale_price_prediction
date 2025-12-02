import csv
import uuid

from django.core.management import BaseCommand

from cars.models import Car


class Command(BaseCommand):
    help = "Imports data from csv file."

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str)

    def handle(self, *args, **options):

        with open(options["file_path"]) as csv_file:
            reader = csv.DictReader(csv_file)
            bulk_create = []
            for index, row in enumerate(reader, start=1):
                bulk_create.append(
                    Car(
                        uuid=uuid.uuid4(),
                        engine_size=row["Engine size"],
                        fuel_type=row["Fuel type"][0].upper(),
                        manufacturer=row["Manufacturer"],
                        millage=row["Mileage"],
                        model=row["Model"],
                        price=row["Price"],
                        year_of_manufacture=row["Year of manufacture"],
                    )
                )
                if index % 100 == 0:
                    Car.objects.bulk_create(bulk_create)
                    bulk_create = []
                    self.stdout.write(self.style.NOTICE(f"{index} records imported."))
            Car.objects.bulk_create(bulk_create)

        self.stdout.write(self.style.SUCCESS("Data imported."))
