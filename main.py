"""
    author: hoaquangthang
    project: a_seed_backend
"""
from __future__ import annotations

import os
import sys
import json
import time
import uuid
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional
import math
import asyncio
import tempfile

import requests
import psutil
from flask import (
    Flask, request, jsonify, session, g, redirect, make_response, render_template
)
from werkzeug.security import generate_password_hash, check_password_hash

# --- Config & Init ---
try:
    import edge_tts
    EDGE_TTS_AVAILABLE = True
except ImportError:
    EDGE_TTS_AVAILABLE = False
    print("Warning: edge-tts not installed")

try:
    import pynvml
    pynvml.nvmlInit()
    NVML_AVAILABLE = True
except Exception:
    NVML_AVAILABLE = False

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
SESS_DIR = DATA_DIR / "sessions"
STATIC_DIR = BASE_DIR / "static"
TRAIN_DIR = BASE_DIR / "training"
USERS_FILE = DATA_DIR / "users.json"
MEM_DIR = DATA_DIR / "memories"

for d in (DATA_DIR, SESS_DIR, MEM_DIR):
    d.mkdir(parents=True, exist_ok=True)

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-oss:120b-cloud")
EMBED_MODEL = os.getenv("EMBED_MODEL", "nomic-embed-text") 
NUM_CTX = int(os.getenv("NUM_CTX", "4096"))
GEN_TEMP = float(os.getenv("GEN_TEMP", "0.7"))
TOP_P = float(os.getenv("TOP_P", "0.9"))

