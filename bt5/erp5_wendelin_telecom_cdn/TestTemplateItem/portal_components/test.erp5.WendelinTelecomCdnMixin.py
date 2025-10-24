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
from io import BytesIO
import json
import msgpack

from erp5.component.test.WendelinTelecomMixin import generateRandomString, \
                                                     TestWendelinTelecomMixin

class TestWendelinTelecomCdnMixin(TestWendelinTelecomMixin):

  def registerCdn(
    self,
    tag_cluster_seed=None,
    tag_node_seed=None,
    tag_shared_seed=None
  ):
    # Create a Data Acquisition Unit and related Data Supply
    # with a tag constructed from the provided seeds.
    # If any seed is NOT defined, it is generated at random.
    if tag_cluster_seed is None:
      tag_cluster_seed = generateRandomString(length=5, only_digits=True)
    if tag_node_seed is None:
      tag_node_seed = generateRandomString(length=5, only_digits=True)
    if tag_shared_seed is None:
      tag_shared_seed = generateRandomString(length=5, only_digits=True)

    cdn_tag = 'cdnaccess_cdnTESTINST-%sa' % tag_cluster_seed
    # Only include a subsequent section if a non-empty string is explicitly provided for it
    if tag_node_seed != '':
      cdn_tag += '_TESTINST-%sb' % tag_node_seed
    if tag_shared_seed != '':
      cdn_tag += '_TESTINST-%sc' % tag_shared_seed

    response = self.portal.ERP5Site_registerCdn(cdn_tag)
    self.tic()

    # Fetch created items from the catalog
    data_acquisition_unit = self.portal.portal_catalog.getResultValue(
      portal_type='Data Acquisition Unit',
      reference=cdn_tag,
      validation_state='validated'
    )
    data_supply = None
    if data_acquisition_unit is not None:
      data_supply = data_acquisition_unit.DataAcquisitionUnit_getOrsDataSupply()

    # Return all associated items
    return {
      'response': response,
      'data_acquisition_unit': data_acquisition_unit,
      'data_supply': data_supply
    }


  def ingestCdnLogDataFromFluentd(self, log_data, cdn_tag):
    # Simulate a fluentd instance sending the provided log data to Wendelin for ingestion
    reference = 'cdnaccess.%s' % cdn_tag
    body = msgpack.packb([0, log_data], use_bin_type=True)
    env = {'CONTENT_TYPE': 'application/octet-stream'}
    path = self.cdn_log_ingestion.getPath() + '/ingest?reference=' + reference
    publish_kw = dict(
      env=env,
      user=self.ingestor_user.Person_getUserId(),
      request_method='POST',
      stdin=BytesIO(body)
    )
    return self.publish(path, **publish_kw)

  def getCdnDataArrayAsDict(self, data_array_url, kpi_type):
    kpi_path = self.cdn_get_data_array_endpoint_path + '?data_array_url=' + \
      data_array_url + '&data_type=' + kpi_type
    publish_kw = dict(
      user='ERP5TypeTestCase'
    )
    response = self.publish(kpi_path, **publish_kw)
    body = response.getBody()
    return json.loads(body)
