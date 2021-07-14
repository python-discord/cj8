VULNERABILITIES = []
FAILURE_POINTS = 0


def add_failure(points):
    global FAILURE_POINTS
    FAILURE_POINTS += points


def add_vulnerabillity(vulnerability):
    VULNERABILITIES.append(vulnerability)


def remove_vulnerabillity(vulnerability):
    VULNERABILITIES.remove(vulnerability)
