#!/usr/bin/env python3
"""
server.py - 미니멀 포트폴리오 로컬 개발 및 CMS 백엔드 서버
- 정적 파일 서빙 (HTML, CSS, JS, Images, RSS)
- /api/verify: 관리자 비밀번호 검증
- /api/get-content: index.html의 About me 및 Notes on building 실시간 추출
- /api/update-content: RSS 히든 스튜디오에서 수정한 내용을 index.html에 안전하게 반영 및 백업 저장
- /api/save: 전체 HTML 직접 저장
"""

import http.server
import socketserver
import json
import os
import re
import hashlib
import shutil
from datetime import datetime

PORT = 3000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

# 기본 관리자 비밀번호 (기본값: '1234')
ADMIN_PASSCODE_HASH = hashlib.sha256("1234".encode('utf-8')).hexdigest()

class CMSRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_GET(self):
        # 1. index.html의 콘텐츠 추출 API
        if self.path == '/api/get-content':
            index_path = os.path.join(DIRECTORY, 'index.html')
            try:
                with open(index_path, 'r', encoding='utf-8') as f:
                    html = f.read()

                # About me 추출
                about_match = re.search(r'<h2>About me</h2>\s*<p>(.*?)</p>', html, re.DOTALL)
                about_text = about_match.group(1).strip() if about_match else ''
                # 태그 정리(strong 등 유지 또는 텍스트)
                about_clean = about_text.replace('\n', ' ').strip()

                # Notes on building 추출
                notes_match = re.search(r'<h2>Notes on building</h2>\s*<ul>(.*?)</ul>', html, re.DOTALL)
                notes_items = []
                if notes_match:
                    raw_items = re.findall(r'<li>(.*?)</li>', notes_match.group(1))
                    notes_items = [item.strip() for item in raw_items if item.strip()]

                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps({
                    'success': True,
                    'about': about_clean,
                    'notes': notes_items
                }, ensure_ascii=False).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps({'success': False, 'error': str(e)}).encode('utf-8'))
            return

        super().do_GET()

    def do_POST(self):
        # 1. 비밀번호 검증 API
        if self.path == '/api/verify':
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            try:
                data = json.loads(body)
                passcode = data.get('passcode', '')
                req_hash = hashlib.sha256(passcode.encode('utf-8')).hexdigest()

                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()

                if req_hash == ADMIN_PASSCODE_HASH:
                    self.wfile.write(json.dumps({'success': True, 'message': '인증 성공'}).encode('utf-8'))
                else:
                    self.wfile.write(json.dumps({'success': False, 'message': '비밀번호가 일치하지 않습니다.'}).encode('utf-8'))
            except Exception as e:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(json.dumps({'success': False, 'error': str(e)}).encode('utf-8'))
            return

        # 2. RSS 히든 스튜디오 전용 부분 콘텐츠 업데이트 API
        if self.path == '/api/update-content':
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            try:
                data = json.loads(body)
                passcode = data.get('passcode', '')
                about_text = data.get('about', '').strip()
                notes_items = data.get('notes', [])

                req_hash = hashlib.sha256(passcode.encode('utf-8')).hexdigest()
                if req_hash != ADMIN_PASSCODE_HASH:
                    self.send_response(403)
                    self.send_header('Content-Type', 'application/json; charset=utf-8')
                    self.end_headers()
                    self.wfile.write(json.dumps({'success': False, 'message': '비밀번호가 올바르지 않습니다.'}).encode('utf-8'))
                    return

                index_path = os.path.join(DIRECTORY, 'index.html')
                with open(index_path, 'r', encoding='utf-8') as f:
                    html = f.read()

                # 자동 백업
                backup_dir = os.path.join(DIRECTORY, '.backups')
                os.makedirs(backup_dir, exist_ok=True)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                shutil.copy2(index_path, os.path.join(backup_dir, f"index.html.{timestamp}.bak"))

                # About me 교체
                if about_text:
                    new_about_block = f"<h2>About me</h2>\n      <p>\n        {about_text}\n      </p>"
                    html = re.sub(r'<h2>About me</h2>\s*<p>.*?</p>', new_about_block, html, flags=re.DOTALL)

                # Notes on building 교체
                if notes_items:
                    li_elements = "\n".join([f"        <li>{item}</li>" for item in notes_items if item.strip()])
                    new_notes_block = f"<h2>Notes on building</h2>\n      <ul>\n{li_elements}\n      </ul>"
                    html = re.sub(r'<h2>Notes on building</h2>\s*<ul>.*?</ul>', new_notes_block, html, flags=re.DOTALL)

                with open(index_path, 'w', encoding='utf-8') as f:
                    f.write(html)

                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps({
                    'success': True,
                    'message': '메인 페이지(index.html)에 성공적으로 영구 반영되었습니다!'
                }, ensure_ascii=False).encode('utf-8'))

            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps({'success': False, 'error': str(e)}).encode('utf-8'))
            return

        # 3. 전체 HTML 저장 API
        if self.path == '/api/save':
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            try:
                data = json.loads(body)
                passcode = data.get('passcode', '')
                html_content = data.get('html', '')
                target_file = data.get('file', 'index.html')

                req_hash = hashlib.sha256(passcode.encode('utf-8')).hexdigest()
                if req_hash != ADMIN_PASSCODE_HASH:
                    self.send_response(403)
                    self.send_header('Content-Type', 'application/json; charset=utf-8')
                    self.end_headers()
                    self.wfile.write(json.dumps({'success': False, 'message': '권한이 없습니다.'}).encode('utf-8'))
                    return

                safe_path = os.path.normpath(os.path.join(DIRECTORY, target_file))
                if not safe_path.startswith(DIRECTORY):
                    raise ValueError('허용되지 않은 파일 경로입니다.')

                backup_dir = os.path.join(DIRECTORY, '.backups')
                os.makedirs(backup_dir, exist_ok=True)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                backup_filename = f"{os.path.basename(safe_path)}.{timestamp}.bak"
                if os.path.exists(safe_path):
                    shutil.copy2(safe_path, os.path.join(backup_dir, backup_filename))

                with open(safe_path, 'w', encoding='utf-8') as f:
                    f.write(html_content)

                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps({
                    'success': True,
                    'message': '파일이 성공적으로 저장되었습니다.'
                }).encode('utf-8'))

            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps({'success': False, 'error': str(e)}).encode('utf-8'))
            return

        self.send_response(404)
        self.end_headers()

if __name__ == '__main__':
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), CMSRequestHandler) as httpd:
        print(f"🚀 CMS Server running at http://localhost:{PORT}/")
        print(f"📁 Root directory: {DIRECTORY}")
        print(f"🔑 Default admin passcode: 1234")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer shutting down.")
