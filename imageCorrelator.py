import os
import sys
from PIL import Image as PIm
from imagehash import average_hash as i_ah

image_directory = sys.argv[1]
address_in_image_directory = sys.argv[2]
threshold = int(sys.argv[3])

allimages = os.listdir(image_directory)

target = allimages.index(address_in_image_directory)

others = [allimages[i] for i in range(
	len(allimages)
	) if i != target]

others = [
	others[
		i
	] for i in range(
		len(
			others
		)
		) if others[i].endswith(
			"jpg"
			) == True or others[
				i
				].endswith(
					"png"
					) == True or others[
						i
						].endswith("jpeg") == True
	]

hash_ = i_ah(
	PIm.open(
		"{}/{}".format(
			image_directory,address_in_image_directory
			)))

print("target image: {}/{}".format(
	image_directory,address_in_image_directory
	))

for m in range(len(others)):
    others_ = i_ah(PIm.open(
        "{}/{}".format(
            image_directory,
            others[m]
        )
    ))

    out = hash_ - others_

    if out < threshold:
        print("similar")
        break
    else:
        print("not similar")
