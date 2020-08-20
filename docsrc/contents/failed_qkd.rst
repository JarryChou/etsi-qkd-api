Failed QKD Requests and Future Work
===================================

Failed requests
+++++++++++++++

The reason for failed QKD requests with Senetas's VMs is due to the way the key UUIDs are concatenated. The CV1000 always expects
a single 256-bit key, presumably for AES256. This was verified by inspecting the GET requests received by the API. Correspondingly, the VMs
expect standard 32 base16 characters UUIDs to go with the keys. However, through our concatenation a 256bit key would have a UUID of length 32 x 8 = 256 base16 characters.
This was not a problem for the ``Get_key`` API call (those were the successful requests), but is problematic for ``Get key with key IDs`` calls.  This was verified by spoofing
fake QKD keys with standard UUID lengths--no failed requests were observed.

Recall that ``Get key with key IDs`` is called when Bob receives the key IDs from Alice over the classical channel, and now wants to retrieve the corresponding keys from his
KME. Ideally, the VM should pass the UUIDs untouched (in its concatenated form) to the KME, and the KME handles the logic of separating by delimiters to obtain the individual UUIDs of each 32-bit key.
However, by inspecting the API calls, it seems the VMs first try to separate the UUIDs before passing it to ``Get key with key IDs``, hence only obtaining 32-bit keys. This should
be the source of the failed requests, as ``Get key with key IDs`` did not return 256-bit keys.


Future work
+++++++++++

Fixed length UUIDs
------------------

Hence, it remains future work to devise a way to implement fixed UUID lengths for keys of arbitrary sizes. This is not an easy task as the KMEs need to infer the length
of the keys solely based on the UUID. The current implementation determines the key length by the number of concatenations. However, losing this property, combined with
the fact that UUID generation is generally irreversible, means inferring key sizes is not trivial. One avenue would be to pass key sizes as an additional entry in the JSON
fed to ``Get key with key IDs``.  For instance, there is a ``key_container_extension`` parameter allowed by the ETSI standard that is hitherto unused. The only caveat is to get the
VMs to actually make use of the parameter--this requires liaising with Senetas engineers to implement this functionality.

Application IDs
---------------

Another area of future work is in handling of application IDs, specifically in ``api.routes``. You may have noticed that the API routes defined in ``api.routes`` have an
``id`` parameter which is currently unused. This ID is typically the IP address of the caller. Currently the API is designed to allow any IP to call it. However, one can imagine
that as the number of applications grow, it is in the interest of the programmer to restrict access to only certain registered IP addresses, for eg. to prevent DDOS attacks. Logic can be implemented to
filter IDs so only recognized IDs are allowed to call the API. One can also consider 'reserving' keys for certain IDs--for eg. if an application is of high priority, the KME
can block off a set number of keys that can be obtained only by the caller of that IP address.

Trusted nodes
-------------

Lastly, it will be interesting, for the further future, to consider how the ETSI API can integrate with trusted node systems, such as that proposed by `OpenQKDNetwork <https://openqkdnetwork.ca/>`_.
As it is not feasible for satellite QKD systems (such as SpeQtral's) to establish direct quantum links between every pair of nodes, trusted nodes have become a leading proposal
in establishing large-scale satellite QKD networks. ETSI has not provided guidelines on integrating its API with trusted nodes, so this would be an interesting area
of research and future consideration.