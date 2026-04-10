"""
XYZtech DMAIC Tracker - Flask web app for collaborative project tracking.

Run with:     python app.py
Then open:    http://localhost:5000

Uploads are stored in ../5. XYZ Data/<Phase>/<Substep>/<Tool>/<filename>
so the team can find attached files directly in the folder tree as well.
"""
import os
import re
import shutil
import sqlite3
from datetime import datetime
from flask import Flask, request, jsonify, render_template, send_from_directory, abort
from werkzeug.utils import secure_filename

from seed_data import TOOLS, TEAM_MEMBERS, INITIAL_ATTACHMENTS

APP_DIR = os.path.dirname(os.path.abspath(__file__))                    # .../4. XYZ App
PROJECT_ROOT = os.path.dirname(APP_DIR)                                 # .../xyztech-dmaic
DB_PATH = os.path.join(APP_DIR, "data.db")
UPLOAD_DIR = os.path.join(PROJECT_ROOT, "5. XYZ Data")                  # New upload root

os.makedirs(UPLOAD_DIR, exist_ok=True)

MAX_FILE_SIZE = 64 * 1024 * 1024  # 64 MB

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = MAX_FILE_SIZE

PHASE_NUM = {"DEFINE": 1, "MEASURE": 2, "ANALYZE": 3, "IMPROVE": 4, "CONTROL": 5}
PHASE_TITLE = {"DEFINE": "Define", "MEASURE": "Measure", "ANALYZE": "Analyze", "IMPROVE": "Improve", "CONTROL": "Control"}


def sanitize_fs(name):
    """Replace characters invalid in Windows filenames."""
    s = re.sub(r'[<>:"/\\|?*]', "_", str(name)).strip()
    return s.rstrip(". ")


def tool_folder(tool_row):
    """Build the upload folder path for a given tool."""
    phase = tool_row["phase"]
    phase_folder = f"{PHASE_NUM[phase]}. {PHASE_TITLE[phase]}"
    substep_folder = sanitize_fs(f"{tool_row['substep_code']} {tool_row['substep_title']}")
    tool_name_folder = sanitize_fs(tool_row["tool_name"])
    return os.path.join(UPLOAD_DIR, phase_folder, substep_folder, tool_name_folder)


def unique_filename(folder, filename):
    base, ext = os.path.splitext(filename)
    candidate = filename
    n = 2
    while os.path.exists(os.path.join(folder, candidate)):
        candidate = f"{base}_{n}{ext}"
        n += 1
    return candidate


