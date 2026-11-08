cat > build.sh << 'EOF'
#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate

python manage.py shell -c "
import os
from django.contrib.auth import get_user_model
U = get_user_model()
name = os.environ['DJANGO_SUPERUSER_USERNAME']
u, _ = U.objects.get_or_create(**{U.USERNAME_FIELD: name})
u.set_password(os.environ['DJANGO_SUPERUSER_PASSWORD'])
u.is_staff = True
u.is_superuser = True
u.is_active = True
u.save()
print('Admin user ready')
"
EOF