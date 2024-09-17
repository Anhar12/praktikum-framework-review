from django.core.management.base import BaseCommand
from faker import Faker
from ais.models import Users, Teachers, Students  # Ganti dengan nama app kamu
from django.db.utils import IntegrityError
import random

class Command(BaseCommand):
    help = 'Seed database with initial data'

    def add_arguments(self, parser):
        # Add optional argument for specifying number of users, teachers, and students to seed
        parser.add_argument('--users', type=int, default=30, help='Number of users to seed (default: 30)')
        parser.add_argument('--teachers', type=int, default=10, help='Number of teachers to seed (default: 10)')
        parser.add_argument('--students', type=int, default=20, help='Number of students to seed (default: 20)')

    def handle(self, *args, **kwargs):
        fake = Faker('id_ID')  # Menggunakan locale 'id_ID' untuk data Indonesia

        # Clear existing data (optional, based on needs)
        Users.objects.all().delete()
        Teachers.objects.all().delete()
        Students.objects.all().delete()

        teacher_list = []
        num_teachers = kwargs['teachers']
        num_students = kwargs['students']

        # Seed Teachers
        for _ in range(num_teachers):
            while True:  # Loop to ensure uniqueness
                try:
                    teacher = Teachers.objects.create(
                        nip=fake.unique.random_int(min=1, max=10**20-1),
                        name=fake.name(),
                        email=fake.unique.email(),
                        phone_number=fake.unique.phone_number()
                    )
                    teacher_list.append(teacher)
                    break
                except IntegrityError:  # Handle uniqueness constraint errors
                    fake.unique.clear()  # Clear uniqueness cache
                    continue

        self.stdout.write(self.style.SUCCESS(f'{len(teacher_list)} Teachers added'))

        # Seed Users (num_teachers Teachers and num_students Students)
        for teacher in teacher_list:
            while True:  # Loop to ensure uniqueness
                try:
                    Users.objects.create(
                        username=teacher.name.replace(" ", "").lower(),
                        password=fake.password(),
                        role=Users.TEACHER
                    )
                    break
                except IntegrityError:
                    fake.unique.clear()
                    continue

        student_list = []
        for _ in range(num_students):
            while True:  # Loop to ensure uniqueness
                try:
                    student = Users.objects.create(
                        username=fake.unique.user_name(),
                        password=fake.password(),
                        role=Users.STUDENT
                    )
                    student_list.append(student)
                    break
                except IntegrityError:
                    fake.unique.clear()
                    continue

        self.stdout.write(self.style.SUCCESS(f'{num_students} Students and {num_teachers} Teachers Users added'))

        # Seed Students
        for _ in range(num_students):
            while True:  # Loop to ensure uniqueness
                try:
                    Students.objects.create(
                        nim=fake.unique.random_int(min=1, max=10**10-1),
                        name=fake.name(),
                        email=fake.unique.email(),
                        phone_number=fake.unique.phone_number(),
                        year=fake.random_int(min=2010, max=2024),
                        teacher=random.choice(teacher_list)
                    )
                    break
                except IntegrityError:
                    fake.unique.clear()
                    continue

        self.stdout.write(self.style.SUCCESS(f'{num_students} Students added with teacher relations.'))
