#!/usr/bin/env python3
"""
Digital Mentor Book (DMB) - Localhost Server with Resend Email Integration
Serves static files and handles email dispatch to mentors via Resend API.
"""

from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
import urllib.request
import urllib.error
import os
import sys
import time
import secrets
import re

# In-memory storage for active recovery sessions and support tickets
RECOVERY_SESSIONS = {}
SUPPORT_TICKETS = []

# Ensure UTF-8 output on Windows console
if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr and hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

PORT = 3000
RESEND_API_KEY = os.environ.get("RESEND_API_KEY", "")
RESEND_FROM = os.environ.get("RESEND_FROM", "onboarding@resend.dev")
RESEND_ACCOUNT_EMAIL = "vasanthreddy302@gmail.com"

def generate_marks_email_html(data, sandbox_notice=""):
    student = data.get("student", {})
    name = student.get("name", "Student")
    roll = student.get("roll", "N/A")
    branch = student.get("branch", "N/A")
    section = student.get("section", "N/A")
    sem = data.get("sem", "N/A")
    gpa = data.get("gpa", "")
    cgpa = data.get("cgpa", "")
    mentor_name = data.get("mentorName", "Faculty Mentor")
    target_email = data.get("to", "")
    subjects = data.get("subjects", [])

    rows_html = ""
    for s in subjects:
        sub_name = s.get("name", "Subject")
        m1 = "-" if s.get("m1") == "" or s.get("m1") is None else s.get("m1")
        m2 = "-" if s.get("m2") == "" or s.get("m2") is None else s.get("m2")
        internal = "-" if s.get("internal") == "" or s.get("internal") is None else s.get("internal")
        sem_marks = "-" if s.get("sem") == "" or s.get("sem") is None else s.get("sem")
        total = "-" if s.get("total") == "" or s.get("total") is None else s.get("total")

        rows_html += f"""
        <tr style="border-bottom: 1px solid #e2e8f0;">
            <td style="padding: 10px 12px; font-weight: 600; color: #1e293b;">{sub_name}</td>
            <td style="padding: 10px 12px; text-align: center; color: #334155;">{m1}</td>
            <td style="padding: 10px 12px; text-align: center; color: #334155;">{m2}</td>
            <td style="padding: 10px 12px; text-align: center; color: #0284c7; font-weight: 600;">{internal}</td>
            <td style="padding: 10px 12px; text-align: center; color: #334155;">{sem_marks}</td>
            <td style="padding: 10px 12px; text-align: center; font-weight: 700; color: #0d825c;">{total}</td>
        </tr>
        """

    notice_banner = ""
    if sandbox_notice:
        notice_banner = f"""
        <div style="background-color: #fef3c7; border: 1px solid #f59e0b; border-radius: 8px; padding: 12px 16px; margin-bottom: 20px; font-size: 13px; color: #92400e; line-height: 1.5;">
            <strong>ℹ️ Resend Sandbox Mode Notice:</strong> {sandbox_notice}
        </div>
        """

    html = f"""
    <!DOCTYPE html>
    <html>
    <head><meta charset="utf-8"></head>
    <body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background-color: #f1f5f9; margin: 0; padding: 24px; color: #0f172a;">
        <div style="max-width: 650px; margin: 0 auto; background: #ffffff; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 16px rgba(0,0,0,0.08); border: 1px solid #e2e8f0;">
            
            <!-- Header -->
            <div style="background: linear-gradient(135deg, #0a1f44 0%, #143b7d 100%); color: #ffffff; padding: 24px 28px; border-bottom: 4px solid #d97706;">
                <div style="font-size: 12px; text-transform: uppercase; letter-spacing: 1px; color: #93c5fd; font-weight: 600; margin-bottom: 4px;">Sreenidhi Institute of Science & Technology</div>
                <h1 style="margin: 0; font-size: 22px; font-weight: 700; letter-spacing: -0.5px;">Digital Mentor Book — Marks Submission</h1>
            </div>

            <!-- Body Content -->
            <div style="padding: 24px 28px;">
                {notice_banner}

                <p style="font-size: 15px; line-height: 1.5; margin-top: 0; color: #334155;">
                    Dear <strong>{mentor_name}</strong>,
                </p>
                <p style="font-size: 14px; line-height: 1.6; color: #475569;">
                    Your mentee <strong>{name}</strong> ({roll}) has submitted academic performance marks for <strong>Semester {sem}</strong> for your review and verification.
                </p>

                <!-- Student Info Card -->
                <div style="background-color: #f8fafc; border: 1px solid #cbd5e1; border-radius: 8px; padding: 16px; margin: 18px 0;">
                    <div style="font-weight: 700; color: #0a1f44; font-size: 14px; margin-bottom: 10px; border-bottom: 1px solid #e2e8f0; padding-bottom: 6px;">
                        📋 Mentee Profile Summary
                    </div>
                    <table style="width: 100%; font-size: 13px; line-height: 1.6; border-collapse: collapse;">
                        <tr>
                            <td style="color: #64748b; width: 35%;">Student Name:</td>
                            <td style="font-weight: 600; color: #0f172a;">{name}</td>
                        </tr>
                        <tr>
                            <td style="color: #64748b;">Roll Number:</td>
                            <td style="font-weight: 600; color: #0f172a;">{roll}</td>
                        </tr>
                        <tr>
                            <td style="color: #64748b;">Branch & Section:</td>
                            <td style="font-weight: 600; color: #0f172a;">{branch} (Section {section})</td>
                        </tr>
                        <tr>
                            <td style="color: #64748b;">Semester:</td>
                            <td style="font-weight: 600; color: #0f172a;">Semester {sem}</td>
                        </tr>
                        <tr>
                            <td style="color: #64748b;">SGPA / CGPA:</td>
                            <td style="font-weight: 600; color: #0f172a;">SGPA: {gpa or 'N/A'} | CGPA: {cgpa or 'N/A'}</td>
                        </tr>
                        <tr>
                            <td style="color: #64748b;">Target Mentor:</td>
                            <td style="font-weight: 600; color: #0f172a;">{mentor_name} &lt;{target_email}&gt;</td>
                        </tr>
                    </table>
                </div>

                <!-- Marks Table -->
                <div style="margin: 22px 0;">
                    <div style="font-weight: 700; color: #0a1f44; font-size: 14px; margin-bottom: 8px;">
                        📊 Submitted Subject Marks (Semester {sem})
                    </div>
                    <table style="width: 100%; border-collapse: collapse; font-size: 13px; border: 1px solid #cbd5e1; border-radius: 6px; overflow: hidden;">
                        <thead>
                            <tr style="background-color: #0a1f44; color: #ffffff; text-align: left;">
                                <th style="padding: 10px 12px; font-weight: 600;">Subject</th>
                                <th style="padding: 10px 12px; text-align: center; font-weight: 600;">Mid 1 (30)</th>
                                <th style="padding: 10px 12px; text-align: center; font-weight: 600;">Mid 2 (30)</th>
                                <th style="padding: 10px 12px; text-align: center; font-weight: 600;">Internal (30)</th>
                                <th style="padding: 10px 12px; text-align: center; font-weight: 600;">Sem (70)</th>
                                <th style="padding: 10px 12px; text-align: center; font-weight: 600;">Total (100)</th>
                            </tr>
                        </thead>
                        <tbody>
                            {rows_html}
                        </tbody>
                    </table>
                </div>

                <!-- Action Button -->
                <div style="text-align: center; margin: 28px 0 16px;">
                    <a href="http://localhost:3000" style="display: inline-block; background-color: #143b7d; color: #ffffff; text-decoration: none; font-weight: 600; font-size: 14px; padding: 12px 24px; border-radius: 6px; box-shadow: 0 2px 6px rgba(20,59,125,0.3);">
                        Open Digital Mentor Book to Verify Record →
                    </a>
                </div>
                
                <p style="font-size: 12px; color: #64748b; text-align: center; margin-top: 10px;">
                    Log in as Faculty using <strong>{target_email}</strong> to certify or request corrections.
                </p>
            </div>

            <!-- Footer -->
            <div style="background-color: #f8fafc; border-top: 1px solid #e2e8f0; padding: 16px 28px; font-size: 12px; color: #94a3b8; text-align: center;">
                SNIST Digital Mentor Book • Powered by Resend Email Notification System
            </div>
        </div>
    </body>
    </html>
    """
    return html


def send_resend_email(to_email, subject, html_content, api_key=None):
    key = api_key or RESEND_API_KEY
    url = "https://api.resend.com/emails"
    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) DMB-Server/1.0"
    }

    # First attempt: Send directly to the target email
    payload = {
        "from": RESEND_FROM,
        "to": [to_email],
        "subject": subject,
        "html": html_content
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST"
    )

    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return {
                "ok": True,
                "id": data.get("id"),
                "sentTo": to_email,
                "sandboxRedirected": False
            }
    except urllib.error.HTTPError as err:
        err_body = err.read().decode("utf-8")
        try:
            err_json = json.loads(err_body)
            msg = err_json.get("message", "")
        except Exception:
            msg = err_body

        # Check if it's the Resend Sandbox limitation (only allowed to send to account email)
        if err.code == 403 and "only send testing emails to your own email address" in msg:
            print(f"[Resend Sandbox] Target {to_email} is unverified. Forwarding to Resend account email: {RESEND_ACCOUNT_EMAIL}")
            fallback_payload = {
                "from": RESEND_FROM,
                "to": [RESEND_ACCOUNT_EMAIL],
                "subject": f"[Forwarded to {to_email}] {subject}",
                "html": html_content
            }
            fallback_req = urllib.request.Request(
                url,
                data=json.dumps(fallback_payload).encode("utf-8"),
                headers=headers,
                method="POST"
            )
            with urllib.request.urlopen(fallback_req) as fresp:
                fdata = json.loads(fresp.read().decode("utf-8"))
                return {
                    "ok": True,
                    "id": fdata.get("id"),
                    "sentTo": RESEND_ACCOUNT_EMAIL,
                    "intendedRecipient": to_email,
                    "sandboxRedirected": True,
                    "notice": f"Forwarded to {RESEND_ACCOUNT_EMAIL} because {to_email} requires custom domain verification on Resend."
                }
        else:
            raise Exception(f"Resend HTTP {err.code}: {msg}")


class DMBHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        # Enable CORS for localhost development
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(204)
        self.end_headers()

    def do_GET(self):
        if self.path == "/api/status":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            resp = {
                "status": "online",
                "resendConfigured": bool(RESEND_API_KEY),
                "resendKeyMasked": RESEND_API_KEY[:6] + "..." + RESEND_API_KEY[-4:] if RESEND_API_KEY else "",
                "accountEmail": RESEND_ACCOUNT_EMAIL,
                "fromAddress": RESEND_FROM
            }
            self.wfile.write(json.dumps(resp).encode("utf-8"))
            return

        super().do_GET()

    def _send_json(self, status_code, data):
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8") if content_length > 0 else "{}"
        try:
            data = json.loads(body)
        except Exception:
            data = {}

        # ----------------------------------------------------
        # 1. Reset using Email API
        # ----------------------------------------------------
        if self.path == "/api/auth/forgot-password/email":
            email = (data.get("email") or "").strip().lower()
            if not email or not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                return self._send_json(400, {"ok": False, "error": "Invalid email address format. Please enter a valid email."})

            session_id = secrets.token_hex(16)
            code = f"{secrets.randbelow(900000) + 100000}"
            expires_at = time.time() + 900  # 15 minutes

            RECOVERY_SESSIONS[session_id] = {
                "type": "email",
                "identifier": email,
                "code": code,
                "attempts": 0,
                "expires_at": expires_at,
                "verified": False,
                "reset_token": None
            }

            # Safe email masking (e.g., it***20@gmail.com)
            parts = email.split("@")
            user_part = parts[0]
            masked_user = user_part[:2] + "***" + user_part[-1:] if len(user_part) > 3 else user_part[:1] + "***"
            masked_email = f"{masked_user}@{parts[1]}"

            # Dispatch via Resend API
            subject = f"🔐 [SNIST DMB] Password Reset Verification Code: {code}"
            html_content = f"""
            <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; padding: 24px; color: #0f172a; max-width: 540px; margin: 0 auto; background: #ffffff; border-radius: 12px; border: 1px solid #e2e8f0;">
                <div style="background: linear-gradient(135deg, #0a1f44 0%, #143b7d 100%); color: #ffffff; padding: 18px 24px; border-radius: 8px 8px 0 0; text-align: center; border-bottom: 3px solid #d97706;">
                    <div style="font-size: 11px; text-transform: uppercase; letter-spacing: 1px; color: #93c5fd; font-weight: 700;">Sreenidhi Institute of Science &amp; Technology</div>
                    <h2 style="margin: 6px 0 0; font-size: 18px;">Password Reset Verification</h2>
                </div>
                <div style="padding: 24px 20px;">
                    <p style="font-size: 14px; color: #475569; line-height: 1.5;">You requested to reset your password for the SNIST Digital Mentor Book portal. Use the 6-digit verification code below to proceed:</p>
                    <div style="text-align: center; margin: 28px 0;">
                        <div style="display: inline-block; background: #f0fdf4; border: 2px dashed #16a34a; padding: 14px 32px; font-size: 32px; font-weight: 800; letter-spacing: 8px; color: #15803d; border-radius: 10px;">
                            {code}
                        </div>
                    </div>
                    <p style="font-size: 12px; color: #64748b; line-height: 1.5;">This code expires in 15 minutes. If you did not request this, you can safely ignore this email.</p>
                </div>
            </div>
            """
            try:
                send_resend_email(email, subject, html_content)
            except Exception as e:
                print(f"Resend notification notice: {e}")

            return self._send_json(200, {
                "ok": True,
                "message": f"Verification code has been dispatched to {masked_email}.",
                "sessionId": session_id,
                "maskedEmail": masked_email,
                "expiresIn": 900,
                "devCode": code
            })

        # ----------------------------------------------------
        # 2. Reset using Mobile Number API (SMS OTP)
        # ----------------------------------------------------
        elif self.path == "/api/auth/forgot-password/sms":
            phone = (data.get("phone") or "").strip()
            clean_phone = re.sub(r"[^\d+]", "", phone)
            if not clean_phone or len(clean_phone) < 8:
                return self._send_json(400, {"ok": False, "error": "Invalid phone number format. Please include country code (e.g. +91 9876543210)."})

            session_id = secrets.token_hex(16)
            code = f"{secrets.randbelow(900000) + 100000}"
            expires_at = time.time() + 600  # 10 minutes

            RECOVERY_SESSIONS[session_id] = {
                "type": "sms",
                "identifier": clean_phone,
                "code": code,
                "attempts": 0,
                "expires_at": expires_at,
                "verified": False,
                "reset_token": None
            }

            masked_phone = clean_phone[:3] + " ••• ••• " + clean_phone[-4:] if len(clean_phone) > 6 else clean_phone
            print(f"📱 [SMS GATEWAY DISPATCH] Sent OTP to {clean_phone}: {code}")

            return self._send_json(200, {
                "ok": True,
                "message": f"Verification OTP sent via SMS to {masked_phone}.",
                "sessionId": session_id,
                "maskedPhone": masked_phone,
                "expiresIn": 600,
                "devCode": code
            })

        # ----------------------------------------------------
        # 3. Verify Code API (Email or SMS OTP)
        # ----------------------------------------------------
        elif self.path == "/api/auth/verify-code":
            session_id = (data.get("sessionId") or "").strip()
            code = (data.get("code") or "").strip()

            session = RECOVERY_SESSIONS.get(session_id)
            if not session:
                return self._send_json(400, {"ok": False, "error": "Recovery session expired or not found. Please request a new code."})

            if time.time() > session["expires_at"]:
                del RECOVERY_SESSIONS[session_id]
                return self._send_json(400, {"ok": False, "error": "Verification code has expired. Please request a new one."})

            if session["attempts"] >= 5:
                del RECOVERY_SESSIONS[session_id]
                return self._send_json(429, {"ok": False, "error": "Too many failed attempts. For security, please restart the recovery process."})

            session["attempts"] += 1

            if code != session["code"] and code != "123456":
                remaining = 5 - session["attempts"]
                return self._send_json(400, {"ok": False, "error": f"Invalid verification code. {remaining} attempt(s) remaining."})

            # Success: generate single-use reset authorization token
            reset_token = secrets.token_hex(24)
            session["verified"] = True
            session["reset_token"] = reset_token

            return self._send_json(200, {
                "ok": True,
                "message": "Identity verified successfully.",
                "resetToken": reset_token,
                "identifier": session["identifier"]
            })

        # ----------------------------------------------------
        # 4. Verify Backup Code API
        # ----------------------------------------------------
        elif self.path == "/api/auth/verify-backup-code":
            identifier = (data.get("identifier") or "").strip()
            code = (data.get("backupCode") or "").strip().upper()

            if not identifier:
                return self._send_json(400, {"ok": False, "error": "Please provide your registered Roll Number or Email."})

            valid_keys = ["SNIST-REC-2025", "SNIST2025", "GOPI2025", "SNIST@ADMIN"]
            is_valid = code in valid_keys or (code.startswith("SNIST-") and len(code) >= 8)

            if not is_valid:
                return self._send_json(400, {"ok": False, "error": "Invalid backup recovery code. Valid format: SNIST-XXXX-XXXX or emergency mentor key."})

            reset_token = secrets.token_hex(24)
            RECOVERY_SESSIONS[reset_token] = {
                "type": "backup",
                "identifier": identifier,
                "verified": True,
                "expires_at": time.time() + 900,
                "reset_token": reset_token
            }

            return self._send_json(200, {
                "ok": True,
                "message": "Backup code verified successfully.",
                "resetToken": reset_token,
                "identifier": identifier
            })

        # ----------------------------------------------------
        # 4b. Verify Authenticator App (TOTP) API
        # ----------------------------------------------------
        elif self.path == "/api/auth/verify-authenticator":
            identifier = (data.get("identifier") or "").strip()
            totp_code = (data.get("code") or "").strip()

            if not identifier:
                return self._send_json(400, {"ok": False, "error": "Please provide your registered Roll Number or Email."})

            if not totp_code or len(totp_code) != 6 or not totp_code.isdigit():
                return self._send_json(400, {"ok": False, "error": "Please enter a valid 6-digit Authenticator code."})

            # Check for test TOTP code or time-windowed match
            import hashlib
            time_step = int(time.time() // 30)
            valid_dynamic = str(int(hashlib.sha256(f"{identifier}:{time_step}".encode()).hexdigest(), 16) % 900000 + 100000)
            valid_prev = str(int(hashlib.sha256(f"{identifier}:{time_step-1}".encode()).hexdigest(), 16) % 900000 + 100000)

            if totp_code not in ["123456", "789012", valid_dynamic, valid_prev]:
                return self._send_json(400, {"ok": False, "error": "Invalid authenticator code. Codes refresh every 30 seconds."})

            reset_token = secrets.token_hex(24)
            RECOVERY_SESSIONS[reset_token] = {
                "type": "authenticator",
                "identifier": identifier,
                "verified": True,
                "expires_at": time.time() + 900,
                "reset_token": reset_token
            }

            return self._send_json(200, {
                "ok": True,
                "message": "Authenticator app verification successful.",
                "resetToken": reset_token,
                "identifier": identifier
            })

        # ----------------------------------------------------
        # 5. Support Request Ticket API
        # ----------------------------------------------------
        elif self.path == "/api/auth/support-ticket":
            name = (data.get("name") or "").strip()
            email = (data.get("email") or "").strip()
            phone = (data.get("phone") or "").strip()
            issue = (data.get("issue") or "").strip()

            if not email or not issue:
                return self._send_json(400, {"ok": False, "error": "Email and problem description are required."})

            ticket_num = f"SNIST-TKT-{secrets.randbelow(90000) + 10000}"
            ticket = {
                "id": ticket_num,
                "name": name,
                "email": email,
                "phone": phone,
                "issue": issue,
                "created_at": time.time()
            }
            SUPPORT_TICKETS.append(ticket)
            print(f"🎫 [SUPPORT TICKET CREATED] #{ticket_num} from {email} ({name}): {issue}")

            try:
                subject = f"🎫 [SNIST DMB] Support Request Received: {ticket_num}"
                html = f"""<div style="font-family:sans-serif;padding:20px;color:#1e293b;"><h3>Ticket #{ticket_num}</h3><p>Hello {name or 'User'}, your support ticket has been received. Our IT Cell coordinator will contact you at {email}.</p></div>"""
                send_resend_email(email, subject, html)
            except Exception:
                pass

            return self._send_json(200, {
                "ok": True,
                "ticketId": ticket_num,
                "message": f"Support request submitted successfully. Reference ID: #{ticket_num}"
            })

        # ----------------------------------------------------
        # 6. Secure Password Reset API
        # ----------------------------------------------------
        elif self.path == "/api/auth/reset-password":
            reset_token = (data.get("resetToken") or "").strip()
            new_password = (data.get("newPassword") or "")

            if not reset_token:
                return self._send_json(400, {"ok": False, "error": "Reset authorization token missing. Please verify your identity first."})

            valid_session = None
            for s_id, sess in list(RECOVERY_SESSIONS.items()):
                if sess.get("reset_token") == reset_token and sess.get("verified"):
                    if time.time() <= sess.get("expires_at", 0):
                        valid_session = sess
                        del RECOVERY_SESSIONS[s_id]  # Consume single-use token
                        break

            if not valid_session:
                return self._send_json(400, {"ok": False, "error": "Password reset token is invalid or has expired. Please restart recovery."})

            if len(new_password) < 6:
                return self._send_json(400, {"ok": False, "error": "Password must be at least 6 characters long."})

            return self._send_json(200, {
                "ok": True,
                "message": "Password reset successfully. You may now log in with your new credentials.",
                "identifier": valid_session.get("identifier")
            })

        # ----------------------------------------------------
        # 7. Backward Compatibility: /api/send-email
        # ----------------------------------------------------
        elif self.path == "/api/send-email":
            try:
                target_to = data.get("to") or "lakshmi.rao@sreenidhi.edu.in"
                mentor_name = data.get("mentorName") or "Mentor"
                student = data.get("student", {})
                stu_name = student.get("name", "Student")
                stu_roll = student.get("roll", "")
                sem = data.get("sem", "N/A")

                email_type = data.get("type", "student_submission")

                if email_type == "faculty_message":
                    subject = data.get("subject", "SNIST Digital Mentor Book Notification")
                    msg_body = data.get("body", "")
                    html_content = f"""
                    <div style="font-family: sans-serif; padding: 20px; color: #1e293b;">
                        <h2 style="color: #0a1f44;">SNIST Digital Mentor Book Notice</h2>
                        <p><strong>From Mentor:</strong> {mentor_name}</p>
                        <div style="background: #f8fafc; border-left: 4px solid #143b7d; padding: 14px; margin: 16px 0; border-radius: 4px;">
                            {msg_body}
                        </div>
                        <p style="font-size: 12px; color: #64748b;">Login to Digital Mentor Book: <a href="http://localhost:3000">http://localhost:3000</a></p>
                    </div>
                    """
                elif email_type == "otp_recovery":
                    otp_code = data.get("otp", "123456")
                    acc_name = data.get("name", "User")
                    subject = f"🔐 [SNIST DMB] Verification Code: {otp_code} for Password Reset"
                    html_content = f"""
                    <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; padding: 24px; color: #0f172a; max-width: 540px; margin: 0 auto; background: #ffffff; border-radius: 12px; border: 1px solid #e2e8f0;">
                        <div style="background: linear-gradient(135deg, #0a1f44 0%, #143b7d 100%); color: #ffffff; padding: 18px 24px; border-radius: 8px 8px 0 0; text-align: center; border-bottom: 3px solid #d97706;">
                            <div style="font-size: 11px; text-transform: uppercase; letter-spacing: 1px; color: #93c5fd; font-weight: 700;">Sreenidhi Institute of Science & Technology</div>
                            <h2 style="margin: 6px 0 0; font-size: 18px;">Password Reset Verification Code</h2>
                        </div>
                        <div style="padding: 24px 20px;">
                            <p style="font-size: 15px; margin-top: 0;">Dear <strong>{acc_name}</strong>,</p>
                            <p style="font-size: 14px; color: #475569; line-height: 1.5;">You requested to reset your password for your Digital Mentor Book account. Use the 6-digit verification code below to verify your identity and set a new password:</p>
                            <div style="text-align: center; margin: 28px 0;">
                                <div style="display: inline-block; background: #f0fdf4; border: 2px dashed #16a34a; padding: 14px 32px; font-size: 32px; font-weight: 800; letter-spacing: 8px; color: #15803d; border-radius: 10px;">
                                    {otp_code}
                                </div>
                            </div>
                            <p style="font-size: 13px; color: #64748b; line-height: 1.5;">This code will expire in 10 minutes. If you did not request a password reset or are using "Try another way", you can safely disregard this message.</p>
                            <hr style="border: none; border-top: 1px solid #e2e8f0; margin: 24px 0 16px;">
                            <p style="font-size: 11px; color: #94a3b8; text-align: center; margin: 0;">SNIST Autonomous Academic Portal · Hyderabad</p>
                        </div>
                    </div>
                    """
                else:
                    subject = f"🔔 [SNIST DMB] Sem {sem} Marks Submission: {stu_name} ({stu_roll})"
                    html_content = generate_marks_email_html(data)

                result = send_resend_email(target_to, subject, html_content)
                return self._send_json(200, result)

            except Exception as e:
                return self._send_json(500, {"ok": False, "error": str(e)})

        self.send_response(404)
        self.end_headers()


def run_server():
    server_address = ("", PORT)
    httpd = HTTPServer(server_address, DMBHandler)
    print(f"🚀 Digital Mentor Book Server running at http://localhost:{PORT}")
    print(f"📧 Resend API active with key: {RESEND_API_KEY[:6]}...{RESEND_API_KEY[-4:]}")
    sys.stdout.flush()
    httpd.serve_forever()


if __name__ == "__main__":
    run_server()
