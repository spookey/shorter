from shorter.start.environment import SYM_POOL


def test_forbidden_routes(app):
    for route in app.url_map.iter_rules():
        rule = route.rule.lstrip("/")
        if rule and "/<" not in rule:
            if all(cha in SYM_POOL for cha in rule):
                assert False, f"/{rule} clashes with symbols!"
