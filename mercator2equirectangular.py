import numpy as np
from PIL import Image

def mercator_to_equirectangular(
    # Full disclosure: Claude Sonnet 5 wrote this function
    src_path,
    dst_path,
    lat_min=85.051129,   # standard Web Mercator limit
    lat_max=-85.051129,
    out_height=None,          # defaults to 2:1 aspect (proper equirectangular)
):
    img = Image.open(src_path).convert("RGB")
    src = np.array(img)
    h, w, _ = src.shape

    if out_height is None:
        out_height = w // 2  # standard 2:1 equirectangular aspect

    def lat_to_merc_y(lat_deg):
        lat_rad = np.radians(lat_deg)
        return np.log(np.tan(np.pi / 4 + lat_rad / 2))

    # Mercator-y range spanned by the source image's top and bottom rows
    merc_y_top = lat_to_merc_y(lat_max)
    merc_y_bottom = lat_to_merc_y(lat_min)

    # Latitude for each row of the OUTPUT (equirectangular) image, linear in lat
    out_lats = np.linspace(lat_max, lat_min, out_height)
    out_merc_y = lat_to_merc_y(out_lats)

    # Map each output row's merc_y back to a fractional row index in the source
    src_row_f = (merc_y_top - out_merc_y) / (merc_y_top - merc_y_bottom) * (h - 1)
    src_row_f = np.clip(src_row_f, 0, h - 1)

    row0 = np.floor(src_row_f).astype(int)
    row1 = np.clip(row0 + 1, 0, h - 1)
    frac = (src_row_f - row0)[:, None, None]

    out = src[row0] * (1 - frac) + src[row1] * frac
    out = out.astype(np.uint8)

    Image.fromarray(out).save(dst_path)


