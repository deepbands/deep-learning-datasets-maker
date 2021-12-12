<div align="center">
  <article style="display: flex; flex-direction: column; align-items: center; justify-content: center;">
      <p align="center"><img width="300" src="./docs/img/logo.png" /></p>
      <h1 style="width: 100%; text-align: center;">Deep Learning Dataset Maker</h1>
      <p align="center">We ❤️ Open Source</p>
  </article>
</div>

[![Python 3.8](https://img.shields.io/badge/python-3.8-red.svg)](https://www.python.org/downloads/release/python-380/) [![QGIS 3.16.13](https://img.shields.io/badge/qgis-3.16.13-green.svg)](https://www.qgis.org/)

Deep Learning Datasets Maker is a QGIS plugin to make datasets creation easier for raster and vector data.

![image](https://user-images.githubusercontent.com/13020265/145733632-cc0d6029-9c51-4b6b-b914-41ad051e8db3.png)

## How to use

1. Download and install [QGIS](https://www.qgis.org/en/site/) and clone the repo :
``` git
git clone git@github.com:deepbands/deep-learning-datasets-maker.git
```
2. Install requirements :
   - Enter the folder and install dependent libraries using OSGeo4W shell (Open As Administrator) :
   ``` shell
   cd deep-learning-datasets-maker
   pip install -r requirements.txt
   ```
   - Or open OSGeo4W shell as administrator and enter :
    ``` shell
    pip install opencv-python --user
    ```

3. Copy folder named deep-learning-datasets-maker in QGIS configuration folder and choose the plugin from plugin manager in QGIS (If not appeared restart QGIS).
   - You can know this folder from QGIS Setting Menu at the top-left of QGIS UI `Settings > User Profiles > Open Active Profile Folder` .
   - Go to `python/plugins` then paste the deep-learning-datasets-maker folder.
   - Full path should be like : `C:\Users\$USER\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\deep-learning-datasets-maker`.

4. Open QGIS, load your raster and vector data then select the output paths for rasterized, images and labels then click `ok`.

## TODO

- [ ] Fix: If vector layer saved in memory not in file, `rasterize` can't work.
- [x] Splitting raster data into equal pieces with [GDAL](https://github.com/OSGeo/gdal) , https://gdal.org/.
- [X] Fix: Splitiing Image Size.
- [x] Rasterize shapefile to raster in the same satellite pixel size and projection.
- [x] Convert 24 or 16 bit raster to 8 bit.
- [x] Export as jpg (for raster) and png (for rasterized shapefile) with GDAL.
- [X] Converted semantic segmentation (0 and 1) to instance segmentation for labels (the original label is 0/255) option, and the result is a single-channel image that uses a palette to color. ![](https://s3.bmp.ovh/imgs/2021/09/008c5b768b7e477a.png)
- [X] PaddlePaddle Train/Val/Testing list text.
- [ ] Use GDAL for instance segmentation instead of openCV.
- [ ] Support COCO format.
- [ ] Update plugin's UI : 
  - [ ] Add new tabs for other methods like COCO.
