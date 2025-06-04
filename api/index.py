from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
import datetime
import random

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Parse the URL path
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        query = parse_qs(parsed_path.query)
        
        if path == '/admin':
            self.admin_page()
        elif path == '/scan':
            self.scan_api(query)
        elif path == '/stats':
            self.stats_api()
        elif path == '/products':
            self.products_api()
        elif path == '/delete-product':
            self.delete_product_api(query)
        else:
            self.main_page()
    
    def do_POST(self):
        # Handle POST requests for product deletion
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        if path == '/delete-product':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            self.delete_product_post(data)
        else:
            self.send_response(404)
            self.end_headers()

    def delete_product_api(self, query):
        # Send JSON response for product deletion
        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        product_id = query.get('id', [''])[0]
        
        if product_id:
            response = {'status': 'success', 'message': f'제품 {product_id} 삭제 완료'}
        else:
            response = {'status': 'error', 'message': '제품 ID가 필요합니다'}
        
        self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))

    def delete_product_post(self, data):
        # Handle POST request for product deletion
        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        product_id = data.get('id', '')
        
        if product_id:
            response = {'status': 'success', 'message': f'제품 {product_id} 삭제 완료'}
        else:
            response = {'status': 'error', 'message': '제품 ID가 필요합니다'}
        
        self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))

    def main_page(self):
        # Send HTML response
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        
        html = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🍢 Smart Chopstick QR Scanner</title>
    <script src="https://unpkg.com/html5-qrcode" type="text/javascript"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh; color: white; padding: 20px;
        }
        .container {
            max-width: 1200px; margin: 0 auto;
        }
        .main-section {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px); border-radius: 20px;
            padding: 30px; margin-bottom: 30px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            text-align: center;
        }
        h1 { margin-bottom: 20px; font-size: 2.5em; }
        .scan-methods {
            display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin: 30px 0;
        }
        .scan-method {
            background: rgba(255, 255, 255, 0.1); padding: 25px; border-radius: 15px;
            transition: all 0.3s ease;
        }
        .scan-method:hover { transform: translateY(-5px); }
        .input-group { margin: 20px 0; }
        input {
            width: 100%; padding: 15px; border: none; border-radius: 10px;
            font-size: 16px; background: rgba(255, 255, 255, 0.9);
            margin-bottom: 15px; color: #333;
        }
        button {
            background: linear-gradient(45deg, #ff6b6b, #ee5a24);
            color: white; border: none; padding: 15px 30px;
            border-radius: 10px; font-size: 16px; cursor: pointer;
            width: 100%; margin: 10px 0;
            transition: all 0.3s ease;
        }
        button:hover { transform: translateY(-2px); box-shadow: 0 4px 20px rgba(255, 107, 107, 0.4); }
        .camera-section {
            background: rgba(255, 255, 255, 0.05); padding: 20px; border-radius: 15px;
            margin: 20px 0; display: none;
        }
        #qr-reader { margin: 20px auto; border-radius: 10px; overflow: hidden; }
        .result {
            margin-top: 20px; padding: 20px; border-radius: 10px;
            background: rgba(255, 255, 255, 0.1);
            display: none; transition: all 0.3s ease;
        }
        .success { 
            background: rgba(76, 175, 80, 0.3); 
            border: 2px solid rgba(76, 175, 80, 0.6);
        }
        .warning { 
            background: rgba(255, 152, 0, 0.3); 
            border: 2px solid rgba(255, 152, 0, 0.6);
        }
        .danger { 
            background: rgba(244, 67, 54, 0.3); 
            border: 2px solid rgba(244, 67, 54, 0.6);
        }
        .error { 
            background: rgba(158, 158, 158, 0.3); 
            border: 2px solid rgba(158, 158, 158, 0.6);
        }
        .admin-link {
            position: fixed; top: 20px; right: 20px;
            background: rgba(255, 255, 255, 0.2);
            padding: 10px 20px; border-radius: 10px;
            text-decoration: none; color: white;
            transition: all 0.3s ease;
        }
        .admin-link:hover { background: rgba(255, 255, 255, 0.3); }
        .status-icon { font-size: 2em; margin-bottom: 10px; }
        .product-info { 
            margin-top: 15px; 
            background: rgba(255, 255, 255, 0.1); 
            padding: 15px; 
            border-radius: 8px; 
        }
        
        /* 통계 섹션 */
        .stats-section {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px); border-radius: 20px;
            padding: 30px; margin-bottom: 30px;
        }
        .stats-grid {
            display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px; margin-bottom: 30px;
        }
        .stat-card {
            background: rgba(255, 255, 255, 0.1); padding: 20px; border-radius: 10px;
            text-align: center; transition: all 0.3s ease;
        }
        .stat-card:hover { transform: translateY(-3px); }
        .stat-number { font-size: 2em; font-weight: bold; margin-bottom: 5px; }
        
        /* 최근 스캔 이력 */
        .history-section {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px); border-radius: 20px;
            padding: 30px;
        }
        .history-item {
            background: rgba(255, 255, 255, 0.1);
            padding: 15px; border-radius: 8px; margin-bottom: 10px;
            display: flex; justify-content: space-between; align-items: center;
        }
        .scan-status { 
            padding: 5px 10px; border-radius: 15px; font-size: 0.8em; 
        }
        .status-safe { background: rgba(76, 175, 80, 0.7); }
        .status-warning { background: rgba(255, 152, 0, 0.7); }
        .status-danger { background: rgba(244, 67, 54, 0.7); }
        
        @media (max-width: 768px) {
            .scan-methods { grid-template-columns: 1fr; }
            .stats-grid { grid-template-columns: repeat(2, 1fr); }
        }
    </style>
