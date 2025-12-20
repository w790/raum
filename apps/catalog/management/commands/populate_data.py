from django.core.management.base import BaseCommand
from django.utils.text import slugify
from apps.catalog.models import Category, Product
from decimal import Decimal

class Command(BaseCommand):
    help = 'Populate database with synthetic data based on user specific products'

    def handle(self, *args, **options):
        self.stdout.write('Deleting old data...')
        Product.objects.all().delete()
        Category.objects.all().delete()

        self.stdout.write('Creating Categories...')
        cat_glasses = Category.objects.create(
            name='Glasses',
            slug='glasses',
            description='Optical frames and clear lenses.'
        )
        cat_sunglasses = Category.objects.create(
            name='Sunglasses',
            slug='sunglasses',
            description='Sun protection and style.'
        )

        products_data = [
            {
                'name': 'Heavenly 02',
                'price': 420.00,
                'category': cat_glasses,
                'description': 'Rimless silver metal frames with a sophisticated rectangular design. Ultra-lightweight titanium temples for maximum comfort.',
                'specs': {
                    'collection': '2025 Minimalist',
                    'frame_material': 'Titanium',
                    'lens_type': 'Clear Blue Light Filter',
                    'shape': 'Rectangular',
                    'uv_protection': '100% UVA/UVB',
                    'lens_width': 54.0,
                    'bridge_width': 18.0,
                    'frame_front_width': 145.0,
                    'temple_length': 148.0,
                    'lens_height': 34.0,
                    'country_of_origin': 'China',
                },
                'stock': 15,
                'available_sizes': ['S', 'M', 'L'],
                'is_active': True
            },
            {
                'name': 'Rollie 02',
                'price': 390.00,
                'category': cat_glasses,
                'description': 'Silver metal oval frames. Features a curved bridge and sleek temples for a modern classic look.',
                'specs': {
                    'collection': '2025 Bold Collection',
                    'frame_material': 'Silver Metal',
                    'lens_type': 'Clear',
                    'shape': 'Oval',
                    'uv_protection': '99.9%',
                    'lens_width': 52.0,
                    'bridge_width': 19.0,
                    'frame_front_width': 142.0,
                    'temple_length': 150.0,
                    'lens_height': 36.0,
                    'country_of_origin': 'South Korea',
                },
                'stock': 8,
                'available_sizes': ['S', 'M'],
                'is_active': True
            },
            {
                'name': 'Lolos 02',
                'price': 365.00,
                'category': cat_glasses,
                'description': 'Compact silver metal frames with a distinct rounded shape. Perfect for smaller face shapes.',
                'specs': {
                    'collection': 'Everyday Essentials',
                    'frame_material': 'Stainless Steel',
                    'lens_type': 'Clear with AR Coating',
                    'shape': 'Round',
                    'uv_protection': 'Standard',
                    'lens_width': 48.0,
                    'bridge_width': 21.0,
                    'frame_front_width': 138.0,
                    'temple_length': 145.0,
                    'lens_height': 40.0,
                    'country_of_origin': 'China',
                },
                'stock': 20,
                'available_sizes': ['XS', 'S', 'M', 'L', 'XL'],
                'is_active': True
            },
            {
                'name': 'Boba 02',
                'price': 420.00,
                'category': cat_glasses,
                'description': 'Futuristic silver metal frames with intricate temple detailing. A statement piece.',
                'specs': {
                    'collection': 'Avant-Garde 2025',
                    'frame_material': 'Titanium Alloy',
                    'lens_type': 'Photochromic Optional',
                    'shape': 'Cat-Eye',
                    'uv_protection': '100%',
                    'lens_width': 55.0,
                    'bridge_width': 17.0,
                    'frame_front_width': 146.0,
                    'temple_length': 152.0,
                    'lens_height': 38.0,
                    'country_of_origin': 'Japan',
                },
                'stock': 5,
                'available_sizes': ['M', 'L'],
                'is_active': True
            },
            {
                'name': 'Limes 02',
                'price': 0.00, # Coming soon usually implies no price yet or placeholder
                'category': cat_glasses,
                'description': 'Upcoming release. Sleek semi-rimless design with sharp angles.',
                'specs': {
                    'collection': 'Preview',
                    'frame_material': 'Beta Titanium',
                    'lens_type': 'Demo',
                    'shape': 'Geometric',
                    'uv_protection': 'N/A',
                    'lens_width': 53.0,
                    'bridge_width': 18.0,
                    'frame_front_width': 144.0,
                    'temple_length': 148.0,
                    'lens_height': 35.0,
                    'country_of_origin': 'China',
                },
                'stock': 0,
                'available_sizes': [],
                'is_active': False # Coming soon
            },
            {
                'name': 'Moody 02',
                'price': 390.00,
                'category': cat_glasses,
                'description': 'Silver metal frames with black acetate temple tips. A balance of industrial and comfort.',
                'specs': {
                    'collection': 'Urban Optical',
                    'frame_material': 'Metal & Acetate',
                    'lens_type': 'Blue Block',
                    'shape': 'Oval',
                    'uv_protection': 'UV400',
                    'lens_width': 51.0,
                    'bridge_width': 20.0,
                    'frame_front_width': 140.0,
                    'temple_length': 145.0,
                    'lens_height': 37.0,
                    'country_of_origin': 'China',
                },
                'stock': 12,
                'available_sizes': ['S', 'M', 'L'],
                'is_active': True
            },
        ]

        # Add some sunglasses just to have items in that category too
        sunglasses_data = [
             {
                'name': 'Rococo 01',
                'price': 520.00,
                'category': cat_sunglasses,
                'description': 'Bold black acetate sunglasses with sculptural curves.',
                'specs': {
                    'collection': '2025 Bold',
                    'frame_material': 'Acetate',
                    'lens_type': 'Black Zeiss Lenses',
                    'shape': 'Goggle',
                    'uv_protection': '100% UVA/UVB',
                    'lens_width': 54.0,
                    'bridge_width': 19.0,
                    'frame_front_width': 148.0,
                    'temple_length': 145.0,
                    'lens_height': 42.0,
                    'country_of_origin': 'Germany',
                },
                'stock': 10,
                'available_sizes': ['One Size'],
                'is_active': True
            },
        ]

        self.stdout.write('Creating Products...')
        
        all_products = products_data + sunglasses_data

        for p_data in all_products:
            specs = p_data.pop('specs')
            product = Product.objects.create(
                slug=slugify(p_data['name']),
                **p_data,
                **specs
            )
            self.stdout.write(f'Created product: {product.name}')

        self.stdout.write(self.style.SUCCESS('Successfully populated database'))
