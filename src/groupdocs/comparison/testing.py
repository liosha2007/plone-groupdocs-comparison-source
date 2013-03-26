from plone.app.testing import PloneWithPackageLayer
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting

import groupdocs.comparison


GROUPDOCS_COMPARISON = PloneWithPackageLayer(
    zcml_package=groupdocs.comparison,
    zcml_filename='testing.zcml',
    gs_profile_id='groupdocs.comparison:testing',
    name="GROUPDOCS_COMPARISON")

GROUPDOCS_COMPARISON_INTEGRATION = IntegrationTesting(
    bases=(GROUPDOCS_COMPARISON, ),
    name="GROUPDOCS_COMPARISON_INTEGRATION")

GROUPDOCS_COMPARISON_FUNCTIONAL = FunctionalTesting(
    bases=(GROUPDOCS_COMPARISON, ),
    name="GROUPDOCS_COMPARISON_FUNCTIONAL")
