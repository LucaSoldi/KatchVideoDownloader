import shutil
import urllib
import urllib.request
import sys
import getopt
import subprocess
import os
from lxml import html
import pprint

def main(argv):

	base_dir = os.path.dirname(os.path.realpath(__file__))
	url = ''
	outputfile = ''
	try:
		opts, args = getopt.getopt(argv,"h:i:o:",["input=","output="])
		if not opts:
			print_usage()
	except getopt.GetoptError:
		print_usage()
	for opt, arg in opts:
		if opt == '-h':
			print_usage()
		elif opt in ("-i", "--input"):
			url = arg
		elif opt in ("-o", "--output"):
			outputfile = arg
   
	print ('URL: ', url)
	print ('Output:', outputfile)

	if shutil.which("ffmpeg") is None:
		print("Error: ffmpeg not found")
		return False

	page = urllib.request.urlopen(url)
	tree = html.fromstring(page.read())

	cloud_link = tree.xpath('//meta[@property="og:image"]')[0].attrib['content']
	
	head, tail = os.path.split(cloud_link)

	url_chunks = head + "/chunk_"

	ts_filenames = []
	ts_filenames_string = '"concat:'
	index = 290
	print ("\nStart downloading chunks...")

	while True:
		ts_url = url_chunks + str(index) + ".ts"
		file_name = ts_url.split('/')[-1]
		try:
			urllib.request.urlretrieve (ts_url, file_name)
		except:
			break
		
		ts_filenames_string += os.path.join(base_dir, file_name) + "|"
		index += 1
		print (file_name)

	ts_filenames_string = ts_filenames_string[:-1]
	ts_filenames_string += '"'

	print ("**Download finished**\n")
	print ("Start merging files...")

	cmd = 'ffmpeg -y -i ' + ts_filenames_string + ' -bsf:a aac_adtstoasc -c copy ' + outputfile
	p = subprocess.Popen(cmd, shell=True,stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
	p.communicate()
	
	print ("\nMerged completed!")

	#delete all chunks
	filelist = [ file for file in os.listdir(".") if file.startswith("chunk_") ]
	for file in filelist:
		os.remove(file)

	sys.exit(0)


def print_usage():
	print ('katch.py -i <katch_url> -o <output_file>')
	sys.exit(1)

if __name__ == "__main__":
   main(sys.argv[1:])