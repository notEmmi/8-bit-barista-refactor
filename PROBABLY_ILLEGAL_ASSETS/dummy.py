import os
from PIL import Image

def process_sprite(image_path):
	with Image.open(image_path) as img:
		# Ensure the image has an alpha channel
		img = img.convert("RGBA")
		
		# Get the bounding box of the non-transparent content
		bbox = img.getbbox()
		if bbox:
			# Crop the image to the bounding box
			cropped_img = img.crop(bbox)
			
			 # Mirror the cropped image horizontally
			mirrored_img = cropped_img.transpose(Image.FLIP_LEFT_RIGHT)
			
			# Save the processed image, replacing the original
			mirrored_img.save(image_path)

def main():
	# Get the directory of the current script
	script_dir = os.path.dirname(os.path.abspath(__file__))
	
	# List of image filenames
	image_files = ["alex.png", "emma.png", "liam.png", "pheonix.png", "riley.png", "sophia.png"]
	
	# Process each image
	for image_file in image_files:
		image_path = os.path.join(script_dir, image_file)
		process_sprite(image_path)

if __name__ == "__main__":
	main()