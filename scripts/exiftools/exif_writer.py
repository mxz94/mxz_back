#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EXIF Writer Tool Class
A Python tool class for writing EXIF metadata to video and image files using exiftool.
"""

import os
import shutil
import subprocess
import sys
from datetime import datetime, timedelta
from typing import Optional, Tuple, List


def format_gps(lat: float, lon: float, alt: float) -> str:
    """
    Format GPS for video (-Keys: format)
    
    Args:
        lat: Latitude in decimal degrees (-90..90)
        lon: Longitude in decimal degrees (-180..180)
        alt: Altitude in meters
        
    Returns:
        Formatted GPS string like "34.673500 N, 112.492300 E, 138.848 m Above Sea Level"
    """
    if not (-90.0 <= lat <= 90.0):
        raise ValueError("Latitude must be between -90 and 90.")
    if not (-180.0 <= lon <= 180.0):
        raise ValueError("Longitude must be between -180 and 180.")

    lat_hem = "N" if lat >= 0 else "S"
    lon_hem = "E" if lon >= 0 else "W"
    lat_abs = abs(lat)
    lon_abs = abs(lon)

    alt_dir = "Above Sea Level" if alt >= 0 else "Below Sea Level"
    alt_abs = abs(alt)

    return f"{lat_abs:.6f} {lat_hem}, {lon_abs:.6f} {lon_hem}, {alt_abs:.3f} m {alt_dir}"


def format_gps_exif(lat: float, lon: float, alt: float) -> Tuple[int, int, float, str, int, int, float, str, float]:
    """
    Format GPS for images (standard EXIF format: degrees, minutes, seconds)
    
    Args:
        lat: Latitude in decimal degrees (-90..90)
        lon: Longitude in decimal degrees (-180..180)
        alt: Altitude in meters
        
    Returns:
        Tuple: (lat_d, lat_m, lat_s, lat_ref, lon_d, lon_m, lon_s, lon_ref, alt)
    """
    if not (-90.0 <= lat <= 90.0):
        raise ValueError("Latitude must be between -90 and 90.")
    if not (-180.0 <= lon <= 180.0):
        raise ValueError("Longitude must be between -180 and 180.")

    def dms_from_decimal(dec: float) -> Tuple[int, int, float]:
        """Convert decimal degrees to (degrees, minutes, seconds)"""
        dec_abs = abs(dec)
        degrees = int(dec_abs)
        minutes = int((dec_abs - degrees) * 60)
        seconds = ((dec_abs - degrees) * 60 - minutes) * 60
        return (degrees, minutes, seconds)

    lat_d, lat_m, lat_s = dms_from_decimal(lat)
    lon_d, lon_m, lon_s = dms_from_decimal(lon)

    lat_ref = "N" if lat >= 0 else "S"
    lon_ref = "E" if lon >= 0 else "W"

    return (lat_d, lat_m, lat_s, lat_ref, lon_d, lon_m, lon_s, lon_ref, alt)


def find_exiftool(provided_path: Optional[str] = None) -> str:
    """
    Find exiftool executable path.
    
    Args:
        provided_path: Optional custom path to exiftool
        
    Returns:
        Path to exiftool executable
        
    Raises:
        FileNotFoundError: If exiftool cannot be found
    """
    # 1) Provided path
    if provided_path:
        if os.path.isfile(provided_path):
            return provided_path
        raise FileNotFoundError(f"exiftool not found at: {provided_path}")
    # 2) PATH
    exe_name = "exiftool.exe" if os.name == "nt" else "exiftool"
    found = shutil.which(exe_name)
    if found:
        return found
    # 3) Current executable folder (for packaged exe)
    exe_dir = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.getcwd()
    candidate = os.path.join(exe_dir, exe_name)
    if os.path.isfile(candidate):
        return candidate
    raise FileNotFoundError("exiftool not found. Place exiftool.exe beside this app or add to PATH.")


def _is_video_file(filepath: str) -> bool:
    """Check if file is a video based on extension"""
    video_exts = {'.mp4', '.mov', '.m4v', '.avi', '.mkv', '.mts', '.m2ts', '.flv', '.wmv'}
    ext = os.path.splitext(filepath)[1].lower()
    return ext in video_exts


def _is_image_file(filepath: str) -> bool:
    """Check if file is an image based on extension"""
    image_exts = {'.jpg', '.jpeg', '.png', '.heic', '.heif', '.tiff', '.tif', '.bmp', '.gif', '.webp'}
    ext = os.path.splitext(filepath)[1].lower()
    return ext in image_exts


class ExifWriter:
    """
    Tool class for writing EXIF metadata to video and image files.
    
    Example:
        writer = ExifWriter()
        writer.set_gps(lat=34.673500, lon=112.492300, alt=138.848)
        writer.set_device(make="Apple", model="iPhone 14 Plus", software="18.6")
        writer.set_creation_date("2024:01:15 14:30:00")
        writer.write("video.mp4")
    """
    
    def __init__(self, exiftool_path: Optional[str] = None):
        """
        Initialize ExifWriter.
        
        Args:
            exiftool_path: Optional path to exiftool executable. If not provided, will search in PATH.
        """
        self._exiftool_path = find_exiftool(exiftool_path)
        self._gps_lat: Optional[float] = None
        self._gps_lon: Optional[float] = None
        self._gps_alt: float = 0.0
        self._accuracy: Optional[float] = None
        self._make: Optional[str] = None
        self._model: Optional[str] = None
        self._software: Optional[str] = None
        self._creation_date: Optional[str] = None
        self._timezone_offset_hours: int = 8  # Default: UTC+8 (subtract 8 hours for UTC)
    
    def set_gps(self, lat: float, lon: float, alt: float = 0.0) -> 'ExifWriter':
        """
        Set GPS coordinates.
        
        Args:
            lat: Latitude in decimal degrees (-90..90)
            lon: Longitude in decimal degrees (-180..180)
            alt: Altitude in meters (default 0.0)
            
        Returns:
            Self for method chaining
        """
        if not (-90.0 <= lat <= 90.0):
            raise ValueError("Latitude must be between -90 and 90.")
        if not (-180.0 <= lon <= 180.0):
            raise ValueError("Longitude must be between -180 and 180.")
        self._gps_lat = lat
        self._gps_lon = lon
        self._gps_alt = alt
        return self
    
    def set_device(self, make: Optional[str] = None, model: Optional[str] = None, 
                   software: Optional[str] = None) -> 'ExifWriter':
        """
        Set device metadata (Make, Model, Software).
        
        Args:
            make: Device manufacturer (e.g., "Apple")
            model: Device model (e.g., "iPhone 14 Plus")
            software: Software version (e.g., "18.6")
            
        Returns:
            Self for method chaining
        """
        self._make = make
        self._model = model
        self._software = software
        return self
    
    def set_accuracy(self, accuracy: float) -> 'ExifWriter':
        """
        Set location accuracy in meters.
        
        Args:
            accuracy: Accuracy in meters (e.g., 5.0)
            
        Returns:
            Self for method chaining
        """
        self._accuracy = accuracy
        return self
    
    def set_creation_date(self, date_str: str, timezone_offset_hours: int = 8) -> 'ExifWriter':
        """
        Set creation date/time.
        
        Args:
            date_str: Date/time string in format "YYYY:MM:DD HH:MM:SS" (e.g., "2024:01:15 14:30:00")
            timezone_offset_hours: Hours to subtract for UTC conversion (default 8 for UTC+8)
            
        Returns:
            Self for method chaining
            
        Raises:
            ValueError: If date format is invalid
        """
        try:
            datetime.strptime(date_str, "%Y:%m:%d %H:%M:%S")
        except ValueError:
            raise ValueError("Creation date/time format must be YYYY:MM:DD HH:MM:SS (e.g., 2024:01:15 14:30:00)")
        self._creation_date = date_str
        self._timezone_offset_hours = timezone_offset_hours
        return self
    
    def set_timezone_offset(self, hours: int) -> 'ExifWriter':
        """
        Set timezone offset for UTC conversion (used for video files).
        
        Args:
            hours: Hours to subtract from local time to get UTC (default 8 for UTC+8)
            
        Returns:
            Self for method chaining
        """
        self._timezone_offset_hours = hours
        return self
    
    def _build_cmd(self, filepath: str, is_video: bool) -> List[str]:
        """Build exiftool command for a file"""
        cmd = [self._exiftool_path, "-overwrite_original"]
        
        # GPS
        if self._gps_lat is not None and self._gps_lon is not None:
            if is_video:
                # Video: use -Keys: prefix
                gps_str = format_gps(self._gps_lat, self._gps_lon, self._gps_alt)
                cmd.append(f"-Keys:GPSCoordinates={gps_str}")
            else:
                # Image: use standard EXIF GPS tags
                lat_d, lat_m, lat_s, lat_ref, lon_d, lon_m, lon_s, lon_ref, alt = \
                    format_gps_exif(self._gps_lat, self._gps_lon, self._gps_alt)
                cmd.extend([
                    f"-GPS:GPSLatitude={lat_d} {lat_m} {lat_s:.6f}",
                    f"-GPS:GPSLatitudeRef={lat_ref}",
                    f"-GPS:GPSLongitude={lon_d} {lon_m} {lon_s:.6f}",
                    f"-GPS:GPSLongitudeRef={lon_ref}",
                    f"-GPS:GPSAltitude={abs(alt):.3f}",
                    f"-GPS:GPSAltitudeRef={0 if alt >= 0 else 1}",
                ])
        
        # Accuracy
        if self._accuracy is not None:
            if is_video:
                cmd.append(f"-Keys:LocationAccuracyHorizontal={self._accuracy}")
            else:
                cmd.append(f"-EXIF:GPSHPositioningError={self._accuracy}")
        
        # Device info
        if self._make:
            if is_video:
                cmd.append(f"-Keys:Make={self._make}")
            else:
                cmd.append(f"-EXIF:Make={self._make}")
        
        if self._model:
            if is_video:
                cmd.append(f"-Keys:Model={self._model}")
            else:
                cmd.append(f"-EXIF:Model={self._model}")
        
        if self._software:
            if is_video:
                cmd.append(f"-Keys:Software={self._software}")
            else:
                cmd.append(f"-EXIF:Software={self._software}")
        
        # Creation date/time
        if self._creation_date:
            if is_video:
                # QuickTime/ISO media timestamps are UTC. Subtract timezone offset from local input.
                try:
                    local_dt = datetime.strptime(self._creation_date, "%Y:%m:%d %H:%M:%S")
                    utc_dt = local_dt - timedelta(hours=self._timezone_offset_hours)
                    utc_str = utc_dt.strftime("%Y:%m:%d %H:%M:%S")
                except Exception:
                    utc_str = self._creation_date
                cmd.extend([
                    f"-CreateDate={utc_str}",
                    f"-DateTimeOriginal={self._creation_date}",
                    f"-MediaCreateDate={utc_str}",
                    f"-MediaModifyDate={utc_str}",
                ])
            else:
                cmd.extend([
                    f"-EXIF:DateTimeOriginal={self._creation_date}",
                    f"-EXIF:CreateDate={self._creation_date}",
                    f"-FileModifyDate={self._creation_date}",
                ])
        
        cmd.append(filepath)
        return cmd
    
    def write(self, filepath: str, dry_run: bool = False) -> Tuple[bool, str, str]:
        """
        Write EXIF metadata to a file.
        
        Args:
            filepath: Path to the video or image file
            dry_run: If True, only print the command without executing
            
        Returns:
            Tuple of (success: bool, stdout: str, stderr: str)
            
        Raises:
            FileNotFoundError: If file does not exist
            ValueError: If file type is not supported
        """
        if not os.path.isfile(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")
        
        is_video = _is_video_file(filepath)
        is_image = _is_image_file(filepath)
        
        if not (is_video or is_image):
            raise ValueError(f"Unsupported file type: {filepath}. Supported: video (mp4, mov, etc.) or image (jpg, png, etc.)")
        
        cmd = self._build_cmd(filepath, is_video)
        
        if dry_run:
            return (True, " ".join(f'"{c}"' if " " in c or ":" in c or "," in c else c for c in cmd), "")
        
        try:
            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=False,
            )
            return (result.returncode == 0, result.stdout, result.stderr)
        except Exception as e:
            return (False, "", str(e))
    
    def write_batch(self, filepaths: List[str], dry_run: bool = False) -> List[Tuple[str, bool, str, str]]:
        """
        Write EXIF metadata to multiple files.
        
        Args:
            filepaths: List of paths to video or image files
            dry_run: If True, only print commands without executing
            
        Returns:
            List of tuples: (filepath, success, stdout, stderr) for each file
        """
        results = []
        for filepath in filepaths:
            success, stdout, stderr = self.write(filepath, dry_run)
            results.append((filepath, success, stdout, stderr))
        return results
    
    def reset(self) -> 'ExifWriter':
        """
        Reset all parameters to default values.
        
        Returns:
            Self for method chaining
        """
        self._gps_lat = None
        self._gps_lon = None
        self._gps_alt = 0.0
        self._accuracy = None
        self._make = None
        self._model = None
        self._software = None
        self._creation_date = None
        self._timezone_offset_hours = 8
        return self


def main():
    """Command-line interface example"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Write EXIF metadata to video/image files")
    parser.add_argument("file", help="Input file path (video or image)")
    parser.add_argument("--lat", type=float, help="Latitude in decimal degrees")
    parser.add_argument("--lon", type=float, help="Longitude in decimal degrees")
    parser.add_argument("--alt", type=float, default=0.0, help="Altitude in meters (default 0)")
    parser.add_argument("--make", help="Device manufacturer (e.g., Apple)")
    parser.add_argument("--model", help="Device model (e.g., iPhone 14 Plus)")
    parser.add_argument("--software", help="Software version (e.g., 18.6)")
    parser.add_argument("--accuracy", type=float, help="Location accuracy in meters")
    parser.add_argument("--date", help="Creation date/time (YYYY:MM:DD HH:MM:SS)")
    parser.add_argument("--timezone-offset", type=int, default=8, 
                       help="Timezone offset hours for UTC conversion (default 8)")
    parser.add_argument("--exiftool", help="Path to exiftool executable")
    parser.add_argument("--dry-run", action="store_true", help="Print command without executing")
    
    args = parser.parse_args()
    
    writer = ExifWriter(exiftool_path=args.exiftool)
    
    if args.lat is not None and args.lon is not None:
        writer.set_gps(args.lat, args.lon, args.alt)
    
    if args.make or args.model or args.software:
        writer.set_device(args.make, args.model, args.software)
    
    if args.accuracy:
        writer.set_accuracy(args.accuracy)
    
    if args.date:
        writer.set_creation_date(args.date, args.timezone_offset)
    
    success, stdout, stderr = writer.write(args.file, dry_run=args.dry_run)
    
    if args.dry_run:
        print(stdout)
    else:
        if success:
            print(f"Successfully wrote metadata to {args.file}")
            if stdout:
                print(stdout)
        else:
            print(f"Failed to write metadata to {args.file}", file=sys.stderr)
            if stdout:
                print(stdout, file=sys.stderr)
            if stderr:
                print(stderr, file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()

