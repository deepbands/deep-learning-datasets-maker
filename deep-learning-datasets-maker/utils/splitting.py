try:
    from osgeo import gdal
except:
    import gdal

import os.path as osp
import math

# Start Splitting 
def splitting(fn_ras, 
              cdpath, 
              scaleoptions,
              needed_out_x, 
              needed_out_y, 
              file_name,
              mode="IMG",
              standard=True):
    ds = gdal.Open(fn_ras)
    gt = ds.GetGeoTransform()

    options = { "outputType": gdal.GDT_Byte }
    frmt_ext = osp.splitext(osp.basename(fn_ras))[-1].replace(".", "")
    if mode == "IMG":
        if not standard:
            options["outputType"] = ds.GetRasterBand(1).DataType
        else:
            options["format"] = "JPEG"
            frmt_ext = "jpg"
    else:
        if standard:
            options["format"] = "PNG"
            frmt_ext = "png"
    
    # get coordinates of upper left corner
    xmin = gt[0]
    ymax = gt[3]
    resx = gt[1]
    res_y = gt[5]
    resy = abs(res_y)

    # round up to nearst int
    xnotround = ds.RasterXSize / needed_out_x
    xround = math.ceil(xnotround)
    ynotround = ds.RasterYSize / needed_out_y
    yround = math.ceil(ynotround)

    # pixel to meter - 512×10×0.18
    pixtomX = needed_out_x * xround * resx
    pixtomy = needed_out_y * yround * resy
    # size of a single tile
    xsize = pixtomX / xround
    ysize = pixtomy / yround
    # create lists of x and y coordinates
    xsteps = [xmin + xsize * i for i in range(xround + 1)]
    ysteps = [ymax - ysize * i for i in range(yround + 1)]

    # loop over min and max x and y coordinates
    for i in range(xround):
        for j in range(yround):
            xmin = xsteps[i]
            xmax = xsteps[i + 1]
            ymax = ysteps[j]
            ymin = ysteps[j + 1]

            # use gdal warp
            # gdal.WarpOptions(outputType=gdal.gdalconst.GDT_Byte)
            # gdal.Warp("ds"+str(i)+str(j)+".tif", ds,
            # outputBounds = (xmin, ymin, xmax, ymax), dstNodata = -9999)

            # or gdal translate to subset the input raster
            gdal.Translate(
                osp.join(cdpath, (str(file_name) + "-" + str(j) + "-" + str(i) + "." + frmt_ext)), 
                ds, 
                projWin=(abs(xmin), abs(ymax), abs(xmax), abs(ymin)),
                xRes=resx, 
                yRes=-resy, 
                scaleParams=[[scaleoptions]],
                **options)

# close the open dataset!!!
ds = None