Digital Mentor Book — Sreenidhi Institute of Science & Technology (SNIST)


Official Listed Branches (from SNIST Examination Timetable):
1. DATA SCIENCE (CSE)
2. ARTIFICIAL INTELLIGENCE AND MACHINE LEARNING (CSE)
3. COMPUTER SCIENCE AND ENGINEERING
4. CYBER SECURITY (CSE)
5. INTERNET OF THINGS (CSE)
6. INFORMATION TECHNOLOGY
7. ELECTRONICS AND COMPUTER ENGINEERING (ECM)
8. ELECTRONICS AND COMMUNICATION ENGINEERING
9. ELECTRICAL AND ELECTRONICS ENGINEERING
10. MECHANICAL ENGINEERING
11. CIVIL ENGINEERING

Mentor Name & Section:
- Option to enter/edit Faculty Mentor Name directly in Registration and in Profile
- Option to choose Section from Section A to Section Z

Student Profile & Demographics:
- Explicit "Name of the student" field (editable, validated)
- "Gender" selection (Female, Male, Other, Prefer not to say)
- Tracked across Profile, Dashboard, Mentee lists, and Printable PDF Book

Academic Performance Format:
- Handwritten Mentor Table: [Subject Names | Mid 1 | Mid 2 | Internal | Sem Marks | Total]
- Direct Entry of Internal Marks: Enter 0-30 directly just like Mid 1, Mid 2, and Sem Marks
- ⚡ Auto-calculate Internals button: Convenience 1-click option to auto-fill (Mid 1 + Mid 2) / 2
- Dedicated Total Marks: (Internal + Sem Marks out of 100) with letter grades (O, A+, A, B+, B, C, F)
- Real-time interactive calculation as student or mentor types
- Semester Summary / Totals footer (Average Mid 1, Average Mid 2, Total Internal, Total Sem Exam, Grand Total & Percentage)
- ⚡ Auto-calculate GPA button to automatically derive SGPA from Total marks
- Add Subject / Remove Subject / Reset to Branch Curriculum

Mentor Email Verification, Submission Tracking & Email Messaging:
- Student Submission Visibility Resolution:
    • Cross-Tab Real-Time Sync: Added automatic localStorage cross-tab listener (`window.storage`) so when a student submits in one browser tab/window, the faculty portal in another tab/window updates immediately without manual reload.
    • Dual-Scope Submissions View:
        - "👤 My Direct Mentees": Filtered to Sir's exact email and assigned name.
        - "🌐 All College Submissions": Toggle to view all submitted records across SNIST, ensuring no submission is missed due to minor email typos or alternate mentor address entries.
    • "⚡ Link to Me (Claim Mentee)": If a student submitted under an alternate mentor email, Sir can click one button to immediately link the student to their mentee list.
    • Transparent Submission Target: Student view clearly displays the exact destination mentor email with a 1-click update button before submitting.
    • Validation Toast: Clear alerts if no subject marks are filled before submitting.

- Faculty Send Message & Email to Student Feature:
    • Dedicated "📧 Send Message & Email to Student" Card on Faculty Dashboard:
        - Enter student email or select from autocomplete datalist.
        - Dynamic student record badge showing matching roll number and student name.
        - Quick template buttons: "📝 Pending Marks Reminder", "⏰ Urgent Submission Deadline", "🏛️ Cabin Counseling Call".
        - 3 Send / Dispatch Actions:
            1. 🚀 Send Portal Message & Trigger Mail to Student (Delivers urgent portal notice + launches mail client).
            2. 🌐 Open in Gmail (Opens pre-filled compose window in Gmail Web).
            3. 📧 Open in Outlook / Mail Client (Launches native mail client via mailto:).
    • Table Quick Actions:
        - Direct "📧 Mail Student" button on every row in both "📥 Submitted Semesters" and "⚠️ Pending / Unsubmitted Students" tables.
    • Student Side:
        - Student profile tracks official student email (e.g., student.roll@sreenidhi.edu.in).
        - Urgent notice banner on Student Dashboard features a direct "✉️ Reply to Sir via Email" button.

Faculty Mentor Remarks & Counseling System:
- Enter Remarks Across Multiple Touchpoints:
    • 💬 Remarks Modal: Accessible via direct "💬 Remarks" button in:
        1. "📥 Submitted Semesters Awaiting Verification & Remarks" table.
        2. "⚠️ Pending / Unsubmitted Students" table (post guidance/remarks even before student submits!).
        3. "👥 All Mentees Roster" table.
        4. "👨‍🏫 Mentee Review & Verification" page.
    • Dedicated Dashboard Card: "💬 Enter & Post Faculty Mentor Remarks to Student" on Faculty Dashboard with student autocomplete, target scope selection, and quick templates.
    • ⚡ 1-Click Mentor Templates: "Outstanding Academic Performance", "Good Progress / Focus on Internals", "Attendance Below Benchmark Warning", "Cabin Counseling Completed", etc.
    • Real-Time Multi-Scope Remarks:
        - Specific Semester Record Remarks (attached to semester verification & marks).
        - Overall Counseling & Academic Observation (student-level guidance).
    • Student Visibility:
        - Real-time portal notification delivered immediately.
        - Displayed prominently on Student Dashboard, Mentor Remarks tab (`rem`), semester cards, and printed PDF book.

Student Admission Entry Pathway (Regular vs Lateral Entry):
- Choose Regular or Lateral Entry at Record Entering Side:
    • Dedicated switcher card at the top of Academic Records page (`recView`).
    • 1-Click interactive buttons: "📘 Regular Entry (Sem 1–8)" vs. "⚡ Lateral Entry (Sem 3–8)".
    • Informative banner explaining exemption: For Lateral Entry students (direct 2nd year admission via ECET/Diploma), Semesters 1 and 2 are exempted, and the mentor book automatically starts tracking from Semester 3 through 8.
    • Instant live update: Switching entry type dynamically updates visible semester forms without page refresh.
    • Profile & PDF Integration: Also editable in Student Profile (`profView`) and certified with clear badges in mentee tables and printable PDF book.


Demo Logins:
- Faculty (by Official Email):
    • lakshmi.rao@sreenidhi.edu.in (Dr. Lakshmi Rao - Data Science & AI/ML)
    • arjun.iyer@sreenidhi.edu.in (Prof. Arjun Iyer - CSE & Cyber Security)
    • jaffar.sadiq@sreenidhi.edu.in (Dr. Jaffar Sadiq - IoT & IT)
    (Also accepts ID: F101, F102, F103 or Mentor Name)
- Student:
    • 23315A6701 / 23CS001 (Ananya Reddy - Sem 4 Submitted awaiting review; Sem 3 Certified with Remarks)
    • 24315A6714 / 24CS014 (Rahul Verma - Sem 3 Submitted awaiting review)
    • 23315A6799 (Zoya Khan - Pending / Not Entered; test sending email/message from Sir!)
- Admin: admin

Resend Email Notification Integration:
- API Key: Set via RESEND_API_KEY environment variable (or .env)
- Server: server.py (Runs on http://localhost:3000)
- Endpoints:
    • POST /api/send-email: Dispatches beautifully styled HTML marks submission notification to mentor
    • GET /api/status: Checks server health and Resend connection
- Automatic Sandbox Handling:
    • In Resend Free/Sandbox tier, emails to unverified domains are delivered to the registered account owner (vasanthreddy302@gmail.com).
    • Once a custom domain is verified at resend.com/domains, emails will be delivered directly to any mentor's official email address.