def relpath_from_upload_dir(abs_path):
    return os.path.relpath(abs_path, UPLOAD_DIR).replace("\\", "/")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS tools (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phase TEXT NOT NULL,
            substep_code TEXT NOT NULL,
            substep_title TEXT NOT NULL,
            tool_name TEXT NOT NULL,
            tool_desc TEXT,
            questions TEXT,
            status TEXT DEFAULT 'todo',
            assignee TEXT DEFAULT 'Unassigned',
            notes TEXT DEFAULT '',
            updated_at TEXT,
            updated_by TEXT DEFAULT ''
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS activity_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tool_id INTEGER,
            user TEXT,
            field TEXT,
            old_value TEXT,
            new_value TEXT,
            timestamp TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS uploads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tool_id INTEGER NOT NULL,
            original_name TEXT NOT NULL,
            stored_name TEXT NOT NULL,
            size INTEGER,
            mime_type TEXT,
            uploaded_by TEXT,
            uploaded_at TEXT,
            FOREIGN KEY (tool_id) REFERENCES tools(id)
        )
    """)

    c.execute("SELECT COUNT(*) FROM tools")
    is_fresh = c.fetchone()[0] == 0

    if is_fresh:
        now = datetime.utcnow().isoformat()
        for t in TOOLS:
            c.execute("""
                INSERT INTO tools
                (phase, substep_code, substep_title, tool_name, tool_desc, questions, status, notes, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (t[0], t[1], t[2], t[3], t[4], t[5], t[6], t[7], now))
        conn.commit()
        print(f"Seeded {len(TOOLS)} tools.")

        # Attach existing files from INITIAL_ATTACHMENTS
        # Relative paths are resolved from APP_DIR (so seed_files/ ships with the app)
        attached = 0
        for src, phase, substep_code, tool_name in INITIAL_ATTACHMENTS:
            if not os.path.isabs(src):
                src = os.path.normpath(os.path.join(APP_DIR, src))
            if not os.path.exists(src):
                print(f"  [skip] Missing source: {src}")
                continue

            tool = c.execute(
                "SELECT * FROM tools WHERE phase = ? AND substep_code = ? AND tool_name = ?",
                (phase, substep_code, tool_name),
            ).fetchone()
            if not tool:
                print(f"  [skip] No tool match: {phase}/{substep_code}/{tool_name}")
                continue

            folder = tool_folder(tool)
            os.makedirs(folder, exist_ok=True)
            filename = unique_filename(folder, os.path.basename(src))
            dst = os.path.join(folder, filename)
            shutil.copy2(src, dst)

            size = os.path.getsize(dst)
            ext = os.path.splitext(filename)[1].lower().lstrip(".")
            mime_map = {
                "pdf": "application/pdf",
                "png": "image/png",
                "jpg": "image/jpeg",
                "jpeg": "image/jpeg",
                "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                "pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
            }
            mime_type = mime_map.get(ext, "application/octet-stream")

            rel_stored = relpath_from_upload_dir(dst)
            c.execute(
                """INSERT INTO uploads
                   (tool_id, original_name, stored_name, size, mime_type, uploaded_by, uploaded_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (tool["id"], os.path.basename(src), rel_stored, size, mime_type, "Initial Seed", now),
            )
            attached += 1
        conn.commit()
        print(f"Attached {attached} initial files.")

    conn.close()


def get_uploads_for_tool(conn, tool_id):
    rows = conn.execute(
        "SELECT * FROM uploads WHERE tool_id = ? ORDER BY uploaded_at DESC",
        (tool_id,),
    ).fetchall()
    return [dict(r) for r in rows]


@app.route("/")
def index():
    return render_template("index.html", team_members=TEAM_MEMBERS)


@app.route("/api/tools")
def api_tools():
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM tools ORDER BY phase, substep_code, id"
    ).fetchall()
    tools_list = []
    for r in rows:
        tool = dict(r)
        tool["uploads"] = get_uploads_for_tool(conn, tool["id"])
        tools_list.append(tool)
    conn.close()
    return jsonify(tools_list)


@app.route("/api/tools/<int:tool_id>", methods=["POST"])
def update_tool(tool_id):
    data = request.get_json() or {}
    user = data.get("user", "Unknown")

    conn = get_db()
    current = conn.execute("SELECT * FROM tools WHERE id = ?", (tool_id,)).fetchone()
    if not current:
        conn.close()
        return jsonify({"error": "Tool not found"}), 404

    updates = []
    params = []
    log_entries = []
    for field in ("status", "assignee", "notes"):
        if field in data and data[field] != current[field]:
            updates.append(f"{field} = ?")
            params.append(data[field])
            log_entries.append((tool_id, user, field, current[field], data[field]))

    if updates:
        now = datetime.utcnow().isoformat()
        updates.extend(["updated_at = ?", "updated_by = ?"])
        params.extend([now, user, tool_id])
        conn.execute(
            f"UPDATE tools SET {', '.join(updates)} WHERE id = ?",
            params,
        )
        for entry in log_entries:
            conn.execute(
                "INSERT INTO activity_log (tool_id, user, field, old_value, new_value, timestamp) VALUES (?, ?, ?, ?, ?, ?)",
                (*entry, now),
            )
        conn.commit()

    updated = dict(conn.execute("SELECT * FROM tools WHERE id = ?", (tool_id,)).fetchone())
    updated["uploads"] = get_uploads_for_tool(conn, tool_id)
    conn.close()
    return jsonify(updated)


@app.route("/api/tools/<int:tool_id>/upload", methods=["POST"])
def upload_file(tool_id):
    """Attach a file to a tool."""
    conn = get_db()
    tool = conn.execute("SELECT * FROM tools WHERE id = ?", (tool_id,)).fetchone()
    if not tool:
        conn.close()
        return jsonify({"error": "Tool not found"}), 404

    if "file" not in request.files:
        conn.close()
        return jsonify({"error": "No file in request"}), 400

    file = request.files["file"]
    if not file or file.filename == "":
        conn.close()
        return jsonify({"error": "No file selected"}), 400

    user = request.form.get("user", "Unknown")
    original_name = file.filename
    safe_base = secure_filename(original_name) or "file"

    folder = tool_folder(tool)
    os.makedirs(folder, exist_ok=True)
    filename = unique_filename(folder, safe_base)
    stored_path = os.path.join(folder, filename)
    file.save(stored_path)

    size = os.path.getsize(stored_path)
    mime_type = file.mimetype or "application/octet-stream"
    now = datetime.utcnow().isoformat()

    rel_stored = relpath_from_upload_dir(stored_path)
    cursor = conn.execute(
        """INSERT INTO uploads (tool_id, original_name, stored_name, size, mime_type, uploaded_by, uploaded_at)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (tool_id, original_name, rel_stored, size, mime_type, user, now),
    )
    upload_id = cursor.lastrowid

    conn.execute(
        "INSERT INTO activity_log (tool_id, user, field, old_value, new_value, timestamp) VALUES (?, ?, ?, ?, ?, ?)",
        (tool_id, user, "upload", "", original_name, now),
    )
    conn.execute(
        "UPDATE tools SET updated_at = ?, updated_by = ? WHERE id = ?",
        (now, user, tool_id),
    )
    conn.commit()

    row = conn.execute("SELECT * FROM uploads WHERE id = ?", (upload_id,)).fetchone()
    conn.close()
    return jsonify(dict(row))


