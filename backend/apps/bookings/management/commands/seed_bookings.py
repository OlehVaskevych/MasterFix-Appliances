import random
from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker

from apps.bookings.models import Booking


fake = Faker()


class Command(BaseCommand):
    help = "Seed database with fake bookings"

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=20,
            help='Number of bookings to create'
        )

    def handle(self, *args, **kwargs):
        count = kwargs['count']

        self.stdout.write(f"Creating {count} bookings...")

        for _ in range(count):
            Booking.objects.create(
                name=fake.name(),
                email=fake.email(),
                phone=fake.phone_number(),
                address=fake.address(),
                city=fake.city(),
                zip_code=fake.postcode(),
                appliance_type=random.choice([
                    'refrigerator',
                    'washing_machine',
                    'dishwasher',
                    'oven'
                ]),
                appliance_brand=random.choice(['Samsung', 'LG', 'Whirlpool', 'Bosch']),
                appliance_model=fake.word(),
                problem_description=fake.text(max_nb_chars=200),
                status=random.choice([
                    'new',
                    'contacted',
                    'scheduled',
                    'completed'
                ]),
                priority=random.choice(['low', 'normal', 'high']),
                created_at=timezone.now(),
            )

        self.stdout.write(self.style.SUCCESS("Database seeded successfully!"))