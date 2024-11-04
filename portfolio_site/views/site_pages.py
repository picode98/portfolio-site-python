import json

from django.conf import settings
from django.urls import reverse
from django.views import View
from django.http import FileResponse, HttpResponseNotFound, HttpResponseBadRequest

from portfolio_site.downloads import ReleaseList, FileDownloadCount
from portfolio_site.views.contact_form import contact_form
from portfolio_site.views.site_views import SiteTemplateView, PlainPageView, LinkListView


class DownloadView(View):
    def get(self, request, *args, **kwargs):
        if '..' not in kwargs['download_path']:
            download_path = settings.DOWNLOADS_ROOT / kwargs['download_path']
            try:
                file_ref = open(download_path, 'rb')

                existing_count = FileDownloadCount.objects.filter(download_path=kwargs['download_path']).first()
                if existing_count is None:
                    FileDownloadCount(download_path=kwargs['download_path'], total_downloads=1, downloads_this_week=1).save()
                else:
                    existing_count.increment()

                return FileResponse(file_ref)
            except FileNotFoundError:
                return HttpResponseNotFound(b'The file requested was not found.')
        else:
            return HttpResponseBadRequest(b'The download path contained disallowed sequences: ".."')


download_view = DownloadView.as_view()


console_calc_release_manifest = settings.BASE_DIR / 'media' / 'console_calculator' / 'release_list.json'


class ConsoleCalculatorDescView(SiteTemplateView):
    template_name = 'projects/console_calculator/index.html'
    display_name = 'Console Calculator'
    desc_markup = '<p>Console Calculator is a console-based calculator with advanced features.</p>'

    def get(self, request, *args, **kwargs):
        with open(console_calc_release_manifest, encoding='utf8') as release_file:
            releases = ReleaseList.from_json_dict(json.load(release_file), resolve_root=console_calc_release_manifest.parent)

        newest_release = releases.releases[0]
        return super().get(request, *args, **{**kwargs, 'latestVersion': newest_release})


console_calc_desc = ConsoleCalculatorDescView.as_view()


class ConsoleCalculatorChangelog(SiteTemplateView):
    breadcrumb_parent = console_calc_desc
    display_name = 'Console Calculator Changelog'
    template_name = 'projects/console_calculator/changelog.html'


console_calc_changelog = ConsoleCalculatorChangelog.as_view()


class ConsoleCalculatorDownloadsView(SiteTemplateView):
    template_name = 'projects/console_calculator/downloads.html'
    display_name = 'Console Calculator Downloads'
    breadcrumb_parent = console_calc_desc

    def get(self, request, *args, **kwargs):
        with open(console_calc_release_manifest, encoding='utf8') as release_file:
            releases = ReleaseList.from_json_dict(json.load(release_file), resolve_root=console_calc_release_manifest.parent)

        return super().get(request, *args, **{**kwargs, 'releaseInfo': releases,
                                              'changelogURL': reverse(console_calc_changelog)})


console_calc_downloads = ConsoleCalculatorDownloadsView.as_view()


class PennSnakeBehrendView(PlainPageView):
    page_name = 'research/penn_snake_behrend.html'
    display_name = 'Penn Snake Behrend'
    desc_markup = 'A research project to create an open-source robotic snake at Penn State Behrend'


class SyNSecGroupView(PlainPageView):
    page_name = 'research/synsec_group.html'
    display_name = 'SyNSec Group'
    desc_markup = 'Research completed with the SyNSec group at Penn State'


penn_snake_behrend = PennSnakeBehrendView.as_view()
synsec_group = SyNSecGroupView.as_view()


class ManufSimView(PlainPageView):
    page_name = 'research/manufacturing_sim.html'
    display_name = 'Manufacturing Simulation'
    desc_markup = 'A manufacturing simulation developed in cooperation with Industrial Engineering at Penn State Behrend'


manuf_sim = ManufSimView.as_view()


class ResearchIndexView(LinkListView):
    display_name = 'Research'
    desc_markup = 'Research projects whose teams I am working on or have worked on'
    list_desc_markup = 'The following are research projects that I\'m currently working on or have worked on in the past:'
    list_views = [penn_snake_behrend, manuf_sim, synsec_group]


research_index = ResearchIndexView.as_view()

class TeamCakeView(SiteTemplateView):
    template_name = 'projects/team_cake.html'
    display_name = 'Ingenuity: Team Cake'
    desc_markup = 'A project to create a giant birthday cake with Ingenuity Cleveland'

team_cake_view = TeamCakeView.as_view()

class ProjectIndexView(LinkListView):
    display_name = 'Projects'
    desc_markup = 'Software projects that I\'m currently developing or have developed'
    list_desc_markup = 'The following are projects that I am working on or have worked on:'
    list_views = [console_calc_desc, team_cake_view]


project_index = ProjectIndexView.as_view()


class AboutWebsiteView(PlainPageView):
    page_name = 'about/about_website.html'
    display_name = 'About This Website'


about_website = AboutWebsiteView.as_view()


class AboutIndexView(LinkListView):
    display_name = 'About'
    desc_markup = 'Information about myself and this website'
    list_desc_markup = '<p>About pages on this website:</p>'
    list_views = [about_website, contact_form]


about_index = AboutIndexView.as_view()


class HomepageView(LinkListView):
    display_name = 'Homepage'
    breadcrumb_name = 'Home'
    list_desc_markup = "<p>Welcome to Saaman Khalilollahi's personal site. This site is divided into the following sections:</p>"
    list_views = [about_index, project_index, research_index]


homepage = HomepageView.as_view()