ADMIN_USER = os.getenv("ADMIN_USER", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")
SECRET_KEY = os.getenv("SECRET_KEY", "a-seed-secret-key-dev")

app = Flask(__name__, static_folder=str(STATIC_DIR), template_folder='templates')
app.secret_key = SECRET_KEY
app.config.update(SESSION_COOKIE_SAMESITE='Lax', SESSION_COOKIE_SECURE=False)

START_TS = time.time()

# --- Helpers ---
def now_ts(): return int(time.time())
def read_users(): return json.load(USERS_FILE.open("r", encoding="utf-8")) if USERS_FILE.exists() else {}
def write_users(u): json.dump(u, USERS_FILE.open("w", encoding="utf-8"), indent=2)
def safe_json(s): 
    try: return json.loads(re.search(r"\{.*\}", s, re.DOTALL).group(0))
    except: return {}
def ensure_sid(sid): return sid or str(uuid.uuid4())

def get_user_session_dir():
    uid = session.get('user_id')
    if not uid: return None
    d = SESS_DIR / re.sub(r'[^\w-]', '', uid)
    d.mkdir(exist_ok=True)
    return d

def session_path(sid):
    d = get_user_session_dir()
    return (d / f"{re.sub(r'[^\w-]', '', sid)}.json") if d else None

def write_json(p, o):
    if p:
        json.dump(o, p.with_suffix(".tmp").open("w", encoding="utf-8"), ensure_ascii=False, indent=2)
        p.with_suffix(".tmp").replace(p)

def read_json(p): return json.load(p.open("r", encoding="utf-8")) if p and p.exists() else None

# --- RAG Logic ---
def get_mem_path(user_id):
    safe_uid = re.sub(r'[^\w-]', '', user_id)
    return MEM_DIR / f"{safe_uid}.json"

def get_embedding(text):
    try:
        url = f"{OLLAMA_HOST}/api/embeddings"
        payload = {"model": EMBED_MODEL, "prompt": text}
        r = requests.post(url, json=payload, timeout=5)
        if r.status_code == 200:
            return r.json().get("embedding")
    except: pass
    return None

def cosine_sim(v1, v2):
    if not v1 or not v2 or len(v1) != len(v2): return 0.0
    dot = sum(a * b for a, b in zip(v1, v2))
    mag1 = math.sqrt(sum(a * a for a in v1))
    mag2 = math.sqrt(sum(b * b for b in v2))
    if mag1 == 0 or mag2 == 0: return 0.0
    return dot / (mag1 * mag2)

def save_memory_npy(user_id, text, role):
    if not text.strip(): return
    vec = get_embedding(text)
    if not vec: return
    path = get_mem_path(user_id)
    data = []
    if path.exists():
        try: data = json.load(path.open("r", encoding="utf-8"))
        except: pass
    data.append({"ts": now_ts(), "role": role, "text": text, "vector": vec})
    try: json.dump(data, path.open("w", encoding="utf-8"), ensure_ascii=False)
    except: pass

def find_relevant_npy(user_id, query, top_k=3):
    path = get_mem_path(user_id)
    if not path.exists(): return ""
    q_vec = get_embedding(query)
    if not q_vec: return ""
    try: data = json.load(path.open("r", encoding="utf-8"))
    except: return ""
    if not data: return ""
    scores = []
    for item in data:
        scores.append((cosine_sim(q_vec, item["vector"]), item["text"]))
    scores.sort(key=lambda x: x[0], reverse=True)
    res = [s[1] for s in scores[:top_k]]
    return ("\n\n[Relevant Context]:\n" + "\n".join([f"- {t}" for t in res])) if res else ""

# --- Trend Analysis (New Feature) ---
def analyze_user_trends(user_id, days=5):
    uid = re.sub(r'[^\w-]', '', user_id)
    d = SESS_DIR / uid
    if not d.exists(): return ""
    
    cutoff = now_ts() - (days * 86400)
    files = []
    
    # Quét file cũ
    for p in d.glob("*.json"):
        try:
            o = json.load(p.open("r", encoding="utf-8"))
            if o.get("updated", 0) > cutoff:
                files.append(o)
        except: pass
    
    if not files: return ""
    
    # Đếm emotion assistant đã dùng
    cnt = {}
    for f in files:
        for m in f.get("chat", []):
            if m.get("role") == "assistant":
                e = m.get("emotion", "neutral")
                if e != "neutral":
                    cnt[e] = cnt.get(e, 0) + 1
    
    if not cnt: return ""
    
    dom = max(cnt, key=cnt.get)
    c = cnt[dom]
    tot = sum(cnt.values())
    
    # Nếu tần suất > 40% và có đủ mẫu -> Kích hoạt Trend Note
    if tot >= 3 and (c / tot) > 0.4:
        msg = f"\n[PSYCHOLOGICAL TREND ANALYSIS]:\n- Last {days} days mood: '{dom.upper()}' ({c}/{tot}).\n"
        bad = ["sadness", "anger", "fear", "anxiety"]
        if dom in bad:
            msg += "- Lingering negative mood detected. Suggest behavioral intervention (rest, brain dump) instead of just comfort.\n"
        return msg
    return ""

def ollama_chat(messages):
    try:
        r = requests.post(f"{OLLAMA_HOST}/api/chat", json={
            "model": MODEL_NAME, "messages": messages, "stream": False,
            "options": {"num_ctx": NUM_CTX, "temperature": GEN_TEMP, "top_p": TOP_P}
        }, timeout=120)
        return {"text": r.json().get("message", {}).get("content", "")}
    except Exception as e: return {"text": "", "error": str(e)}

def get_system_prompt():
    p = TRAIN_DIR / "a_seed_prompt.txt"
    return p.read_text(encoding="utf-8") if p.exists() else "You are A SEED."

# --- Routes ---
@app.route("/")
def root(): return redirect('/chat') if 'user_id' in session else redirect('/login')

@app.route("/chat")
def chat_page():
    if not session.get('user_id'): return redirect('/login')
    u = read_users()
    return render_template('index.html', display_name=u.get(session['user_id'], {}).get('display_name', session['user_id']))

@app.route("/login")
def login_page(): return render_template('login.html')

@app.post("/api/register")
def api_register():
    d = request.get_json()
    u, dn, p = d.get('username'), d.get('displayName'), d.get('password')
    if not all([u, dn, p]): return jsonify({"ok": False}), 400
    users = read_users()
    if u in users: return jsonify({"ok": False}), 409
    users[u] = {"hash": generate_password_hash(p), "display_name": dn, "created_at": now_ts()}
    write_users(users)
    return jsonify({"ok": True})

@app.post("/api/login")
def api_login():
    d = request.get_json()
    users = read_users()
    u = users.get(d.get('username'))
    if u and check_password_hash(u['hash'], d.get('password')):
        session['user_id'] = d.get('username')
        return jsonify({"ok": True})
    return jsonify({"ok": False}), 401

@app.post("/api/logout")
def api_logout():
    session.clear()
    return jsonify({"ok": True})

@app.get("/api/session-check")
def api_session_check(): return jsonify({"logged_in": 'user_id' in session})

@app.post("/api/chat")
def api_chat():
    if 'user_id' not in session: return jsonify({"error": "unauthorized"}), 401
    d = request.get_json()
    msg, hist = d.get("message", "").strip(), d.get("history", [])
    if not msg: return jsonify({"error": "empty"}), 400
    
    uid = session['user_id']
    
    # 1. Lấy context trend (MỚI)
    trend_ctx = analyze_user_trends(uid)
    
    # 2. Lấy context RAG
    ctx = find_relevant_npy(uid, msg)
    
    sys_p = get_system_prompt()
    if trend_ctx: sys_p += trend_ctx
    if ctx: sys_p += f"\n\n{ctx}"

    msgs = [{"role": "system", "content": sys_p}]
    for h in hist: msgs.append({"role": h['role'], "content": h['text']})
    msgs.append({"role": "user", "content": msg})

    out = ollama_chat(msgs)
    txt = out.get("text", "")
    if not txt: return jsonify({"error": "backend-failed"}), 500

    save_memory_npy(uid, msg, "user")
    save_memory_npy(uid, txt, "assistant")

    obj = safe_json(txt)
    return jsonify({
        "emotion": (obj.get("emotion") or "neutral").lower().strip(),
        "reply": (obj.get("reply") or txt).strip()
    })

@app.post("/api/save")
def api_save():
    if 'user_id' not in session: return jsonify({"error": "401"}), 401
    d = request.get_json()
    sid = ensure_sid(d.get("sid"))
    write_json(session_path(sid), {"sid": sid, "title": (d.get("chat", [])[0]['text'] if d.get("chat") else "New Chat")[:60], "chat": d.get("chat"), "updated": now_ts()})
    return jsonify({"ok": True, "sid": sid})

@app.get("/api/sessions")
def api_sessions():
    if 'user_id' not in session: return jsonify({"error": "401"}), 401
    d = get_user_session_dir()
    res = []
    if d:
        for p in d.glob("*.json"):
            try: res.append(read_json(p))
            except: pass
    res.sort(key=lambda x: x.get("updated", 0), reverse=True)
    return jsonify(res)

@app.get("/api/load")
def api_load():
    if 'user_id' not in session: return jsonify({"error": "401"}), 401
    return jsonify(read_json(session_path(request.args.get("sid"))) or {})

@app.post("/api/tts")
def api_tts():
    if 'user_id' not in session: return jsonify({"error": "unauthorized"}), 401
    if not EDGE_TTS_AVAILABLE: return jsonify({"error": "edge-tts missing"}), 500
    
    data = request.get_json()
    text = data.get("text", "").strip()
    if not text: return jsonify({"error": "empty"}), 400

    vn_chars = "àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ"
    voice = "vi-VN-HoaiMyNeural" if any(c in text.lower() for c in vn_chars) else "en-US-AriaNeural"

    async def get_audio():
        communicate = edge_tts.Communicate(text, voice)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            tmp_name = fp.name
        await communicate.save(tmp_name)
        return tmp_name

    try:
        tmp_file = asyncio.run(get_audio())
        with open(tmp_file, "rb") as f: audio_bytes = f.read()
        os.unlink(tmp_file)
        return make_response(audio_bytes, 200, {'Content-Type': 'audio/mpeg'})
    except Exception as e: return jsonify({"error": str(e)}), 500

# --- Admin ---
@app.route("/admin")
def admin_page(): return redirect("/admin/dashboard") if session.get("admin") else render_template("admin_login.html")
@app.route("/admin/dashboard")
def admin_dashboard(): return render_template("admin.html") if session.get("admin") else redirect("/admin")
@app.post("/api/admin/login")
def admin_login():
    d = request.get_json()
    if d.get("username")==ADMIN_USER and d.get("password")==ADMIN_PASSWORD:
        session["admin"]=True
        return jsonify({"ok": True})
    return jsonify({"ok": False}), 401
@app.post("/api/admin/logout")
def admin_logout():
    session.pop("admin", None)
    return jsonify({"ok": True})
@app.post("/api/admin/restart")
def api_restart():
    if not session.get("admin"): return jsonify({"error": "401"}), 401
    os.execv(sys.executable, ['python'] + sys.argv)
@app.get("/api/stats")
def api_stats():
    if not session.get("admin"): return jsonify({"error": "401"}), 401
    try: tags = requests.get(OLLAMA_HOST+"/api/tags", timeout=1).json()
    except: tags = {}
    return jsonify({
        "ts": now_ts(), "uptime_sec": int(time.time()-START_TS),
        "memory": {"percent": psutil.virtual_memory().percent},
        "cpu": {"percent": psutil.cpu_percent()},
        "ollama": {"ok": bool(tags)}
    })

if __name__ == "__main__":
    from waitress import serve
    print("A SEED (Trend + TTS) starting...", flush=True)
    serve(app, host="0.0.0.0", port=8000)