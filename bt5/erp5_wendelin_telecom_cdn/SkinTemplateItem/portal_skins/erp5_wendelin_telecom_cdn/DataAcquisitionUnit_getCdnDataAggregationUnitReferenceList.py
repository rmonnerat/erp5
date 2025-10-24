"""
  Generate a set of references that will be used to group
  multiple Data Acquisition Units data.

  for instance, the expected reference is:

   cdnaccess_cdn<cluster>_<instance node>_<shared instance>

  then we would like to build reference list based on:

  - DAGGU-cdn<cluster>_<shared instance>: Shared instance accross all nodes
  - DAGGU-cdn<cluster>_<instance node>: Single node all shared instances
  - DAGGU-cdn<cluster>: While cluster, all sites

"""
reference = context.getReference()
if reference is None or not reference.startswith("cdnaccess_"):
  raise ValueError("Reference is not related to CDN.")

_, cluster, node, shared = reference.split("_")

return [
  "DAGGU-%s" % "_".join([cluster, shared]),
  "DAGGU-%s" % "_".join([cluster, node]),
  "DAGGU-%s" % cluster
]
