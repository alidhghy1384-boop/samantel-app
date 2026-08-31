# -*- coding: utf-8 -*-
from flask import Flask, render_template_string, request, jsonify
import requests

app = Flask(__name__)

API_URL = "https://payment.samantel.ir/api/mediator/samantel/"

# ============================================================
# HTML صفحه (دیزاین خفن با محصولات)
# ============================================================
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>سامانتل - بسته نبسته</title>
    <link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;700;900&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
    <style>
        *{margin:0;padding:0;box-sizing:border-box}
        body{font-family:'Vazirmatn',sans-serif;background:#0d0d0d;min-height:100vh;display:flex;justify-content:center;align-items:center;padding:15px}
        .container{max-width:420px;width:100%;background:rgba(20,20,20,.92);border-radius:32px;padding:24px 20px 32px;box-shadow:0 30px 60px -15px rgba(0,0,0,.8),0 0 0 1px rgba(255,107,0,.12)inset;border:1px solid rgba(255,107,0,.06)}
        .header{text-align:center;margin-bottom:20px}
        .header .icon-box{width:64px;height:64px;background:linear-gradient(145deg,#ff6b00,#cc5500);border-radius:22px;display:inline-flex;align-items:center;justify-content:center;margin-bottom:10px;box-shadow:0 10px 28px -6px rgba(255,107,0,.35)}
        .header .icon-box i{font-size:32px;color:#fff}
        .header h1{font-size:24px;font-weight:900;background:linear-gradient(135deg,#ff7b2c,#ff5500);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
        .header p{color:#9ca3af;font-size:13px}
        .phone-section{background:#1a1a1a;border-radius:16px;padding:12px 16px;margin-bottom:18px;border:1px solid #2a2a2a;display:flex;align-items:center;gap:10px}
        .phone-section i{color:#ff6b00;font-size:18px}
        .phone-section label{color:#9ca3af;font-size:13px;font-weight:700}
        .phone-section input{flex:1;background:transparent;border:none;color:#f1f5f9;font-size:16px;font-family:'Vazirmatn',sans-serif;font-weight:500;direction:ltr;text-align:left;letter-spacing:1px;outline:none}
        .phone-section input::placeholder{color:#4b5563}
        .products-title{color:#d1d5db;font-size:15px;font-weight:700;margin-bottom:12px}
        .products-title i{color:#ff6b00}
        .product-card{background:#161616;border:2px solid #2a2a2a;border-radius:16px;padding:12px 14px;margin-bottom:10px;cursor:pointer;transition:all .3s;position:relative}
        .product-card.active{border-color:#ff6b00;background:#1f120a;box-shadow:0 0 20px rgba(255,107,0,.08)}
        .product-card .badge{position:absolute;top:-8px;right:-8px;background:#ff6b00;color:#fff;font-size:9px;font-weight:700;padding:2px 8px;border-radius:10px;display:none}
        .product-card.active .badge{display:block}
        .product-card .p-name{color:#f1f5f9;font-size:15px;font-weight:700}
        .product-card .p-details{color:#9ca3af;font-size:12px;margin-top:4px;line-height:1.6}
        .product-card .p-details span{color:#ff6b00;font-weight:700}
        .product-card .p-price{color:#ff6b00;font-size:16px;font-weight:900;margin-top:6px}
        .btn-primary{width:100%;padding:16px;background:linear-gradient(135deg,#ff6b00,#e65c00);border:none;border-radius:16px;color:#fff;font-size:17px;font-weight:700;font-family:'Vazirmatn',sans-serif;cursor:pointer;transition:all .3s;box-shadow:0 6px 24px -4px rgba(255,107,0,.4)}
        .btn-primary:hover:not(:disabled){transform:translateY(-2px);box-shadow:0 10px 32px -4px rgba(255,107,0,.55)}
        .btn-primary:disabled{opacity:.5;cursor:not-allowed}
        .btn-primary .spinner{display:none;width:22px;height:22px;border:3px solid rgba(255,255,255,.25);border-top-color:#fff;border-radius:50%;animation:spin .7s linear infinite;margin:0 auto}
        .btn-primary.loading .spinner{display:inline-block}
        .btn-primary.loading .btn-text{display:none}
        @keyframes spin{to{transform:rotate(360deg)}}
        .result-card{margin-top:18px;background:#161616;border-radius:18px;padding:18px 16px;border:1px solid #2a2a2a;display:none}
        .result-card.show{display:block}
        .result-card .success-icon{text-align:center;font-size:32px;color:#22c55e;margin-bottom:4px}
        .result-card .amount{text-align:center;font-size:18px;font-weight:900;color:#f1f5f9}
        .result-card .amount span{color:#ff6b00}
        .result-card .link-box{margin-top:12px;background:#0d0d0d;border-radius:12px;padding:10px 14px;border:1px solid #2a2a2a;word-break:break-all;font-size:12px;color:#d1d5db;direction:ltr;text-align:left;font-family:monospace;position:relative}
        .result-card .link-box .copy-btn{position:absolute;left:6px;top:50%;transform:translateY(-50%);background:#2a2a2a;border:none;border-radius:6px;padding:3px 10px;font-size:11px;color:#d1d5db;cursor:pointer;font-family:'Vazirmatn',sans-serif}
        .result-card .link-box .copy-btn:hover{background:#3a3a3a;color:#fff}
        .result-card .auto-open-info{text-align:center;color:#6b7280;font-size:12px;margin-top:10px}
        .result-card .auto-open-info i{color:#ff6b00}
        .error-msg{color:#ef4444;font-size:13px;text-align:center;margin-top:12px;display:none}
        .error-msg.show{display:block}
        .footer{margin-top:18px;text-align:center;font-size:11px;color:#4b5563}
        .footer i{color:#ff6b00}
        .toast-msg{position:fixed;bottom:30px;left:50%;transform:translateX(-50%);background:#1a1a1a;color:#fff;padding:12px 24px;border-radius:12px;font-size:14px;font-family:'Vazirmatn',sans-serif;box-shadow:0 8px 24px rgba(0,0,0,.5);z-index:999;max-width:90%;text-align:center;border:1px solid #2a2a2a}
        .loading-overlay{position:fixed;inset:0;background:rgba(0,0,0,.75);backdrop-filter:blur(8px);display:none;justify-content:center;align-items:center;flex-direction:column;z-index:1000;gap:16px}
        .loading-overlay.show{display:flex}
        .loading-overlay .big-spinner{width:50px;height:50px;border:4px solid #2a2a2a;border-top-color:#ff6b00;border-radius:50%;animation:spin .8s linear infinite}
        .loading-overlay .loading-text{color:#f1f5f9;font-size:16px;font-weight:700}
        .loading-overlay .loading-sub{color:#9ca3af;font-size:13px}
        .history-section{margin-top:18px;background:#161616;border-radius:18px;padding:14px 16px;border:1px solid #2a2a2a}
        .history-header{display:flex;justify-content:space-between;align-items:center;margin-bottom:8px}
        .history-header .title{color:#d1d5db;font-size:14px;font-weight:700}
        .history-header .title i{color:#ff6b00}
        .history-actions{display:flex;gap:8px}
        .history-actions button{background:#2a2a2a;border:none;color:#9ca3af;padding:3px 12px;border-radius:8px;font-size:11px;font-family:'Vazirmatn',sans-serif;cursor:pointer}
        .history-actions button:hover{background:#3a3a3a;color:#fff}
        .history-actions button.danger:hover{background:#7f1d1d;color:#fca5a5}
        .history-list{color:#9ca3af;font-size:12px;max-height:80px;overflow-y:auto;line-height:1.8}
        .history-list .empty{text-align:center;color:#4b5563;padding:8px 0}
        .history-list .item{padding:2px 0;border-bottom:1px solid #1a1a1a;display:flex;justify-content:space-between;font-size:11px}
        .history-list .item .h-date{color:#6b7280}
        .history-list .item .h-amount{color:#ff6b00;font-weight:700}
    </style>
</head>
<body>

<div class="loading-overlay" id="loadingOverlay">
    <div class="big-spinner"></div>
    <div class="loading-text">در حال دریافت لینک پرداخت...</div>
    <div class="loading-sub">لطفاً صبر کنید</div>
</div>

<div class="container">
    <div class="header">
        <div class="icon-box"><i class="fas fa-sim-card"></i></div>
        <h1>سامانتل</h1>
        <p>خرید بسته نبسته</p>
    </div>

    <div class="phone-section">
        <i class="fas fa-phone"></i>
        <label>شماره:</label>
        <input type="text" id="phoneInput" maxlength="11" value="09999846838" inputmode="numeric" placeholder="۰۹۹۹۱۲۳۴۵۶۷">
    </div>

    <div class="products-title"><i class="fas fa-box"></i> انتخاب بسته</div>

    <!-- محصول استاندارد -->
    <div class="product-card active" data-index="0">
        <span class="badge">پیش‌فرض</span>
        <div class="p-name">📦 Standard</div>
        <div class="p-details">
            اینترنت <span>6</span> گیگ &nbsp;|&nbsp; درون‌شبکه <span>800</span> دق &nbsp;|&nbsp; برون‌شبکه <span>80</span> دق &nbsp;|&nbsp; پیامک <span>100</span>
        </div>
        <div class="p-price">💰 ۳۳۴,۲۹۰ ریال</div>
    </div>

    <!-- محصول VIP -->
    <div class="product-card" data-index="1">
        <div class="p-name">⭐ VIP</div>
        <div class="p-details">
            اینترنت <span>6</span> گیگ &nbsp;|&nbsp; درون‌شبکه <span>800</span> دق &nbsp;|&nbsp; برون‌شبکه <span>200</span> دق &nbsp;|&nbsp; پیامک <span>200</span>
        </div>
        <div class="p-price">💰 ۳۹۶,۱۱۰ ریال</div>
    </div>

    <button class="btn-primary" id="submitBtn">
        <span class="btn-text"><i class="fas fa-arrow-left"></i> دریافت لینک پرداخت</span>
        <span class="spinner"></span>
    </button>

    <div class="error-msg" id="errorMsg"></div>

    <div class="result-card" id="resultCard">
        <div class="success-icon"><i class="fas fa-check-circle"></i></div>
        <div class="amount">💰 مبلغ کل: <span id="totalAmount">۰</span> ریال</div>
        <div class="link-box">
            <span id="paymentLink">https://payment.samantel.ir/pay/...</span>
            <button class="copy-btn" onclick="copyLink()">📋 کپی</button>
        </div>
        <div class="auto-open-info"><i class="fas fa-clock"></i> در حال باز کردن صفحه پرداخت...</div>
    </div>

    <div class="history-section">
        <div class="history-header">
            <div class="title"><i class="fas fa-history"></i> تاریخچه خرید</div>
            <div class="history-actions">
                <button onclick="showHistory()">🔄 نمایش</button>
                <button class="danger" onclick="clearHistory()">🗑️ پاک</button>
            </div>
        </div>
        <div class="history-list" id="historyList"><div class="empty">هیچ خریدی ثبت نشده</div></div>
    </div>

    <div class="footer"><i class="fas fa-lock"></i> اطلاعات شما محفوظ است</div>
</div>

<script>
    // ============================
    // محصولات (فقط ۲ تا)
    // ============================
    const PRODUCTS = [
        { name: 'Standard', data: 6, onnet: 800, offnet: 80, sms: 100, price: 334290 },
        { name: 'VIP', data: 6, onnet: 800, offnet: 200, sms: 200, price: 396110 }
    ];

    let selectedIndex = 0;
    let payUrl = '';
    let totalAmount = 0;

    // ============================
    // انتخاب محصول
    // ============================
    document.querySelectorAll('.product-card').forEach((card, index) => {
        card.addEventListener('click', function() {
            document.querySelectorAll('.product-card').forEach(c => c.classList.remove('active'));
            this.classList.add('active');
            selectedIndex = index;
            document.getElementById('resultCard').classList.remove('show');
            document.getElementById('errorMsg').classList.remove('show');
        });
    });

    // ============================
    // دریافت لینک پرداخت (از طریق سرور Flask)
    // ============================
    document.getElementById('submitBtn').addEventListener('click', function() {
        const btn = this;
        const phone = document.getElementById('phoneInput').value.trim();
        const errorMsg = document.getElementById('errorMsg');
        const resultCard = document.getElementById('resultCard');
        const linkSpan = document.getElementById('paymentLink');
        const totalSpan = document.getElementById('totalAmount');
        const overlay = document.getElementById('loadingOverlay');

        if (phone.length !== 11 || !/^\\d+$/.test(phone)) {
            errorMsg.textContent = '❌ شماره باید ۱۱ رقم باشد';
            errorMsg.classList.add('show');
            resultCard.classList.remove('show');
            return;
        }

        errorMsg.classList.remove('show');
        resultCard.classList.remove('show');

        btn.disabled = true;
        btn.classList.add('loading');
        overlay.classList.add('show');

        const product = PRODUCTS[selectedIndex];

        // ارسال درخواست به سرور Flask خودمون
        fetch('/api/buy', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                phone: phone,
                product: product
            })
        })
        .then(res => res.json())
        .then(data => {
            if (data.status === 'error') {
                throw new Error(data.message);
            }
            payUrl = data.payURL;
            totalAmount = data.total;

            saveHistory(phone, totalAmount, product.name);
            totalSpan.textContent = totalAmount.toLocaleString('fa-IR');
            linkSpan.textContent = payUrl;
            resultCard.classList.add('show');

            setTimeout(() => {
                window.open(payUrl, '_blank');
            }, 3000);

            resultCard.scrollIntoView({ behavior: 'smooth', block: 'center' });
        })
        .catch(err => {
            errorMsg.textContent = '❌ ' + err.message;
            errorMsg.classList.add('show');
        })
        .finally(() => {
            btn.disabled = false;
            btn.classList.remove('loading');
            overlay.classList.remove('show');
        });
    });

    // ============================
    // کپی لینک
    // ============================
    function copyLink() {
        if (!payUrl) return;
        if (navigator.clipboard && navigator.clipboard.writeText) {
            navigator.clipboard.writeText(payUrl)
                .then(() => showToast('✅ لینک کپی شد!'))
                .catch(() => fallbackCopy(payUrl));
        } else {
            fallbackCopy(payUrl);
        }
    }

    function fallbackCopy(text) {
        const ta = document.createElement('textarea');
        ta.value = text;
        ta.style.position = 'fixed';
        ta.style.opacity = '0';
        document.body.appendChild(ta);
        ta.select();
        try {
            document.execCommand('copy');
            showToast('✅ لینک کپی شد!');
        } catch {
            showToast('❌ کپی نشد، دستی کپی کنید');
        }
        document.body.removeChild(ta);
    }

    function showToast(msg) {
        const old = document.querySelector('.toast-msg');
        if (old) old.remove();
        const div = document.createElement('div');
        div.className = 'toast-msg';
        div.textContent = msg;
        document.body.appendChild(div);
        setTimeout(() => div.remove(), 2500);
    }

    // ============================
    // تاریخچه
    // ============================
    function saveHistory(phone, amount, productName) {
        let history = [];
        try {
            history = JSON.parse(localStorage.getItem('samantel_history') || '[]');
        } catch {}
        history.unshift({
            date: new Date().toLocaleString('fa-IR'),
            phone: phone,
            amount: amount,
            product: productName
        });
        if (history.length > 50) history = history.slice(0, 50);
        localStorage.setItem('samantel_history', JSON.stringify(history));
        showHistory();
    }

    function showHistory() {
        let history = [];
        try {
            history = JSON.parse(localStorage.getItem('samantel_history') || '[]');
        } catch {}
        const list = document.getElementById('historyList');
        if (history.length === 0) {
            list.innerHTML = '<div class="empty">هیچ خریدی ثبت نشده</div>';
            return;
        }
        list.innerHTML = history.slice(0, 15).map(item =>
            `<div class="item">
                <span class="h-date">${item.date}</span>
                <span class="h-amount">${item.product} - ${item.amount.toLocaleString('fa-IR')} ریال</span>
            </div>`
        ).join('');
    }

    function clearHistory() {
        if (confirm('آیا از پاک کردن تاریخچه اطمینان دارید؟')) {
            localStorage.removeItem('samantel_history');
            document.getElementById('historyList').innerHTML = '<div class="empty">هیچ خریدی ثبت نشده</div>';
            showToast('🗑️ تاریخچه پاک شد');
        }
    }

    // رویدادها
    document.getElementById('phoneInput').addEventListener('keydown', function(e) {
        if (e.key === 'Enter') document.getElementById('submitBtn').click();
    });

    document.getElementById('phoneInput').addEventListener('input', function() {
        this.value = this.value.replace(/\\D/g, '');
    });

    showHistory();
</script>

</body>
</html>
"""

# ============================================================
# مسیرهای Flask
# ============================================================
@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)


@app.route('/api/buy', methods=['POST'])
def buy():
    data = request.get_json()
    phone = data.get('phone')
    product = data.get('product')

    if not phone or len(phone) != 11:
        return jsonify({"status": "error", "message": "شماره باید ۱۱ رقم باشد"})

    try:
        # مرحله ۱: قیمت‌گیری
        price_data = {
            "method": "getpricenabaste",
            "MSISDN": phone,
            "duration": "30",
            "onnet": product["onnet"],
            "offnet": product["offnet"],
            "sms": product["sms"],
            "data": product["data"]
        }
        price_res = requests.post(API_URL, data=price_data).json()

        if price_res.get("errCode") != 0:
            return jsonify({"status": "error", "message": price_res.get("errDesc", "خطا در قیمت‌گیری")})

        fee = price_res["result"]["PricePlanFee"]
        tax = price_res["result"]["Tax"]
        total = int(fee) + int(tax)

        # مرحله ۲: دریافت لینک پرداخت
        pay_data = {
            "method": "buynabaste",
            "MSISDN": phone,
            "duration": "30",
            "onnet": product["onnet"],
            "offnet": product["offnet"],
            "sms": product["sms"],
            "data": product["data"],
            "fee": fee,
            "tax": tax,
            "gatewayId": "1"
        }
        pay_res = requests.post(API_URL, data=pay_data).json()

        if pay_res.get("errCode") != 0:
            return jsonify({"status": "error", "message": pay_res.get("errDesc", "خطا در دریافت لینک")})

        return jsonify({
            "status": "success",
            "payURL": pay_res["result"]["payURL"],
            "total": total
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


if __name__ == '__main__':
    print("✅ سرور روشن شد!")
    print("🌐 آدرس: http://127.0.0.1:5000")
    print("📱 برای استفاده با گوشی، آی‌پی سیستمت رو پیدا کن و به جای 127.0.0.1 بذار.")
    app.run(host='0.0.0.0', port=5000, debug=False)