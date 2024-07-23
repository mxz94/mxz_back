import math
import os

import gpxpy.gpx

# !/usr/bin/env python
# -*- coding: utf-8 -*-


__all__ = ['wgs2gcj', 'gcj2wgs', 'gcj2wgs_exact',
           'distance', 'gcj2bd', 'bd2gcj', 'wgs2bd', 'bd2wgs']

earthR = 6378137.0
X_PI = math.pi * 3000 / 180

def outOfChina(lat, lng):
    return not (72.004 <= lng <= 137.8347 and 0.8293 <= lat <= 55.8271)


def transform(x, y):
    xy = x * y
    absX = math.sqrt(abs(x))
    xPi = x * math.pi
    yPi = y * math.pi
    d = 20.0*math.sin(6.0*xPi) + 20.0*math.sin(2.0*xPi)

    lat = d
    lng = d

    lat += 20.0*math.sin(yPi) + 40.0*math.sin(yPi/3.0)
    lng += 20.0*math.sin(xPi) + 40.0*math.sin(xPi/3.0)

    lat += 160.0*math.sin(yPi/12.0) + 320*math.sin(yPi/30.0)
    lng += 150.0*math.sin(xPi/12.0) + 300.0*math.sin(xPi/30.0)

    lat *= 2.0 / 3.0
    lng *= 2.0 / 3.0

    lat += -100.0 + 2.0*x + 3.0*y + 0.2*y*y + 0.1*xy + 0.2*absX
    lng += 300.0 + x + 2.0*y + 0.1*x*x + 0.1*xy + 0.1*absX

    return lat, lng


def delta(lat, lng):
    ee = 0.00669342162296594323
    dLat, dLng = transform(lng-105.0, lat-35.0)
    radLat = lat / 180.0 * math.pi
    magic = math.sin(radLat)
    magic = 1 - ee * magic * magic
    sqrtMagic = math.sqrt(magic)
    dLat = (dLat * 180.0) / ((earthR * (1 - ee)) / (magic * sqrtMagic) * math.pi)
    dLng = (dLng * 180.0) / (earthR / sqrtMagic * math.cos(radLat) * math.pi)
    return dLat, dLng


def wgs2gcj(wgsLat, wgsLng):
    if outOfChina(wgsLat, wgsLng):
        return wgsLat, wgsLng
    else:
        dlat, dlng = delta(wgsLat, wgsLng)
        return wgsLat + dlat, wgsLng + dlng


def gcj2wgs(gcjLat, gcjLng):
    if outOfChina(gcjLat, gcjLng):
        return gcjLat, gcjLng
    else:
        dlat, dlng = delta(gcjLat, gcjLng)
        return gcjLat - dlat, gcjLng - dlng


def gcj2wgs_exact(gcjLat, gcjLng):
    initDelta = 0.01
    threshold = 0.000001
    dLat = dLng = initDelta
    mLat = gcjLat - dLat
    mLng = gcjLng - dLng
    pLat = gcjLat + dLat
    pLng = gcjLng + dLng
    for i in range(30):
        wgsLat = (mLat + pLat) / 2
        wgsLng = (mLng + pLng) / 2
        tmplat, tmplng = wgs2gcj(wgsLat, wgsLng)
        dLat = tmplat - gcjLat
        dLng = tmplng - gcjLng
        if abs(dLat) < threshold and abs(dLng) < threshold:
            return wgsLat, wgsLng
        if dLat > 0:
            pLat = wgsLat
        else:
            mLat = wgsLat
        if dLng > 0:
            pLng = wgsLng
        else:
            mLng = wgsLng
    return wgsLat, wgsLng


def distance(latA, lngA, latB, lngB):
    pi180 = math.pi / 180
    arcLatA = latA * pi180
    arcLatB = latB * pi180
    x = (math.cos(arcLatA) * math.cos(arcLatB) *
         math.cos((lngA - lngB) * pi180))
    y = math.sin(arcLatA) * math.sin(arcLatB)
    s = x + y
    if s > 1:
        s = 1
    if s < -1:
        s = -1
    alpha = math.acos(s)
    distance = alpha * earthR
    return distance


def gcj2bd(gcjLat, gcjLng):
    if outOfChina(gcjLat, gcjLng):
        return gcjLat, gcjLng

    x = gcjLng
    y = gcjLat
    z = math.hypot(x, y) + 0.00002 * math.sin(y * X_PI)
    theta = math.atan2(y, x) + 0.000003 * math.cos(x * X_PI)
    bdLng = z * math.cos(theta) + 0.0065
    bdLat = z * math.sin(theta) + 0.006
    return bdLat, bdLng


def bd2gcj(bdLat, bdLng):
    if outOfChina(bdLat, bdLng):
        return bdLat, bdLng

    x = bdLng - 0.0065
    y = bdLat - 0.006
    z = math.hypot(x, y) - 0.00002 * math.sin(y * X_PI)
    theta = math.atan2(y, x) - 0.000003 * math.cos(x * X_PI)
    gcjLng = z * math.cos(theta)
    gcjLat = z * math.sin(theta)
    return gcjLat, gcjLng


def wgs2bd(wgsLat, wgsLng):
    return gcj2bd(*wgs2gcj(wgsLat, wgsLng))


def bd2wgs(bdLat, bdLng):
    return gcj2wgs(*bd2gcj(bdLat, bdLng))



def gpx_wgs84_2_gcj02(from_path: str, to_path: str) -> None:
    with open(from_path, 'rb') as f:
        gpx_old = gpxpy.parse(f)
        gpx_new = gpxpy.gpx.GPX()

        gpx_new_track = gpxpy.gpx.GPXTrack()
        gpx_new.tracks.append(gpx_new_track)
        gpx_new_segment = gpxpy.gpx.GPXTrackSegment()
        gpx_new_track.segments.append(gpx_new_segment)

        for track in gpx_old.tracks:
            for segment in track.segments:
                for point in segment.points:
                    new_lat, new_lon = gcj2wgs(point.latitude, point.longitude)
                    gpx_new_segment.points.append(gpxpy.gpx.GPXTrackPoint(new_lat,
                                                                          new_lon,
                                                                          elevation=point.elevation,
                                                                          time=point.time))
    with open(to_path, 'wt') as f:
        f.write(gpx_new.to_xml())


if __name__ == "__main__":
    files = os.listdir("old_track")
    # print(files)
    # from_path = ""
    to_path = "new_track"
    for file in files:
        gpx_wgs84_2_gcj02("old_track/"+file, to_path + "/" + file)

