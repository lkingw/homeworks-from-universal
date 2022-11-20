from math import sin, cos, sqrt, atan2, radians, acos

def getGeoDistance(lat1, lon1, lat2, lon2, r=6371):
    # Convert degrees to radians
    coordinates = lat1, lon1, lat2, lon2
    phi1, lambda1, phi2, lambda2 = [
        radians(c) for c in coordinates
    ]
    
    # Apply the haversine formula
    d = r * acos(cos(phi2 - phi1) - cos(phi1) * cos(phi2) *
              (1 - cos(lambda2 - lambda1)))
    return d