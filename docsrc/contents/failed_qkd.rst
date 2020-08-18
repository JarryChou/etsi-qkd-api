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

Hence, it remains future work to devise a way to implement fixed UUID lengths for keys of arbitrary sizes. This is not an easy task as the KMEs need to infer the length
of the keys solely based on the UUID. The current implementation determines the key length by the number of concatenations. However, losing this property, combined with
the fact that UUID generation is generally irreversible, means inferring key sizes is not trivial. One avenue would be to pass key sizes as an additional entry in the JSON
fed to ``Get key with key IDs``.  For instance, there is a ``key_container_extension`` parameter allowed by the ETSI standard that is hitherto unused. The only caveat is to get the
VMs to actually make use of the parameter--this requires liaising with Senetas engineers to implement this functionality.