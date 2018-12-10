import csv
import os
import sys
import matplotlib.pyplot as plt
proj_path = os.path.dirname(os.path.dirname(__file__))
sys.path.append(proj_path)

from processor.interpolate import simple_interpolate
from processor.utils import create_raster_dataset, transform_points


if __name__ == "__main__":
    points = [
        (-105.56697738953633, 39.81947938735356),
        (-105.21678100734708, 39.62703150391643),
        (-105.77203282502806, 41.350334822326985),
        (-105.44194259315248, 40.42134397606875),
        (-105.75605818377305, 41.27879519182998),
        (-105.37770977083764, 40.279490706399166),
        (-104.28772577563689, 40.302569381951244),
        (-105.3684853823174, 40.067957199865674),
        (-106.0200389734573, 40.701936989432234),
        (-104.95472463428365, 40.73354899968384),
        (-104.29537020632878, 40.54951843368691),
        (-104.48548940006741, 41.05679332597173),
        (-105.55428969884345, 39.85509397598161),
        (-104.11060466367678, 41.06959752139767),
        (-104.79225305750832, 39.883012584792816),
        (-104.38969584409064, 40.51407810945676),
        (-105.09984196706546, 41.43398595156309),
        (-105.90087016461587, 39.60390556548707),
        (-105.38003292697505, 40.82426716390299),
        (-105.9208053739297, 40.63176663097788)
    ]

    values = [
        211, 393, 484, 441, 431, 
        434, 247, 195, 124, 423, 
        253, 101, 105, 234, 379, 
        237, 460, 125, 466, 299
    ]

    data = []
    for point, value in zip(points, values):
        data.append((point[0], point[1], value))

    csv_file = "/home/gu/Downloads/points.csv"
    with open(csv_file, "w") as f:
        writer = csv.writer(f)
        writer.writerow(['lon', 'lat', 'value'])
        writer.writerows(data)

    data, x, y = simple_interpolate(points, values)
    plt.imshow(data)
    plt.show()
    work_dir = "/home/gu/Downloads"
    file_name = "grid_map.tif"
    create_raster_dataset(data, x, y, work_dir, file_name)
