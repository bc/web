#!/usr/bin/env python3
"""
Image Optimization Script
Converts images to WebP format, creates responsive sizes, and optimizes quality.
"""

import os
import subprocess
import json
from pathlib import Path
from datetime import datetime

# Configuration
IMG_DIR = Path("./img")
QUALITY = 85  # ImageMagick quality (0-100)
WEBP_QUALITY = 80  # WebP specific quality
RESPONSIVE_SIZES = {
    "thumbnail": 300,
    "small": 600,
    "medium": 900,
    "large": 1200,
}

class ImageOptimizer:
    def __init__(self):
        self.stats = {
            "processed": 0,
            "skipped": 0,
            "errors": [],
            "original_size": 0,
            "optimized_size": 0,
        }

    def get_file_size(self, filepath):
        """Get file size in bytes."""
        return os.path.getsize(filepath)

    def optimize_image(self, filepath):
        """Optimize a single image and convert to WebP."""
        try:
            original_size = self.get_file_size(filepath)
            filename = Path(filepath).stem
            img_dir = Path(filepath).parent

            # Convert to WebP main image
            webp_path = img_dir / f"{filename}.webp"

            # Use ImageMagick to convert and optimize
            cmd = [
                "magick",
                str(filepath),
                "-quality",
                str(WEBP_QUALITY),
                "-strip",  # Remove metadata
                "-interlace",
                "Plane",  # Progressive encoding
                str(webp_path),
            ]

            subprocess.run(cmd, check=True, capture_output=True)

            # Create responsive versions
            for size_name, width in RESPONSIVE_SIZES.items():
                responsive_path = img_dir / f"{filename}-{size_name}.webp"
                resp_cmd = [
                    "magick",
                    str(filepath),
                    "-resize",
                    f"{width}x>",  # Only resize if larger
                    "-quality",
                    str(WEBP_QUALITY),
                    "-strip",
                    "-interlace",
                    "Plane",
                    str(responsive_path),
                ]
                subprocess.run(resp_cmd, check=True, capture_output=True)

            optimized_size = self.get_file_size(webp_path)
            compression_ratio = (1 - optimized_size / original_size) * 100

            print(
                f"✓ {filename:<40} "
                f"{original_size/1024:>8.1f}KB → {optimized_size/1024:>8.1f}KB "
                f"({compression_ratio:>5.1f}% saved)"
            )

            self.stats["processed"] += 1
            self.stats["original_size"] += original_size
            self.stats["optimized_size"] += optimized_size

        except subprocess.CalledProcessError as e:
            error_msg = f"Error processing {filepath}: {e}"
            print(f"✗ {error_msg}")
            self.stats["errors"].append(error_msg)
        except Exception as e:
            error_msg = f"Unexpected error for {filepath}: {str(e)}"
            print(f"✗ {error_msg}")
            self.stats["errors"].append(error_msg)

    def run(self):
        """Main optimization pipeline."""
        print("\n" + "=" * 100)
        print("IMAGE OPTIMIZATION PIPELINE")
        print("=" * 100)
        print(
            f"Directory: {IMG_DIR.absolute()}\n"
            f"Quality:   {WEBP_QUALITY}/100\n"
            f"Sizes:     {', '.join(f'{k}({v}px)' for k, v in RESPONSIVE_SIZES.items())}\n"
        )

        if not IMG_DIR.exists():
            print(f"✗ Image directory not found: {IMG_DIR}")
            return

        # Find all images (excluding WebP and PSD)
        image_extensions = {".png", ".jpg", ".jpeg", ".gif"}
        image_files = [
            f for f in IMG_DIR.iterdir()
            if f.suffix.lower() in image_extensions
            and not f.name.endswith(("-thumbnail.webp", "-small.webp", "-medium.webp", "-large.webp"))
        ]

        if not image_files:
            print(f"No images found in {IMG_DIR}")
            return

        print(f"Found {len(image_files)} images to process:\n")

        for img_file in sorted(image_files):
            self.optimize_image(str(img_file))

        # Print summary
        print("\n" + "=" * 100)
        print("OPTIMIZATION SUMMARY")
        print("=" * 100)
        print(f"Processed:        {self.stats['processed']} images")
        print(f"Errors:           {len(self.stats['errors'])}")
        print(
            f"Total saved:      "
            f"{(self.stats['original_size'] - self.stats['optimized_size']) / 1024 / 1024:.2f}MB "
            f"({(1 - self.stats['optimized_size'] / self.stats['original_size']) * 100:.1f}%)"
        )
        print(
            f"Before:           {self.stats['original_size'] / 1024 / 1024:.2f}MB\n"
            f"After:            {self.stats['optimized_size'] / 1024 / 1024:.2f}MB"
        )

        if self.stats["errors"]:
            print("\nErrors encountered:")
            for error in self.stats["errors"]:
                print(f"  - {error}")

        print("=" * 100 + "\n")


if __name__ == "__main__":
    optimizer = ImageOptimizer()
    optimizer.run()
