import hashlib

from django.db import models
from django.contrib.auth.models import User

from .utils import send_transaction


class Post(models.Model):
    title = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    # SHA-256 hex digest is 64 characters long (not 32 — that would be MD5).
    hash = models.CharField(max_length=64, default=None, null=True)
    # Ethereum tx hash: "0x" + 64 hex chars = 66 characters.
    tx_id = models.CharField(max_length=66, default=None, null=True)

    def __str__(self):
        return self.title

    def write_on_chain(self):
        self.hash = hashlib.sha256(self.content.encode('utf-8')).hexdigest()
        self.tx_id = send_transaction(self.hash)
        self.save()
