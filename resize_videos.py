import datetime
from datetime import date
import multiprocessing
import tqdm
import shutil
from shutil import copyfile
from pathlib import Path 
import os
import glob

# use ffmpeg to split the video into frames
# ffmpeg -r 1 -i SDO_10_Year_Sun_4k_20mbps.mp4 -r 1 "$filename%03d.png"


def workit(awork):


	out = awork.replace('/videos/','/videos_resize/').replace('.mp4','_low.mp4')

	r= os.system(f"ffmpeg -i {awork} -filter:v scale=720:-2 -c:a copy {out}")


	return awork

if __name__ == "__main__":


	work = list(glob.glob('/Users/m/data/sun/videos/*.mp4'))
	


	print('working with ', multiprocessing.cpu_count(), 'cores')
	the_pool = multiprocessing.Pool(multiprocessing.cpu_count())
	# the_pool = multiprocessing.Pool(1)
	for result in tqdm.tqdm(the_pool.imap_unordered(workit, work), total=len(work)):  

		print(result)




	# kill the workers
	the_pool.close()
	the_pool.join()