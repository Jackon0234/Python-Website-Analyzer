import ssl
import socket
import whois
from datetime import datetime
from urllib.parse import urlparse

class NetworkIntelligence:
    def get_whois_data(self, domain: str) -> dict:
        try:
            w = whois.whois(domain)
            return {
                "registrar": w.registrar,
                "creation_date": self._format_date(w.creation_date),
                "expiration_date": self._format_date(w.expiration_date),
                "emails": w.emails
            }
        except:
            return None

    def get_ssl_info(self, url: str) -> dict:
        try:
            hostname = urlparse(url).netloc
            ctx = ssl.create_default_context()
            with ctx.wrap_socket(socket.socket(), server_hostname=hostname) as s:
                s.settimeout(5)
                s.connect((hostname, 443))
                cert = s.getpeercert()
                
                subject = dict(x[0] for x in cert['subject'])
                issuer = dict(x[0] for x in cert['issuer'])
                not_after = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
                
                remaining_days = (not_after - datetime.now()).days
                
                return {
                    "issuer": issuer.get('organizationName', issuer.get('commonName', 'Unknown')),
                    "valid_until": not_after.strftime('%d.%m.%Y'),
                    "days_left": remaining_days,
                    "secure": True
                }
        except:
            return {"secure": False, "error": "SSL Not Found or Invalid"}

    def _format_date(self, date_obj) -> str:
        if isinstance(date_obj, list):
            date_obj = date_obj[0]
        if isinstance(date_obj, datetime):
            return date_obj.strftime('%d.%m.%Y')
        return str(date_obj)