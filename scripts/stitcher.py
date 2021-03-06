# Python 2/3 compatibility
from __future__ import print_function

import numpy as np
import cv2 as cv2

import argparse
import sys

modes = (cv2.Stitcher_PANORAMA, cv2.Stitcher_SCANS)

parser = argparse.ArgumentParser(prog = 'stitching.py', description = 'Stitching sample.')
parser.add_argument(' -- mode', 
    type = int, choices = modes, default = cv2.Stitcher_PANORAMA, 
    help = 'Determines configuration of stitcher. The default is `PANORAMA` (%d), '
        'mode suitable for creating photo panoramas. Option `SCANS` (%d) is suitable '
        'for stitching materials under affine transformation, such as scans.' % modes)
parser.add_argument(' -- output', default = 'result.jpg', 
    help = 'Resulting image. The default is `result.jpg`.')
parser.add_argument('img', nargs = '+', help = 'input images')


__doc__ += '\n' + parser.format_help()

def main():
    args = parser.parse_args()

    # read input images

    imgs = []
    for img_name in args.img:
        img = cv2.imread(cv2.samples.findFile(img_name))
        if img is None:
            print("can't read image " + img_name)
            sys.exit(-1)
        imgs.append(img)


    #Set CV2 Stitcher mode
    stitcher = cv2.Stitcher.create(args.mode)

    #Stitch images in array with given mode
    status, pano = stitcher.stitch(imgs)

    #Error in stitching

    if status != cv2.Stitcher_OK:
        print("Can't stitch images, error code = %d" % status)
        sys.exit(-1)

    #Writes image to output arg

    cv2.imwrite(args.output, pano)
    print("stitching completed successfully. %s saved!" % args.output)

    print('Done')


if __name__ == '__main__':
    print(__doc__)
    main()
    cv2.destroyAllWindows()