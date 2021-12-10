<div align="center">
  <article style="display: flex; flex-direction: column; align-items: center; justify-content: center;">
      <p align="center"><img width="300" src="./docs/img/logo.png" /></p>
      <h1 style="width: 100%; text-align: center;">Deep Learning Dataset Maker</h1>
  </article>
</div>

[![Python 3.8](https://img.shields.io/badge/python-3.8-red.svg)](https://www.python.org/downloads/release/python-380/) [![QGIS 3.16.13](https://img.shields.io/badge/qgis-3.16.13-green.svg)](https://www.qgis.org/)

Deep Learning Datasets Maker is a QGIS plugin to make datasets creation easier for raster and vector data.

![image](https://user-images.githubusercontent.com/13020265/145611943-5895b715-68d2-4de8-96a7-c7e6170936e1.png)

## How to use

1. Download and install [QGIS](https://www.qgis.org/en/site/) and clone the repo :
``` git
git clone git@github.com:deepbands/deep-learning-datasets-maker.git
```

2. Copy folder named deep-learning-datasets-maker in QGIS configuration folder and choose the plugin from plugin manager in QGIS (If not appeared restart QGIS).
   - You can know this folder from QGIS Setting Menu at the top-left of QGIS UI `Settings > User Profiles > Open Active Profile Folder` .
   - Go to `python/plugins` then paste the deep-learning-datasets-maker folder.
   - Full path should be like : `C:\Users\$USER\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\deep-learning-datasets-maker`.

3. Open QGIS, load your raster and vector data then select the output paths for rasterized, images and labels then click `ok`.

## TODO

- [ ] Fix: If vector layer saved in memory not in file, `rasterize` can't work.
- [X] Fix: Splitiing Image Size.