@app.route("/api/uploads/<int:upload_id>")
def download_file(upload_id):
    """Serve an uploaded file for download/preview."""
    conn = get_db()
    row = conn.execute("SELECT * FROM uploads WHERE id = ?", (upload_id,)).fetchone()
    conn.close()
    if not row:
        abort(404)
    rel = row["stored_name"].replace("/", os.sep)
    abs_path = os.path.join(UPLOAD_DIR, rel)
    if not os.path.exists(abs_path):
        abort(404)
    directory = os.path.dirname(abs_path)
    filename = os.path.basename(abs_path)
    return send_from_directory(
        directory,
        filename,
        as_attachment=False,
        download_name=row["original_name"],
    )


@app.route("/api/uploads/<int:upload_id>", methods=["DELETE"])
def delete_file(upload_id):
    user = request.args.get("user", "Unknown")
    conn = get_db()
    row = conn.execute("SELECT * FROM uploads WHERE id = ?", (upload_id,)).fetchone()
    if not row:
        conn.close()
        return jsonify({"error": "Not found"}), 404

    rel = row["stored_name"].replace("/", os.sep)
    abs_path = os.path.join(UPLOAD_DIR, rel)
    if os.path.exists(abs_path):
        try:
            os.remove(abs_path)
        except OSError:
            pass

    now = datetime.utcnow().isoformat()
    conn.execute("DELETE FROM uploads WHERE id = ?", (upload_id,))
    conn.execute(
        "INSERT INTO activity_log (tool_id, user, field, old_value, new_value, timestamp) VALUES (?, ?, ?, ?, ?, ?)",
        (row["tool_id"], user, "upload_delete", row["original_name"], "", now),
    )
    conn.execute(
        "UPDATE tools SET updated_at = ?, updated_by = ? WHERE id = ?",
        (now, user, row["tool_id"]),
    )
    conn.commit()
    conn.close()
    return jsonify({"ok": True})


@app.route("/api/stats")
def api_stats():
    conn = get_db()
    rows = conn.execute(
        "SELECT phase, status, COUNT(*) as c FROM tools GROUP BY phase, status"
    ).fetchall()

    phase_order = ["DEFINE", "MEASURE", "ANALYZE", "IMPROVE", "CONTROL"]
    result = {p: {"done": 0, "partial": 0, "todo": 0, "total": 0} for p in phase_order}
    for r in rows:
        phase = r["phase"]
        if phase in result:
            result[phase][r["status"]] = r["c"]
            result[phase]["total"] += r["c"]

    assignee_rows = conn.execute(
        "SELECT assignee, COUNT(*) as c FROM tools GROUP BY assignee"
    ).fetchall()
    assignees = {r["assignee"]: r["c"] for r in assignee_rows}

    log_rows = conn.execute(
        """SELECT al.*, t.tool_name, t.substep_code
           FROM activity_log al JOIN tools t ON al.tool_id = t.id
           ORDER BY al.timestamp DESC LIMIT 10"""
    ).fetchall()
    activity = [dict(r) for r in log_rows]

    conn.close()
    return jsonify({
        "phases": result,
        "assignees": assignees,
        "recent_activity": activity,
    })


@app.route("/api/reset", methods=["POST"])
def api_reset():
    """Reset the database to initial seed state."""
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    init_db()
    return jsonify({"ok": True, "message": "Database reset to initial seed."})


@app.errorhandler(413)
def too_large(e):
    return jsonify({"error": f"File too large (max {MAX_FILE_SIZE // (1024*1024)} MB)"}), 413


if __name__ == "__main__":
    init_db()
    print("\n" + "=" * 60)
    print("  XYZtech DMAIC Tracker")
    print("=" * 60)
    print(f"  Upload dir: {UPLOAD_DIR}")
    print("  Open in browser: http://localhost:5000")
    print("  Team LAN access: http://<your-ip>:5000")
    print("  Press Ctrl+C to stop")
    print("=" * 60 + "\n")
    app.run(host="0.0.0.0", port=5000, debug=False)
