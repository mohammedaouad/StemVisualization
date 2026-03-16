import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QHBoxLayout,
                              QVBoxLayout, QLabel, QSlider, QFrame,
                              QLineEdit, QPushButton)
from PyQt6.QtCore import Qt

from visualisation import Visualisation
from ui import BG, PANEL_BG, BORDER, ACCENT, TEXT_DIM, TEXT_MED, TEXT_HI, STYLE


class MainWindow(QMainWindow):
    def __init__(self, mesh_path):
        super().__init__()
        self.setWindowTitle("Femoral Stem Planning  ·  FH Aachen")
        self.resize(1800, 960)
        self.setStyleSheet(STYLE)

        self.vis = Visualisation(mesh_path)
        self.ccd_deg = 125.0
        self.frac    = 0.75

        central = QWidget()
        self.setCentralWidget(central)
        root = QHBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # sidebar
        sidebar = QWidget()
        sidebar.setFixedWidth(230)
        sidebar.setStyleSheet(f"background-color: {PANEL_BG}; border-right: 1px solid {BORDER};")
        sb = QVBoxLayout(sidebar)
        sb.setContentsMargins(20, 24, 20, 24)
        sb.setSpacing(6)

        title = QLabel("STEMVIS")
        title.setStyleSheet(f"font-size: 18px; font-weight: 700; letter-spacing: 4px; color: {TEXT_HI};")
        sb.addWidget(title)

        sub = QLabel("Femoral Planning Tool")
        sub.setStyleSheet(f"font-size: 10px; color: {TEXT_DIM}; letter-spacing: 1px; margin-bottom: 16px;")
        sb.addWidget(sub)

        div1 = QFrame()
        div1.setFrameShape(QFrame.Shape.HLine)
        div1.setStyleSheet(f"background-color: {BORDER}; max-height: 1px;")
        sb.addWidget(div1)
        sb.addSpacing(16)

        # CCD angle
        ccd_title = QLabel("CCD ANGLE")
        ccd_title.setObjectName("title")
        sb.addWidget(ccd_title)

        self.ccd_value_lbl = QLabel("125.0")
        self.ccd_value_lbl.setObjectName("value")

        ccd_row = QHBoxLayout()
        ccd_row.addWidget(self.ccd_value_lbl)
        deg_lbl = QLabel("°"); deg_lbl.setObjectName("unit")
        ccd_row.addWidget(deg_lbl)
        ccd_row.addStretch()

        self.ccd_input = QLineEdit("125.0")
        self.ccd_input.setFixedWidth(55)
        self.ccd_input.setStyleSheet(
            f"background:{BORDER}; color:{TEXT_HI}; border:1px solid #2E3F50;"
            f"border-radius:4px; padding:3px 6px; font-family:Consolas; font-size:12px;")
        ccd_row.addWidget(self.ccd_input)

        ccd_btn = QPushButton("↵")
        ccd_btn.setFixedWidth(28)
        ccd_btn.setStyleSheet(
            f"background:{ACCENT}; color:#000; border:none; border-radius:4px; font-size:13px; padding:3px;")
        ccd_btn.clicked.connect(self.on_ccd_input)
        self.ccd_input.returnPressed.connect(self.on_ccd_input)
        ccd_row.addWidget(ccd_btn)
        sb.addLayout(ccd_row)

        self.ccd_slider = QSlider(Qt.Orientation.Horizontal)
        self.ccd_slider.setRange(1150, 1350)
        self.ccd_slider.setValue(1250)
        self.ccd_slider.valueChanged.connect(self.on_ccd_changed)
        sb.addWidget(self.ccd_slider)

        ccd_range = QHBoxLayout()
        lbl_115 = QLabel("115°"); lbl_115.setObjectName("unit")
        lbl_135 = QLabel("135°"); lbl_135.setObjectName("unit")
        ccd_range.addWidget(lbl_115)
        ccd_range.addStretch()
        ccd_range.addWidget(lbl_135)
        sb.addLayout(ccd_range)
        sb.addSpacing(20)

        # resection level
        res_title = QLabel("RESECTION LEVEL")
        res_title.setObjectName("title")
        sb.addWidget(res_title)

        self.frac_value_lbl = QLabel("75")
        self.frac_value_lbl.setObjectName("value")

        frac_row = QHBoxLayout()
        frac_row.addWidget(self.frac_value_lbl)
        neck_lbl = QLabel("% neck"); neck_lbl.setObjectName("unit")
        frac_row.addWidget(neck_lbl)
        frac_row.addStretch()

        self.frac_input = QLineEdit("75")
        self.frac_input.setFixedWidth(55)
        self.frac_input.setStyleSheet(
            f"background:{BORDER}; color:{TEXT_HI}; border:1px solid #2E3F50;"
            f"border-radius:4px; padding:3px 6px; font-family:Consolas; font-size:12px;")
        frac_row.addWidget(self.frac_input)

        frac_btn = QPushButton("↵")
        frac_btn.setFixedWidth(28)
        frac_btn.setStyleSheet(
            f"background:{ACCENT}; color:#000; border:none; border-radius:4px; font-size:13px; padding:3px;")
        frac_btn.clicked.connect(self.on_frac_input)
        self.frac_input.returnPressed.connect(self.on_frac_input)
        frac_row.addWidget(frac_btn)
        sb.addLayout(frac_row)

        self.frac_slider = QSlider(Qt.Orientation.Horizontal)
        self.frac_slider.setRange(20, 80)
        self.frac_slider.setValue(75)
        self.frac_slider.valueChanged.connect(self.on_frac_changed)
        sb.addWidget(self.frac_slider)

        frac_range = QHBoxLayout()
        lbl_20 = QLabel("20%"); lbl_20.setObjectName("unit")
        lbl_80 = QLabel("80%"); lbl_80.setObjectName("unit")
        frac_range.addWidget(lbl_20)
        frac_range.addStretch()
        frac_range.addWidget(lbl_80)
        sb.addLayout(frac_range)
        sb.addSpacing(24)

        div2 = QFrame()
        div2.setFrameShape(QFrame.Shape.HLine)
        div2.setStyleSheet(f"background-color: {BORDER}; max-height: 1px;")
        sb.addWidget(div2)
        sb.addSpacing(16)

        # legend
        leg_title = QLabel("LEGEND")
        leg_title.setObjectName("title")
        sb.addWidget(leg_title)
        sb.addSpacing(8)

        for color, text in [
            ("#7CFC00", "Femoral Head Center"),
            ("#E05A3A", "Stem implant"),
            ("#3A8FD4", "Neck axis"),
            ("#E2E8F0", "Stem Tip"),
            ("#FF8C00", "Stem Toe"),
            ("#00CED1", "Shaft axis"),
            ("#FF8C00", "Resection plane"),
        ]:
            row = QHBoxLayout()
            row.setSpacing(6)
            dot = QLabel("●")
            dot.setStyleSheet(f"color: {color}; font-size: 18px;")
            row.addWidget(dot)
            lbl = QLabel(text); lbl.setObjectName("leg_text")
            row.addWidget(lbl)
            row.addStretch()
            sb.addLayout(row)

        sb.addStretch()
        footer = QLabel("FH AACHEN  ·  Medical Engineering")
        footer.setStyleSheet(f"font-size: 9px; color: {TEXT_DIM}; letter-spacing: 1px;")
        sb.addWidget(footer)
        root.addWidget(sidebar)

        # viewports
        vp = QWidget()
        vp_layout = QHBoxLayout(vp)
        vp_layout.setContentsMargins(0, 0, 0, 0)
        vp_layout.setSpacing(0)
        root.addWidget(vp, stretch=1)

        for plotter, title_text in [
            (self.vis.pl_left,  "  PRE-OP  ·  Full Femur"),
            (self.vis.pl_right, "  POST-RESECTION  ·  Resected Femur"),
        ]:
            frame = QWidget()
            fl = QVBoxLayout(frame)
            fl.setContentsMargins(0, 0, 0, 0)
            fl.setSpacing(0)
            pt = QLabel(title_text)
            pt.setObjectName("panel_title")
            pt.setAlignment(Qt.AlignmentFlag.AlignCenter)
            fl.addWidget(pt)
            fl.addWidget(plotter.app_window)
            vp_layout.addWidget(frame, stretch=1)
            if plotter is self.vis.pl_left:
                sep = QFrame()
                sep.setObjectName("separator")
                sep.setFrameShape(QFrame.Shape.VLine)
                vp_layout.addWidget(sep)

        self.vis.update(self.ccd_deg, self.frac)

    def on_ccd_changed(self, val):
        self.ccd_deg = val / 10.0
        self.ccd_value_lbl.setText(f"{self.ccd_deg:.1f}")
        self.ccd_input.setText(f"{self.ccd_deg:.1f}")
        self.vis.update(self.ccd_deg, self.frac)

    def on_frac_changed(self, val):
        self.frac = val / 100.0
        self.frac_value_lbl.setText(str(val))
        self.frac_input.setText(str(val))
        self.vis.update(self.ccd_deg, self.frac)

    def on_ccd_input(self):
        try:
            val = max(115.0, min(135.0, float(self.ccd_input.text())))
            self.ccd_slider.setValue(int(val * 10))
        except ValueError:
            pass

    def on_frac_input(self):
        try:
            val = max(20, min(80, int(self.frac_input.text())))
            self.frac_slider.setValue(val)
        except ValueError:
            pass


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    win = MainWindow("X:/StemVis/Data/Femur_Bone.stl")
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()