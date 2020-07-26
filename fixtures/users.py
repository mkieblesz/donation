from django.contrib.auth.models import User

if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='admin',
        first_name='Mr',
        last_name='Admin',
    )

User.objects.get_or_create(
    username='user1',
    first_name='John',
    last_name='Smith',
)

User.objects.get_or_create(
    username='user2',
    first_name='Mark',
    last_name='Twain',
)
