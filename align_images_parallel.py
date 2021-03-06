import os
import sys
import bz2
from keras.utils import get_file
from ffhq_dataset.face_alignment import image_align
from ffhq_dataset.landmarks_detector import LandmarksDetector
import concurrent.futures

LANDMARKS_MODEL_URL = 'http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2'


def unpack_bz2(src_path):
    data = bz2.BZ2File(src_path).read()
    dst_path = src_path[:-4]
    with open(dst_path, 'wb') as fp:
        fp.write(data)
    return dst_path



def processimage(img_name,paths = [sys.argv[1],sys.argv[2]] ):
	LANDMARKS_MODEL_URL = 'http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2'
	landmarks_model_path = 'C:\\Users\\spiorf\\.keras\\temp\\shape_predictor_68_face_landmarks.dat' #unpack_bz2(get_file('shape_predictor_68_face_landmarks.dat.bz2',LANDMARKS_MODEL_URL, cache_subdir='temp'))
	landmarks_detector = LandmarksDetector(landmarks_model_path)
	raw_img_path = os.path.join(paths[0], img_name)
	
	for i, face_landmarks in enumerate(landmarks_detector.get_landmarks(raw_img_path), start=1):
		face_img_name = '%s_%02d.png' % (os.path.splitext(img_name)[0], i)
		print(face_img_name)
		aligned_face_path = os.path.join(paths[1], face_img_name)
		image_align(raw_img_path, aligned_face_path, face_landmarks)
		print(face_img_name + "ok")		
	return img_name

if __name__ == "__main__":


	with concurrent.futures.ProcessPoolExecutor() as executor:
		# Get a list of files to process
		paths = ['','']
		paths[0] = sys.argv[1]
		paths[1] = sys.argv[2]
		LANDMARKS_MODEL_URL = 'http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2'
		landmarks_model_path = unpack_bz2(get_file('shape_predictor_68_face_landmarks.dat.bz2',
												   LANDMARKS_MODEL_URL, cache_subdir='temp'))
		print(landmarks_model_path)
		RAW_IMAGES_DIR = paths[0]
		ALIGNED_IMAGES_DIR = paths[1]
		landmarks_detector = LandmarksDetector(landmarks_model_path)
		image_files = os.listdir(paths[0])
			#	 Process the list of files, but split the work across the process pool to use all CPUs!
		for image_file in zip(image_files, executor.map(processimage, image_files)):
			print(f"{image_file}")