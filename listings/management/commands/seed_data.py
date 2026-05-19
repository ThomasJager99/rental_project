from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date
from users.models import User
from listings.models import Listing
from bookings.models import Booking
from reviews.models import Review


class Command(BaseCommand):
    help = 'Fill the database with test data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Clearing old test data...')
        Review.objects.all().delete()
        Booking.objects.all().delete()
        Listing.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()

        self.stdout.write('Creating users...')

        # landlords
        ivan = User.objects.create_user(
            email='ivan@test.com',
            name='Ivan Petrov',
            password='pass1234',
            role='landlord'
        )
        maria = User.objects.create_user(
            email='maria@test.com',
            name='Maria Smirnova',
            password='pass1234',
            role='landlord'
        )

        # tenants
        anna = User.objects.create_user(
            email='anna@test.com',
            name='Anna Koroleva',
            password='pass1234',
            role='tenant'
        )
        alex = User.objects.create_user(
            email='alex@test.com',
            name='Alex Volkov',
            password='pass1234',
            role='tenant'
        )
        kate = User.objects.create_user(
            email='kate@test.com',
            name='Kate Morozova',
            password='pass1234',
            role='tenant'
        )

        self.stdout.write('Creating listings...')

        l1 = Listing.objects.create(
            owner=ivan,
            title='Cozy apartment in the city center',
            description='Bright apartment near the metro, fully furnished, fast wifi',
            location='Berlin',
            price=1200,
            rooms=2,
            property_type='apartment',
        )
        l2 = Listing.objects.create(
            owner=ivan,
            title='Studio near the park',
            description='Compact studio, perfect for one person, quiet area',
            location='Berlin',
            price=750,
            rooms=1,
            property_type='studio',
        )
        l3 = Listing.objects.create(
            owner=ivan,
            title='Large house with garden',
            description='Spacious house with a big garden, garage, two floors',
            location='Munich',
            price=2800,
            rooms=5,
            property_type='house',
        )
        l4 = Listing.objects.create(
            owner=maria,
            title='Room in a shared flat',
            description='Nice room in a friendly shared apartment, all bills included',
            location='Berlin',
            price=500,
            rooms=1,
            property_type='room',
        )
        l5 = Listing.objects.create(
            owner=maria,
            title='Modern apartment with balcony',
            description='New building, panoramic view, parking spot included',
            location='Hamburg',
            price=1600,
            rooms=3,
            property_type='apartment',
        )
        l6 = Listing.objects.create(
            owner=maria,
            title='Small studio near university',
            description='Good transport links, suitable for students',
            location='Munich',
            price=620,
            rooms=1,
            property_type='studio',
            is_active=False,  # inactive listing to test filtering
        )

        self.stdout.write('Creating bookings...')

        # anna books l1 from ivan — confirmed (so she can leave a review)
        b1 = Booking.objects.create(
            listing=l1,
            tenant=anna,
            start_date=date(2025, 6, 1),
            end_date=date(2025, 6, 15),
            status='confirmed'
        )

        # alex books l1 — different dates, pending
        b2 = Booking.objects.create(
            listing=l1,
            tenant=alex,
            start_date=date(2025, 7, 1),
            end_date=date(2025, 7, 10),
            status='pending'
        )

        # kate books l5 from maria — confirmed
        b3 = Booking.objects.create(
            listing=l5,
            tenant=kate,
            start_date=date(2025, 6, 20),
            end_date=date(2025, 6, 30),
            status='confirmed'
        )

        # anna books l3 — rejected
        b4 = Booking.objects.create(
            listing=l3,
            tenant=anna,
            start_date=date(2025, 8, 1),
            end_date=date(2025, 8, 7),
            status='rejected'
        )

        # alex books l4 — cancelled
        b5 = Booking.objects.create(
            listing=l4,
            tenant=alex,
            start_date=date(2025, 9, 1),
            end_date=date(2025, 9, 14),
            status='cancelled'
        )

        self.stdout.write('Creating reviews...')

        # anna can review l1 — she has confirmed booking
        Review.objects.create(
            listing=l1,
            user=anna,
            rating=5,
            text='Amazing place, exactly as described. Ivan was very responsive!'
        )

        # kate can review l5 — she has confirmed booking
        Review.objects.create(
            listing=l5,
            user=kate,
            rating=4,
            text='Great apartment, beautiful view. Only minor issue was the parking.'
        )

        # bump views_count manually to make analytics interesting
        l1.views_count = 42
        l1.save()
        l2.views_count = 18
        l2.save()
        l3.views_count = 31
        l3.save()
        l4.views_count = 7
        l4.save()
        l5.views_count = 25
        l5.save()

        self.stdout.write(self.style.SUCCESS('\nDone! Test data created:'))
        self.stdout.write(f'  Users:    5 (2 landlords, 3 tenants)')
        self.stdout.write(f'  Listings: 6 (5 active, 1 inactive)')
        self.stdout.write(f'  Bookings: 5 (confirmed x2, pending x1, rejected x1, cancelled x1)')
        self.stdout.write(f'  Reviews:  2')
        self.stdout.write(f'\nTest accounts (all passwords: pass1234):')
        self.stdout.write(f'  ivan@test.com    — landlord (3 listings)')
        self.stdout.write(f'  maria@test.com   — landlord (3 listings)')
        self.stdout.write(f'  anna@test.com    — tenant (can review listing 1)')
        self.stdout.write(f'  alex@test.com    — tenant')
        self.stdout.write(f'  kate@test.com    — tenant (can review listing 5)')
