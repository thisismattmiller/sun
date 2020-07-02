import datetime
from datetime import date
import multiprocessing
import tqdm
import shutil
from shutil import copyfile
from pathlib import Path 
import os

# use ffmpeg to split the video into frames
# ffmpeg -r 1 -i SDO_10_Year_Sun_4k_20mbps.mp4 -r 1 "$filename%03d.png"


def workit(awork):
	p = f"/Users/m/data/sun/{awork['date_string']}/"

	Path(p).mkdir(parents=True, exist_ok=True)

	new_counter = 0
	for f in awork['frames']:
		copyfile(f"/Users/m/data/sun/{f}.png", f"{p}{new_counter}.png")		
		new_counter+=1

	for f in reversed(awork['frames']):
		copyfile(f"/Users/m/data/sun/{f}.png", f"{p}{new_counter}.png")		
		new_counter+=1

	r= os.system(f"ffmpeg -r 24 -f image2 -s 3840x2160 -start_number 0 -i {p}%01d.png -vcodec libx264 -crf 25  -pix_fmt yuv420p {p}{awork['date_string']}.mp4")

	copyfile(f"{p}{awork['date_string']}.mp4", f"/Users/m/data/sun/videos/{awork['date_string']}.mp4")		



	shutil.rmtree(p)

	return awork

if __name__ == "__main__":



	start_date = "06/02/10"
	start_date = datetime.datetime.strptime(start_date, "%m/%d/%y")

	d0 = date(2010, 6, 2)
	d1 = date(2020, 6, 3)
	delta = d1 - d0
	print(delta.days)

	start_frame = 240

	work = []

	for d in range(0,delta.days+1):

		frames = list(range(start_frame,start_frame+24))
		work.append({
			'date': date(start_date.year, start_date.month, start_date.day),
			'date_string': f"{start_date.year}{start_date.month}{start_date.day}",
			'frames': frames
		})

		start_date = start_date + datetime.timedelta(days=1)	
		start_frame=start_frame+24


	print(len(work))
	


	print('working with ', multiprocessing.cpu_count(), 'cores')
	the_pool = multiprocessing.Pool(multiprocessing.cpu_count())
	# the_pool = multiprocessing.Pool(1)
	for result in tqdm.tqdm(the_pool.imap_unordered(workit, work), total=len(work)):  

		print(result)




	# kill the workers
	the_pool.close()
	the_pool.join()