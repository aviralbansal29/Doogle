# Doogle

### Google Search

##### Command format: 
    [flags...] !google [content]
##### Examples
    limit=3 !google game of thrones
    !google play store
##### Flags
- **limit**
    Number of results to be fetched
    1. *Default* :
        > Default number of results is 5.
    2. *Validate* :
        > Min is 1 and Max is 10.

#
### Search History

##### Command format: 
    [flags...] !recent [content]
##### Examples
    limit=3 quick_search=1 !recent game
    !recent store
##### Flags
- **limit**
    Number of results to be fetched
    1. *Default* :
        > Default number of results is 5.
    2. *Validate* :
        > Min is 1 and Max is 10.
- **quick_search**
    Whether to fetch data using vector search (is not accurate)
    1. *Default* :
        > Default is False for normal search.
    2. *Validate* :
        > Min is 1 and Max is 10.