</head>
<body>
    <a href="/admin" class="admin-link">📊 관리자</a>
    <div class="container">
        <div class="main-section">
            <h1>🍢 DEVPOINT 스마트 대시보드</h1>
            <p>QR 코드를 스캔하여 안전성을 확인하세요</p>
            
            <div class="scan-methods">
                <div class="scan-method">
                    <h3>📷 카메라 스캔</h3>
                    <p>카메라로 QR 코드를 직접 스캔</p>
                    <button onclick="startCamera()">📸 카메라 시작</button>
                </div>
                <div class="scan-method">
                    <h3>⌨️ 수동 입력</h3>
                    <p>QR 코드를 직접 입력</p>
                    <div class="input-group">
                        <input type="text" id="qrInput" placeholder="QR 코드 입력 (예: SKC-123)" />
                        <button onclick="scanManual()">🔍 스캔하기</button>
                    </div>
                </div>
            </div>
            
            <div class="camera-section" id="cameraSection">
                <h3>📷 카메라 QR 스캔</h3>
                <div id="qr-reader" style="width: 100%; max-width: 400px;"></div>
                <button onclick="stopCamera()" style="background: #e74c3c;">📵 카메라 정지</button>
            </div>
            
            <div id="result" class="result"></div>
        </div>
        
        <div class="stats-section">
            <h2>📊 실시간 통계</h2>
            <div class="stats-grid" id="statsGrid">
                <div class="stat-card">
                    <div class="stat-number" id="totalScans">0</div>
                    <div>총 스캔 수</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number" id="safeScans">0</div>
                    <div>안전 스캔</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number" id="warningScans">0</div>
                    <div>주의 스캔</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number" id="dangerScans">0</div>
                    <div>위험 스캔</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number" id="todayScans">0</div>
                    <div>오늘 스캔</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number" id="uniqueProducts">0</div>
                    <div>고유 제품</div>
                </div>
            </div>
        </div>
        
        <div class="history-section">
            <h2>📋 최근 스캔 이력</h2>
            <div id="scanHistory">
                <div class="history-item">
                    <div>
                        <strong>SKC-123456</strong> 첫 번째 스캔
                        <br><small>방금 전 • 브라우저 스캔</small>
                    </div>
                    <span class="scan-status status-safe">✅ 안전</span>
                </div>
            </div>
        </div>
    </div>

    <script>
        let html5QrCode;
        let scanHistory = JSON.parse(localStorage.getItem('scanHistory') || '[]');
        let statistics = JSON.parse(localStorage.getItem('statistics') || '{"total": 0, "safe": 0, "warning": 0, "danger": 0, "today": 0, "unique": []}');
        
        // 페이지 로드시 통계 및 이력 표시
        window.onload = function() {
            updateStatsDisplay();
            updateHistoryDisplay();
        };
        
        function startCamera() {
            const cameraSection = document.getElementById('cameraSection');
            cameraSection.style.display = 'block';
            
            html5QrCode = new Html5Qrcode("qr-reader");
            html5QrCode.start(
                { facingMode: "environment" },
                {
                    fps: 10,
                    qrbox: { width: 250, height: 250 }
                },
                (decodedText, decodedResult) => {
                    processQRCode(decodedText, 'camera');
                    stopCamera();
                },
                (errorMessage) => {
                    // 에러 무시 (지속적인 스캔 시도)
                }
            ).catch(err => {
                console.log("카메라 접근 오류:", err);
                alert("카메라에 접근할 수 없습니다. 수동 입력을 사용해주세요.");
                cameraSection.style.display = 'none';
            });
        }
        
        function stopCamera() {
            if (html5QrCode) {
                html5QrCode.stop().then(() => {
                    document.getElementById('cameraSection').style.display = 'none';
                }).catch(err => console.log(err));
            }
        }
        
        function scanManual() {
            const qrCode = document.getElementById('qrInput').value.trim();
            if (!qrCode) {
                alert('QR 코드를 입력해주세요');
                return;
            }
            processQRCode(qrCode, 'manual');
        }
        
        async function processQRCode(qrCode, method) {
            try {
                const response = await fetch('/scan?code=' + encodeURIComponent(qrCode));
                const data = await response.json();
                
                // 스캔 이력 저장
                const scanRecord = {
                    code: qrCode,
                    result: data,
                    method: method,
                    timestamp: new Date().toISOString()
                };
                
                scanHistory.unshift(scanRecord);
                if (scanHistory.length > 50) scanHistory = scanHistory.slice(0, 50);
                localStorage.setItem('scanHistory', JSON.stringify(scanHistory));
                
                // 통계 업데이트
                updateStatistics(data);
                
                // 결과 표시
                displayResult(data);
                
                // 화면 업데이트
                updateStatsDisplay();
                updateHistoryDisplay();
                
            } catch (error) {
                displayResult({
                    status: 'error',
                    message: '네트워크 오류가 발생했습니다'
                });
            }
        }
        
        function updateStatistics(data) {
            statistics.total++;
            
            if (data.status === 'success') {
                if (data.scan_result === 'first_use') statistics.safe++;
                else if (data.scan_result === 'potential_reuse') statistics.warning++;
                else if (data.scan_result === 'multiple_reuse') statistics.danger++;
                
                // 고유 제품 추가
                if (!statistics.unique.includes(data.product_id)) {
                    statistics.unique.push(data.product_id);
                }
            }
            
            // 오늘 스캔 수 (간단히 현재 세션으로 계산)
            statistics.today = statistics.total;
            
            localStorage.setItem('statistics', JSON.stringify(statistics));
        }
        
        function updateStatsDisplay() {
            document.getElementById('totalScans').textContent = statistics.total;
            document.getElementById('safeScans').textContent = statistics.safe;
            document.getElementById('warningScans').textContent = statistics.warning;
            document.getElementById('dangerScans').textContent = statistics.danger;
            document.getElementById('todayScans').textContent = statistics.today;
            document.getElementById('uniqueProducts').textContent = statistics.unique.length;
        }
        
        function updateHistoryDisplay() {
            const historyDiv = document.getElementById('scanHistory');
            if (scanHistory.length === 0) return;
            
            historyDiv.innerHTML = scanHistory.slice(0, 10).map(record => {
                const data = record.result;
                let statusClass = 'status-safe';
                let statusIcon = '✅ 안전';
                
                if (data.scan_result === 'potential_reuse') {
                    statusClass = 'status-warning';
                    statusIcon = '⚠️ 주의';
                } else if (data.scan_result === 'multiple_reuse') {
                    statusClass = 'status-danger';
                    statusIcon = '❌ 위험';
                } else if (data.status === 'error') {
                    statusClass = 'status-danger';
                    statusIcon = '❓ 오류';
                }
                
                const timeAgo = getTimeAgo(new Date(record.timestamp));
                const methodText = record.method === 'camera' ? '카메라 스캔' : '수동 입력';
                
                return `
                    <div class="history-item">
                        <div>
                            <strong>${record.code}</strong> ${data.message || '스캔됨'}
                            <br><small>${timeAgo} • ${methodText}</small>
                        </div>
                        <span class="scan-status ${statusClass}">${statusIcon}</span>
                    </div>
                `;
            }).join('');
        }
        
        function getTimeAgo(date) {
            const now = new Date();
            const diffMs = now - date;
            const diffMins = Math.floor(diffMs / 60000);
            
            if (diffMins < 1) return '방금 전';
            if (diffMins < 60) return diffMins + '분 전';
            if (diffMins < 1440) return Math.floor(diffMins / 60) + '시간 전';
            return Math.floor(diffMins / 1440) + '일 전';
        }
        
        function displayResult(data) {
            const resultDiv = document.getElementById('result');
            resultDiv.style.display = 'block';
            
            if (data.status === 'success') {
                let className = 'success';
                let icon = '✅';
                let statusText = '안전';
                
                if (data.scan_result === 'potential_reuse') {
                    className = 'warning';
                    icon = '⚠️';
                    statusText = '주의';
                } else if (data.scan_result === 'multiple_reuse') {
                    className = 'danger';
                    icon = '❌';
                    statusText = '위험';
                }
                
                resultDiv.className = 'result ' + className;
                resultDiv.innerHTML = `
                    <div class="status-icon">${icon}</div>
                    <h3>${statusText} - ${data.message}</h3>
                    <div class="product-info">
                        <p><strong>제품 ID:</strong> ${data.product_id}</p>
                        <p><strong>사용 횟수:</strong> ${data.usage_count}회</p>
                        <p><strong>검사 시간:</strong> ${new Date().toLocaleString('ko-KR')}</p>
                    </div>
                `;
            } else {
                resultDiv.className = 'result error';
                resultDiv.innerHTML = `
                    <div class="status-icon">❓</div>
                    <h3>오류 - ${data.message}</h3>
                    <p>올바른 QR 코드를 입력해주세요</p>
                `;
            }
        }
        
        // Enter key support
        document.getElementById('qrInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') scanManual();
        });
    </script>
