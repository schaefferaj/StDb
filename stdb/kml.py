# Copyright 2019 Andrew Schaeffer
#
# This file is part of StDb.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
Tools used in the creation of a kml file from a station database. These
functions are used in the script ``stdb_to_kml.py``. In a terminal,
type ``stdb_to_kml.py -h`` for help on usage.

"""

import xml.dom.minidom
from operator import itemgetter
from datetime import datetime

def createKML(nets=[], netd={}, fileName="stdb.kml", opts=None):
    """
    Initializes and creates the kml document.

    Parameters
    ----------
    nets : List
        List of networks
    netd : Dict
        Dictionary of network elements
    filename : str
        File name for output .kml file
    opts : 
        Options read from command line

    """
    
    # initialize new KML document
    kmlDoc = xml.dom.minidom.Document()

    kmlElement = kmlDoc.createElementNS('http://earth.google.com/kml/2.2', 'kml')
    kmlElement.setAttribute('xmlns', 'http://earth.google.com/kml/2.2')
    kmlElement = kmlDoc.appendChild(kmlElement)

    #generate document environment
    documentElement = createDoc(kmlDoc, opts.doctitle)
    documentElement = kmlElement.appendChild(documentElement)

    #create document style maps
    stylenorm = createStyleState(kmlDoc, '0', 'normalState')
    stylehigh = createStyleState(kmlDoc, '1', 'highlightState')
    stylemap = createStyleMap(kmlDoc)
    documentElement.appendChild(stylenorm)
    documentElement.appendChild(stylehigh)
    documentElement.appendChild(stylemap)

    # Generater Colours for networks
    netcolours = gen_colors(len(nets),opts.randoff)
    
    # loop over the unique networks and make folders
    for inet, net in enumerate(nets):
        if opts.verb > 0: print("Network: " + net)

        # create KML Folder
        folderElement = createFolder(kmlDoc, net, netd[net], netcolours[inet], opts)
        documentElement.appendChild(folderElement)

    # write out kml file
    kmlFile = open(fileName, 'w')
    kmlFile.write(kmlDoc.toprettyxml())
    # kmlFile.write(kmlDoc.toprettyxml('  ', newl='\n', encoding='utf-8'))

def createFolder(kmlDoc, net, stlist, netcolour, opts):
    """
    For a kmlDocument and a dictionary of stations for a given network,
    make a folder element for this network, then create a placemark
    for every station.

    Parameters
    ----------
    kmldoc : 
        Object
    net : str
        Name of network
    stlist : List
        List of station names
    netcolour : str
        RGB colour for network code
    opts : 
        Options read from command line

    Returns
    -------
    folderElement : :class:`~kmlDoc.Folder`
        Instance of :class:`~kmlDoc.Folder`

    """
    
    # this creates a <Folder> element for a network of data
    folderElement = kmlDoc.createElement('Folder')
    fname = kmlDoc.createElement('name')
    fname.appendChild(kmlDoc.createTextNode(net))
    fopen = kmlDoc.createElement('open')
    fopen.appendChild(kmlDoc.createTextNode("1"))
    folderElement.appendChild(fname)
    folderElement.appendChild(fopen)
    
    # Sort Stations Alphabetically
    stns = []
    for st in stlist:
        stns.append(st.station)
    istns = [aa[0] for aa in sorted(enumerate(stns), key=itemgetter(1))]

    # Loop over Stations
    for istn in istns:
        if opts.verb > 1: print("     " + stns[istn])
        stdict = stlist[istn]
        placemarkElement = createPlacemark(kmlDoc, stdata=stdict, netcolor=rgb2hex(netcolour), opts=opts)
        folderElement.appendChild(placemarkElement)

    return folderElement

def createPlacemark(kmlDoc, stdata=None, netcolor='ffffffff', opts=None):
    """
    Creates a placemark in kmlDoc for a given row of a dictionary

    Parameters
    ----------
    kmldoc : 
        Object
    stdata : Dict
        Dictionary of station metadata
    netcolour : str
        RGB colour for network code
    opts : 
        Options read from command line

    Returns
    -------
    placemarkElement : :class:`~kmlDoc.Folder`
        Instance of :class:`~kmlDoc.Folder`

    """

    # Current Date/Time
    cdt = datetime.now()
    if cdt >= stdata.startdate and cdt <= stdata.enddate:
        operating = 1
    elif cdt < stdata.startdate:
        operating =- 1
    else:
        operating = 0

    # This creates a <Placemark> element for a Station.
    placemarkElement = kmlDoc.createElement('Placemark')
    nmeElement = kmlDoc.createElement('name')
    placemarkElement.appendChild(nmeElement)
    stylemappm = kmlDoc.createElement('styleUrl')
    stylemappm.appendChild(kmlDoc.createTextNode('#on-offText'))
    placemarkElement.appendChild(stylemappm)

    # Create Label Name for Item
    nmeElement.appendChild(kmlDoc.createTextNode(stdata.network + "." + stdata.station))

    # Point Style
    styleElement = createStyle(kmlDoc, netcolor, opts.scale, 'Network', op=operating)
    placemarkElement.appendChild(styleElement)

    extElement = kmlDoc.createElement('ExtendedData')
    placemarkElement.appendChild(extElement)

    # Create List of Fields to include in extended Data
    order = ['network', 'station', 'channel', 'location', 'startdate', 'enddate', \
        'status', 'polarity', 'azcorr', 'elevation', 'longitude', 'latitude']
    for key in order:
        if stdata[key]:
            dataElement = kmlDoc.createElement('Data')
            dataElement.setAttribute('name', key)
            valueElement = kmlDoc.createElement('value')
            dataElement.appendChild(valueElement)
            if key == "location":
                value="; ".join(stdata[key])
            elif key == "startdate" or key == "enddate":
                value = stdata[key].strftime("%Y-%m-%d %H:%M:%S")
            elif key == "polarity":
                value = str(stdata[key])
            elif key == "azcorr":
                value = str(stdata[key])
            elif key == "elevation":
                value = "{0:.2f} km".format(stdata[key])
            elif key == "latitude" or key == "longitude":
                value = "{0:.3f}".format(stdata[key])
            else:
                value = stdata[key]
            valueText = kmlDoc.createTextNode(value)
            valueElement.appendChild(valueText)
            extElement.appendChild(dataElement)
    
    pointElement = kmlDoc.createElement('Point')
    placemarkElement.appendChild(pointElement)
    coordinates = "{0:f},{1:f}".format(stdata.longitude, stdata.latitude)
    coorElement = kmlDoc.createElement('coordinates')
    coorElement.appendChild(kmlDoc.createTextNode(coordinates))
    pointElement.appendChild(coorElement)

    return placemarkElement

def createStyleState(kmlDoc, scale, idtag):
    """
    Used to create a doucment wide style state with the LabelStyle internal field scale.
    Sets the Labelstyle scale field to value "scale" and names the field "idtag"
    """

    styleState = kmlDoc.createElement('Style')
    styleState.setAttribute('id', idtag)
    labels = kmlDoc.createElement('LabelStyle')
    lscale = kmlDoc.createElement('scale')
    lscale.appendChild(kmlDoc.createTextNode(str(scale)))
    labels.appendChild(lscale)
    styleState.appendChild(labels)

    return styleState

def createPair(kmlDoc, mode, state):
    """
    Used to create a single Pair environment that has a particular mode and state
    """

    pairElement = kmlDoc.createElement('Pair')
    key = kmlDoc.createElement('key')
    key.appendChild(kmlDoc.createTextNode(str(mode)))
    sturl = kmlDoc.createElement('styleUrl')
    sturl.appendChild(kmlDoc.createTextNode("#" + str(state)))
    pairElement.appendChild(key)
    pairElement.appendChild(sturl)

    return pairElement

def createStyleMap(kmlDoc):
    """
    Creates a StyleMap environment called on-offText which enables label text 
    for Placemarks on mouseover only.
    """

    styleMap = kmlDoc.createElement('StyleMap')
    styleMap.setAttribute('id', 'on-offText')
    pairnorm = createPair(kmlDoc, 'normal', 'normalState')
    pairhigh = createPair(kmlDoc, 'highlight', 'highlightState')
    styleMap.appendChild(pairnorm)
    styleMap.appendChild(pairhigh)

    return styleMap

def createStyle(kmlDoc, netcolor, size, labtype='net', op=0):
    """
    Creates a Style Environment with a variable size and colour.
    The last argument selects between two different icon types.
    """

    #print size, size.__class__

    if labtype == "event": 
        link = 'http://maps.google.com/mapfiles/kml/shapes/caution.png'
        netcolor = "ff0000ff"
    elif labtype == 'knots':
        link = 'http://maps.google.com/mapfiles/kml/paddle/red-stars-lv.png'
        netcolor = "ff0000ff"
    else:
        if op > 0:
            link = 'http://maps.google.com/mapfiles/kml/shapes/triangle.png'
            size = str(float(size)*0.75)
        elif op < 0:
            link = 'http://maps.google.com/mapfiles/kml/shapes/star.png'
            size = str(float(size)*0.75)
        else:
            link = 'http://maps.google.com/mapfiles/kml/pal4/icon57.png'
    styleElement = kmlDoc.createElement('Style')
    iconstyle = kmlDoc.createElement('IconStyle')
    styleElement.appendChild(iconstyle)

    # scale element
    scale = kmlDoc.createElement('scale')
    scale.appendChild(kmlDoc.createTextNode(size))
    iconstyle.appendChild(scale)

    # color
    iconcolor = kmlDoc.createElement('color')
    iconcolor.appendChild(kmlDoc.createTextNode(netcolor))
    iconstyle.appendChild(iconcolor)

    # icon element
    icon = kmlDoc.createElement('Icon')
    iconlink = kmlDoc.createElement('href')
    iconlink.appendChild(kmlDoc.createTextNode(link))
    icon.appendChild(iconlink)
    iconstyle.appendChild(icon)

    return styleElement

def createDoc(kmlDoc, name):
    """
    Initialize the KML Document using name
    """

    # create the document element
    documentElement = kmlDoc.createElement('Document')

    # create the docname element
    docnameElement = kmlDoc.createElement('name')
    docnameElement.appendChild(kmlDoc.createTextNode(str(name)))
    documentElement.appendChild(docnameElement)
    
    return documentElement

def gen_colors(n, norand=False):
    """
    Produce n evenly distributed colors using the HSV colour pickle and the
    golden ratio value of ~0.6 to separate the colours. By default the initial
    colour selected is random.
    """

    import colorsys
    
    from random import random
    golden_ratio = 0.618033988749895
    if norand: h = 0.22717784590367374
    else:      h = random() 
    ll = []
    for x in range(0, n):
        h += golden_ratio
        h %= 1
        HSV_tuple = [h, 0.95, 0.95]  # this defines how "deep" are the colors
        RGB_tuple = colorsys.hsv_to_rgb(*HSV_tuple)
        ll.append([str(int(x*256)) for x in RGB_tuple])
    return ll

def rgb2hex(rgbl):
    """
    Return hexidecial XML form of RGB colour tuple. Note that the xml parsing
    of the tuple reads bgr rather than standard rgb, so the rgb tuple is reversed
    in order on output to represent the true colour
    """
    return "ff{0:02x}{1:02x}{2:02x}".format(int(rgbl[2]), int(rgbl[1]), int(rgbl[0]))
