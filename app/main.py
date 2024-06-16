from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
import copy

from app.utils.utils import set_locale, inr, dict_inr, dict_clean
from app.services.tax_cal import deductions_dict, tax_handler, compare


set_locale()

app = FastAPI()

templates = Jinja2Templates(directory="app/templates")


@app.get("/", response_class=templates.TemplateResponse)
async def home_page(request: Request):
    try:
        return templates.TemplateResponse(
            "calc.html",
            {
                "request": request,
            },
        )
    except Exception as e:
        return templates.TemplateResponse(
            "error.html",
            {
                "request": request,
                "messages": [e, "Something Unexpected Happened"],
            },
        )


@app.get("/compare/", response_class=templates.TemplateResponse)
async def home_page(request: Request):
    try:
        return templates.TemplateResponse(
            "compare.html",
            {
                "request": request,
            },
        )
    except Exception as e:
        return templates.TemplateResponse(
            "error.html",
            {
                "request": request,
                "messages": [e, "Something Unexpected Happened"],
            },
        )


@app.post("/deductions/", response_class=templates.TemplateResponse)
async def deductions(
    request: Request,
    income: str = Form(...),
    regime: str = Form(...),
):
    try:
        income_clean = (
            income.replace(" ", "")
            .replace("₹", "")
            .replace(",", "")
            .replace(".00", "")
        )
        if isinstance(income_clean, str) and not income_clean.isdigit():
            return templates.TemplateResponse(
                "error.html",
                {
                    "request": request,
                    "messages": ["Found Invalid Input In Atleast One Field"],
                },
            )
        else:
            income = float(income_clean)

        deductions = dict_inr(copy.deepcopy(deductions_dict))

        return templates.TemplateResponse(
            "deductions.html",
            {
                "request": request,
                "income": inr(income),
                "regime": regime,
                "deductions": deductions[regime],
            },
        )
    except Exception as e:
        return templates.TemplateResponse(
            "error.html",
            {
                "request": request,
                "messages": [e, "Something Unexpected Happened"],
            },
        )


@app.post("/calculate/", response_class=templates.TemplateResponse)
async def calculate(
    request: Request,
):
    try:
        form_data = dict_clean(dict(await request.form()))
        income = form_data["income"]
        regime = form_data["regime"]
        deductions = {
            key: value
            for key, value in form_data.items()
            if (key in deductions_dict["old"] or key in deductions_dict["new"])
        }

        for value in deductions.values():
            if isinstance(value, str):
                return templates.TemplateResponse(
                    "error.html",
                    {
                        "request": request,
                        "messages": [
                            "Found Invalid Input In Atleast One Field"
                        ],
                    },
                )

        tax, messages = tax_handler(
            income=income,
            regime=regime,
            deductions=deductions,
            messages=[],
        )

        if tax != -1:
            return templates.TemplateResponse(
                "results.html",
                {
                    "request": request,
                    "income": inr(income),
                    "regime": regime,
                    "tax": inr(tax),
                    "messages": messages,
                },
            )
        else:
            return templates.TemplateResponse(
                "error.html",
                {
                    "request": request,
                    "messages": messages,
                },
            )
    except Exception as e:
        return templates.TemplateResponse(
            "error.html",
            {
                "request": request,
                "messages": [e, "Something Unexpected Happened"],
            },
        )
