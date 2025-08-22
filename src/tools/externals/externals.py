# -*- coding: utf-8 -*-
"""
Externals implementation using compiled UI and two GroupGrid widgets.

Requirements:
- Python 3.9.13
- PyQt5
- components/links.py: provides GroupGrid with API:
    - load_links_from_json(json_path: str, icons_dir: str) -> None
    - setTitle(str) -> None
"""

from pathlib import Path
from PyQt5.QtWidgets import QWidget, QSizePolicy

# compiled UI
from .externals_ui import Ui_Externals  # rename your generated file to externals_ui.py or adjust import path
# GroupGrid component
from .components.group_grid_box import GroupGridWidget


class ExternalsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.ui = Ui_Externals()
        self.ui.setupUi(self)

        # ----- resource path resolve -----
        base = Path(__file__).resolve().parents[3]  # repo root heuristic: .../src/tools/externals/externals.py -> up 3
        default_json = base / "resources" / "data" / "external_links.json"
        default_icons = base / "resources" / "icons"

        self._json_path = str(default_json)
        self._icons_dir = str(default_icons)

        # ----- grids -----
        self.grid_top = GroupGridWidget(self)
        self.grid_bottom = GroupGridWidget(self)

        self.grid_top.setTitle("자주 쓰는 링크")
        self.grid_bottom.setTitle("프로젝트/릴리즈 링크")

        # size policy: horizontal expanding, vertical fixed height per GroupGrid 설계(3행)
        spx = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.grid_top.setSizePolicy(spx)
        self.grid_bottom.setSizePolicy(spx)

        # add to UI layout (compiled: self.main_layout)
        # 체크리스트 레이아웃 가져오기
                
        self.ui.main_layout.addWidget(self.grid_top)
        self.ui.main_layout.addWidget(self.grid_bottom)

        # spacing between the two grids is already controlled by main_layout.spacing()

        # load links into each grid (동일 JSON 사용; 필요 시 필터링 로직으로 대체 가능)
        self._load_links()

        # resize propagation
        self.setMinimumWidth(600)

    # ----- internals -----
    def _load_links(self):
        # 기본 동작: 동일 데이터 세트를 두 그리드에 로드
        # 필터가 필요하면 이 지점에서 id/label 기준으로 분기하여 addItemWidget 수행
        self.grid_top.clearItems()
        self.grid_bottom.clearItems()
        self.grid_top.load_links_from_json(self._json_path, self._icons_dir)
        self.grid_bottom.load_links_from_json(self._json_path, self._icons_dir)