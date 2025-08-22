
# -*- coding: utf-8 -*-
"""
GroupGrid widget (PyQt5, Python 3.9.13)
- Uses compiled UI class (no .ui loading at runtime)
- Top-level: QGroupBox with QGridLayout
- 3 fixed rows, 120x120 cells
- Columns adapt to available width
- Populates from resource/data/external_links.json with icons under resource/icons
"""

import sys
import json
from pathlib import Path
from typing import List
from PyQt5 import QtCore, QtGui, QtWidgets, QtNetwork
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QIcon, QResizeEvent
from PyQt5.QtWidgets import QGroupBox, QGridLayout, QToolButton, QSizePolicy, QMainWindow, QWidget, QVBoxLayout
from PyQt5.QtGui import QDesktopServices

from .group_grid_box_ui import Ui_GroupGridBox

CELL_W = 120
CELL_H = 120
ICON_W = 72
ICON_H = 72

class GroupGridWidget(QGroupBox, Ui_GroupGridBox):
    columnsChanged = QtCore.pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)  # from compiled UI
        assert isinstance(self.gridLayout, QGridLayout)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # Fix height to 3 rows
        spacing = self.gridLayout.spacing()
        margins = self.gridLayout.contentsMargins()
        # Add approx title band (style dependent); keep same as ui (24 top margin already accounts for label)
        total_h = (CELL_H * 3) + (spacing * (3 - 1)) + margins.top() + margins.bottom()
        self.setMinimumHeight(total_h)
        self.setMaximumHeight(total_h)

        self._items: List[QtWidgets.QWidget] = []
        self._last_cols = -1

    # ----- Public API -----
    def addItemWidget(self, w: QtWidgets.QWidget):
        w.setMinimumSize(CELL_W, CELL_H)
        w.setMaximumSize(CELL_W, CELL_H)
        w.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self._items.append(w)
        w.setParent(self)
        self._relayout()

    def clearItems(self):
        while self._items:
            w = self._items.pop()
            self.gridLayout.removeWidget(w)
            w.setParent(None)
            w.deleteLater()
        self._last_cols = -1
        self._relayout()

    def load_links_from_json(self, json_path: str, icons_dir: str):
        """Create icon+label toolbuttons from links JSON and add to grid."""
        p = Path(json_path)
        with p.open("r", encoding="utf-8") as f:
            data = json.load(f)
        links = data.get("links", [])
        for item in links:
            btn = self._make_link_button(
                text=item.get("label", ""),
                icon_path=str(Path(icons_dir) / item.get("icon", "")),
                url=item.get("url", "")
            )
            self.addItemWidget(btn)

    # ----- Events -----
    def resizeEvent(self, event: QResizeEvent) -> None:
        super().resizeEvent(event)
        self._relayout()

    # ----- Internal -----
    def _make_link_button(self, text: str, icon_path: str, url: str) -> QToolButton:
        btn = QToolButton()
        btn.setCheckable(False)
        btn.setAutoRaise(False)
        btn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        btn.setText(text or "")
        if icon_path and Path(icon_path).exists():
            btn.setIcon(QIcon(icon_path))
        btn.setIconSize(QtCore.QSize(ICON_W, ICON_H))
        btn.setMinimumSize(CELL_W, CELL_H)
        btn.setMaximumSize(CELL_W, CELL_H)
        btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        if url:
            btn.clicked.connect(lambda _=False, u=url: QDesktopServices.openUrl(QUrl(u)))
        return btn

    def _calc_columns(self) -> int:
        margins = self.gridLayout.contentsMargins()
        spacing = self.gridLayout.spacing()
        avail = max(0, self.width() - margins.left() - margins.right())
        denom = CELL_W + spacing
        if denom <= 0:
            return 1
        cols = max(1, int((avail + spacing) // denom))
        return cols

    def _relayout(self):
        cols = self._calc_columns()
        if cols == self._last_cols and cols > 0:
            return

        # Clear existing placements (do not delete widgets)
        while self.gridLayout.count():
            item = self.gridLayout.takeAt(0)
            if item and item.widget():
                item.widget().hide()

        rows = 3
        for idx, w in enumerate(self._items):
            row = idx % rows
            col = idx // rows
            if col >= cols:
                w.hide()
                continue
            self.gridLayout.addWidget(w, row, col, 1, 1)
            w.show()

        self._last_cols = cols
        self.columnsChanged.emit(cols)

