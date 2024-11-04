"""portfolio_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from pathlib import Path

from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static

from portfolio_site import settings
from portfolio_site.views import site_pages

urlpatterns = [
    path('', site_pages.homepage, name='home'),
    path('about/', site_pages.about_index, name='about_index'),
    path('about/about_website', site_pages.about_website, name='about_website'),
    path('about/contact_me', site_pages.contact_form, name='contact_me'),
    path('projects/', site_pages.project_index, name='project_index'),
    path('projects/console_calculator/', site_pages.console_calc_desc, name='console_calc_index'),
    path('projects/console_calculator/changelog', site_pages.console_calc_changelog, name='console_calc_changelog'),
    path('projects/console_calculator/downloads', site_pages.console_calc_downloads, name='console_calc_downloads'),
    path('projects/team_cake', site_pages.team_cake_view, name='team_cake'),
    path('download/<path:download_path>', site_pages.download_view, name='download_file'),
    path('research/', site_pages.research_index, name='research_index'),
    path('research/penn_snake_behrend', site_pages.penn_snake_behrend, name='penn_snake_behrend'),
    path('research/manufacturing_sim', site_pages.manuf_sim, name='manufacturing_sim'),
    path('research/synsec_group', site_pages.synsec_group, name='synsec_group'),
    path('admin/', admin.site.urls),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
