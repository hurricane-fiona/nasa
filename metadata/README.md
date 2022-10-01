# Metadata store
This directory contains the json files, eaach containing citation json data about one citation.

## Tracking files
- .metadata_id_tracking - tracks citation IDs already for which we already downloaded metadata
- .metadata_page_tracking - tracks the page_idx and fetch_size that was used so far. This is used to for restartability to ensure we start making search calls to NTRS from the next page_idx that is not yet fetched.

### Format for .metadata_page_tracking
- Each row is a pair of page_size,fetch_size
- Each row ends with a newline "\n"

### Format for .metadata_id_tracking
- Each row is citation_id
- Each row ends with a newline "\n"
