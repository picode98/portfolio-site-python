import datetime
import pathlib
from os.path import getsize
import hashlib
from pathlib import Path
from typing import List

from django.conf import settings
from django.db import models

from portfolio_site.json_oop import JSONDeserializable


def file_hash(path: Path, method, chunk_size: int = 1048576):
    with open(path, 'rb') as file:
        while True:
            chunk: bytes = file.read(chunk_size)
            if len(chunk) == 0:
                break
            else:
                method.update(chunk)

    return method


class ReleaseFile(JSONDeserializable):
    releaseDate: datetime.date
    releaseDate_format = '%d/%m/%Y'
    filePath: str
    resolve_root: pathlib.Path
    displayName: str

    @property
    def full_path(self):
        return self.resolve_root / self.filePath

    @property
    def url_rel_downloads_root(self):
        return '/'.join(self.full_path.relative_to(settings.DOWNLOADS_ROOT).parts)

    @property
    def fileSize(self):
        return getsize(self.full_path)

    @property
    def sha1(self):
        return file_hash(self.full_path, hashlib.sha1()).hexdigest()

    @property
    def sha256(self):
        return file_hash(self.full_path, hashlib.sha256()).hexdigest()


class Release(JSONDeserializable):
    version: str
    files: List[ReleaseFile]


class ReleaseList(JSONDeserializable):
    releases: List[Release]


class FileDownloadCount(models.Model):
    download_path = models.CharField(verbose_name='Download path', max_length=255, primary_key=True)
    downloads_this_week = models.PositiveBigIntegerField(verbose_name='Downloads this week', null=False, default=0)
    total_downloads = models.PositiveBigIntegerField(verbose_name='Total downloads', null=False, default=0)

    def increment(self):
        self.downloads_this_week += 1
        self.total_downloads += 1
        self.save()
