import decimal
from decimal import Decimal
from typing import Any, Final, List

minutes_per_year: int = 2080 * 60
MINUTES_PER_YEAR: Final[Decimal] = Decimal(str(minutes_per_year) + ".00")


def _convert_to_two_dig_dec(value: Any) -> Decimal:
    if isinstance(value, str):
        value = "".join(value.split(","))
        if "." not in value:
            value += ".00"
    elif isinstance(value, int):
        value = str(value) + ".00"
    elif isinstance(value, Decimal):
        try:
            value = round(value, 2)
        except decimal.InvalidOperation:
            ...
        return value
    else:
        assert False
    return Decimal(value)


def calc_per_min_cost(salary: Decimal) -> Decimal:
    salary: Decimal = _convert_to_two_dig_dec(salary)
    per_min: Decimal = salary / MINUTES_PER_YEAR
    rounded: Decimal = round(per_min, 2)
    return rounded


def calc_attendee_cost(salary: Decimal, minutes: int) -> Decimal:
    attendee_cost: Decimal = calc_per_min_cost(salary=salary) * minutes
    return attendee_cost


def calc_meeting_cost(salaries: List[Decimal], minutes: int) -> Decimal:
    return sum(
        [calc_attendee_cost(salary=salary, minutes=minutes) for salary in salaries]
    )
