from typing import Any


def diff_between_two_lists(li1, li2):
    li_dif = [i for i in li1 + li2 if i not in li1 or i not in li2]
    return li_dif


def map_application(app):
    redirect_uris: list[str] = [
        uri
        for group in [
            value.get("redirectUris") or []
            for value in app.values()
            if isinstance(value, dict)
        ]
        for uri in group
    ]
    return {"client_id": app.get("appId"), "redirect_uris": redirect_uris}


def search_list(key: str, value: Any, list: list):
    return [item for item in list if item.get(key) == value]
