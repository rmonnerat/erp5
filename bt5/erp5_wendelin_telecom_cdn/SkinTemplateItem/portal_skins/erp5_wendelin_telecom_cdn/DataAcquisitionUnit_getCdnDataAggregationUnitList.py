if context.getReference() is None:
  return []

portal = context.getPortalObject()
reference_list = context.DataAcquisitionUnit_getCdnDataAggregationUnitReferenceList()
if not reference_list:
  return []

return portal.portal_catalog(
  portal_type='Data Aggregation Unit',
  reference=reference_list,
  validation_state='validated'
)
