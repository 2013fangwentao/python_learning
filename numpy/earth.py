import numpy as np


def xyz2blh(xyz):
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


def array_xyz2blh(xyz):
    blh = np.zeros(np.shape(xyz))
    index = 0
    for dat in np.nditer(xyz, flags=['external_loop']):
        blh[index, ...] = xyz2blh(dat)
        index = index + 1
    return blh


def blh2xyz(blh):
    xyz = np.zeros(blh.shape)
    m_A84 = 6378137.0
    m_B84 = 6378137.0 * 297.257223563 / 298.257223563
    m_E84 = (1.0 - m_B84 * m_B84 / m_A84 / m_A84)
    W84 = np.sqrt(1.00 - m_E84 * np.sin(blh[0]) * np.sin(blh[0]))
    N84 = m_A84 / W84

    xyz[0] = (N84 + blh[2]) * np.cos(blh[0]) * np.cos(blh[1])
    xyz[1] = (N84 + blh[2]) * np.cos(blh[0]) * np.sin(blh[1])
    xyz[2] = (N84 * (1 - m_E84) + blh[2]) * np.sin(blh[0])
    return xyz


def array_blh2xyz(blh):
    xyz = np.zeros(np.shape(blh))
    index = 0
    for dat in np.nditer(blh, flags=['external_loop']):
        xyz[index, ...] = blh2xyz(dat)
        index = index + 1
    return xyz
