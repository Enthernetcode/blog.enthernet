"""Evidence-backed content modules for the Enthernet engineering blog."""

from content.aws import AWS_DAYS, UNVERIFIED_AWS
from content.ansible import ANSIBLE_DAYS
from content.linux_networking import LINUX_NETWORKING_DAYS
from content.docker import DOCKER_DAYS
from content.kubernetes import KUBERNETES_DAYS
from content.cicd import CICD_DAYS

SOURCES = (AWS_DAYS, ANSIBLE_DAYS, LINUX_NETWORKING_DAYS, DOCKER_DAYS, KUBERNETES_DAYS, CICD_DAYS)

DAY_CONTENT = {}
for _src in SOURCES:
    _overlap = set(DAY_CONTENT).intersection(_src)
    if _overlap:
        raise SystemExit(f"Duplicate day definitions: {sorted(_overlap)}")
    DAY_CONTENT.update(_src)

LAST_DAY = max(DAY_CONTENT)
PUBLISHED_DAYS = range(1, LAST_DAY + 1)

__all__ = ["DAY_CONTENT", "PUBLISHED_DAYS", "LAST_DAY", "UNVERIFIED_AWS"]
