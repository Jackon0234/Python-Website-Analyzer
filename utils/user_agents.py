from fake_useragent import UserAgent

class AgentManager:
    def __init__(self):
        self.ua = UserAgent()

    def get_random(self) -> str:
        try:
            return self.ua.random
        except:
            return "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"