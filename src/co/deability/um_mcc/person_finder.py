from typing import Any, Dict, List

from co.deability.um_mcc import EmployeeProperties, SALARY_DATA


def find(args: dict[str, str]) -> List[Dict[str, Any]]:
    name: str = args.get(EmployeeProperties.NAME)
    if not name:
        raise KeyError(
            "You must include a query parameter called name with a non-empty value"
        )
    title: str = args.get(EmployeeProperties.TITLE)
    department: str = args.get(EmployeeProperties.DEPARTMENT)
    if title and department:
        return _find_by_name_dept_title(name=name, dept=department, title=title)
    if title:
        return _find_by_name_title(name=name, title=title)
    if department:
        return _find_by_name_dept(name=name, dept=department)
    return list(_find_by_name(name=name))


def _find_by_name(name: str) -> List[Dict[str, Any]]:
    assert name
    name_uc: str = name.upper()
    result: List[Dict[str, Any]] = list(
        filter(lambda item: name_uc in item[EmployeeProperties.NAME], SALARY_DATA)
    )
    result.sort(key=(lambda item: item.get(EmployeeProperties.NAME)))
    return result


def _find_by_name_dept(name: str, dept: str) -> List[Dict[str, Any]]:
    possible_matches: List[Dict[str, Any]] = list(_find_by_name(name=name))
    if not possible_matches:
        return []
    dept_uc: str = dept.upper()
    if (
        len(possible_matches) == 1
        and dept == possible_matches[0][EmployeeProperties.DEPARTMENT]
    ):
        return [possible_matches[0]]
    else:
        assert len(possible_matches) > 1
        return list(
            filter(
                lambda item: dept_uc in item[EmployeeProperties.DEPARTMENT],
                possible_matches,
            )
        )


def _find_by_name_title(name: str, title: str) -> List[Dict[str, Any]]:
    possible_matches: List[Dict[str, Any]] = list(_find_by_name(name=name))
    if not possible_matches:
        return []
    title_uc: str = title.upper()
    if (
        len(possible_matches) == 1
        and title == possible_matches[0][EmployeeProperties.TITLE]
    ):
        return [possible_matches[0]]
    else:
        assert len(possible_matches) > 1
        return list(
            filter(
                lambda item: title_uc in item[EmployeeProperties.TITLE],
                possible_matches,
            )
        )


def _find_by_name_dept_title(name: str, dept: str, title: str) -> List[Dict[str, Any]]:
    possible_matches: List[Dict[str, Any]] = list(
        _find_by_name_dept(name=name, dept=dept)
    )
    title_uc = title.upper()
    if (
        len(possible_matches) == 1
        and title_uc == possible_matches[0][EmployeeProperties.TITLE]
    ):
        return [possible_matches[0]]
    else:
        return (
            list(
                filter(
                    lambda item: title_uc in item[EmployeeProperties.TITLE],
                    possible_matches,
                )
            )
            if possible_matches
            else []
        )
