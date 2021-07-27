"""
Marker: A highly configurable automarker for university assignments.

For more details on this library please refer to:
- GitHub: https://www.github.com:mustafaquraish/marker
- PyPI: https://pypi.python.org/pypi/marker
- Documentation: http://marker-docs.readthedocs.org/
"""

from .marker import Marker
from .utils import Marksheet, pushd
from .utils.console import ConsoleABC
from .utils.token import TokenNotFoundError
from .utils import CONFIG_DIR

from .settings import __version__
