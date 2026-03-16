import numpy as np
from scipy.optimize import least_squares

# Detect the femoral head center by fitting a sphere on the dome region.
# The head is cut at the neck in the STL export from 3D Slicer so we
# need to isolate only the top part before fitting, otherwise the fit is bad.

def compute_hjc(vertices):
    z_min  = vertices[:,2].min()
    z_max  = vertices[:,2].max()
    height = z_max - z_min
    x_mean = vertices[:,0].mean()

    # head is in the top 18% of the bone, lateral side (x > mean)
    z_thresh = z_min + 0.82 * height
    head_pts = vertices[
        (vertices[:,2] > z_thresh) &
        (vertices[:,0] > x_mean)
    ]
    print(f"HJC: found {len(head_pts)} pts in head region")

    if len(head_pts) < 30:
        # fallback if lateral filter is too aggressive
        head_pts = vertices[vertices[:,2] > z_thresh]

    # keep only the upper 60% of the head region (true dome, avoids neck cut)
    hz_min = head_pts[:,2].min()
    hz_max = head_pts[:,2].max()
    dome_pts = head_pts[head_pts[:,2] > hz_min + 0.40 * (hz_max - hz_min)]
    print(f"HJC: dome has {len(dome_pts)} pts")

    if len(dome_pts) < 20:
        dome_pts = head_pts

    # initial guess from bounding box center, biased downward
    # because the sphere center sits inside the bone, not on the surface
    cx0 = (dome_pts[:,0].min() + dome_pts[:,0].max()) / 2.0
    cy0 = (dome_pts[:,1].min() + dome_pts[:,1].max()) / 2.0
    cz0 = (dome_pts[:,2].min() + dome_pts[:,2].max()) / 2.0 - 22.0

    def residuals(p):
        cx, cy, cz, r = p
        return np.sqrt((dome_pts[:,0]-cx)**2 +
                       (dome_pts[:,1]-cy)**2 +
                       (dome_pts[:,2]-cz)**2) - r

    res = least_squares(
        residuals,
        [cx0, cy0, cz0, 24.0],
        bounds=([-np.inf, -np.inf, -np.inf, 18.0],
                [ np.inf,  np.inf,  np.inf, 32.0]),
        method='trf'
    )

    cx, cy, cz, r = res.x
    hjc = np.array([cx, cy, cz])
    print(f"HJC: {np.round(hjc,1)}  r={r:.1f}mm")
    return hjc, abs(r)
