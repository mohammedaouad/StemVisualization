import numpy as np
import pyvista as pv

# Resection plane placed at a fraction along the neck (StemTip -> HJC).
# Default 3/4 of neck length, same as MATLAB reference.


def compute_resection_plane(stem_tip, hjc, fraction=0.75):
    neck_vec    = hjc - stem_tip
    neck_length = np.linalg.norm(neck_vec)
    normal      = neck_vec / neck_length  # points toward HJC

    res_point = stem_tip + fraction * neck_length * normal
    print(f"Resection: neck={neck_length:.1f}mm  point={np.round(res_point,1)}")
    return res_point, normal, neck_length


def resect_femur_mesh(mesh, resection_point, plane_normal, shaft_point):
    # Manual face filtering — same logic as the MATLAB code.
    # Keep only faces where ALL vertices are on the shaft side of the plane.
    # Shaft side = opposite direction to plane_normal (which points to HJC).

    vertices = np.array(mesh.points)
    faces_raw = mesh.faces.reshape(-1, 4)[:, 1:]  # strip the leading "3"

    # signed distance of every vertex from the resection plane
    # negative = shaft side, positive = head side
    signed_dist = (vertices - resection_point) @ plane_normal

    # verify shaft_point is negative (shaft side)
    sd_shaft = np.dot(shaft_point - resection_point, plane_normal)
    print(f"Resection: shaft_point signed_dist={sd_shaft:.1f} (should be negative)")

    if sd_shaft > 0:
        # normal is pointing wrong way — flip it
        print("Resection: flipping normal direction")
        signed_dist = -signed_dist

    # keep faces where ALL 3 vertices have signed_dist <= 0 (shaft side)
    keep = np.all(signed_dist[faces_raw] <= 0, axis=1)
    kept_faces = faces_raw[keep]

    print(f"Resection: kept {keep.sum()}/{len(faces_raw)} faces ({100*keep.sum()/len(faces_raw):.1f}%)")

    # rebuild clean mesh from kept faces
    used_idx = np.unique(kept_faces)
    new_verts = vertices[used_idx]

    # remap face indices
    remap = np.zeros(len(vertices), dtype=int)
    remap[used_idx] = np.arange(len(used_idx))
    new_faces = remap[kept_faces]

    # convert to pyvista format (prepend 3 for each triangle)
    pv_faces = np.hstack([np.full((len(new_faces), 1), 3), new_faces]).ravel()

    cut_mesh = pv.PolyData(new_verts, pv_faces)
    return cut_mesh


def make_resection_disk(resection_point, plane_normal, radius=20.0, n_pts=60):
    n = plane_normal / np.linalg.norm(plane_normal)
    perp = np.array([1.0, 0.0, 0.0]) if abs(n[0]) < 0.9 else np.array([0.0, 1.0, 0.0])

    u = np.cross(n, perp);  u /= np.linalg.norm(u)
    v = np.cross(n, u);     v /= np.linalg.norm(v)

    theta  = np.linspace(0, 2 * np.pi, n_pts, endpoint=False)
    circle = (resection_point
              + radius * np.outer(np.cos(theta), u)
              + radius * np.outer(np.sin(theta), v))

    faces = np.hstack([[n_pts], np.arange(n_pts)])
    return pv.PolyData(circle, faces)