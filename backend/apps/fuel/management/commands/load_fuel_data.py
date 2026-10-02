import csv
import time
from pathlib import Path
from django.core.management.base import BaseCommand
from apps.fuel.models import FuelStation
from apps.trips.services.geocoding import geocode_address


class Command(BaseCommand):
    help = "Load fuel stations from CSV and geocode addresses via Nominatim."

    def add_arguments(self, parser):
        parser.add_argument("--csv", type=str, default="data/fuel-prices-for-be-assessment.csv")
        parser.add_argument("--limit", type=int, default=None)
        parser.add_argument("--skip-geocode", action="store_true")

    def handle(self, *args, **options):
        csv_path = Path(options["csv"])
        if not csv_path.exists():
            self.stderr.write(self.style.ERROR(f"CSV not found: {csv_path}"))
            return

        seen = set()
        rows = []
        with csv_path.open("r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                opis_id = row["OPIS Truckstop ID"].strip()
                price = float(row["Retail Price"])
                key = (opis_id, price)
                if key in seen:
                    continue
                seen.add(key)
                rows.append(row)

        if options["limit"]:
            rows = rows[: options["limit"]]

        self.stdout.write(f"Loading {len(rows)} unique stations...")

        created = 0
        for i, row in enumerate(rows, 1):
            opis_id = int(row["OPIS Truckstop ID"].strip())
            name = row["Truckstop Name"].strip()
            address = row["Address"].strip()
            city = row["City"].strip()
            state = row["State"].strip()
            price = float(row["Retail Price"])
            rack_id = int(row["Rack ID"]) if row.get("Rack ID") else None

            lat, lng = None, None
            if not options["skip-geocode"]:
                full_address = f"{address}, {city}, {state}, USA"
                lat, lng = geocode_address(full_address)
                time.sleep(1.1)

            FuelStation.objects.update_or_create(
                opis_truckstop_id=opis_id,
                retail_price=price,
                defaults={
                    "truckstop_name": name,
                    "address": address,
                    "city": city,
                    "state": state,
                    "rack_id": rack_id,
                    "latitude": lat,
                    "longitude": lng,
                },
            )
            created += 1
            if i % 25 == 0:
                self.stdout.write(f"  ... {i}/{len(rows)} processed")

        self.stdout.write(self.style.SUCCESS(f"Loaded {created} stations."))
