import numpy as np
import pyvista as pv
from pyvistaqt import BackgroundPlotter

from HJC           import compute_hjc
from StemAxis      import compute_shaft_axis
from StemTip       import compute_stem_points
from ResectedFemur import compute_resection_plane, resect_femur_mesh, make_resection_disk

BG       = "#080C10"
BONE     = "#C49A2A"
STEM_COL = "#E05A3A"
NECK_COL = "#3A8FD4"
LIME     = "#7CFC00"
ORANGE   = "#FF8C00"


def align_to_z(mesh, vertices):
    centered = vertices - vertices.mean(axis=0)
    _, _, Vt = np.linalg.svd(centered, full_matrices=False)
    long_axis = Vt[0]
    if long_axis[2] < 0:
        long_axis = -long_axis
    z_axis = np.array([0, 0, 1.0])
    v = np.cross(long_axis, z_axis)
    s = np.linalg.norm(v)
    c = np.dot(long_axis, z_axis)
    if s < 1e-6:
        return mesh, vertices
    vx = np.array([[0,-v[2],v[1]],[v[2],0,-v[0]],[-v[1],v[0],0]])
    R  = np.eye(3) + vx + vx @ vx * ((1 - c) / (s ** 2))
    new_vertices = (R @ vertices.T).T
    mesh = mesh.rotate_vector(vector=v.tolist(),
                              angle=np.degrees(np.arcsin(s)), inplace=False)
    return mesh, new_vertices


def add_landmarks(pl, hjc, head_radius, axis_dir, c1, c2):
    pl.add_mesh(pv.Sphere(radius=head_radius, center=hjc.tolist()),
                color="#CC2200", opacity=0.10, render=False)
    pl.add_mesh(pv.Sphere(radius=head_radius, center=hjc.tolist()),
                color="#FF4422", opacity=0.25, style="wireframe", render=False)
    pl.add_mesh(pv.Sphere(radius=3.5, center=hjc.tolist()),
                color=LIME, render=False)
    pl.add_point_labels([hjc.tolist()], ["HJC"],
        font_size=9, text_color=LIME, always_visible=True,
        shape_opacity=0.0, render=False)
    pl.add_mesh(pv.Line((c1 - axis_dir*15).tolist(), (c2 + axis_dir*15).tolist()),
                color="#00CED1", line_width=1, opacity=0.4, render=False)
    for pt, label in [(c1, "C1"), (c2, "C2")]:
        pl.add_mesh(pv.Sphere(radius=2.0, center=pt.tolist()),
                    color="white", opacity=0.5, render=False)
        pl.add_point_labels([pt.tolist()], [label],
            font_size=8, text_color="#555555", always_visible=True,
            shape_opacity=0.0, render=False)


class Visualisation:
    """Handles all 3D rendering — two BackgroundPlotters, left and right."""

    def __init__(self, mesh_path):
        # load and process
        mesh = pv.read(mesh_path).clean()
        cx = (mesh.bounds[0] + mesh.bounds[1]) / 2
        cy = (mesh.bounds[2] + mesh.bounds[3]) / 2
        cz = (mesh.bounds[4] + mesh.bounds[5]) / 2
        mesh     = mesh.translate(-np.array([cx, cy, cz]), inplace=False)
        vertices = np.array(mesh.points)
        mesh, vertices = align_to_z(mesh, vertices)

        self.mesh        = mesh
        self.vertices    = vertices
        self.hjc, self.head_radius          = compute_hjc(vertices)
        self.axis_origin, self.axis_dir, \
            self.c1, self.c2, _, _          = compute_shaft_axis(vertices)

        # create the two plotters
        self.pl_left  = BackgroundPlotter(show=False)
        self.pl_right = BackgroundPlotter(show=False)
        self.pl_left.set_background(BG)
        self.pl_right.set_background(BG)

        self._init_left()
        self._init_right()

        self.L = {"stem": None, "neck": None, "tip": None, "toe": None,
                  "tip_lbl": None, "toe_lbl": None}
        self.R = {"stem": None, "neck": None, "tip": None, "toe": None,
                  "tip_lbl": None, "toe_lbl": None,
                  "cut": None, "cut_wire": None, "disk": None, "dot": None}

    def _init_left(self):
        self.pl_left.add_mesh(self.mesh, color=BONE, style="wireframe", opacity=0.055)
        add_landmarks(self.pl_left, self.hjc, self.head_radius,
                      self.axis_dir, self.c1, self.c2)
        self.pl_left.add_axes(xlabel="R", ylabel="A", zlabel="S",
                              color="#333333", label_size=(0.06, 0.06))
        self.pl_left.view_isometric()
        self.pl_left.reset_camera()

    def _init_right(self):
        add_landmarks(self.pl_right, self.hjc, self.head_radius,
                      self.axis_dir, self.c1, self.c2)
        self.pl_right.add_axes(xlabel="R", ylabel="A", zlabel="S",
                               color="#333333", label_size=(0.06, 0.06))
        self.pl_right.view_isometric()
        self.pl_right.reset_camera()

    def update(self, ccd_deg, frac):
        cam_right = self.pl_right.camera.copy()

        tip, toe = compute_stem_points(
            self.vertices, self.axis_origin, self.axis_dir,
            self.hjc, ccd_deg, self.c1)

        neck_vec    = self.hjc - tip
        neck_len    = float(np.linalg.norm(neck_vec))
        neck_center = ((tip + self.hjc) / 2).tolist()
        neck_dir    = (neck_vec / neck_len).tolist()
        stem_len    = float(np.linalg.norm(tip - toe))
        stem_center = ((tip + toe) / 2).tolist()

        # left panel
        for a in self.L.values():
            if a is not None: self.pl_left.remove_actor(a)

        self.L["stem"] = self.pl_left.add_mesh(
            pv.Cylinder(center=stem_center, direction=self.axis_dir.tolist(),
                        radius=2.5, height=stem_len, resolution=40, capping=True),
            color=STEM_COL, smooth_shading=True)
        self.L["neck"] = self.pl_left.add_mesh(
            pv.Cylinder(center=neck_center, direction=neck_dir,
                        radius=2.5, height=neck_len, resolution=40, capping=True),
            color=NECK_COL, smooth_shading=True)
        self.L["tip"] = self.pl_left.add_mesh(
            pv.Sphere(radius=4.5, center=tip.tolist()), color="white")
        self.L["toe"] = self.pl_left.add_mesh(
            pv.Sphere(radius=4.5, center=toe.tolist()), color=ORANGE)
        self.L["tip_lbl"] = self.pl_left.add_point_labels(
            [tip.tolist()], ["  Stem Tip"], font_size=8,
            text_color="#888888", always_visible=True, shape_opacity=0.0)
        self.L["toe_lbl"] = self.pl_left.add_point_labels(
            [toe.tolist()], ["  Stem Toe"], font_size=8,
            text_color="#AA6600", always_visible=True, shape_opacity=0.0)

        # right panel
        for a in self.R.values():
            if a is not None: self.pl_right.remove_actor(a)

        self.R["stem"] = self.pl_right.add_mesh(
            pv.Cylinder(center=stem_center, direction=self.axis_dir.tolist(),
                        radius=2.5, height=stem_len, resolution=40, capping=True),
            color=STEM_COL, smooth_shading=True)
        self.R["neck"] = self.pl_right.add_mesh(
            pv.Cylinder(center=neck_center, direction=neck_dir,
                        radius=2.5, height=neck_len, resolution=40, capping=True),
            color=NECK_COL, smooth_shading=True)
        self.R["tip"] = self.pl_right.add_mesh(
            pv.Sphere(radius=4.5, center=tip.tolist()), color="white")
        self.R["toe"] = self.pl_right.add_mesh(
            pv.Sphere(radius=4.5, center=toe.tolist()), color=ORANGE)
        self.R["tip_lbl"] = self.pl_right.add_point_labels(
            [tip.tolist()], ["  Stem Tip"], font_size=8,
            text_color="#888888", always_visible=True, shape_opacity=0.0)
        self.R["toe_lbl"] = self.pl_right.add_point_labels(
            [toe.tolist()], ["  Stem Toe"], font_size=8,
            text_color="#AA6600", always_visible=True, shape_opacity=0.0)

        res_pt, res_norm, _ = compute_resection_plane(
            tip, self.hjc, fraction=frac)
        cut = resect_femur_mesh(self.mesh, res_pt, res_norm, self.c1)

        self.R["cut"]      = self.pl_right.add_mesh(
            cut, color=BONE, opacity=0.3, smooth_shading=True)
        self.R["cut_wire"] = self.pl_right.add_mesh(
            cut, color=BONE, style="wireframe", opacity=0.055)

        disk = make_resection_disk(res_pt, res_norm, radius=18.0)
        self.R["disk"] = self.pl_right.add_mesh(
            disk, color=ORANGE, opacity=0.8, style="wireframe", line_width=1.5)
        self.R["dot"] = self.pl_right.add_mesh(
            pv.Sphere(radius=3.0, center=res_pt.tolist()), color=ORANGE)

        # restore right camera
        self.pl_right.camera = cam_right