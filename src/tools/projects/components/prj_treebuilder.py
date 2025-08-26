from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt

ROLE_TYPE = Qt.UserRole + 1
ROLE_ID   = Qt.UserRole + 2

def make_item(text: str, node_type: str, node_id: str) -> QStandardItem:
    it = QStandardItem(text)
    it.setEditable(False)
    it.setData(node_type, ROLE_TYPE)
    it.setData(node_id, ROLE_ID)
    return it

def build_tree_model(data_model):
    # Root model with two top-level buckets: 진행 중 / 완료
    model = QStandardItemModel()
    model.setHorizontalHeaderLabels(["Projects"])

    buckets = {
        "in_progress": make_item("🟢 진행 중", "status_root", "in_progress"),
        "completed":   make_item("🔴 완료",   "status_root", "completed"),
    }
    for b in buckets.values():
        model.appendRow(b)

    # group wrappers by status
    wrappers_by_status = {"in_progress": [], "completed": []}
    for w in data_model.wrappers:
        wrappers_by_status[w.status].append(w)

    # map wrapper id to item per status
    wrapper_items = {}

    for status_key, bucket_item in buckets.items():
        # wrappers
        for w in wrappers_by_status[status_key]:
            w_item = make_item("📚" + w.name, "wrapper", w.id)
            bucket_item.appendRow(w_item)
            wrapper_items[w.id] = w_item
        # loose projects under the status bucket (no wrapper)
        for p in [p for p in data_model.projects if p.status == status_key and not p.wrapper_id]:
            if p.status == 'in_progress':
                p_item = make_item("📗" + p.name, "project", p.id)
            else:
                p_item = make_item("📕" + p.name, "project", p.id)
            bucket_item.appendRow(p_item)

    # attach projects under wrappers
    for p in data_model.projects:
        if p.wrapper_id:
            parent = wrapper_items.get(p.wrapper_id)
            if parent is not None:
                if p.status == 'in_progress':
                    parent.appendRow(make_item("📗" + p.name, "project", p.id))
                else:
                    parent.appendRow(make_item("📕" + p.name, "project", p.id))

    return model
