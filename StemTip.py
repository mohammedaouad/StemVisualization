import numpy as np

# StemToe is fixed at C1 (proximal shaft slice).
# StemTip is found by scanning up the shaft axis until the angle
# between (tip->HJC) and (tip->toe) matches the target CCD angle.

def compute_stem_points(vertices, axis_origin, axis_dir, hjc, ccd_deg, c1):
    d = axis_dir / np.linalg.norm(axis_dir)
    toe = c1

    cos_ccd = np.cos(np.deg2rad(ccd_deg))
    t_toe   = np.dot(toe - axis_origin, d)

    best_t    = t_toe + 100
    best_diff = 999.0

    for t in np.linspace(t_toe, t_toe + 300, 20000):
        tip_c = axis_origin + t * d
        v1 = hjc - tip_c
        v2 = toe - tip_c
        n1, n2 = np.linalg.norm(v1), np.linalg.norm(v2)
        if n1 < 1e-6 or n2 < 1e-6:
            continue
        cos_a = np.clip(np.dot(v1, v2) / (n1 * n2), -1, 1)
        diff  = abs(cos_a - cos_ccd)
        if diff < best_diff:
            best_diff = diff
            best_t    = t

    tip = axis_origin + best_t * d

    # check achieved angle
    v1 = hjc - tip
    v2 = toe - tip
    achieved = np.degrees(np.arccos(
        np.clip(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)), -1, 1)
    ))

    print(f"StemTip: tip={np.round(tip,1)}  length={np.linalg.norm(tip-toe):.1f}mm  CCD={achieved:.1f}°")
    return tip, toe