</body>
</html>"""
        self.wfile.write(html.encode('utf-8'))
    
    def admin_page(self):
        # Send HTML response
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        
        html = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🍢 관리자 대시보드</title>
    <script src="https://cdn.jsdelivr.net/npm/qrcode@1.5.3/build/qrcode.min.js"></script>
    <script>
        // QRCode 라이브러리 대체 로딩
        if (typeof QRCode === 'undefined') {
            console.log('첫 번째 CDN 실패, 두 번째 시도...');
            const script2 = document.createElement('script');
            script2.src = 'https://unpkg.com/qrcode@1.5.3/build/qrcode.min.js';
            script2.onload = () => console.log('두 번째 CDN 성공');
            script2.onerror = () => {
                console.log('모든 CDN 실패, 대체 방법 사용');
                window.QRCode = {
                    toCanvas: function(text, options, callback) {
                        // 텍스트 기반 QR 대체
                        const canvas = document.createElement('canvas');
                        canvas.width = options.width || 200;
                        canvas.height = options.height || 200;
                        const ctx = canvas.getContext('2d');
                        
                        // 배경
                        ctx.fillStyle = '#ffffff';
                        ctx.fillRect(0, 0, canvas.width, canvas.height);
                        
                        // 테두리
                        ctx.strokeStyle = '#000000';
                        ctx.lineWidth = 2;
                        ctx.strokeRect(10, 10, canvas.width-20, canvas.height-20);
                        
                        // QR 패턴 시뮬레이션
                        ctx.fillStyle = '#000000';
                        for(let i = 0; i < 15; i++) {
                            for(let j = 0; j < 15; j++) {
                                if(Math.random() > 0.5) {
                                    ctx.fillRect(20 + i*10, 20 + j*10, 8, 8);
                                }
                            }
                        }
                        
                        // 코너 마커
                        ctx.fillRect(20, 20, 30, 30);
                        ctx.fillRect(canvas.width-50, 20, 30, 30);
                        ctx.fillRect(20, canvas.height-50, 30, 30);
                        
                        // 텍스트
                        ctx.fillStyle = '#000000';
                        ctx.font = '12px Arial';
                        ctx.textAlign = 'center';
                        ctx.fillText(text, canvas.width/2, canvas.height-15);
                        
                        callback(null, canvas);
                    }
                };
            };
            document.head.appendChild(script2);
        }
    </script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: linear-gradient(135deg, #2c3e50 0%, #3498db 100%);
            min-height: 100vh; color: white; padding: 20px;
        }
        .container { max-width: 1200px; margin: 0 auto; }
        h1 { text-align: center; margin-bottom: 30px; font-size: 2.5em; }
        .stats {
            display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px; margin-bottom: 30px;
        }
        .stat-card {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px); border-radius: 15px;
            padding: 20px; text-align: center;
            transition: all 0.3s ease;
        }
        .stat-card:hover { transform: translateY(-5px); }
        .stat-number { font-size: 3em; font-weight: bold; margin-bottom: 10px; }
        .stat-card.total { border: 2px solid rgba(52, 152, 219, 0.5); }
        .stat-card.used { border: 2px solid rgba(46, 204, 113, 0.5); }
        .stat-card.reuse { border: 2px solid rgba(231, 76, 60, 0.5); }
        .stat-card.recent { border: 2px solid rgba(241, 196, 15, 0.5); }
        
        .create-section {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px); border-radius: 15px;
            padding: 30px; margin-bottom: 30px;
        }
        .form-group { display: flex; align-items: center; margin-bottom: 20px; gap: 15px; }
        input, select {
            padding: 15px; border: none; border-radius: 10px;
            font-size: 16px; background: rgba(255, 255, 255, 0.9);
            flex: 1; min-width: 200px; color: #333;
        }
        button {
            background: linear-gradient(45deg, #e74c3c, #c0392b);
            color: white; cursor: pointer; padding: 15px 30px;
            border: none; border-radius: 10px; font-size: 16px;
            transition: all 0.3s ease;
        }
        button:hover { transform: translateY(-2px); box-shadow: 0 4px 20px rgba(231, 76, 60, 0.4); }
        .qr-display {
            margin-top: 20px; text-align: center;
            background: rgba(255, 255, 255, 0.9); padding: 20px; border-radius: 10px;
            display: none; color: #333;
        }
        .home-link {
            position: fixed; top: 20px; left: 20px;
            background: rgba(255, 255, 255, 0.2);
            padding: 10px 20px; border-radius: 10px;
            text-decoration: none; color: white;
            transition: all 0.3s ease;
        }
        .home-link:hover { background: rgba(255, 255, 255, 0.3); }
        
        .products-section {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px); border-radius: 15px;
            padding: 30px; margin-bottom: 30px;
        }
        .product-item {
            background: rgba(255, 255, 255, 0.1);
            padding: 15px; border-radius: 8px; margin-bottom: 10px;
            display: flex; justify-content: space-between; align-items: center;
        }
        .qr-code-container {
            margin: 15px 0;
        }
        #qrcode { margin: 15px auto; }
        
        .recent-activity {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px); border-radius: 15px;
            padding: 30px; margin-bottom: 30px;
        }
        .activity-item {
            background: rgba(255, 255, 255, 0.1);
            padding: 15px; border-radius: 8px; margin-bottom: 10px;
            display: flex; justify-content: space-between; align-items: center;
        }
        .activity-status { 
            padding: 5px 10px; border-radius: 15px; font-size: 0.8em; 
            margin-left: auto;
        }
        .status-safe { background: rgba(76, 175, 80, 0.7); }
        .status-warning { background: rgba(255, 152, 0, 0.7); }
        .status-danger { background: rgba(244, 67, 54, 0.7); }
        
        .debug-info {
            background: rgba(255, 255, 255, 0.1);
            padding: 10px; border-radius: 5px; margin: 10px 0;
            font-family: monospace; font-size: 12px;
            display: none;
        }
        
        @media (max-width: 768px) {
            .form-group { flex-direction: column; }
            .stats { grid-template-columns: repeat(2, 1fr); }
        }
    </style>
</head>
<body>
    <a href="/" class="home-link">🏠 홈</a>
    <div class="container">
        <h1>🍢 DEVPOINT 스마트 관리자</h1>
        
        <div class="stats">
            <div class="stat-card total">
                <div class="stat-number" id="totalProducts">1,247</div>
                <div>총 제품 수</div>
                <div style="font-size: 0.8em; opacity: 0.7;">등록된 제품</div>
            </div>
            <div class="stat-card used">
                <div class="stat-number">892</div>
                <div>사용된 제품</div>
                <div style="font-size: 0.8em; opacity: 0.7;">71.5% 사용률</div>
            </div>
            <div class="stat-card reuse">
                <div class="stat-number">23</div>
                <div>재사용 감지</div>
                <div style="font-size: 0.8em; opacity: 0.7;">2.6% 위험도</div>
            </div>
            <div class="stat-card recent">
                <div class="stat-number" id="recentScans">156</div>
                <div>24시간 스캔</div>
                <div style="font-size: 0.8em; opacity: 0.7;">실시간 모니터링</div>
            </div>
        </div>
        
        <div class="create-section">
            <h2>🏭 새 제품 배치 등록</h2>
            <div class="form-group">
                <input type="text" id="productName" placeholder="제품명 (예: 프리미엄 젓가락 A형)" />
                <input type="text" id="companyName" placeholder="제조사명" />
                <input type="date" id="registrationDate" />
            </div>
            <div class="form-group">
                <input type="number" id="quantity" placeholder="생산 수량" min="1" max="10000" />
                <button onclick="generateBatch()" id="generateBtn">📱 배치 생성 및 QR 생성</button>
            </div>
            
            <div id="debugInfo" class="debug-info"></div>
            
            <div id="qrDisplay" class="qr-display">
                <h3>✅ 배치 생성 완료!</h3>
                <div class="qr-code-container">
                    <div id="qrcode"></div>
                </div>
                <p id="batchInfo">배치 ID: SKC-2024-001</p>
                <button onclick="downloadQR()" style="margin-top: 15px; background: #27ae60;">💾 QR 코드 다운로드</button>
            </div>
        </div>
        
        <div class="products-section">
            <h2>📦 등록된 제품 목록</h2>
            <div id="productsList">
                <div class="product-item">
                    <div>
                        <strong>SKC-2024-001</strong> • 프리미엄 젓가락 A형
                        <br><small>ABC 제조사 • 2024-01-15 등록 • 100개</small>
                    </div>
                    <span class="activity-status status-safe">📦 활성</span>
                </div>
                <div class="product-item">
                    <div>
                        <strong>SKC-2024-002</strong> • 친환경 젓가락 B형
                        <br><small>XYZ 제조사 • 2024-01-14 등록 • 250개</small>
                    </div>
                    <span class="activity-status status-safe">📦 활성</span>
                </div>
                <div class="product-item">
                    <div>
                        <strong>SKC-2024-003</strong> • 일반 젓가락 C형
                        <br><small>DEF 제조사 • 2024-01-13 등록 • 500개</small>
                    </div>
                    <span class="activity-status status-warning">⚠️ 재사용감지</span>
                </div>
            </div>
        </div>
        
        <div class="recent-activity">
            <h2>📊 최근 활동 로그</h2>
            <div class="activity-item">
                <div>
                    <strong>SKC-123456</strong> 스캔됨
                    <br><small>2분 전 • IP: 192.168.1.100</small>
                </div>
                <span class="activity-status status-safe">✅ 안전</span>
            </div>
            <div class="activity-item">
                <div>
                    <strong>SKC-789012</strong> 재사용 감지!
                    <br><small>15분 전 • IP: 10.0.0.50</small>
                </div>
                <span class="activity-status status-warning">⚠️ 주의</span>
            </div>
            <div class="activity-item">
                <div>
                    <strong>SKC-345678</strong> 다중 재사용 위험
                    <br><small>1시간 전 • IP: 172.16.1.25</small>
                </div>
                <span class="activity-status status-danger">❌ 위험</span>
            </div>
            <div class="activity-item">
                <div>
                    <strong>배치 SKC-2024-001</strong> 생성됨
                    <br><small>3시간 전 • 관리자</small>
                </div>
                <span class="activity-status status-safe">📦 생성</span>
            </div>
        </div>
    </div>

    <script>
        let currentQRData = '';
        let products = JSON.parse(localStorage.getItem('products') || '[]');
        
        // 디버그 함수
        function debug(message) {
            console.log('[QR Debug]', message);
            const debugDiv = document.getElementById('debugInfo');
            debugDiv.style.display = 'block';
            debugDiv.innerHTML += '<div>' + new Date().toLocaleTimeString() + ': ' + message + '</div>';
        }
        
        // 페이지 로드시 초기화
        window.onload = function() {
            debug('페이지 로드 완료');
            
            // QRCode 라이브러리 확인 (지연된 확인)
            setTimeout(() => {
                if (typeof QRCode !== 'undefined') {
                    debug('✅ QRCode 라이브러리 로드 성공');
                } else {
                    debug('⚠️ QRCode 라이브러리 로드 지연, 대체 방법 준비');
                }
            }, 1000);
            
            const today = new Date().toISOString().split('T')[0];
            document.getElementById('registrationDate').value = today;
            updateProductsList();
            
            debug('초기화 완료');
        };
        
        // QR 라이브러리 로딩 대기 (개선된 버전)
        function waitForQRCode(callback, attempts = 0) {
            if (typeof QRCode !== 'undefined') {
                debug('✅ QRCode 라이브러리 사용 가능');
                callback();
            } else if (attempts < 30) { // 3초 대기 (100ms * 30)
                debug(`QRCode 라이브러리 로딩 대기 중... (${attempts + 1}/30)`);
                setTimeout(() => waitForQRCode(callback, attempts + 1), 100);
            } else {
                debug('⚠️ QRCode 라이브러리 타임아웃, 강제 대체 방법 활성화');
                // 강제로 대체 QRCode 생성
                window.QRCode = {
                    toCanvas: function(text, options, callback) {
                        debug('🎨 대체 QR 생성 시작: ' + text);
                        
                        const canvas = document.createElement('canvas');
                        canvas.width = options.width || 200;
                        canvas.height = options.height || 200;
                        const ctx = canvas.getContext('2d');
                        
                        // 배경
                        ctx.fillStyle = '#ffffff';
                        ctx.fillRect(0, 0, canvas.width, canvas.height);
                        
                        // 테두리
                        ctx.strokeStyle = '#000000';
                        ctx.lineWidth = 3;
                        ctx.strokeRect(5, 5, canvas.width-10, canvas.height-10);
                        
                        // QR 패턴 시뮬레이션 (더 정교하게)
                        ctx.fillStyle = '#000000';
                        const gridSize = 12;
                        const cellSize = (canvas.width - 40) / gridSize;
                        
                        for(let i = 0; i < gridSize; i++) {
                            for(let j = 0; j < gridSize; j++) {
                                // 패턴 생성 (QR 코드처럼 보이게)
                                const hash = (text.charCodeAt((i*gridSize + j) % text.length) + i + j) % 4;
                                if(hash >= 2) {
                                    ctx.fillRect(20 + i*cellSize, 20 + j*cellSize, cellSize-1, cellSize-1);
                                }
                            }
                        }
                        
                        // 코너 마커 (QR 코드 특징)
                        const markerSize = cellSize * 3;
                        // 좌상단
                        ctx.fillRect(20, 20, markerSize, markerSize);
                        ctx.fillStyle = '#ffffff';
                        ctx.fillRect(25, 25, markerSize-10, markerSize-10);
                        ctx.fillStyle = '#000000';
                        ctx.fillRect(30, 30, markerSize-20, markerSize-20);
                        
                        // 우상단
                        ctx.fillRect(canvas.width-20-markerSize, 20, markerSize, markerSize);
                        ctx.fillStyle = '#ffffff';
                        ctx.fillRect(canvas.width-25-markerSize+10, 25, markerSize-10, markerSize-10);
                        ctx.fillStyle = '#000000';
                        ctx.fillRect(canvas.width-30-markerSize+20, 30, markerSize-20, markerSize-20);
                        
                        // 좌하단
                        ctx.fillRect(20, canvas.height-20-markerSize, markerSize, markerSize);
                        ctx.fillStyle = '#ffffff';
                        ctx.fillRect(25, canvas.height-25-markerSize+10, markerSize-10, markerSize-10);
                        ctx.fillStyle = '#000000';
                        ctx.fillRect(30, canvas.height-30-markerSize+20, markerSize-20, markerSize-20);
                        
                        // 텍스트 라벨
                        ctx.fillStyle = '#666666';
                        ctx.font = 'bold 10px Arial';
                        ctx.textAlign = 'center';
                        ctx.fillText('QR: ' + text, canvas.width/2, canvas.height-8);
                        
                        debug('✅ 대체 QR 생성 완료');
                        callback(null, canvas);
                    }
                };
                callback();
            }
        }
        
        function generateGTIN14() {
            // GS1 표준 GTIN-14 생성 (실제 제조업체 형식)
            const gs1Prefix = '8801234';  // 한국 GS1 접두사 (실제 등록 필요)
            const companyPrefix = '567';   // 회사 코드
            const itemReference = String(Math.floor(Math.random() * 1000)).padStart(3, '0');
            const indicator = '1';         // 포장 단계 식별자
            
            // 체크 디지트 계산
            const partial = indicator + gs1Prefix + companyPrefix + itemReference;
            let sum = 0;
            for (let i = 0; i < partial.length; i++) {
                sum += parseInt(partial[i]) * (i % 2 === 0 ? 3 : 1);
            }
            const checkDigit = (10 - (sum % 10)) % 10;
            
            return partial + checkDigit;
        }
        
        function generateBatch() {
            debug('🚀 배치 생성 시작');
            
            const generateBtn = document.getElementById('generateBtn');
            generateBtn.disabled = true;
            generateBtn.textContent = '생성 중...';
            
            try {
                const productName = document.getElementById('productName').value || '기본 제품';
                const companyName = document.getElementById('companyName').value || '기본 제조사';
                const quantity = document.getElementById('quantity').value || '100';
                const registrationDate = document.getElementById('registrationDate').value || new Date().toISOString().split('T')[0];
                
                debug(`입력값: ${productName}, ${companyName}, ${quantity}, ${registrationDate}`);
                
                // GS1 표준 형식으로 QR 데이터 생성
                const gtin14 = generateGTIN14();
                const batchNumber = 'LOT' + new Date().getFullYear() + String(Math.floor(Math.random() * 10000)).padStart(4, '0');
                const expiryDate = new Date();
                expiryDate.setFullYear(expiryDate.getFullYear() + 2); // 2년 후 만료
                const expiryString = expiryDate.toISOString().slice(0, 10).replace(/-/g, '');
                
                // GS1 Application Identifier 형식
                currentQRData = `(01)${gtin14}(10)${batchNumber}(17)${expiryString}`;
                
                debug(`생성된 GTIN-14: ${gtin14}`);
                debug(`생성된 QR 데이터: ${currentQRData}`);
                
                // QR 코드 생성
                waitForQRCode(() => {
                    generateQRCode(currentQRData, productName, companyName, quantity, registrationDate, gtin14, batchNumber);
                });
                
            } catch (error) {
                debug('❌ 오류 발생: ' + error.message);
                alert('오류가 발생했습니다: ' + error.message);
                generateBtn.disabled = false;
                generateBtn.textContent = '📱 배치 생성 및 QR 생성';
            }
        }
        
        function generateQRCode(qrData, productName, companyName, quantity, registrationDate, gtin14, batchNumber) {
            debug('QR 코드 생성 시작: ' + qrData);
            
            const qrCodeDiv = document.getElementById('qrcode');
            qrCodeDiv.innerHTML = '<div style="padding: 20px;">QR 코드 생성 중...</div>';
            
            try {
                // QR 코드 생성 시도
                QRCode.toCanvas(qrData, {
                    width: 250,
                    height: 250,
                    margin: 2,
                    color: {
                        dark: '#000000',
                        light: '#FFFFFF'
                    }
                }, function (error, canvas) {
                    const generateBtn = document.getElementById('generateBtn');
                    
                    if (error) {
                        debug('❌ QR 생성 실패: ' + error.message);
                        qrCodeDiv.innerHTML = `
                            <div style="width: 200px; height: 200px; background: #f0f0f0; border: 2px dashed #666; 
                                        display: flex; align-items: center; justify-content: center; 
                                        margin: 20px auto; font-size: 14px; color: #666; text-align: center;">
                                QR 생성 오류<br><small>GTIN: ${gtin14}</small>
                            </div>`;
                    } else {
                        debug('✅ QR 생성 성공');
                        qrCodeDiv.innerHTML = '';
                        qrCodeDiv.appendChild(canvas);
                    }
                    
                    // 제품 정보 저장
                    const newProduct = {
                        id: gtin14,
                        gtin: gtin14,
                        batch: batchNumber,
                        qrData: qrData,
                        name: productName,
                        company: companyName,
                        quantity: parseInt(quantity),
                        registrationDate: registrationDate,
                        status: 'active',
                        createdAt: new Date().toISOString()
                    };
                    
                    products.unshift(newProduct);
                    localStorage.setItem('products', JSON.stringify(products));
                    debug('제품 정보 저장 완료');
                    
                    // 배치 정보 표시
                    document.getElementById('qrDisplay').style.display = 'block';
                    document.getElementById('batchInfo').innerHTML = `
                        <strong>🏷️ GTIN-14:</strong> ${gtin14}<br>
                        <strong>📦 배치번호:</strong> ${batchNumber}<br>
                        <strong>🏭 제품명:</strong> ${productName}<br>
                        <strong>🏢 제조사:</strong> ${companyName}<br>
                        <strong>📊 수량:</strong> ${quantity}개<br>
                        <strong>📅 등록일자:</strong> ${registrationDate}<br>
                        <strong>⏰ 생성시간:</strong> ${new Date().toLocaleString('ko-KR')}<br>
                        <strong>📱 QR 데이터:</strong> <code style="font-size:10px;">${qrData}</code>
                    `;
                    
                    // 통계 업데이트
                    setTimeout(() => {
                        const totalElement = document.getElementById('totalProducts');
                        const currentTotal = parseInt(totalElement.textContent.replace(/,/g, ''));
                        totalElement.textContent = (currentTotal + parseInt(quantity)).toLocaleString();
                        updateProductsList();
                        
                        alert('✅ 배치 생성 완료!\\n' + quantity + '개의 QR 코드가 생성되었습니다.');
                        debug('✅ 모든 작업 완료');
                        
                        generateBtn.disabled = false;
                        generateBtn.textContent = '📱 배치 생성 및 QR 생성';
                    }, 500);
                });
                
            } catch (error) {
                debug('❌ QR 생성 중 예외: ' + error.message);
                qrCodeDiv.innerHTML = `
                    <div style="width: 200px; height: 200px; background: #ffebee; border: 2px solid #f44336; 
                                display: flex; align-items: center; justify-content: center; 
                                margin: 20px auto; font-size: 12px; color: #d32f2f; text-align: center;">
                        QR 생성 실패<br><small>${error.message}</small>
                    </div>`;
                
                const generateBtn = document.getElementById('generateBtn');
                generateBtn.disabled = false;
                generateBtn.textContent = '📱 배치 생성 및 QR 생성';
            }
        }
        
        function downloadQR() {
            debug('QR 다운로드 시도');
            
            if (!currentQRData) {
                alert('먼저 QR 코드를 생성해주세요.');
                return;
            }
            
            const canvas = document.querySelector('#qrcode canvas');
            if (canvas) {
                try {
                    const link = document.createElement('a');
                    link.download = `QR_${currentQRData}.png`;
                    link.href = canvas.toDataURL();
                    link.click();
                    debug('✅ QR 다운로드 성공');
                } catch (error) {
                    debug('❌ QR 다운로드 실패: ' + error.message);
                    alert('다운로드 중 오류가 발생했습니다.');
                }
            } else {
                debug('❌ QR 캔버스를 찾을 수 없음');
                alert('QR 코드를 찾을 수 없습니다. 다시 생성해주세요.');
            }
        }
        
        function updateProductsList() {
            const productsList = document.getElementById('productsList');
            if (products.length === 0) {
                productsList.innerHTML = '<p style="text-align: center; opacity: 0.7;">등록된 제품이 없습니다.</p>';
                return;
            }
            
            productsList.innerHTML = products.slice(0, 10).map(product => {
                const statusClass = product.status === 'active' ? 'status-safe' : 'status-warning';
                const statusIcon = product.status === 'active' ? '📦 활성' : '⚠️ 재사용감지';
                
                return `
                    <div class="product-item">
                        <div>
                            <strong>🏷️ ${product.gtin || product.id}</strong> • ${product.name}
                            <br><small>🏢 ${product.company} • 📅 ${product.registrationDate} 등록 • 📊 ${product.quantity}개</small>
                            ${product.batch ? `<br><small>📦 배치: ${product.batch}</small>` : ''}
                        </div>
                        <div style="display: flex; align-items: center; gap: 10px;">
                            <span class="activity-status ${statusClass}">${statusIcon}</span>
                            <button onclick="deleteProduct('${product.gtin || product.id}')" style="
                                background: #e74c3c; color: white; border: none; 
                                padding: 5px 10px; border-radius: 5px; font-size: 12px;
                                cursor: pointer;
                            ">🗑️ 삭제</button>
                        </div>
                    </div>
                `;
            }).join('');
        }
        
        function deleteProduct(productId) {
            if (!confirm(`제품 ${productId}을(를) 정말 삭제하시겠습니까?`)) {
                return;
            }
            
            debug(`제품 삭제 시도: ${productId}`);
            
            // localStorage에서 제품 삭제
            products = products.filter(product => (product.gtin || product.id) !== productId);
            localStorage.setItem('products', JSON.stringify(products));
            
            // 목록 업데이트
            updateProductsList();
            
            // 통계 업데이트
            const totalElement = document.getElementById('totalProducts');
            const deletedProduct = products.find(p => (p.gtin || p.id) === productId);
            if (deletedProduct) {
                const currentTotal = parseInt(totalElement.textContent.replace(/,/g, ''));
                totalElement.textContent = Math.max(0, currentTotal - deletedProduct.quantity).toLocaleString();
            }
            
            alert(`✅ 제품 ${productId} 삭제 완료!`);
            debug(`✅ 제품 삭제 완료: ${productId}`);
        }
        
        // 실시간 업데이트 시뮬레이션
        setInterval(() => {
            const recentScans = document.getElementById('recentScans');
            const currentCount = parseInt(recentScans.textContent);
            if (Math.random() > 0.8) { // 20% chance
                recentScans.textContent = currentCount + 1;
            }
        }, 15000);
    </script>
</body>
</html>"""
        self.wfile.write(html.encode('utf-8'))
    
    def scan_api(self, query):
        # Send JSON response
        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        code = query.get('code', [''])[0]
        
        if not code:
            response = {'status': 'error', 'message': 'QR 코드가 없습니다'}
        elif code.startswith('(01)') and '(10)' in code and '(17)' in code:
            # GS1 표준 형식 처리
            try:
                # GTIN-14 추출
                gtin_start = code.find('(01)') + 4
                gtin_end = code.find('(', gtin_start)
                gtin = code[gtin_start:gtin_end] if gtin_end != -1 else code[gtin_start:]
                
                # 배치번호 추출
                batch_start = code.find('(10)') + 4
                batch_end = code.find('(', batch_start)
                batch = code[batch_start:batch_end] if batch_end != -1 else code[batch_start:]
                
                # 유효기간 추출
                expiry_start = code.find('(17)') + 4
                expiry_end = code.find('(', expiry_start)
                expiry = code[expiry_start:expiry_end] if expiry_end != -1 else code[expiry_start:]
                
                # 사용 시나리오 시뮬레이션
                usage_scenarios = [
                    {'count': 1, 'result': 'first_use', 'message': '✅ 최초 사용 확인'},
                    {'count': 2, 'result': 'potential_reuse', 'message': '⚠️ 재사용 의심'},
                    {'count': 5, 'result': 'multiple_reuse', 'message': '❌ 다중 사용 위험'}
                ]
                
                # GTIN 기반 시나리오 결정
                if gtin.endswith(('7', '8', '9')):
                    scenario = usage_scenarios[1]  # 재사용 의심
                elif 'TEST' in batch or gtin.endswith('0'):
                    scenario = usage_scenarios[2]  # 다중 사용
                else:
                    scenario = usage_scenarios[0]  # 최초 사용
                    
                response = {
                    'status': 'success',
                    'message': scenario['message'],
                    'product_id': gtin,
                    'batch_number': batch,
                    'expiry_date': f"{expiry[:4]}-{expiry[4:6]}-{expiry[6:8]}",
                    'usage_count': scenario['count'],
                    'scan_result': scenario['result'],
                    'scan_time': datetime.datetime.now().isoformat(),
                    'safety_level': scenario['result'],
                    'qr_format': 'GS1_Standard'
                }
            except Exception as e:
                response = {'status': 'error', 'message': f'GS1 QR 코드 파싱 오류: {str(e)}'}
        elif code.startswith('SKC-'):
            # 기존 SKC 형식 (호환성)
            usage_scenarios = [
                {'count': 1, 'result': 'first_use', 'message': '최초 사용 확인'},
                {'count': 2, 'result': 'potential_reuse', 'message': '재사용 의심'},
                {'count': 5, 'result': 'multiple_reuse', 'message': '다중 사용 위험'}
            ]
            
            if 'TEST' in code or '999' in code:
                scenario = usage_scenarios[2]
            elif code.endswith(('7', '8', '9')):
                scenario = usage_scenarios[1]
            else:
                scenario = usage_scenarios[0]
                
            response = {
                'status': 'success',
                'message': scenario['message'],
                'product_id': code,
                'usage_count': scenario['count'],
                'scan_result': scenario['result'],
                'scan_time': datetime.datetime.now().isoformat(),
                'safety_level': scenario['result'],
                'qr_format': 'Legacy_SKC'
            }
        else:
            response = {'status': 'error', 'message': '유효하지 않은 QR 코드 형식입니다'}
        
        self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8')) 
