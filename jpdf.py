#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2012 Tomas Meszaros <exo [at] tty [dot] sk>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# --------------------------------------------------------------------
#
# DESCRIPTION:
#
# jpdf is a simple program which can join several pdf files into one
#
# --------------------------------------------------------------------
#
# DEPENDENCES:
#
#	pyPdf
#
# pyPdf can be found at http://pybrary.net/pyPdf/
#
# --------------------------------------------------------------------
#
# USAGE:
#
# $ python jpdf.py final.pdf file1 [file2 file3 ... fileN]
#
#  to show help
#
# $ python jpdf.py [-h] [--help]

from pyPdf import PdfFileWriter, PdfFileReader
from sys import argv
from getpass import getpass

def main():
	destination = argv[1]

	# take pdf files (file1 ... fileN) from argv & save them into input_files[]
	input_files = []
	try:
		for pdf_file in argv[2:]:
			input_files.append(PdfFileReader(file(pdf_file, "rb")))
	except IOError:
		print "error: file \"%s\" does not exist" % pdf_file
		return

	# check for any encrypted file
	for i in range(len(input_files)):
		if (input_files[i].getIsEncrypted()):
			print "warrning: file \"%s\" is encrypted" % argv[i+2]
			pw = getpass("decrypt %s, password: " % argv[i+2])
			if (input_files[i].decrypt(pw) == 0):
				print "error: sorry, wrong passowrd"
				return
			else: print "%s has been dencrypted, processing..." % argv[i+2]

	# add all pages from input_files[] to output
	output = PdfFileWriter()
	for one_pdf in input_files:
		for i in range(one_pdf.getNumPages()):
			output.addPage(one_pdf.getPage(i))			

	# write all stuff to destination
	outputStream = file(destination, "wb")
	output.write(outputStream)
	outputStream.close()
	print "done!"

def show_help():
	print "USAGE: %s final.pdf file1 [file2 file3 ... fileN]" % argv[0]
	print "       %s [-h] [--help]" % argv[0]	

if __name__ == "__main__":
	if ((len(argv) == 2) and (argv[1] == "-h" or argv[1] == "--help")): show_help()
	elif (len(argv) >= 3): main()
	else: show_help()
