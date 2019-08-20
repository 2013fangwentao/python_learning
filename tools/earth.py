import numpy as np


def WGS84XYZ2BLH(xyz):
    a = 6378137.0
    b = 6378137.0 * 297.257223563 / 298.257223563
    e2 = (1.0 - b * b / a / a)
    if (xyz[0] == 0.0 and xyz[1] == 0.0):
        lon = 0.0
        if (xyz[2] < 0):
            hgt = -xyz[2] - b
            lat = -np.pi / 2.0
        else:
            hgt = xyz[2] - b
            lat = np.pi / 2.0
    else:
        p = np.sqrt(xyz[0] * xyz[0] + xyz[1] * xyz[1])
        lon = 2.0 * np.arctan2(xyz[1], (xyz[0] + p))
        lat = xyz[2] / (p * (1.0 - e2))
        np.arctan(lat)
        hgt = 0.0
        dtmp = 1.0
        while (np.abs(hgt - dtmp) > 0.0001):
            dtmp = hgt
            sinlat = np.sin(lat)
            N = a / np.sqrt(1.0 - e2 * sinlat * sinlat)
            hgt = p / np.cos(lat) - N
            lat = xyz[2] / (p * (1.0 - e2 * N / (N + hgt)))
            np.arctan(lat)
    return np.array([lat, lon, hgt])
