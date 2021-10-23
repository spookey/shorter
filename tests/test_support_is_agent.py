from werkzeug.user_agent import UserAgent

from shorter.support import is_botagent, is_socialagent

BOTS = {
    "bing": """
Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)
    """.strip(),
    "google": """
Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)
""".strip(),
    "yahoo": """
Mozilla/5.0 (compatible; Yahoo! Slurp;
http://help.yahoo.com/help/us/ysearch/slurp)
    """.strip(),
    "yandex": """
Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)
    """.strip(),
}

SOCIAL = {
    "facebook": """
facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)
    """.strip(),
    "facebot": """
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1)
AppleWebKit/601.2.4 (KHTML, like Gecko) Version/9.0.1 Safari/601.2.4
facebookexternalhit/1.1 Facebot Twitterbot/1.0
    """.strip(),
    "twitterbot": """
Twitterbot/1.0
    """.strip(),
}

BROWSERS = {
    "chrome": """
Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)
Chrome/51.0.2704.103 Safari/537.36
    """.strip(),
    "edge": """
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36
(KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246
    """.strip(),
    "firefox": """
Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0
    """.strip(),
    "internet_explorer": """
Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5;
Trident/5.0; IEMobile/9.0)
    """.strip(),
    "iphone": """
Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X)
AppleWebKit/604.1.38 (KHTML, like Gecko)
Version/11.0 Mobile/15A372 Safari/604.1
    """.strip(),
    "opera": """
Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)
Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41
    """.strip(),
    "safari": """
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9
(KHTML, like Gecko) Version/9.0.2 Safari/601.3.9
    """.strip(),
}


def test_is_botagent():
    for agent_str in BOTS.values():
        agent = UserAgent(agent_str)
        assert is_botagent(agent) is True
        assert is_socialagent(agent) is False


def test_is_socialagent():
    for agent_str in SOCIAL.values():
        agent = UserAgent(agent_str)
        assert is_botagent(agent) is False
        assert is_socialagent(agent) is True


def test_browsers():
    for agent_str in BROWSERS.values():
        agent = UserAgent(agent_str)
        assert is_botagent(agent) is False
        assert is_socialagent(agent) is False
