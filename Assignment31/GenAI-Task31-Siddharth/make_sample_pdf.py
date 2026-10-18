"""Generates data/sample_handbook.pdf (a multi-page sample PDF used for testing).
Optional - the PDF is already included.   Needs:  pip install reportlab
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer

SECTIONS = [
("1. Welcome to Nimbus Tech", [
"Nimbus Tech is a software company founded in 2015 with headquarters in Pune, India and a second office in Bengaluru. We build cloud-based analytics products for retail and logistics companies. This handbook explains how we work, what you can expect from us, and what we expect from you. It applies to all full-time and part-time employees, and a shorter version applies to interns.",
"Our mission is to make data useful for every team. We follow four values: customer first, build with honesty, keep learning, and take ownership. New employees receive a copy of this handbook on their first day and are asked to confirm in writing that they have read it within the first two weeks.",
"Every new employee is assigned an onboarding buddy for the first 90 days. The buddy is a colleague from the same team who answers day-to-day questions about tools, processes and culture. The probation period lasts six months, after which a confirmation letter is issued if performance has been satisfactory.",
]),
("2. Working Hours and Remote Work", [
"Standard working hours are 10:00 a.m. to 6:30 p.m., Monday to Friday, including a 45-minute lunch break. Employees are expected to be available for team meetings during core hours, which are 11:00 a.m. to 4:00 p.m. Outside core hours, teams may agree on flexible start and end times with their manager.",
"Nimbus Tech follows a hybrid model. Employees work from the office three days a week, normally Tuesday, Wednesday and Thursday, and may work remotely on Monday and Friday. Fully remote work for more than two consecutive weeks requires written approval from the department head and the HR team.",
"Employees who work remotely receive a one-time home-office allowance of 15,000 rupees to buy a chair, desk or monitor, and a monthly internet reimbursement of up to 1,000 rupees on submission of the bill. Company laptops must always be used for work and must be kept updated with the latest security patches.",
"Overtime is not expected on a regular basis. If a production incident requires work outside normal hours, the employee receives compensatory time off equal to the extra hours worked, to be taken within 30 days.",
]),
("3. Leave Policy", [
"Full-time employees receive 24 days of paid annual leave per calendar year, credited at the start of the year. Leave for employees who join mid-year is calculated proportionally. Up to 10 unused days can be carried forward to the next year; any additional unused days lapse on 31 March.",
"Sick leave: each employee is entitled to 12 days of paid sick leave per year. A medical certificate is required if sick leave exceeds three consecutive days. Sick leave cannot be carried forward or encashed.",
"Parental leave: mothers are entitled to 26 weeks of paid maternity leave, and fathers to 2 weeks of paid paternity leave, which can be taken within six months of the birth or adoption. Employees should inform HR at least 8 weeks before the expected start of maternity leave.",
"Public holidays: Nimbus Tech observes 12 public holidays per year, and the list is published every December for the following year. Employees may also choose two optional holidays from a list of regional festivals.",
"Leave requests must be submitted through the HR portal at least five working days in advance for leave longer than two days. Short leave of one or two days should be requested at least one day before, except in emergencies. Managers approve or decline leave requests within two working days.",
]),
("4. Compensation and Benefits", [
"Salaries are paid on the last working day of each month by bank transfer. Salary revisions take place once a year in April, based on the outcome of the annual performance review and company results.",
"Health insurance: every employee, their spouse and up to two children are covered by a group health insurance policy with a sum insured of 5 lakh rupees. Parents can be added to the policy at the employee's cost. The premium for the employee and immediate family is paid by the company.",
"Provident fund: both the employee and the company contribute 12 percent of basic salary to the provident fund. The company also provides a gratuity after five years of continuous service in line with applicable law.",
"Learning budget: each employee has an annual learning budget of 30,000 rupees for courses, certifications, books and conferences. Courses must be related to the employee's role and approved in advance by the manager. Employees who leave within 12 months of receiving reimbursement for a certification must repay the amount.",
"Referral bonus: employees who refer a candidate who is hired and completes six months receive a referral bonus of 20,000 rupees. The bonus is paid with the next monthly salary after the six-month mark.",
]),
("5. Code of Conduct", [
"We expect everyone to treat colleagues, customers and partners with respect. Harassment, discrimination and bullying of any kind are not tolerated. Concerns can be reported to the HR team or confidentially to the Ethics Committee through the email address ethics at nimbustech dot example. Retaliation against anyone who reports a concern in good faith is strictly prohibited.",
"Conflicts of interest: employees must disclose any outside business, consulting or investment that could conflict with their work at Nimbus Tech. Working for a competitor while employed at the company is not allowed. Gifts from customers or vendors worth more than 2,000 rupees must be declared to the manager and may need to be returned.",
"Confidentiality: customer data, source code and internal documents are confidential. They must not be shared outside the company or posted on public websites, including public code repositories and AI chat tools, without written permission. The confidentiality obligation continues after employment ends.",
]),
("6. IT and Information Security", [
"All company accounts must use multi-factor authentication. Passwords must be at least 14 characters long and must not be reused across systems. Employees must use the company password manager and must never share passwords by email or chat.",
"Lost or stolen devices must be reported to the IT helpdesk within two hours so that the device can be locked and wiped remotely. Personal USB drives must not be connected to company laptops. Software may only be installed from the approved software catalogue; requests for additional software are made through the helpdesk portal.",
"Security incidents such as phishing emails, suspicious logins or accidental data exposure must be reported immediately to the security team at the helpdesk. Reporting quickly is always appreciated, and employees will not be penalised for honest mistakes that are reported promptly.",
"Production systems are accessed only through the company VPN. Access to production data is granted on a least-privilege basis and reviewed every quarter by the security team.",
]),
("7. Performance Reviews and Growth", [
"Performance is reviewed twice a year, in October and in April. Each review includes a self-assessment, manager feedback and peer feedback from at least three colleagues. Ratings use a five-point scale from Needs Improvement to Outstanding. The April review determines salary revision and promotion eligibility.",
"Employees who receive a rating below Meets Expectations are placed on a 90-day performance improvement plan with clear goals and fortnightly check-ins with their manager. The aim of the plan is to support improvement, and most employees complete it successfully.",
"Promotions are considered once a year. To be eligible, an employee must have spent at least 12 months in their current role and must have received a rating of Exceeds Expectations or higher in the last review cycle.",
]),
("8. Travel and Expenses", [
"Business travel must be approved by the manager before booking. Flights should be booked at least 14 days in advance in economy class. Hotel stays are reimbursed up to 6,000 rupees per night in metro cities and 4,000 rupees per night in other cities.",
"A daily meal allowance of 1,200 rupees applies during business travel. Expense claims must be submitted within 30 days of the trip with original receipts through the expense portal. Claims submitted after 30 days will not be reimbursed unless the finance team approves an exception.",
"Local travel for client meetings is reimbursed at 12 rupees per kilometre for personal vehicles, or at actual cost for taxis and public transport. Alcohol is not reimbursable under any circumstances.",
]),
("9. Resignation and Exit", [
"Employees who wish to resign must submit a written resignation to their manager and HR. The notice period is 60 days for confirmed employees and 30 days during probation. The company may agree to a shorter notice period in exceptional cases, and unused leave up to 10 days may be encashed at the final settlement.",
"During the notice period the employee is expected to hand over responsibilities, document ongoing work and return all company property, including laptops, access cards and any equipment purchased with the home-office allowance in the last 12 months. The final settlement is processed within 45 days of the last working day. An exit interview with HR is conducted in the final week.",
]),
]

def main():
    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate("data/sample_handbook.pdf", pagesize=A4, title="Nimbus Tech Employee Handbook")
    story = [Paragraph("Nimbus Tech Employee Handbook", styles["Title"]),
             Paragraph("Sample document for the Conversational PDF Q&amp;A chatbot. Fictional company.", styles["Italic"]),
             Spacer(1, 18)]
    for i, (title, paras) in enumerate(SECTIONS):
        story.append(Paragraph(title, styles["Heading1"]))
        for p in paras:
            story += [Paragraph(p, styles["BodyText"]), Spacer(1, 8)]
        if i % 2 == 1:
            story.append(PageBreak())
    doc.build(story)

if __name__ == "__main__":
    main()
