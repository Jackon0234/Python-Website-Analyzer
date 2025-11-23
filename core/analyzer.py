import requests
import re
import socket
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from utils.user_agents import AgentManager
from core.network_tools import NetworkIntelligence
from config import settings

class WebAnalyzer:
    def __init__(self):
        self.agent = AgentManager()
        self.net_intel = NetworkIntelligence()
        self.session = requests.Session()

    def analyze(self, target_url: str) -> dict:
        if not target_url.startswith("http"):
            target_url = "https://" + target_url

        try:
            domain = urlparse(target_url).netloc
            ip_address = socket.gethostbyname(domain)
            
            headers = {
                "User-Agent": self.agent.get_random(),
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
            }

            response = self.session.get(target_url, headers=headers, timeout=settings.TIMEOUT, verify=False)
            response_time = round(response.elapsed.total_seconds(), 2)
            
            soup = BeautifulSoup(response.text, 'html.parser')
            html_content = response.text

            whois_data = self.net_intel.get_whois_data(domain)
            ssl_data = self.net_intel.get_ssl_info(target_url)

            seo_data = {
                "title": self._get_meta(soup, "title"),
                "description": self._get_meta(soup, "description"),
                "h1": self._get_h1(soup),
                "speed": response_time
            }

            tech_stack = {
                "cms": self._detect_cms(soup, html_content),
                "theme": self._detect_theme(html_content),
                "plugins": self._detect_plugins(html_content),
                "server": response.headers.get("Server", "Hidden"),
                "security": self._detect_security(response.headers),
                "ip": ip_address,
                "domain": domain,
                "whois": whois_data,
                "ssl": ssl_data,
                "seo": seo_data,
                "status_code": response.status_code
            }
            
            return tech_stack

        except Exception as e:
            return {"error": str(e)}

    def _get_meta(self, soup, type: str) -> str:
        if type == "title":
            return soup.title.string.strip() if soup.title else "Yok"
        if type == "description":
            desc = soup.find("meta", attrs={"name": "description"})
            return desc["content"][:50] + "..." if desc else "Yok"
        return "-"

    def _get_h1(self, soup) -> str:
        h1 = soup.find("h1")
        return h1.text.strip()[:30] + "..." if h1 else "Yok"

    def _detect_cms(self, soup, html: str) -> str:
        generator = soup.find("meta", attrs={"name": "generator"})
        if generator and generator.get("content"):
            return generator["content"]
        if "/wp-content/" in html: return "WordPress"
        if "Joomla" in html: return "Joomla"
        if "Shopify.d" in html: return "Shopify"
        if "Wix.com" in html: return "Wix"
        if "PrestaShop" in html: return "PrestaShop"
        return "Custom / Unknown"

    def _detect_theme(self, html: str) -> str:
        themes = re.findall(r'/wp-content/themes/([a-zA-Z0-9\-_]+)/', html)
        if themes: return list(set(themes))[0].title()
        shopify_theme = re.search(r'Shopify\.theme\s*=\s*{"name":"(.*?)"', html)
        if shopify_theme: return shopify_theme.group(1)
        return "Not Detected"

    def _detect_plugins(self, html: str) -> list:
        plugins = re.findall(r'/wp-content/plugins/([a-zA-Z0-9\-_]+)/', html)
        if plugins: return list(set(plugins))
        return []

    def _detect_security(self, headers: dict) -> list:
        sec_headers = []
        if "CF-RAY" in headers: sec_headers.append("Cloudflare")
        if "X-Frame-Options" in headers: sec_headers.append("Clickjack Protection")
        if "Strict-Transport-Security" in headers: sec_headers.append("HSTS")
        return sec_headers if sec_headers else ["Standard"]