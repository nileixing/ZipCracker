# coding=utf-8
#
# Usage:
#
# python zipCracker.py -f target.zip
#
# python zipCracker.py -f target.zip -s 1 -e 6
# 
# python zipCracker.py -f target.zip -d password.txt
#

import sys, time
from zipfile import ZipFile
from argparse import ArgumentParser
import itertools

def _exit(string):
	global parser
	print ('\nExit : ' + string + '\n')
	parser.print_help()
	exit(0)

def _resultExit(count, passwd):
	print('Tried %d passwords and password is: %s' % (count, passwd))
	_timeEnd()
	exit(0)

def _zFile(zFile, fileName, password):
	try:
		info = zFile.getinfo(fileName)
		source = zFile.open(name=info, pwd=password.encode('utf-8'))
		source.read(10)
		source.close()
	except Exception as e:
		#print(e)
		return False
	return True

def _timeStart():
	global t1
	t1 = time.time()

def _timeEnd():
	global t1
	print('Used time is %d ms' % int((time.time() - t1) * 1000))

def main():
	global parser
	parser = ArgumentParser()
	parser.add_argument('-f', '--file', dest='zipFile', metavar='<filename>', required=True, type=str, help='path to zip file')
	parser.add_argument('-d', '--dictionary', dest='dictionary', metavar='<filename>', type=str, help='path to password dictionary file')
	parser.add_argument('-s', '--start-length', dest='minLength', metavar='N', default=1, type=int, help='minimum length for brute-force - defaults to 1 (only available in no dictionary file)')
	parser.add_argument('-e', '--end-length', dest='maxLength', metavar='N', default=6, type=int, help='maximum length for brute-force - defaults to 6 (only available in no dictionary file)')
	args = parser.parse_args()

	print('')

	_timeStart()

	zFile = ZipFile(args.zipFile)
	namelist = zFile.namelist()
	dictionary = args.dictionary
	minLength = args.minLength
	maxLength = args.maxLength

	zFileName = ''
	for name in namelist:
		if name[-1] != '/':
			zFileName = name
			break
	if zFileName == '':
		_exit('No valid file in zip ')

	count = 0
	if dictionary is not None:
		f = open(dictionary, 'r')
		content = f.readlines()
		f.close()
		print('%s passwords in dictionary file \n' % len(content))
		for passwd in content:
			count += 1
			if _zFile(zFile,zFileName,passwd.strip('\n\r')):
				_resultExit(count, passwd)
	else:
		#characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
		characters = "abcdefghijklmnopqrstuvwxyz"

		for length in range(minLength, maxLength + 1):
			print('Length of password : %s' % length)
			content = itertools.product(characters, repeat=length)
			for pw in content:
				passwd = ''.join(pw)
				count += 1
				if _zFile(zFile,zFileName,passwd):
					_resultExit(count, passwd)
	print('Tried %d passwords but no password found ...\n' % count)
	_timeEnd()

if __name__ == '__main__':
	main()