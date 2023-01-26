import html
from decimal import Decimal
from enum import Enum
from pathlib import Path
from typing import Dict, Iterator, List, Final, Any

from flask import Flask

__version__: str = "0.0.1"


def init_app() -> Flask:

    app: Flask = Flask("um_mcc")
    app.config.from_object("co.deability.um_mcc.config")
    app.static_folder = Path(app.root_path, "build")
    app.static_url_path = "/"
    app.url_map.strict_slashes = False
    return app


class Employee(str, Enum):
    NAME = "name"
    TITLE = "title"
    DEPARTMENT = "department"
    SALARY = "salary"


def _read_file() -> Iterator[Dict]:
    filedir: Path = Path(__file__).parent
    filepath: Path = Path(filedir, "resources", "salary-disclosure-2022.csv")
    with filepath.open(mode="r", buffering=1) as salaryfile:
        salaryfile.readline()  # ignore header line
        line = salaryfile.readline()
        while line:
            yield _parse_line(html.unescape(line))
            line = salaryfile.readline()


def _parse_line(line: str):
    words: List[str] = line.split("|")
    assert len(words) == 8
    return {
        Employee.NAME: words[1].upper(),
        Employee.TITLE: words[2].upper(),
        Employee.DEPARTMENT: words[3].upper(),
        Employee.SALARY: Decimal("".join(words[4].split(","))),
    }


SALARY_DATA: Final[List[Dict[str, Any]]] = list(_read_file())
