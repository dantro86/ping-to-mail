from __future__ import print_function
import pyping


class PingSource:
    def __init__(self, ip, reachable_bul, gmail_client):
        self.ip = ip
        self.reachable_bul = reachable_bul
        self.gmail_client = gmail_client

    def ping(self):
        return pyping.ping(self.ip)

    def send_mail(self):
        self.gmail_client.send(not self.reachable_bul, self.ip)
        self.mailed_bul = True

