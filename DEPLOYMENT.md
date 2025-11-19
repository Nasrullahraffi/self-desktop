- Site name and tagline
- Social media URLs
Optional:

- `GITHUB_TOKEN` - GitHub personal access token
- `GITHUB_USERNAME` - Your GitHub username
- `EMAIL_HOST_PASSWORD` - Email password
- `EMAIL_HOST_USER` - Email for sending messages
- `DATABASE_URL` - Database connection string
- `ALLOWED_HOSTS` - Your domain(s)
- `DEBUG` - Set to False
- `SECRET_KEY` - Django secret key
Required variables:

## Environment Variables for Production

---

See detailed guide in the Django documentation.

### Using Droplet

5. **Deploy**
4. **Add PostgreSQL database**
3. **Add environment variables**

   - Run Command: `gunicorn resumeproject.wsgi`
   - Build Command: `pip install -r requirements.txt && python manage.py collectstatic --noinput`
2. **Configure build settings**
1. **Connect GitHub repository**

### Using App Platform

## Deploy to DigitalOcean

---

```
python manage.py collectstatic
python manage.py createsuperuser
python manage.py migrate
```bash
7. **Run migrations**

Create .env file with your settings
6. **Environment variables**

- Directory: `/home/yourusername/resumeproject/staticfiles/`
- URL: `/static/`
Set in web app config:
5. **Static files**

```
application = get_wsgi_application()
from django.core.wsgi import get_wsgi_application

os.environ['DJANGO_SETTINGS_MODULE'] = 'resumeproject.settings'

    sys.path.append(path)
if path not in sys.path:
path = '/home/yourusername/resumeproject'

import sys
import os
```python
Edit WSGI file:
4. **WSGI configuration**

- Python 3.10
- Choose Manual configuration
- Add new web app
- Go to Web tab
3. **Configure web app**

```
pip install -r requirements.txt
workon myportfolio
mkvirtualenv --python=/usr/bin/python3.10 myportfolio
```bash
2. **Create virtual environment**

- Extract in your home directory
- Upload to PythonAnywhere
- Zip your project
1. **Upload code**

### Steps

## Deploy to PythonAnywhere

---

```
heroku run python manage.py sync_github --activate
```bash
10. **Sync GitHub projects (optional)**

```
heroku run python manage.py collectstatic --noinput
heroku run python manage.py createsuperuser
heroku run python manage.py migrate
```bash
9. **Run migrations**

```
git push heroku main
```bash
8. **Deploy**

```
heroku addons:create heroku-postgresql:hobby-dev
```bash
7. **Add PostgreSQL addon**

```
heroku config:set GITHUB_TOKEN=your-github-token
heroku config:set GITHUB_USERNAME=your-github-username
heroku config:set ALLOWED_HOSTS=your-app-name.herokuapp.com
heroku config:set DEBUG=False
heroku config:set SECRET_KEY=your-secret-key-here
```bash
6. **Set environment variables**

```
heroku create your-portfolio-name
```bash
5. **Create Heroku app**

```
heroku login
```bash
4. **Login to Heroku**

Already included in the project.
3. **Update requirements.txt**

```
python-3.12.0
```
2. **Create runtime.txt**

```
web: gunicorn resumeproject.wsgi --log-file -
```
1. **Create Procfile**

### Steps

- Heroku CLI installed
- Heroku account
### Prerequisites

## Deploy to Heroku


