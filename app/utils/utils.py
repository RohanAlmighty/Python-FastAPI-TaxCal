import locale
from typing import Union


def set_locale() -> None:
    locale.setlocale(locale.LC_ALL, "en_IN")


def inr(value: Union[int, float]) -> str:
    return locale.currency(value, grouping=True)


def dict_inr(dict_in: dict) -> dict:
    for key, value in dict_in.items():
        if isinstance(value, dict):
            dict_inr(dict_in=value)
        else:
            if not isinstance(value, str):
                dict_in[key] = inr(value=value)
    return dict_in


def dict_clean(dict_in: dict) -> dict:
    for key, value in dict_in.items():
        if isinstance(value, dict):
            dict_inr(dict_in=value)
        else:
            if isinstance(value, str) and (
                "₹" in value or value.strip().isdigit()
            ):
                dict_in[key] = float(
                    value.replace("₹", "").replace(",", "").replace(" ", "")
                )
    return dict_in
