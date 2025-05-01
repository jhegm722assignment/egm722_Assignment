import os
import geopandas as gpd
import matplotlib.pyplot as plt
from cartopy.feature import ShapelyFeature
import cartopy.crs as ccrs
import matplotlib.patches as mpatches
import matplotlib.lines as mlines

plt.ion()  # make the plotting interactive


def generate_handles(labels, colors, edge='k', alpha=1):
    """
    Generate matplotlib patch handles to create a legend of each of the features in the map.

    Parameters
    ----------

    labels : list(str)
        the text labels of the features to add to the legend

    colors : list(matplotlib color)
        the colors used for each of the features included in the map.

    edge : matplotlib color (default: 'k')
        the color to use for the edge of the legend patches.

    alpha : float (default: 1.0)
        the alpha value to use for the legend patches.

    Returns
    -------

    handles : list(matplotlib.patches.Rectangle)
        the list of legend patches to pass to ax.legend()
    """
    lc = len(colors)  # get the length of the color list
    handles = []  # create an empty list
    for ii in range(
            len(labels)):  # for each label and color pair that we're given, make an empty box to pass to our legend
        handles.append(mpatches.Rectangle((0, 0), 1, 1, facecolor=colors[ii % lc], edgecolor=edge, alpha=alpha))
    return handles


# adapted this question: https://stackoverflow.com/q/32333870
# answered by SO user Siyh: https://stackoverflow.com/a/35705477
def scale_bar(ax, length=20, location=(0.92, 0.95)):
    """
    Create a scale bar in a cartopy GeoAxes.

    Parameters
    ----------

    ax : cartopy.mpl.geoaxes.GeoAxes
        the cartopy GeoAxes to add the scalebar to.

    length : int, float (default 20)
        the length of the scalebar, in km

    location : tuple(float, float) (default (0.92, 0.95))
        the location of the center right corner of the scalebar, in fractions of the axis.

    Returns
    -------
    ax : cartopy.mpl.geoaxes.GeoAxes
        the cartopy GeoAxes object

    """
    x0, x1, y0, y1 = ax.get_extent()  # get the current extent of the axis
    sbx = x0 + (x1 - x0) * location[0]  # get the right x coordinate of the scale bar
    sby = y0 + (y1 - y0) * location[1]  # get the right y coordinate of the scale bar

    ax.plot([sbx, sbx - length * 1000], [sby, sby], color='k', linewidth=4,
            transform=ax.projection)  # plot a thick black line
    ax.plot([sbx - (length / 2) * 1000, sbx - length * 1000], [sby, sby], color='w', linewidth=2,
            transform=ax.projection)  # plot a white line from 0 to halfway

    ax.text(sbx, sby - (length / 4) * 1000, f"{length} km", ha='center', transform=ax.projection,
            fontsize=6)  # add a label at the right side
    ax.text(sbx - (length / 2) * 1000, sby - (length / 4) * 1000, f"{int(length / 2)} km", ha='center',
            transform=ax.projection, fontsize=6)  # add a label in the center
    ax.text(sbx - length * 1000, sby - (length / 4) * 1000, '0 km', ha='center', transform=ax.projection,
            fontsize=6)  # add a label at the left side

    return ax


outline = gpd.read.file(os.path.abspath('data_files/NI_outline.shp'))
SAC = gpd.read.file(os.path.abspath('data_files/SAC.shp'))
SPA = gpd.read.file(os.path.abspath('data_files/SPA.shp'))
Reserves = gpd.read.file(os.path.abspath('data_files/NNR_and_NR_Points.shp'))

ni_utm = ccrs.UTM(29)  # create a Universal Transverse Mercator reference system to transform our data to the UTM Zone that Northern Ireland is part of.

ccrs.CRS(outline.crs) # create a cartopy CRS representation of the CRS associated with the Outline dataset

fig = plt.figure(figsize=(8, 8))  # create a figure of size 8x8 (representing the page size in inches)
ax = plt.axes(projection=ni_utm)  # create an axes object in the figure, using a UTM projection,
# where we can actually plot our data.

# first, we just add the outline of Northern Ireland using cartopy's ShapelyFeature
outline_feature = ShapelyFeature(outline['geometry'], ni_utm, edgecolor='k', facecolor='w')
ax.add_feature(outline_feature) # add the features we've created to the map.

xmin, ymin, xmax, ymax = outline.total_bounds
# using the boundary of the shapefile features, zoom the map to our area of interest
ax.set_extent([xmin-5000, xmax+5000, ymin-5000, ymax+5000], crs=ni_utm)  # because total_bounds
# gives output as xmin, ymin, xmax, ymax,
# but set_extent takes xmin, xmax, ymin, ymax, we re-order the coordinates here.

# pick colors, add features to the map
SAC_colors = ['#003f5c']
SPA_colors = ['#ffa600']
Reserves_colors = ['#955196']

