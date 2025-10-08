import random
import uuid
from django.core.management.base import BaseCommand
from faker import Faker
from core.models import Student, Course

CAMPUS_CHOICES = ["Main", "South", "San Jose"]
YEAR_LEVEL_CHOICES = [1, 2, 3, 4, 5]

fake = Faker()

def generate_qr_id():
    return str(uuid.uuid4())  # Proper UUID

class Command(BaseCommand):
    help = "Seed the database with fake students including year level and UUID QR ID"

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='Number of fake students to create')

    def handle(self, *args, **kwargs):
        total = kwargs['total']
        courses = list(Course.objects.all())
        if not courses:
            self.stdout.write(self.style.ERROR('No courses found. Please seed departments and courses first.'))
            return

        for _ in range(total):
            name = fake.name()
            email = fake.unique.email()
            student_id = fake.unique.random_int(min=10000000, max=99999999)
            campus = random.choices(
                population=["South", "Main", "San Jose"],
                weights=[85, 14, 1],
                k=1
            )[0]

            course = random.choice(courses)
            year_level = random.choice(YEAR_LEVEL_CHOICES)

            student = Student.objects.create(
                name=name,
                studentId=student_id,
                email=email,
                roles='student',
                campus=campus,
                course=course,
                year_level=year_level,
                qrId=generate_qr_id()
            )

            self.stdout.write(self.style.SUCCESS(f"Created student {student}"))

# To run, 
# 
#       python ./manage.py student_seeder x
# 
# 
# Where x is the number of student to be generated
