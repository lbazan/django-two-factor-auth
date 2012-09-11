# coding=utf-8
from django.contrib.auth.backends import ModelBackend
from django.utils.timezone import now
from oath import accept_totp


class TokenBackend(ModelBackend):
    def authenticate(self, user, token):
        accepted, drift = accept_totp(token, user.token.seed)
        return user if accepted else None


class VerifiedComputerBackend(ModelBackend):
    def authenticate(self, user, computer_id):
        verification = user.verifiedcomputer_set.get(pk=computer_id)
        return user if verification.verified_until > now() else None