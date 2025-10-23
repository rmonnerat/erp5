portal = context.getPortalObject()
if not context.getReference():
  if batch:
    return None
  return context.Base_redirect('view', keep_items={
    'portal_status_message': 'Reference is not defined.',
    'portal_status_level': 'error'
  })

data_aggregation_reference_list = context.DataAcquisitionUnit_getCdnDataAggregationUnitReferenceList()
_data_aggregation_value_list = context.DataAcquisitionUnit_getCdnDataAggregationUnitList()

found_reference_list = [i.getReference() for i in _data_aggregation_value_list]
missing_data_aggregation_reference_list = [
  i for i in data_aggregation_reference_list if i not in found_reference_list]

if not missing_data_aggregation_reference_list:
  if batch:
    return _data_aggregation_value_list
  # XXX Redirect to module
  return context.Base_redirect('view', keep_items={
    'portal_status_message': 'All Data Aggregation Units already exist.'
  })

data_aggregation_value_list = [i.getObject() for i in _data_aggregation_value_list]
for reference in missing_data_aggregation_reference_list:
  data_aggregation_value_list.append(
    portal.data_aggregatation_unit.newContent(
      portal_type='Data Aggregation Unit',
      reference=reference
    )
  )

if batch:
  return data_aggregation_value_list
# XXX Redirect to module
return context.Base_redirect('view', keep_items={
  'portal_status_message': 'Data Aggregation Units successfully created.'
})
