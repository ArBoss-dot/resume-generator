from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase.pdfmetrics import stringWidth
import io
import json

# ============================ DEV - 1 ====================================================
class resume_generator:
    def __init__(self):
        self.file_name = "resume.pdf"
        self.page_width, self.page_height = A4
        self.bold_font                    = "Helvetica-Bold"
        self.body_font                    = "Times-Roman"
        self.header_font_size             = 24
        self.section_header_font_size     = 16
        self.body_font_size               = 12
        self.small_font_size              = 10
        self.highlight_color              = "#1F4E79"
        self.text_color                   = colors.black
        self.margin                       = 50
        self.line_spacing                 = 15
        self.pdf_canvas                   = canvas.Canvas(self.file_name, pagesize=A4)

# ============================ DEV - 2 ====================================================

    def add_line_space(self, additional_space=0):
        if(self.page_height <= self.margin):
            self.pdf_canvas.showPage()
            self.page_width, self.page_height = A4
            self.page_height -= self.margin
        else:
            self.page_height -= self.line_spacing + additional_space

# ============================ DEV - 3 ====================================================

    def add_colored_header_strip(self):
        self.pdf_canvas.setFillColor(self.highlight_color)
        self.pdf_canvas.rect(0, self.page_height-10, self.page_width, 10, fill=True, stroke=False)
        self.page_height -= 10

    def add_section_header(self, header_text):
        self.add_line_space(10)
        self.pdf_canvas.setFont(self.bold_font, self.section_header_font_size)
        self.pdf_canvas.drawString(self.margin, self.page_height, header_text, charSpace=1)
        self.add_line_space(-10)

# ============================ DEV - 4 ====================================================

    def add_paragraph(self, content):
        styles = ParagraphStyle(
                'Custom',
                fontName  = self.body_font,
                fontSize  = self.body_font_size,
                leading   = self.line_spacing,
                textColor = self.text_color,
                alignment = 4,
                )
        content_lines = content.split("\n")
        for content_line in content_lines:
            paragraph = Paragraph(content_line, styles)
            actual_width, actual_height = paragraph.wrap(self.page_width - self.margin*2, self.page_height)
            if(self.page_height <= self.margin + actual_height):
                self.pdf_canvas.showPage()
                self.page_width, self.page_height = A4
                self.page_height -= self.margin
            paragraph.drawOn(self.pdf_canvas, self.margin, self.page_height - actual_height)
            self.add_line_space(actual_height-15)

    def draw_rounded_rect(self, x, y, width, height, radius, fill_color, stroke_color):
        self.pdf_canvas.setFillColor(fill_color)
        self.pdf_canvas.setStrokeColor(stroke_color)
        self.pdf_canvas.roundRect(x, y, width, height, radius, fill=True, stroke=False)

# ============================ DEV - 1 ====================================================

    def add_header(self, user_details, website):
        self.pdf_canvas.setFillColor(self.text_color)
        self.pdf_canvas.setFont(self.bold_font, self.header_font_size)
        self.pdf_canvas.drawString(self.margin, self.page_height-self.margin, user_details.get("name"))
        self.add_line_space(self.margin + 5)
        self.pdf_canvas.setFont(self.body_font, self.body_font_size)
        self.pdf_canvas.drawString(self.margin, self.page_height, f"Email: {user_details.get("email_id")}")
        self.add_line_space()
        self.pdf_canvas.drawString(self.margin, self.page_height, f"Phone: {user_details.get("phone_no")}")
        self.add_line_space()
        self.pdf_canvas.drawString(self.margin, self.page_height, f"Linkedin: {user_details.get("linkedin")}")
        self.add_line_space()
        if website:
            self.pdf_canvas.drawString(self.margin, self.page_height, f"Website: {website}")
            self.add_line_space()
        self.pdf_canvas.setLineWidth(0.5)
        self.pdf_canvas.line(self.margin, self.page_height, self.page_width - self.margin, self.page_height)
        self.add_section_header("About")
        self.add_paragraph(user_details.get("about_user"))

# ============================ DEV - 2 ====================================================

    def add_skills(self, skills):
        self.add_section_header("Skills")
        self.add_line_space(10)
        self.pdf_canvas.setFont(self.body_font, self.small_font_size)
        skill_padding = 5
        skill_height  = 20
        x_position    = self.margin + 5
        for skill in skills:
            skill_width = stringWidth(skill, self.body_font, self.small_font_size) + 2 * skill_padding
            if x_position + skill_width > (self.page_width - (self.margin)):
                x_position = self.margin + 5
                self.add_line_space(10)
            fill_color = colors.Color(0.75, 0.75, 0.75, alpha=0.3)
            stroke_color = colors.Color(0.75, 0.75, 0.75, alpha=0.3)
            self.draw_rounded_rect(x_position, self.page_height, skill_width, skill_height, radius=8, fill_color=fill_color, stroke_color=stroke_color)
            self.pdf_canvas.setFillColor(colors.black)
            self.pdf_canvas.drawString(x_position + skill_padding, self.page_height + 6, skill)
            x_position += skill_width + 10

# ============================ DEV - 3 ====================================================

    def add_education(self, education_details):
        self.add_section_header("Education")
        for education in education_details:
            self.add_line_space(5)
            self.pdf_canvas.setFont(self.bold_font, self.body_font_size)
            self.pdf_canvas.drawString(self.margin, self.page_height, education.get("course"))
            self.add_line_space()
            self.pdf_canvas.setFont(self.body_font, self.body_font_size)
            self.pdf_canvas.drawString(self.margin, self.page_height, education.get("university"))
            self.add_line_space()
            self.pdf_canvas.drawString(self.margin, self.page_height, f"{education.get("from_date")} to {education.get("to_date")}")

# ============================ DEV - 4 ====================================================

    def add_work_experience(self, experience_details):
        self.add_section_header("Work Experience")
        for experience in experience_details:
            self.add_line_space()
            self.pdf_canvas.setFont(self.bold_font, self.body_font_size)
            self.pdf_canvas.drawString(self.margin, self.page_height, experience.get("designation"))
            self.add_line_space(2)
            self.pdf_canvas.setFont(self.body_font, self.body_font_size)
            self.pdf_canvas.drawString(self.margin, self.page_height, experience.get("organization"))
            self.add_line_space()
            if(experience.get("currently_working_here")):
                self.pdf_canvas.drawString(self.margin, self.page_height, f"{experience.get("from_date")} to present")
            else:
                self.pdf_canvas.drawString(self.margin, self.page_height, f"{experience.get("from_date")} to {experience.get("to_date")}")
            self.add_line_space(-10)
            self.add_paragraph(experience.get("about_role"))

    def save(self):
        self.pdf_canvas.showPage()
        self.pdf_canvas.save()




resume = resume_generator()
with open("user_data_template.json", "r") as template:
    user_data = json.load(template)

# resume.add_colored_header_strip()
# resume.add_header(user_data.get("user_details"),"")
# resume.add_skills(user_data.get("skills"))
# resume.add_education(user_data.get("education_details"))
# resume.add_work_experience(user_data.get("experience_details"))

resume.save()