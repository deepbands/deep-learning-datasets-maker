try:
    from osgeo import gdal, ogr
    import random
except:
    import gdal
    import ogr


def rasterizeInsSeg(ras_path, vec_path, outputRasIN, InsSegGDALout, color_text_path):
    driver = ogr.GetDriverByName("ESRI Shapefile")
    ras_ds = gdal.Open(ras_path)
    vec_ds = driver.Open(vec_path, 1)

    lyr = vec_ds.GetLayer()
    geot = ras_ds.GetGeoTransform()
    proj = ras_ds.GetProjection()  # Get the projection from original tiff (fn_ras)

    layerdefinition = lyr.GetLayerDefn()
    feature = ogr.Feature(layerdefinition)

    schema = []
    for n in range(layerdefinition.GetFieldCount()):
        fdefn = layerdefinition.GetFieldDefn(n)
        schema.append(fdefn.name)
    yy = feature.GetFieldIndex("MLDS")
    if yy < 0:
        print("MLDS field not found, we will create one for you and make all values to 1")
    else:
        lyr.DeleteField(yy)
        # lyr.ResetReading()
    new_field = ogr.FieldDefn("MLDS", ogr.OFTInteger)
    lyr.CreateField(new_field)
    feature_count = lyr.GetFeatureCount()
    for feature in lyr:
        for col in range(feature_count):
            col = random.randint(1, 255)
            feature.SetField("MLDS", col)
        lyr.SetFeature(feature)
        feature = None

    # isAttributeOn = att_field_input if att_field_input != '' else first_att_field
    # pixelsizeX = 0.2 if ras_ds.RasterXSize < 0.2 else ras_ds.RasterXSize
    # pixelsizeY = -0.2 if ras_ds.RasterYSize < -0.2 else ras_ds.RasterYSize

    drv_tiff = gdal.GetDriverByName("GTiff")
    chn_ras_ds = drv_tiff.Create(
        outputRasIN, ras_ds.RasterXSize, ras_ds.RasterYSize, 1, gdal.GDT_Byte)

    # Set the projection from original tiff (fn_ras) to the rasterized tiff
    chn_ras_ds.SetGeoTransform(geot)
    chn_ras_ds.SetProjection(proj)
    chn_ras_ds.FlushCache()

    gdal.RasterizeLayer(chn_ras_ds, [1], lyr, burn_values=[
                        1], options=["ATTRIBUTE=MLDS"])

    # Change No Data Value to 0
    # chn_ras_ds.GetRasterBand(1).SetNoDataValue(0)
    chn_ras_ds = None
    # lyr.DeleteField(yy) # delete field
    vec_ds = None

    gdal.DEMProcessing(InsSegGDALout, outputRasIN, 'color-relief',
                       colorFilename=color_text_path, computeEdges=False)
