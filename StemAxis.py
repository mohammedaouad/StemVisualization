import numpy as np

# two slices in the proximal shaft to define the axis direction
# fractions tuned visually on the femur mesh
SLICE_FRAC_1 = 0.55
SLICE_FRAC_2 = 0.75
SLICE_TOL_MM = 6.0


def get_slice_center(vertices, z_val, tol=SLICE_TOL_MM):
    slab = vertices[np.abs(vertices[:, 2] - z_val) <= tol]
    if len(slab) < 10:
        raise RuntimeError(f"too few points at z={z_val:.1f}")

    cx = np.median(slab[:, 0])
    cy = np.median(slab[:, 1])
    return np.array([cx, cy, z_val])


def compute_shaft_axis(vertices):
    z_min  = vertices[:, 2].min()
    z_max  = vertices[:, 2].max()
    height = z_max - z_min

    z1 = z_min + SLICE_FRAC_1 * height
    z2 = z_min + SLICE_FRAC_2 * height

    c1 = get_slice_center(vertices, z1)
    c2 = get_slice_center(vertices, z2)

    print(f"StemAxis: C1={np.round(c1,1)}  C2={np.round(c2,1)}")

    direction = c2 - c1
    direction = direction / np.linalg.norm(direction)
    if direction[2] < 0:
        direction = -direction

    origin = (c1 + c2) / 2.0
    return origin, direction, c1, c2, 0.0, 0.0
