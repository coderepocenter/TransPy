import os
import click
import geopandas as gpd
from multiprocessing import Pool
from transpy.utils import file_parts, split_linestring_df


@click.command()
@click.option(
    '-i', '--input_file',
    type=str,
    required=True,
    prompt=True,
    default=None,
    help='Path to the spatial file that contains the LineString geometries. The file should be readable with GeoPandas',
    show_default=False
)
@click.option(
    '-o', '--output_file',
    type=str,
    required=False,
    prompt=False,
    default=None,
    help='Path to the filename used as output. If none provided the input file name with "_split" appended to the end'
         'is used',
    show_default=False
)
@click.option(
    '-l', '--max_length',
    type=float,
    required=False,
    prompt=False,
    default=10.0,
    help='The maximum allowable length. Any Longer LineStrings are divided. The unit is defined'
         'by length_epsg parameter. Default is 10.0 meter.',
    show_default=True
)
@click.option(
    '--length_epsg',
    type=int,
    required=False,
    prompt=False,
    default=3857,
    help='The EPSG that max_length is defined.',
    show_default=True
)
@click.option(
    '-n', '--nprocesses',
    type=int,
    required=False,
    prompt=False,
    default=0,
    help='Number of parallel processes to be used. Default is 0, i.e. serial processing',
    show_default=True
)
@click.option(
    '--geom_field',
    type=str,
    required=False,
    prompt=False,
    default='geometry',
    help='The name of the geometry field.',
    show_default=True
)
@click.option(
    '--part_id_field',
    type=str,
    required=False,
    prompt=False,
    default='part_id',
    help='The name of the column or attribute to be added, which identifies the '
         'different part of the LineString',
    show_default=True
)
@click.option(
    '-d', '--driver',
    type=str,
    required=False,
    prompt=False,
    default='GPKG',
    help='The Driver to be used for output file.',
    show_default=True
)
@click.option(
    '--layer',
    type=str,
    required=False,
    prompt=False,
    default=None,
    help='the layer to be used for GPKG driver. Default value is the input filename',
    show_default=False
)
def split_linestring(max_length, **kwargs):
    # processing input file name
    input_file = kwargs.get('input_file')
    file_path, filename, file_basename, file_extension = file_parts(input_file)
    print((file_path, filename, file_basename, file_extension))

    # processing output filename
    if kwargs.get('driver') not in {'GPKG', 'Shapefile', 'GeoJSON'}:
        raise ValueError('Unsupported driver.')

    output_file = kwargs.get('output_file')
    if output_file is None:
        output_file_ext = {
            'GPKG': 'gpkg',
            'Shapefile': 'shp',
            'GeoJSON': 'geojson'
        }.get(kwargs.get('driver'))
        output_file = os.path.join(
            '.',
            f'{file_basename}_split.{output_file_ext}'
        )

    layer = file_basename if kwargs.get('layer') is None else kwargs.get('layer')

    # Preparing worker pool
    nprocesses = kwargs.get('nprocesses')
    pool = Pool(processes=nprocesses) if nprocesses > 1 else None

    # reading input file
    df = gpd.read_file(input_file)

    # processing
    o_gdf = split_linestring_df(
        df=df,
        max_length=max_length,
        pool=pool,
        **kwargs
    )

    # writing output file
    if kwargs.get('driver') == 'GPKG':
        o_gdf.to_file(
            output_file,
            layer=layer,
            driver='GPKG'
        )
    elif kwargs.get('driver') == 'Shapefile':
        o_gdf.to_file(output_file)
    elif kwargs.get('driver') == 'GeoJSON':
        o_gdf.to_file(
            output_file,
            driver='GeoJSON'
        )

if __name__ == '__main__':
    split_linestring()
