##############################################################################
#
# Copyright (c) 2025 Nexedi SA and Contributors. All Rights Reserved.
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsibility of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# guarantees and support are strongly adviced to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
##############################################################################
from erp5.component.test.WendelinTelecomCdnMixin import TestWendelinTelecomCdnMixin
from erp5.component.test.WendelinTelecomMixin import generateRandomString
import json

class WendelinTelecomCdnTest(TestWendelinTelecomCdnMixin):

  def test_01_createCdnDataSupply(self):
    reference = 'test_%s' % generateRandomString()

    # Create and validate a Data Acquisition Unit
    data_acquisition_unit = self.portal.data_acquisition_unit_module.newContent(
      portal_type='Data Acquisition Unit',
      reference=reference
    )
    data_acquisition_unit.validate()
    self.tic()

    # Call the script which creates a related Data Supply
    created_data_supply = data_acquisition_unit.DataAcquisitionUnit_createCdnDataSupply(batch=1)
    self.tic()

    # Check that the Data Supply exists and is validated
    self.assertNotEqual(created_data_supply, None)
    self.assertEqual(created_data_supply.getValidationState(), 'validated')

    # Call the script again to retrieve the same Data Supply
    retrieved_data_supply = data_acquisition_unit.DataAcquisitionUnit_createCdnDataSupply(batch=1)

    # Check that both Data Supplies are identical
    self.assertEqual(retrieved_data_supply, created_data_supply)

    # Pathological case: create another identical Data Supply
    created_data_supply.invalidate()
    self.tic()
    data_acquisition_unit.DataAcquisitionUnit_createCdnDataSupply(batch=1)
    created_data_supply.validate()
    self.tic()

    re_retrieved_data_supply = \
      data_acquisition_unit.DataAcquisitionUnit_createCdnDataSupply(batch=1)

    self.assertEqual(re_retrieved_data_supply, created_data_supply)

    # Pathological case: create a Data Acquisition Unit without a reference
    data_acquisition_unit = self.portal.data_acquisition_unit_module.newContent(
      portal_type='Data Acquisition Unit',
    )
    data_acquisition_unit.validate()
    self.tic()
    self.addCleanup(self._removeDocument, data_acquisition_unit)

    # Call the script which should NOT create a Data Supply (no reference to copy over)
    none_data_supply = \
         data_acquisition_unit.DataAcquisitionUnit_createCdnDataSupply(batch=1)
    self.tic()
    self.assertEqual(none_data_supply, None)

  def test_03_1_registerCdnValid(self):

    # Call the script with an initial seed setup
    tag_cluster_seed = generateRandomString(length=3, only_digits=True)
    tag_node_seed = generateRandomString(length=4, only_digits=True)
    tag_shared_seed = generateRandomString(length=5, hexadecimal=True)
    cdn_item_dict = self.registerCdn(
      tag_cluster_seed=tag_cluster_seed,
      tag_node_seed=tag_node_seed,
      tag_shared_seed=tag_shared_seed
    )

    # Parse the JSON response and check that it indicates a success
    response_dict = json.loads(cdn_item_dict['response'])
    self.assertEqual(response_dict['status'], "ok")
    self.assertEqual(
      response_dict['message'], "CDN Access with tag %s successfully registered." \
      % cdn_item_dict['data_acquisition_unit'].getReference()
    )

    # Check that the Data Acquisition Unit and Data Supply have been created
    self.assertNotEqual(cdn_item_dict['data_acquisition_unit'], None)
    self.assertNotEqual(cdn_item_dict['data_supply'], None)

    # Call the script a second time with the same seeds
    # This should not do anything as the Data Acquisition Unit already exists
    repeated_cdn_item_dict = self.registerCdn(
      tag_cluster_seed=tag_cluster_seed,
      tag_node_seed=tag_node_seed,
      tag_shared_seed=tag_shared_seed
    )

    # Parse the JSON response and check the status and message
    response_dict = json.loads(repeated_cdn_item_dict['response'])
    self.assertEqual(response_dict['status'], "ok")
    self.assertEqual(
      response_dict['message'], "CDN Access with tag %s already exists." \
      % cdn_item_dict['data_acquisition_unit'].getReference()
    )
