# Copyright (c) 2021 PaddlePaddle Authors. All Rights Reserved. 
# 
# Licensed under the Apache License, Version 2.0 (the "License"); 
# you may not use this file except in compliance with the License. 
# You may obtain a copy of the License at 
# 
#     http://www.apache.org/licenses/LICENSE-2.0 
# 
# Unless required by applicable law or agreed to in writing, software 
# distributed under the License is distributed on an "AS IS" BASIS, 
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. 
# See the License for the specific language governing permissions and 
# limitations under the License.

import os
import argparse
import numpy as np
import cv2
from PIL import Image


def _savePalette(label, save_path):
    bin_colormap = np.random.randint(0, 255, (256, 3))  # Visualized colors
    bin_colormap[0, :] = [0, 0, 0]
    bin_colormap = bin_colormap.astype(np.uint8)
    visualimg  = Image.fromarray(label, "P")
    palette = bin_colormap  # long palette of 768 items
    visualimg.putpalette(palette) 
    visualimg.save(save_path, format='PNG')

def segMaskB2I(mask_path, save_path):
    img = np.asarray(Image.open(mask_path))
    mask = np.zeros_like(img)
    results = cv2.findContours(img, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
    cv2_v = cv2.__version__.split(".")[0]
    contours = results[1] if cv2_v == "3" else results[0]  # boundary
    hierarchys = results[2] if cv2_v == "3" else results[1]  # Affiliation information
    areas = {}  # area
    for i in range(len(contours)):
        areas[i] = cv2.contourArea(contours[i])
    sorted(areas.items(), key = lambda kv:(kv[1], kv[0]), reverse=True)  # Area ascending
    # Start filling
    color = 1
    for idx in areas.keys():
        contour = contours[idx]
        hierarchy = hierarchys[0][idx]
        # print(hierarchy)
        if hierarchy[-1] == -1:  # Enter sub-contour
            cv2.fillPoly(mask, [contour], color)
            color += 1
        else:
            cv2.fillPoly(mask, [contour], 0)
    # show
    # cv2.drawContours(mask, contours, -1, (125,125,125), 1)
    # cv2.imshow('src',mask)
    # cv2.waitKey()
    _savePalette(mask, save_path)


# parser = argparse.ArgumentParser(description='Label path and save path')
# parser.add_argument('--label_path', '-o', help='Read the path of the semantic segmentation label folder, necessary parameters', required=True)
# parser.add_argument('--save_path', '-d', help='The path to the folder where the instance segmentation label is saved, and the necessary parameters', required=True)
# args = parser.parse_args()

# if __name__ == "__main__":