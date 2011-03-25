# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2011 Justin Santa Barbara
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import unittest

from nova import flags
from nova import test
from nova.log import logging
from nova.tests.integrated import integrated_helpers
from nova.tests.integrated.api import client


LOG = logging.getLogger('nova.tests.integrated')

FLAGS = flags.FLAGS
FLAGS.verbose = True


class LoginTest(test.TestCase):
    def setUp(self):
        super(LoginTest, self).setUp()
        self.context = integrated_helpers.IntegratedUnitTestContext()
        self.user = self.context.test_user
        self.api = self.user.openstack_api

    def tearDown(self):
        self.context.cleanup()
        super(LoginTest, self).tearDown()

    def test_login(self):
        """Simple check - we list flavors - so we know we're logged in"""
        flavors = self.api.get_flavors()
        for flavor in flavors:
            LOG.debug(_("flavor: %s") % flavor)

    def test_bad_login_password(self):
        """Test that I get a 401 with a bad username"""
        bad_credentials_api = client.TestOpenStackClient(self.user.name,
                                                         "notso_password",
                                                         self.user.auth_url)

        self.assertRaises(client.OpenStackApiAuthenticationException,
                          bad_credentials_api.get_flavors)

    def test_bad_login_username(self):
        """Test that I get a 401 with a bad password"""
        bad_credentials_api = client.TestOpenStackClient("notso_username",
                                                         self.user.secret,
                                                         self.user.auth_url)

        self.assertRaises(client.OpenStackApiAuthenticationException,
                          bad_credentials_api.get_flavors)

    def test_bad_login_both_bad(self):
        """Test that I get a 401 with both bad username and bad password"""
        bad_credentials_api = client.TestOpenStackClient("notso_username",
                                                         "notso_password",
                                                         self.user.auth_url)

        self.assertRaises(client.OpenStackApiAuthenticationException,
                          bad_credentials_api.get_flavors)


if __name__ == "__main__":
    unittest.main()