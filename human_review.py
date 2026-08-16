import json
import sys
from pathlib import Path

QUEUE_FILE = Path(__file__).resolve().parent.parent / "review_queue.json"


def load_queue():
    if QUEUE_FILE.exists():
        return json.loads(QUEUE_FILE.read_text())
    return {}


def save_queue(queue):
    QUEUE_FILE.write_text(json.dumps(queue, indent=2))


def submit(section_id, text):
    queue = load_queue()
    queue[section_id] = {"status": "pending", "text": text, "note": None}
    save_queue(queue)


def approve(section_id):
    queue = load_queue()
    if section_id not in queue:
        print("no such section:", section_id)
        return
    queue[section_id]["status"] = "approved"
    save_queue(queue)
    print("approved:", section_id)


def flag(section_id, note=""):
    queue = load_queue()
    if section_id not in queue:
        print("no such section:", section_id)
        return
    queue[section_id]["status"] = "flagged"
    queue[section_id]["note"] = note
    save_queue(queue)
    print("flagged:", section_id, "-", note)


def list_queue():
    queue = load_queue()
    if not queue:
        print("queue is empty")
        return
    for section_id, item in queue.items():
        print(f"[{item['status']}] {section_id}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: python human_review.py list|approve|flag <section_id> [note]")
        sys.exit(0)

    cmd = sys.argv[1]
    if cmd == "list":
        list_queue()
    elif cmd == "approve":
        approve(sys.argv[2])
    elif cmd == "flag":
        flag(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "")