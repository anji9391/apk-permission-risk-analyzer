from flask import Flask, render_template, request, jsonify
from androguard.core.apk import APK

import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

RISKY_PERMISSIONS = {
    "android.permission.READ_SMS": "High",
    "android.permission.SEND_SMS": "High",
    "android.permission.RECORD_AUDIO": "High",
    "android.permission.CAMERA": "Medium",
    "android.permission.ACCESS_FINE_LOCATION": "Medium",
    "android.permission.READ_CONTACTS": "Medium",
}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        apk_file = request.files["apk"]
        path = os.path.join(UPLOAD_FOLDER, apk_file.filename)
        apk_file.save(path)

        apk = APK(path)
        permissions = apk.get_permissions()

        report = []
        for p in permissions:
            report.append({
                "permission": p,
                "risk": RISKY_PERMISSIONS.get(p, "Low")
            })

        return jsonify({
            "app_name": apk.get_app_name(),
            "package_name": apk.get_package(),
            "total_permissions": len(permissions),
            "permissions": report
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

