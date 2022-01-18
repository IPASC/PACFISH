from coverage import Coverage
import pytest

cov = Coverage(source=['pacfish'])
cov.start()

pytest.main()

cov.stop()
cov.save()

cov.report(skip_empty=True, skip_covered=False)
cov.html_report(directory="../docs/source/coverage")
