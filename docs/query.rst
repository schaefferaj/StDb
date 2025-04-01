.. _query:

Create Database by Querying FDSN
================================

Program ``query_fdsn_stdb``
---------------------------

Description
-----------
Program to query a datacenter using the ``obspy`` fdsn client. All stations 
returned based on the query criteria are saved into a both a ``.csv`` file and a 
stdb dictionary ``pickle`` file for future use.

Usage
-----

.. code-block:: none

    $ query_fdsn_stdb -h
    Usage: query_fdsn_stdb [options] <station list filename>

    Program to query a datacenter using the obspy fdsn client. All station
    returned in this query are saved into both a csv format 1sls file as well as a
    stationdb (stdb.StDbElement) pickled dictionary. The input argument, <station
    file name> is the prefix for the output file, which is by default <station
    file name>.csv and <station file name>.pkl.

    Options:
      -h, --help            show this help message and exit
      -D, --debug           Debug mode. After the client query is complete (and
                            successful), instead of parsing the inventory, it is
                            instead pickled to <station file name>_query_debug.pkl
                            which can be loaded in ipython to examine manually.
      --long-keys           Specify Key format. Default is Net.Stn. Long keys are
                            Net.Stn.Chn
      -a, --ascii           Specify to write ascii Pickle files instead of
                            binary.
                            Ascii are larger file size, but more likely to be
                            system independent.

      Server Settings:
        Settings associated with which datacenter to log into.

        --server=SERVER     Base URL of FDSN web service compatible server (e.g.
                            “http://service.iris.edu”) or key string for
                            recognized server (one of ‘AUSPASS’, ‘BGR’,
                            ‘EARTHSCOPE’, ‘EIDA’, ‘EMSC’, ‘ETH’, ‘GEOFON’,
                            ‘GEONET’, ‘GFZ’, ‘ICGC’, ‘IESDMC’, ‘INGV’, ‘IPGP’,
                            ‘IRIS’, ‘IRISPH5’, ‘ISC’, ‘KNMI’, ‘KOERI’, ‘LMU’,
                            ‘NCEDC’, ‘NIEP’, ‘NOA’, ‘NRCAN’, ‘ODC’, ‘ORFEUS’,
                            ‘RASPISHAKE’, ‘RESIF’, ‘RESIFPH5’, ‘SCEDC’, ‘TEXNET’,
                            ‘UIB-NORSAR’, ‘USGS’, ‘USP’) [Default IRIS]
        --user-auth=USERAUTH
                            Enter your Authentification Username and Password
                            (--user-auth='username:authpassword') to access and
                            download restricted data. [Default no user and
                            password]
        --eida-token=TOKENFILE
                            Token for EIDA authentication mechanism, see
                            http://geofon.gfz-
                            potsdam.de/waveform/archive/auth/index.php. If a token
                            is provided, argument --user-auth will be ignored.
                            This mechanism is only available on select EIDA nodes.
                            The token can be provided in form of the PGP message
                            as a string, or the filename of a local file with the
                            PGP message in it.
                        
      Channel Priority/Selection Settings:
        Settings associated with selecting the channels to retain.

        --channel-rank=CHNRANK
                            If requesting more than one type of channel, specify a
                            comma separated list of the first two lettres of the
                            desired components to retain. Default is HH > BH > LH
                            : [ 'HH','BH','LH']

      Station-Channel Settings:
        Options to narrow down the specific channels based on network,
        station, etc

        -N NETS, --networks=NETS
                            Specify a comma separated list of network codes to
                            search for [Default *]
        -S STNS, --stations=STNS
                            Specify a comma separated list of station names. If
                            you want wildcards, enclose in quotes [Default *]
        -L LOCS, --locations=LOCS
                            Specify a comma separated list of location codes. If
                            you want wildcards, enclose in quotes [Default *]
        -C CHNS, --channels=CHNS
                            Specify a comma separated, wildcarded list of channel
                            names. [Default LH*,BH*,HH*]

      Geographic Lat/Lon Box Search:
        Define the coordinates of a lat/lon box in which to select stations.
        If filled out, takes precedence over values for Radius Search (below).

        --minlat=MINLAT, --min-latitude=MINLAT
                            Specify minimum latitude to search (must specify all
                            of minlat, maxlat, minlon, maxlon).
        --maxlat=MAXLAT, --max-latitude=MAXLAT
                            Specify maximum latitude to search (must specify all
                            of minlat, maxlat, minlon, maxlon).
        --minlon=MINLON, --min-longitude=MINLON
                            Specify minimum longitude to search (must specify all
                            of minlat, maxlat, minlon, maxlon).
        --maxlon=MAXLON, --max-longitude=MAXLON
                            Specify maximum longitude to search (must specify all
                            of minlat, maxlat, minlon, maxlon).

      Geographic Radius Search:
        Central point and min/max radius search settings. Box Search Settings
        take precedence over radius search.

        --lat=LAT, --latitude=LAT
                            Specify a Lat (if any of --lon --min-radius and --max-
                            radius are empty, an error will prompt).
        --lon=LON, --longitude=LON
                            Specify a Lon (if any of --lat --min-radius and --max-
                            radius are empty, an error will prompt).
        --minr=MINR, --min-radius=MINR
                            Specify a minimum search radius (in degrees) around
                            the point defined by --lat and --lon (if any of --lat
                            --lon and --max-radius are empty, an error will
                            prompt). [Default 0. degrees]
        --maxr=MAXR, --max-radius=MAXR
                            Specify a maximum search radius (in degrees) around
                            the point defined by --lat and --lon (if any of --lat
                            --lon and --min-radius are empty, an error will
                            prompt).

      Fixed Time Range Settings:
        Find all stations operating within the start and end date/time. If
        either are filled out, they take precedence over Non-Specific time
        range search (below)

        --start=STDATE, --start-date=STDATE
                            Specify the Start Date/Time in a UTCDateTime
                            compatible String (ie, 2010-01-15 15:15:45.2).
                            [Default Blank]
        --end=ENDDATE, --end-date=ENDDATE
                            Specify the End Date/Time in a UTCDateTime compatible
                            String (ie, 2010-01-15 15:15:45.2). [Default Blank]

      Non-Specific Time Range Settings:
        Time settings with less specificity. Ensure that those you specify do
        not interfere with each other. If above Fixed Range values are set,
        they will take precedence over these values.

        --start-before=STBEFORE
                            Specify a Date/Time which stations must start before
                            (must be UTCDateTime compatible string, ie 2010-01-15
                            15:15:45.2). [Default empty]
        --start-after=STAFTER
                            Specify a Date/Time which stations must start after
                            (must be UTCDateTime compatible string, ie 2010-01-15
                            15:15:45.2). [Default empty]
        --end-before=ENDBEFORE
                            Specify a Date/Time which stations must end before
                            (must be UTCDateTime compatible string, ie 2010-01-15
                            15:15:45.2). [Default empty]
        --end-after=ENDAFTER
                            Specify a Date/Time which stations must end after
                            (must be UTCDateTime compatible string, ie 2010-01-15
                            15:15:45.2). [Default empty]

Example
-------

Extract all stations with broadband seismic data (``-C BH``) in the TA network (``-N TA``) 
in the region delimited by min and max latitudes of 60 to 65 deg, and min anx max longitudes
of -135 to -120 deg, which hold data recorded since January 1, 2017:

.. code-block::

    $ query_fdsn_stdb -C BH? -N TA --minlat=60 --maxlat=65 --minlon=-135 --maxlon=-120  --start=2017-01-01 ta_list
    Performing Geographic Box Search:
        LL:   60.0000, -135.0000
        UR:   65.0000, -120.0000
     
    Performing Fixed Time Range Search: 
       Start: 2017-01-01 00:00:00
       End:   2599-12-31 23:59:59
     
    Station/Channel Search Parameters:
       Network:  TA
       Stations: *
       Channels: BH?
       Channel Rank: LH,BH,HH
     
    Output Files: ta_list.csv and ta_list.pkl
     
    Initializing Client (IRIS)...Done

    Querying client...Done

    Search Complete: 
      3 stations in 1 networks
     
    Network: TA
       Station: M31M
         Lon, Lat, Elev: -134.3906,  62.2024,   0.639
         Start Date: 2015-10-17 00:00:00
         End Date:   2599-12-31 23:59:59
         Status:     open
         Selected Channel: BH
         Locations:        --
        Added as: TA.M31M
       Station: N32M
         Lon, Lat, Elev: -133.0818,  61.1512,   0.816
         Start Date: 2016-05-11 00:00:00
         End Date:   2599-12-31 23:59:59
         Status:     open
         Selected Channel: BH
         Locations:        --
        Added as: TA.N32M
       Station: P33M
         Lon, Lat, Elev: -132.8174,  60.2114,   1.066
         Start Date: 2015-10-15 00:00:00
         End Date:   2599-12-31 23:59:59
         Status:     open
         Selected Channel: BH
         Locations:        --
        Added as: TA.P33M
     
      Pickling to ta_list.pkl
      Saving csv to: ta_list.csv

