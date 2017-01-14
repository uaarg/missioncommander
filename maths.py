import pyproj

def utm_to_DD( easting, northing, zone, hemisphere="northern"):
    """
    Converts a set of UTM GPS coordinates to WGS84 Decimal Degree GPS coordinates.
    Returns (latitude, longitude) as a tuple.
    easting - UTM easting in metres
    northing - UTM northing in metres
    zone - current UTM zone

    Note that no hemisphere is specified; in the southern hemisphere, this function expects the false northing (10 000 000m) to be subtracted.

    An exception will be raised if the conversion involves invalid values.
    """

    easting = float(easting) / 100
    northing =  float(northing) / 100
    zone = int(zone)
    # Easting and Northing ranges from https://www.e-education.psu.edu/natureofgeoinfo/c2_p23.html
    min_easting, max_easting = 167000, 833000
    if not (min_easting < easting < max_easting):
        raise(ValueError("Easting value of %s is out of bounds (%s to %s)." % (easting, min_easting, max_easting)))
    min_northing, max_northing = -9900000, 9400000
    if not (min_northing < northing < max_northing):
        raise(ValueError("Northing value of %s is out of bounds (%s to %s)." % (northing, min_northing, max_northing)))

    if not (1 <= zone <= 60):
        raise(ValueError("Zone value of %s is out of bounds" % zone))

    pr = pyproj.Proj(proj='utm', zone=zone, ellps='WGS84', errcheck=True)

    lon, lat = pr(easting, northing, inverse=True)
    return repr(lat), repr(lon)
