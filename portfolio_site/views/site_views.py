from typing import List
import json

from bs4 import BeautifulSoup

from django.conf import settings
from django.utils.decorators import classonlymethod
from django.views.generic import TemplateView
from django.urls import reverse


class SiteTemplateView(TemplateView):
    display_name = None
    breadcrumb_name = None
    breadcrumb_parent = None
    view_generator = None

    @classonlymethod
    def as_view(cls, **initkwargs):
        if cls.view_generator is None:
            cls.view_generator = super().as_view(**initkwargs)
        return cls.view_generator

    def render_to_response(self, context, **response_kwargs):
        with open(settings.BASE_DIR / 'templates' / 'nav_items.json', 'r', encoding='utf8') as nav_items_file:
            nav_dict = json.load(nav_items_file)

        page_title = context.get('pageTitle') or getattr(self, 'display_name')

        this_cls = self.__class__
        breadcrumb_links = [(this_cls.breadcrumb_name or page_title, reverse(this_cls.view_generator))]
        while this_cls.breadcrumb_parent is not None:
            this_cls = this_cls.breadcrumb_parent.view_class
            breadcrumb_links.append((this_cls.breadcrumb_name or this_cls.display_name, reverse(this_cls.view_generator)))

        return super().render_to_response({**context, 'navItems': nav_dict['subList'], 'pageTitle': page_title,
                                           'breadcrumbAncestors': reversed(breadcrumb_links)}, **response_kwargs)


class PlainPageView(SiteTemplateView):
    template_name = 'plain_page_adapter.html'
    page_name: str = None

    def render_to_response(self, context, **response_kwargs):
        with open(settings.BASE_DIR / 'templates' / self.page_name, 'r', encoding='utf8') as page_file:
            document = BeautifulSoup(page_file, 'html.parser')
        head_content: str = document.head.decode_contents() if document.head else ''
        body_content: str = document.body.decode_contents()
        page_title: str = self.display_name or document.title.string

        return super().render_to_response({**context, 'page_head_content': head_content, 'page_body_content': body_content,
                                           'pageTitle': page_title}, **response_kwargs)


class LinkListView(SiteTemplateView):
    template_name = 'link_list_page.html'
    list_views = []
    list_desc_markup = ''

    @classonlymethod
    def as_view(cls, **initkwargs):
        view_obj = super().as_view(**initkwargs)

        for listed_view in view_obj.view_class.list_views:
            if listed_view.view_class.breadcrumb_parent is None:
                listed_view.view_class.breadcrumb_parent = view_obj

        return view_obj

    def render_to_response(self, context, **response_kwargs):
        view_info_dicts = [{'displayName': getattr(this_view.view_class, 'display_name', None),
                            'url': reverse(this_view),
                            'descMarkup': getattr(this_view.view_class, 'desc_markup', None)} for this_view in self.list_views]
        return super().render_to_response({**context, 'listDesc': self.list_desc_markup, 'viewList': view_info_dicts},
                                          **response_kwargs)
