import random
import uuid

from django.core.management.base import BaseCommand

from faker import Faker

from storehouse.models import Product


"""
class Product(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    stock = models.PositiveIntegerField(blank=True)
    isbn_no = models.CharField(primary_key=True, max_length=50, db_index=True, unique=True)

"""


class Command(BaseCommand):
    help = "Creating fake 50 Books"  # noqa: A003

    def handle(self, *args, **options):
        fake = Faker()
        list_books = []

        # Creating 50 Books
        for _ in range(50):
            book_name = fake.text(18)
            book_price = round((random.randint(100, 10_000) / random.randint(10, 100)), 2)
            book_stock = random.randint(1, 100)
            book_isbn_no = uuid.uuid4()
            list_books.append(
                Product(
                    name=book_name,
                    price=book_price,
                    stock=book_stock,
                    isbn_no=book_isbn_no,
                )
            )

        Product.objects.bulk_create(list_books)

        self.stdout.write(self.style.SUCCESS("Successfully created fake 50 Books"))
