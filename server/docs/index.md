# WiFind Server

Documentation for the WiFind Django Server.

# Ingestion

* [models](ingestion/models.html)
* [views](ingestion/views.html)

The ingestion component is responsible for receiving requests from the mobile
app and storing those readings into the MySQL database.

# wifipulling

* [lib](wifipulling/lib.html)
* [views](wifipulling/views.html)
* [urls](wifipulling/urls.html)

The wifipulling component is for data retrieval.  It exposes data in two ways:
an API for accessing raw data and a set of APIs for returning map tile images
specifically for displaying a heatmap of signal strength by network.
