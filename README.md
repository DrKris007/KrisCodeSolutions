KrisCodeSolutions Website
A professional business website for KrisCodeSolutions ("We Build Websites and Apps."), built with Python and Django. Content (projects, services, team, contact details, social links) is managed from the Django admin dashboard.
1. Features
- Pages: Home, About Us, Services, Projects / Portfolio, Contact
- Sticky responsive navigation with mobile menu and active-page highlighting
- Dynamic portfolio and services loaded from the database, with empty states
- Contact form with server-side validation, CSRF protection, a spam honeypot and database storage
- Optional email notification (the form only records a notification as "sent" if an email really was sent)
- Custom-branded admin at /admin/ ("KrisCodeSolutions Administration") to manage projects, categories, services, team members, inquiries (with status: New / Contacted / In Progress / Completed) and site content
- SEO: page titles, meta descriptions, Open Graph tags, favicon, sitemap (/sitemap.xml), robots.txt
- Production-ready settings: environment variables, WhiteNoise static files, PostgreSQL via DATABASE_URL, HTTPS hardening
2. Technologies
Python, Django, Django ORM, HTML5, CSS3, vanilla JavaScript, Bootstrap Icons, SQLite (local) / PostgreSQL (production), WhiteNoise, Gunicorn.
3. Project structure
KrisCodeSolutions/
├── manage.py
├── requirements.txt
├── .env.example
├── .gitignore
├── config/                  # settings, urls, wsgi, asgi
└── website/
    ├── models.py  views.py  forms.py  admin.py  urls.py
    ├── management/commands/seed_content.py
    ├── migrations/
    ├── templates/website/   # base.html, home.html, about.html, ...
    └── static/website/      # css/, js/, images/
4. Clone the repository
git clone https://github.com/YOUR-USERNAME/KrisCodeSolutions.git
cd KrisCodeSolutions
5. Create and activate a virtual environment (Windows)
In the VS Code terminal (Command Prompt or PowerShell):
python -m venv venv
Activate it:
- Command Prompt: venv\Scripts\activate
- PowerShell: venv\Scripts\Activate.ps1
If PowerShell blocks the script, run this once and try again:
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned

You should now see (venv) at the start of your prompt.
6. Install dependencies
pip install -r requirements.txt
Then copy the example environment file:
copy .env.example .env
The defaults work for local development. Never commit .env.
7. Set up the database
python manage.py migrate
python manage.py seed_content
seed_content creates the default site settings, the five services and the four portfolio projects. It is safe to run again; it will not overwrite text you edited in the admin.
If Django says your models have changes not reflected in a migration, run python manage.py makemigrations and then python manage.py migrate once.

Add the two real screenshots (Acadestine and Capital City Trust)
The actual homepage screenshots are not bundled in this download. Save them with these exact names:
website/static/website/images/acadestine-homepage.png
website/static/website/images/capital-city-trust-homepage.png
Then run python manage.py seed_content again, which attaches each image to its project. Alternatively, upload them in the admin under Projects → Acadestine / Capital City Trust → Preview image. Until an image is added, the project card shows a neutral placeholder.

Those two projects are static previews only: no link, no iframe, no "Visit Website" button.
Add your official logo
A simple placeholder mark is included at website/static/website/images/logo-mark.svg (used in the navbar, footer and favicon). To use your supplied logo, replace that file, keeping the same name, or change the <img> references in website/templates/website/base.html. Replace og-image.png (1200x630) with a branded image for social sharing.
8. Create a superuser
python manage.py createsuperuser
Choose your own username and a strong password. Do not share or hard-code them.
9. Run the development server
python manage.py runserver
- Website: http://127.0.0.1:8000/
- Admin dashboard: http://127.0.0.1:8000/admin/
10. Using the admin
- Projects: add, edit, delete, upload or replace images, reorder (edit the Order number in the list), mark featured or inactive.
- Project categories: manage categories used by projects.
- Services: edit text, choose a Bootstrap Icons class (e.g. bi-cart3), upload an image, set order, enable or disable.
- Team members: add real team members only. The Team section appears on the site only when at least one active member exists.
- Contact inquiries: search, filter by status, change status inline or with bulk actions. Inquiries are visible only to logged-in staff.
- Site settings: About text, mission, vision, call-to-action text, contact details and social links.
External links on projects are hidden by default. A link only appears publicly if you add a URL and tick "Show external link".
11. Email notifications
By default, emails print to the terminal (development). For real email set these in .env:
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-address@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=KrisCodeSolutions <your-address@gmail.com>
CONTACT_NOTIFY_EMAIL=where-to-receive-notifications@example.com
For Gmail you need an App Password (not your normal password). Leave CONTACT_NOTIFY_EMAIL empty to turn notifications off; inquiries are still saved in the admin either way.
12. Run the tests
python manage.py test
13. Push to GitHub
git init
git add .
git commit -m "Initial commit: KrisCodeSolutions website"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/KrisCodeSolutions.git
git push -u origin main
Later changes: git add ., git commit -m "Describe your change", git push.

.gitignore already excludes .env, venv/, db.sqlite3 and media/, so secrets and local data are not uploaded.
14. Production configuration
Set these environment variables on your host (never in the code):
Variable	Example
DJANGO_SECRET_KEY	a long random string (see .env.example for how to generate one)
DJANGO_DEBUG	False
DJANGO_ALLOWED_HOSTS	www.yourdomain.com,yourdomain.com
DJANGO_CSRF_TRUSTED_ORIGINS	https://www.yourdomain.com,https://yourdomain.com
DATABASE_URL	postgres://USER:PASSWORD@HOST:5432/DBNAME
Email variables	see section 11


With DJANGO_DEBUG=False the app refuses to start without a real secret key, redirects to HTTPS, sets secure cookies and HSTS, and serves compressed, cache-busted static files through WhiteNoise.
15. Deploy (example: Render, Railway or similar)
1. Push the project to GitHub.
2. Create a new Web Service from the repository, and a PostgreSQL database. Copy its connection URL into DATABASE_URL.
3. Build command: pip install -r requirements.txt && python manage.py collectstatic --no-input && python manage.py migrate
4. Start command: gunicorn config.wsgi
5. Add the environment variables from section 14.
6. After the first deploy, open the service shell and run python manage.py createsuperuser and python manage.py seed_content.
Uploaded images in production
Images uploaded in the admin are stored in the media/ folder. Many hosts have a temporary filesystem, so uploads can disappear on redeploy. Either attach a persistent disk mounted at media/ and set DJANGO_SERVE_MEDIA=True, or move media to cloud storage (for example with django-storages and S3 or Cloudinary). Screenshots shipped in website/static/website/images/ are always available because they are static files.
16. Troubleshooting
- Icons or fonts not showing locally: Bootstrap Icons and Google Fonts load from a CDN, so you need an internet connection.
- ModuleNotFoundError: the virtual environment is not active. Activate it and re-run pip install -r requirements.txt.
- Images not appearing in admin or site during development: make sure DJANGO_DEBUG=True locally so /media/ is served.