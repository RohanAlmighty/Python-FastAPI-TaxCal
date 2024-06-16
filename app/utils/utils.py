from typing import Union


def inr(value: Union[int, float]) -> str:
    s, *d = str(value).partition(".")
    r = ",".join(
        [s[x - 2 : x] for x in range(-3, -len(s), -2)][::-1] + [s[-3:]]
    )
    return "₹ " + "".join([r] + d)


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
                "₹" in value or value.strip().replace(".", "").isdigit()
            ):
                dict_in[key] = float(
                    value.replace("₹", "").replace(",", "").replace(" ", "")
                )
    return dict_in
