"""
Copyright (C) 2022-present  SauceyRed (42098474+SauceyRed@users.noreply.github.com)
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import cv2
import argparse

from os import mkdir, getcwd, path
from time import time
from math import floor

parser = argparse.ArgumentParser()
parser.add_argument("path")
parser.add_argument("--output-dir", "-o", "-O")
parser.add_argument("--quality", "-q", "-Q", type=int)
parser.add_argument("--verbose", "-v", "-V", action="store_true")

def CalcDuration(duration):
	total_minutes = duration / 60
	seconds = floor(duration % 60)
	hours = floor(total_minutes / 60)
	minutes = floor(total_minutes % 60)
	if seconds < 10: seconds = "0" + str(seconds)
	if hours < 10: hours = "0" + str(hours)
	if minutes < 10: minutes = "0" + str(minutes)
	return hours, minutes, seconds

def FrameCapture(file_path, _dir, quality, verbose):
	out_dir = path.join(_dir, "frames")
	if verbose: print("Output directory: " + str(out_dir))

	if not path.exists(out_dir):
		if verbose: print("Output path directory does not exist, creating...")
		mkdir(out_dir)
		if verbose: print("Created output directory.")

	video = cv2.VideoCapture(file_path)

	frame_count = 1

	read = True

	if verbose:
			print("FPS: " + str(video.get(cv2.CAP_PROP_FPS)))
			print("Frames in video: " + str(video.get(cv2.CAP_PROP_FRAME_COUNT)))
			print("Starting conversion.")

	start_time = time()

	while True:
		if verbose: print(f"Frame: {str(frame_count)}/{str(video.get(cv2.CAP_PROP_FRAME_COUNT))}")
		read, frame = video.read()
		if not read: break

		image_dir = path.join(out_dir, f"frame{frame_count}.jpg")
		if path.exists(image_dir):
			if verbose: print("Frame already exists in directory, skipping...")
			frame_count += 1
			continue
		if verbose: print(f"Writing frame {frame_count} to file...")
		cv2.imwrite(image_dir, frame, [cv2.IMWRITE_JPEG_QUALITY, quality])
		if verbose: print(f"Written frame {frame_count} to file: {image_dir}")

		frame_count += 1
	
	duration = time() - start_time
	hours, minutes, seconds = CalcDuration(duration)
	if verbose: print(f"Process duration: {hours}:{minutes}:{seconds}")

if __name__ == "__main__":
	args = parser.parse_args()
	_dir = args.output_dir if args.output_dir else getcwd()
	quality = args.quality if args.quality else 95
	FrameCapture(args.path, _dir, quality, args.verbose)
