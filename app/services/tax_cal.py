from typing import Union
from app.utils.utils import inr


deductions_dict = {
    "old": {
        "standard": {
            "name": "80TTB Standard",
            "limit": 50000,
        },
        "lta": {
            "name": "Sec 10(5) LTA",
            "limit": "na",
        },
        "hra": {
            "name": "Sec 10(13A) HRA",
            "limit": "na",
        },
        "food_voucher": {
            "name": "Food Voucher / Coupon",
            "limit": "na",
        },
        "vi_a": {
            "name": "Chapter VIA Investments (80C,80D,..)",
            "limit": 150000,
        },
        "employer_nps": {
            "name": "Sec 80CCD(2) Employer's NPS Contribution",
            "limit": "na",
        },
        "employee_nps": {
            "name": "80CCD(1B) Employee's NPS Contribution",
            "limit": 50000,
        },
        "medical_insurance": {
            "name": "Sec 80D Medical Insurance Premium",
            "limit": 50000,
        },
        "home_loan": {
            "name": "Home Loan Interest",
            "limit": "na",
        },
    },
    "new": {
        "standard": {
            "name": "80TTB Standard",
            "limit": 50000,
        },
        "employer_nps": {
            "name": "Sec 80CCD(2) Employer's NPS Contribution",
            "limit": "na",
        },
    },
}


def compare(
    old_tax: Union[int, float],
    new_tax: Union[int, float],
    messages: list = [],
) -> list:
    if old_tax > new_tax:
        messages.append(
            f"Benefit Of {inr(old_tax - new_tax)} Under New Tax Regime"
        )
    elif new_tax > old_tax:
        messages.append(
            f"Benefit Of {inr(new_tax - old_tax)} Under Old Tax Regime"
        )
    else:
        messages.append(f"No Benefit In Either Tax Regime")

    return messages


def deduct(
    income: Union[int, float],
    regime: str,
    deductions: dict,
    messages: list = [],
) -> Union[Union[int, float], tuple]:
    for deduction in deductions:
        if deduction in deductions_dict[regime]:
            less = deductions[deduction]
            if (
                deductions_dict[regime][deduction]["limit"] != "na"
                and less > deductions_dict[regime][deduction]["limit"]
            ):
                less = deductions_dict[regime][deduction]["limit"]
            income -= less
            if income <= 0:
                messages.append(f"Deductions Exceeded Income, Exiting ..")
                return -1, messages
            messages.append(
                f"Taxable Income After "
                f"{deductions_dict[regime][deduction]['name']} "
                f"Deduction Of {inr(less)} = {inr(income)}"
            )
    return income, messages


def tax_handler(
    income: Union[int, float],
    regime: str,
    deductions: dict,
    messages: list = [],
) -> Union[Union[int, float], tuple]:
    income, messages = deduct(
        income=income,
        regime=regime,
        deductions=deductions,
        messages=messages,
    )
    if income == -1:
        return income, messages
    if regime == "old":
        tax, messages = tax_old(
            income=income,
            messages=messages,
        )
    elif regime == "new":
        tax, messages = tax_new(
            income=income,
            messages=messages,
        )
    else:
        messages.append("Invalid Regime")
        return -1, messages
    messages.append(f"Total Tax = {inr(tax)}")
    cess = round(0.04 * tax, 2)
    messages.append(f"Cess @ 4% = {inr(cess)}")
    tax = round(tax + cess, 2)
    messages.append(f"Total Tax Inclusive Of Cess = {inr(tax)}")
    return tax, messages


def tax_old(
    income: Union[int, float],
    messages: list = [],
) -> Union[Union[int, float], tuple]:
    tax = 0
    if income > 1000000:
        taxable = income - 1000000
        tax_at_slab = round(0.3 * taxable, 2)
        messages.append(f"{inr(taxable)} Taxed @ 30% = {inr(tax_at_slab)}")
        tax, messages = tax_old(income=1000000, messages=messages)
        tax = tax + tax_at_slab
    elif income > 500000:
        taxable = income - 500000
        tax_at_slab = round(0.2 * taxable, 2)
        messages.append(f"{inr(taxable)} Taxed @ 20% = {inr(tax_at_slab)}")
        tax, messages = tax_old(income=500000, messages=messages)
        tax = tax + tax_at_slab
    elif income > 250000:
        taxable = income - 250000
        tax_at_slab = round(0.05 * taxable, 2)
        messages.append(f"{inr(taxable)} Taxed @ 05% = {inr(tax_at_slab)}")
        tax = tax_at_slab
    return tax, messages


def tax_new(
    income: Union[int, float],
    messages: list = [],
) -> Union[Union[int, float], tuple]:
    tax = 0
    if income > 1500000:
        taxable = income - 1500000
        tax_at_slab = round(0.3 * taxable, 2)
        messages.append(f"{inr(taxable)} Taxed @ 30% = {inr(tax_at_slab)}")
        tax, messages = tax_new(income=1500000, messages=messages)
        tax = tax + tax_at_slab
    elif income > 1200000:
        taxable = income - 1200000
        tax_at_slab = round(0.2 * taxable, 2)
        messages.append(f"{inr(taxable)} Taxed @ 20% = {inr(tax_at_slab)}")
        tax, messages = tax_new(income=1200000, messages=messages)
        tax = tax + tax_at_slab
    elif income > 900000:
        taxable = income - 900000
        tax_at_slab = round(0.15 * taxable, 2)
        messages.append(f"{inr(taxable)} Taxed @ 15% = {inr(tax_at_slab)}")
        tax, messages = tax_new(income=900000, messages=messages)
        tax = tax + tax_at_slab
    elif income > 600000:
        taxable = income - 600000
        tax_at_slab = round(0.1 * taxable, 2)
        messages.append(f"{inr(taxable)} Taxed @ 10% = {inr(tax_at_slab)}")
        tax, messages = tax_new(income=600000, messages=messages)
        tax = tax + tax_at_slab
    elif income > 300000:
        taxable = income - 300000
        tax_at_slab = round(0.05 * taxable, 2)
        messages.append(f"{inr(taxable)} Taxed @ 05% = {inr(tax_at_slab)}")
        tax = tax_at_slab
    return tax, messages
