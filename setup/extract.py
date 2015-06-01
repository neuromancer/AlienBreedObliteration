"""	
	Written By:
 		Chris Humphreys
 		Email: < chris (--AT--) habitualcoder [--DOT--] com >
 
 	All python source code copyright Chris Humphreys 2010
	Level data, Obliteration name and some media copyright 
	Flash Jester Punk 2007
	Alien Breed name, concept and media copyright Team17 1992
 
	This file is part of alien breed obliteration wii edition
 
 	This program is free software; you can redistribute it and/or modify
 	it under the terms of the GNU General Public License as published by
 	the Free Software Foundation; either version 3 of the License, or
 	(at your option) any later version.
 
 	This program is distributed in the hope that it will be useful,
 	but WITHOUT ANY WARRANTY; without even the implied warranty of
 	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 	GNU General Public License for more details.
 
 	You should have received a copy of the GNU General Public License
 	along with this program.  If not, see <http://www.gnu.org/licenses/>.
 """
import hashlib
import zipfile

from xavreader import *
from patch import *

DATA1_SUM = "53bf34e2430174873f8109b7a44cc603" 

def main():
	extract_data_file()
	extract_files()

def extract_data_file():
	zf = zipfile.ZipFile("alienbreed2k5x6.zip")
	zf.extract("data1.xav")

	if md5sum("data1.xav"):
		print "Checksums match. Archive is valid"
	else:
		print "Checksums do not match. Archive is invalid"
		exit(1)

def md5sum(datafile):
	with open(datafile, 'rb') as f:
		content = f.read()
	m = hashlib.md5()
	m.update(content)
	md5 = m.hexdigest()
	return md5 == DATA1_SUM

def extract_files():
	print "Extracting media files"
	to_patch = [
"biospike.uni", "firebossworm.uni", "forcefieldhorizontal.uni", "GameEndText.txt", "hostage.uni", "level12.lev", "level13.lev", "level1.lev", "level2.lev",  "level8.lev", "level9.lev", "shipfire.uni", "toolsandweapons.wep"]

	dirs = dict()
	dirs["bmp"] = "../images/"
	dirs["ogg"] = "../sounds/"
	dirs["xm"] = "../sounds/"
	dirs["txt"] = "../config/"
	dirs["uni"] = "../config/"
	dirs["lev"] = "../config/"
	dirs["til"] = "../config/"
	dirs["wep"] = "../config/"
	dirs["map"] = "../config/"
	dirs["to_patch"] = to_patch
	dirs["working"] = "working/"

	x = XavReader("data1.xav", dirs)
	x.read_all()
	x.close()

	for patch in to_patch:
		patch_file = patch.split(".")[0] + ".patch"
		print "Patching %s" % patch_file
		SimplePatch.patch("working/" + patch, "../config/" + patch, patch_file)		

main()
