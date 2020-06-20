import os
import dj_database_url

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '%-#u&bhr_31k901s6vf6ktiax9x!_(efmh6-n*!5w6joqgz#fa'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic', 
    'django.contrib.staticfiles',
    'django.contrib.sites', 
    'users.apps.UsersConfig',
    'report.apps.ReportConfig',

    'crispy_forms',
    'allauth',
    'allauth.account',
    'django_social_share',

    
    'pages.apps.PagesConfig',
    'articles.apps.ArticlesConfig',
    'notifications.apps.NotificationsConfig',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Empire_of_Movies.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
            ],
        },
    },
]

WSGI_APPLICATION = 'Empire_of_Movies.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.postgresql_psycopg2',
    #     'NAME': 'd1ivjqpgpjngmn',
    #     'USER': 'dirhxrxonskcrc',
    #     'PASSWORD': 'd7033cbd8d273e1fae89037217a9a6038d25d8d40eacdd639cce078aa12645b9',
    #     'HOST': 'ec2-34-195-169-25.compute-1.amazonaws.com',
    #     'PORT': '5432',
    # }

        # 'default': {
        # 'ENGINE': 'django.db.backends.postgresql_psycopg2',
        # 'NAME': 'empire2',
        # 'USER': 'postgres',
        # 'PASSWORD': 'gilbert19',
        # 'HOST': '127.0.0.1',
        # 'PORT': '5432',
    # }
    

    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'empire_of_movies',
        'USER': 'dhafinrazaq',
        'PASSWORD': '123',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }

}
db_from_env = dj_database_url.config(conn_max_age=600)
DATABASES['default'].update(db_from_env)

#  PGUSER=dhafinrazaq PGPASSWORD=123  heroku pg:push postgres://127.0.0.1/empire_of_movies postgresql-perpendicular-60239

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Singapore'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'#location where django collect all static files

AUTH_USER_MODEL = 'users.CustomUser'

LOGIN_REDIRECT_URL = 'home'
ACCOUNT_LOGOUT_REDIRECT = 'home'

CRISPY_TEMPLATE_PACK = 'bootstrap4'

#django-allauth config
SITE_ID = 1

AUTHENTICATION_BACKENDS = (
'django.contrib.auth.backends.ModelBackend',
'allauth.account.auth_backends.AuthenticationBackend', # new
)

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

ACCOUNT_SESSION_REMEMBER = True