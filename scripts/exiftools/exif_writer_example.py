#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Example usage of ExifWriter tool class
"""

from exif_writer import ExifWriter


def example_single_file():
    """Example: Write EXIF to a single file"""
    print("=== Example 1: Single File ===")
    
    writer = ExifWriter()
    
    # Set GPS coordinates
    writer.set_gps(lat=34.673500, lon=112.492300, alt=138.848)
    
    # Set device information
    writer.set_device(make="Apple", model="iPhone 14 Plus", software="18.6")
    
    # Set location accuracy
    writer.set_accuracy(5.0)
    
    # Set creation date (local time, will be converted to UTC for video)
    writer.set_creation_date("2024:01:15 14:30:00", timezone_offset_hours=8)
    
    # Write to file
    success, stdout, stderr = writer.write("example.mp4")
    
    if success:
        print("✓ Success!")
        if stdout:
            print(stdout)
    else:
        print("✗ Failed!")
        if stderr:
            print(stderr)


def example_batch_files():
    """Example: Write EXIF to multiple files"""
    print("\n=== Example 2: Batch Files ===")
    
    writer = ExifWriter()
    writer.set_gps(lat=34.673500, lon=112.492300, alt=138.848)
    writer.set_device(make="Apple", model="iPhone 14 Plus")
    writer.set_creation_date("2024:01:15 14:30:00")
    
    files = ["video1.mp4", "video2.mp4", "image1.jpg"]
    results = writer.write_batch(files)
    
    for filepath, success, stdout, stderr in results:
        status = "✓" if success else "✗"
        print(f"{status} {filepath}")
        if not success and stderr:
            print(f"  Error: {stderr}")


def example_method_chaining():
    """Example: Method chaining"""
    print("\n=== Example 3: Method Chaining ===")
    
    writer = (ExifWriter()
              .set_gps(lat=34.673500, lon=112.492300, alt=138.848)
              .set_device(make="Apple", model="iPhone 14 Plus", software="18.6")
              .set_accuracy(5.0)
              .set_creation_date("2024:01:15 14:30:00"))
    
    success, stdout, stderr = writer.write("example.mp4", dry_run=True)
    print("Dry run command:")
    print(stdout)


def example_image_file():
    """Example: Write EXIF to an image file"""
    print("\n=== Example 4: Image File ===")
    
    writer = ExifWriter()
    writer.set_gps(lat=34.673500, lon=112.492300, alt=138.848)
    writer.set_device(make="Canon", model="EOS R5")
    writer.set_creation_date("2024:01:15 14:30:00")
    # Note: For images, creation_date is written as-is (no timezone conversion)
    
    success, stdout, stderr = writer.write("photo.jpg")
    
    if success:
        print("✓ Success!")
    else:
        print("✗ Failed!")
        print(stderr)


def example_dry_run():
    """Example: Dry run to see the command"""
    print("\n=== Example 5: Dry Run ===")
    
    writer = ExifWriter()
    writer.set_gps(lat=34.673500, lon=112.492300)
    writer.set_device(make="Apple", model="iPhone 14 Plus")
    writer.set_creation_date("2024:01:15 14:30:00")
    
    success, cmd, _ = writer.write("example.mp4", dry_run=True)
    print("Command that would be executed:")
    print(cmd)


def example_reset():
    """Example: Reset and reuse writer"""
    print("\n=== Example 6: Reset and Reuse ===")
    
    writer = ExifWriter()
    
    # First file
    writer.set_gps(lat=34.673500, lon=112.492300)
    writer.set_device(make="Apple", model="iPhone 14 Plus")
    writer.write("file1.mp4")
    
    # Reset and configure for second file
    writer.reset()
    writer.set_gps(lat=40.7128, lon=-74.0060)  # New York
    writer.set_device(make="Samsung", model="Galaxy S23")
    writer.write("file2.mp4")


if __name__ == "__main__":
    print("ExifWriter Usage Examples\n")
    print("Note: These examples use placeholder file paths.")
    print("Replace with actual file paths to test.\n")
    
    # Uncomment the examples you want to run:
    # example_single_file()
    # example_batch_files()
    # example_method_chaining()
    # example_image_file()
    # example_dry_run()
    # example_reset()
    
    print("\nSee exif_writer_example.py for code examples.")

