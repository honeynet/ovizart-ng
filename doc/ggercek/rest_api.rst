.. _rest-api:

********
REST API
********

Ovizart system is built on top of this REST API. Main reason of this design approach is providing equality while
minimizing maintenance/porting efforts. Our current interfaces use OvizartProxy to communicate with this REST API.
As webserver Python's BaseHttpServer extended and following features added.

* HTTPS support
* Cookie/Session management
* Easy to extend REST API decorator system
* File operations such as, Upload/Download

Here is the list of REST API features currently supported.

Default Base URL: http://localhost:9009/

.. list-table::
   :widths: 15 15 70
   :header-rows: 1

   * - Url
     - Method/

       Content-TYPE
     - Description
   * - /login

       {username:, password:}
     - POST

       application/json
     - Authenticate user and generates a cookie. All of the API calls require that cookie value.
   * - /upload/<filename>

       <file-content>
     - POST

       application/octet-stream or multipart/form-data
     - Uploads the specified file to core daemon, in case of name conflict system will rename the given file as <base_name>_#.<extension> and returns the given name to client.. eg, smtp.pcap -> smtp_1.pcap File must be a pcap file otherwise users cookie will be be terminate.
   * - /pcap/<analysisId>/<streamKey>
     - GET

       application/json
     - serves split pcap file belongs to given streamKey of given analysisId
   * - /attachment/<analysisId>/<streamKey>)/<filePath>
     - GET

       application/json
     - serves extracted file by given filePath streamKey and analysisId parameters
   * - /reassembled/<analysisId>/<streamKey>/<trafficType>
     - GET

       application/json
     - serves reassembled application layer traffic file based on trafficType (0:A->B; 1:A<-B; 2:A<->B)
   * - /start
     - POST

       application/json
     - After uploading pcap file, this will trigger the core system to start the analyze. This is an async call. This call will return id of analysis started.
   * - /analysis/
     - GET

       application/json
     - This call will return a summary analysis’ crated by current user.
   * - /analysis/<analysisId>
     - GET

       application/json
     - This call will return details of given analysis
   * - /analysis/<analysisId>
     - DELETE

       application/json
     - This call will delete all the information related analysis. All records from database, all the attachment files, both the original and separated pcap files.
   * - /analyzer
     - PUT

       application/json
     - This call will allow user to load custom analyzer into the system. This feature is in a very early stage and does not have security checks. It could be dangerous.
