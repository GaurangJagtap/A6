"""
generate_report_doc.py
Comprehensive generator for MLOps Assignment 6 Lab Report Word Document:
"Containerize a Machine Learning Model Using Docker and Expose It as a REST API"
Adheres strictly to the VIT Pune Department of AI & DS Lab Manual specifications.
"""

import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

DOC_DIR = r"C:\College\SEM 5\MLOPs\Assignment_6"
ALT_DOC_DIR = r"C:\College\SEM 5\MLOPs\Assignment_6\iris-ml-docker"
REPORT_FILENAME = "MLOps_Assignment_6_Containerize_ML_Model_Docker_Report.docx"
REPORT_ALT_FILENAME = "Assignment_Report.docx"

PRIMARY_COLOR = RGBColor(15, 76, 129)     # Deep Classic Blue (#0F4C81)
SECONDARY_COLOR = RGBColor(30, 64, 175)   # Subheading Blue (#1E40AF)
TEXT_COLOR = RGBColor(30, 41, 59)         # Dark Slate (#1E293B)
MUTED_COLOR = RGBColor(100, 116, 139)     # Slate Gray (#64748B)


def set_cell_background(cell, fill_hex):
    """Set background color of a table cell."""
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)


def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Set inner padding for a table cell (in twips: 20 twips = 1 pt)."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tcPr.append(tcMar)


def set_table_borders(table, color="D1D5DB", sz="4", val="single"):
    """Apply clean borders to a table."""
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:insideV w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:left w:val="none"/>'
        f'<w:right w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)


def add_heading_1(doc, text):
    """Add a styled Heading 1."""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = "Calibri"
    run.font.size = Pt(14)
    run.font.bold = True
    run.font.color.rgb = PRIMARY_COLOR
    return p


def add_heading_2(doc, text):
    """Add a styled Heading 2."""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = "Calibri"
    run.font.size = Pt(12)
    run.font.bold = True
    run.font.color.rgb = SECONDARY_COLOR
    return p


def add_body_paragraph(doc, text, bold_prefix="", space_after=4):
    """Add a standard body paragraph."""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = "Calibri"
        r_pre.font.size = Pt(11)
        r_pre.font.bold = True
        r_pre.font.color.rgb = PRIMARY_COLOR
    run = p.add_run(text)
    run.font.name = "Calibri"
    run.font.size = Pt(11)
    run.font.color.rgb = TEXT_COLOR
    return p


def add_bullet_point(doc, text, bold_prefix=""):
    """Add a bullet point paragraph."""
    p = doc.add_paragraph(style="List Paragraph")
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = "Calibri"
        r_pre.font.size = Pt(10.5)
        r_pre.font.bold = True
        r_pre.font.color.rgb = PRIMARY_COLOR
    run = p.add_run(text)
    run.font.name = "Calibri"
    run.font.size = Pt(10.5)
    run.font.color.rgb = TEXT_COLOR
    return p


def add_code_block(doc, code_text):
    """Add a clean shaded code box."""
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    cell = table.cell(0, 0)
    cell.width = Inches(6.5)
    set_cell_background(cell, "F8FAFC")
    set_cell_margins(cell, top=120, bottom=120, left=180, right=180)

    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:top w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>'
        f'<w:left w:val="single" w:sz="12" w:space="0" w:color="0F4C81"/>'
        f'<w:bottom w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>'
        f'<w:right w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(borders)

    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.05
    run = p.add_run(code_text.strip())
    run.font.name = "Consolas"
    run.font.size = Pt(8.5)
    run.font.color.rgb = RGBColor(30, 41, 59)
    doc.add_paragraph().paragraph_format.space_after = Pt(4)


def add_figure(doc, img_path, caption_text, width=Inches(5.8)):
    """Add a centered figure with an italicized caption."""
    if not os.path.exists(img_path):
        p_ph = doc.add_paragraph()
        p_ph.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_ph.paragraph_format.space_before = Pt(6)
        p_ph.paragraph_format.space_after = Pt(2)
        r = p_ph.add_run(f"[ Screenshot Placeholder: {caption_text} ]")
        r.font.name = "Calibri"
        r.font.size = Pt(10)
        r.font.italic = True
        r.font.color.rgb = MUTED_COLOR
        return

    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.paragraph_format.space_before = Pt(6)
    p_img.paragraph_format.space_after = Pt(2)
    p_img.paragraph_format.keep_with_next = True
    run_img = p_img.add_run()
    run_img.add_picture(img_path, width=width)

    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_before = Pt(0)
    p_cap.paragraph_format.space_after = Pt(8)
    run_cap = p_cap.add_run(caption_text)
    run_cap.font.name = "Calibri"
    run_cap.font.size = Pt(9.5)
    run_cap.font.italic = True
    run_cap.font.bold = True
    run_cap.font.color.rgb = MUTED_COLOR


def build_document():
    doc = docx.Document()

    # Set page margins to 1 inch
    section = doc.sections[0]
    section.top_margin = Inches(1.0)
    section.bottom_margin = Inches(1.0)
    section.left_margin = Inches(1.0)
    section.right_margin = Inches(1.0)
    section.header_distance = Inches(0.5)
    section.footer_distance = Inches(0.5)

    # -------------------------------------------------------------------------
    # COVER PAGE TABLE
    # -------------------------------------------------------------------------
    p_cover = doc.add_paragraph()
    p_cover.paragraph_format.space_after = Pt(4)
    run_c = p_cover.add_run("Cover Page")
    run_c.font.name = "Calibri"
    run_c.font.size = Pt(13)
    run_c.font.bold = True
    run_c.font.color.rgb = PRIMARY_COLOR

    cover_table = doc.add_table(rows=15, cols=2)
    cover_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    cover_table.autofit = False
    set_table_borders(cover_table, color="B0C4DE", sz="6", val="single")

    cover_table.columns[0].width = Inches(2.2)
    cover_table.columns[1].width = Inches(4.3)

    # Row 0: Logo & Institute Heading
    cell_logo = cover_table.cell(0, 0)
    cell_inst = cover_table.cell(0, 1)
    set_cell_background(cell_logo, "F8FAFC")
    set_cell_background(cell_inst, "F8FAFC")
    set_cell_margins(cell_logo, top=140, bottom=140, left=140, right=140)
    set_cell_margins(cell_inst, top=140, bottom=140, left=140, right=140)

    # Add Logo
    logo_path = os.path.join(DOC_DIR, "vit_logo.jpeg")
    p_l = cell_logo.paragraphs[0]
    p_l.alignment = WD_ALIGN_PARAGRAPH.CENTER
    if os.path.exists(logo_path):
        p_l.add_run().add_picture(logo_path, width=Inches(1.35))
    else:
        p_l.add_run("[VIT LOGO]")

    # Add Institute Header Text
    p_inst = cell_inst.paragraphs[0]
    p_inst.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r1 = p_inst.add_run("Bansilal Ramnath Agarwal Charitable Trust's\n")
    r1.font.name = "Calibri"
    r1.font.size = Pt(10)
    r1.font.color.rgb = MUTED_COLOR

    r2 = p_inst.add_run("Vishwakarma Institute of Technology, Pune\n")
    r2.font.name = "Calibri"
    r2.font.size = Pt(13)
    r2.font.bold = True
    r2.font.color.rgb = PRIMARY_COLOR

    r3 = p_inst.add_run("(An Autonomous Institute Affiliated to Savitribai Phule Pune University)")
    r3.font.name = "Calibri"
    r3.font.size = Pt(9.5)
    r3.font.italic = True
    r3.font.color.rgb = MUTED_COLOR

    # Table metadata rows
    table_data = [
        ("Department", "Department of Artificial Intelligence and Data Science"),
        ("Student Name", "Gaurang"),
        ("Class", "TY (Third Year B.Tech)"),
        ("Division", "B"),
        ("Roll No", "[Roll Number]"),
        ("PRN NO", "[PRN Number]"),
        ("Semester", "Semester V (Sem 5)"),
        ("Academic Year", "2026-27"),
        ("Subject Name & Code", "MLOps (AI3206C)"),
        ("Assignment No.", "6"),
        ("Title of Assignment", "Containerize a Machine Learning Model Using Docker and Expose It as a REST API"),
        ("Date of Performance", "12/11/2026"),
        ("Date of Submission", "21/11/2026"),
        ("", ""),
    ]

    for idx, (label, val) in enumerate(table_data, start=1):
        c0 = cover_table.cell(idx, 0)
        c1 = cover_table.cell(idx, 1)
        set_cell_margins(c0, top=70, bottom=70, left=120, right=120)
        set_cell_margins(c1, top=70, bottom=70, left=120, right=120)

        if idx % 2 == 1:
            set_cell_background(c0, "F8FAFC")
            set_cell_background(c1, "FFFFFF")
        else:
            set_cell_background(c0, "F1F5F9")
            set_cell_background(c1, "F8FAFC")

        p0 = c0.paragraphs[0]
        p0.paragraph_format.space_after = Pt(0)
        r0 = p0.add_run(label)
        r0.font.name = "Calibri"
        r0.font.size = Pt(10)
        r0.font.bold = True
        r0.font.color.rgb = PRIMARY_COLOR

        p1 = c1.paragraphs[0]
        p1.paragraph_format.space_after = Pt(0)
        r1 = p1.add_run(val)
        r1.font.name = "Calibri"
        r1.font.size = Pt(10)
        r1.font.color.rgb = TEXT_COLOR

    doc.add_page_break()

    # -------------------------------------------------------------------------
    # MAIN REPORT CONTENT
    # -------------------------------------------------------------------------

    # 1. Title
    add_heading_1(doc, "Assignment No. 6")
    add_body_paragraph(
        doc,
        "Containerize a Machine Learning Model Using Docker and Expose It as a REST API",
        bold_prefix="Title: "
    )

    # 2. Aim & Objectives
    add_heading_1(doc, "1. Aim and Objectives")
    add_body_paragraph(
        doc,
        "To develop an end-to-end Machine Learning pipeline that trains a classification model on the Iris dataset, packages it as a production-grade REST API using Flask, and containerizes the entire application using Docker to ensure reproducibility, environment isolation, and platform-independent deployment.",
        bold_prefix="Aim: "
    )
    add_heading_2(doc, "Objectives:")
    add_bullet_point(doc, "Train a RandomForestClassifier on the Scikit-learn Iris dataset with 80/20 stratified split.", bold_prefix="1. Model Training: ")
    add_bullet_point(doc, "Evaluate performance using Accuracy and Classification Report, saving the artifact as model.joblib.", bold_prefix="2. Evaluation & Serialization: ")
    add_bullet_point(doc, "Develop a robust Flask REST API exposing /, /health, and /predict endpoints with thorough input validation.", bold_prefix="3. API Engineering: ")
    add_bullet_point(doc, "Write an optimized Dockerfile adhering to multi-layer caching and lightweight footprint best practices.", bold_prefix="4. Docker Containerization: ")
    add_bullet_point(doc, "Build the Docker image (iris-model-api:1.0) and run the container mapping port 5000.", bold_prefix="5. Image & Container Lifecycle: ")
    add_bullet_point(doc, "Perform live inference requests against the containerized API using Python and PowerShell.", bold_prefix="6. Verification: ")

    # 3. Theory & Introduction to MLOps and Docker
    add_heading_1(doc, "2. Theory & Background")
    add_body_paragraph(
        doc,
        "Machine Learning Operations (MLOps) is an engineering practice unifying ML system development (Dev) with operations (Ops) to automate and standardize the continuous deployment of ML models into reliable production environments. A central friction in machine learning deployment is the 'Dependency Drift' or 'Works on My Machine' dilemma—where subtle library version discrepancies cause serialization failures or erroneous inferences in production.",
        bold_prefix="Introduction to MLOps: "
    )
    add_body_paragraph(
        doc,
        "Docker is an open-source platform that enables developers to package applications and their full runtime dependencies (system libraries, interpreter, packages, binaries) into isolated, portable units called containers. A Docker Image serves as a read-only blueprint, while a Docker Container is the live, runnable instantiation of that image.",
        bold_prefix="What is Docker? "
    )

    # Comparison Table: Containers vs VMs
    add_heading_2(doc, "Comparison: Containers vs. Virtual Machines (VMs)")
    comp_table = doc.add_table(rows=6, cols=3)
    comp_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(comp_table)
    comp_headers = ["Attribute", "Docker Container", "Virtual Machine (VM)"]
    for c_idx, h_text in enumerate(comp_headers):
        c = comp_table.cell(0, c_idx)
        set_cell_background(c, "0F4C81")
        p = c.paragraphs[0]
        r = p.add_run(h_text)
        r.font.name = "Calibri"
        r.font.size = Pt(10)
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)

    comp_rows = [
        ("Architecture", "Shares Host OS kernel; isolated processes via cgroups & namespaces.", "Hypervisor emulates full virtual hardware with dedicated Guest OS."),
        ("Startup Time", "Milliseconds to seconds (instant process spawn).", "Minutes (full operating system boot cycle)."),
        ("Resource Footprint", "Lightweight; consumes minimal CPU & RAM overhead.", "Heavy; allocates multi-GB RAM and dedicated disk storage."),
        ("Portability", "Extremely high; runs anywhere Docker Engine is available.", "Moderate; VM disk files (.vmdk/.ova) are massive and platform-tied."),
        ("Isolation Level", "Process-level isolation.", "Complete hardware-level isolation.")
    ]
    for r_idx, (attr, c_val, vm_val) in enumerate(comp_rows, start=1):
        bg = "F8FAFC" if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate([attr, c_val, vm_val]):
            cell = comp_table.cell(r_idx, c_idx)
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=60, bottom=60, left=100, right=100)
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.name = "Calibri"
            r.font.size = Pt(9.5)
            r.font.color.rgb = TEXT_COLOR
            if c_idx == 0:
                r.font.bold = True

    # 4. Project Structure
    add_heading_1(doc, "3. Project Structure")
    add_body_paragraph(
        doc,
        "The project follows a clean, modular structure conforming to standard MLOps microservice architecture:"
    )
    struct_code = (
        "iris-ml-docker/\n"
        "|\n"
        "+-- model/\n"
        "|   \\-- train_model.py       # ML Pipeline: training, evaluation & joblib export\n"
        "|\n"
        "+-- screenshots/             # Output verification screenshots\n"
        "|\n"
        "+-- app.py                   # Production Flask REST API\n"
        "+-- model.joblib             # Serialized RandomForest model binary\n"
        "+-- requirements.txt         # Pinned production dependencies\n"
        "+-- Dockerfile               # Container build blueprint\n"
        "+-- .dockerignore            # Build context exclusions\n"
        "+-- .gitignore               # Version control exclusions\n"
        "+-- test_api.py              # Automated test suite (Python requests)\n"
        "+-- test_api.ps1             # Automated test suite (PowerShell)\n"
        "\\-- README.md                # Comprehensive documentation"
    )
    add_code_block(doc, struct_code)

    # 5. Model Training & Evaluation
    add_heading_1(doc, "4. Model Training & Evaluation")
    add_body_paragraph(
        doc,
        "The model training pipeline is executed via model/train_model.py. We train an ensemble RandomForestClassifier with n_estimators=100 and random_state=42 on an 80/20 stratified split of the 150-sample Iris dataset."
    )
    train_results = (
        "Dataset: 150 samples (50 Setosa, 50 Versicolor, 50 Virginica), 4 features\n"
        "Split: 120 training samples, 30 testing samples\n"
        "Model Accuracy: 90.00% (0.9000)\n\n"
        "Classification Report:\n"
        "              precision    recall  f1-score   support\n\n"
        "      setosa       1.00      1.00      1.00        10\n"
        "  versicolor       0.82      0.90      0.86        10\n"
        "   virginica       0.89      0.80      0.84        10\n\n"
        "    accuracy                           0.90        30\n"
        "   macro avg       0.90      0.90      0.90        30\n"
        "weighted avg       0.90      0.90      0.90        30\n\n"
        "Trained model saved successfully to: model.joblib (167,729 bytes)"
    )
    add_code_block(doc, train_results)

    # 6. REST API Implementation
    add_heading_1(doc, "5. Flask REST API Implementation")
    add_body_paragraph(
        doc,
        "The REST API is engineered using Flask inside app.py and exposes three production endpoints:"
    )
    add_bullet_point(doc, "GET / - Service probe returning {'message': 'Iris Model API is running'}.", bold_prefix="1. Root Endpoint: ")
    add_bullet_point(doc, "GET /health - Liveness/Readiness probe confirming model is loaded and listing available classes.", bold_prefix="2. Health Endpoint: ")
    add_bullet_point(doc, "POST /predict - Inference endpoint accepting 4 numerical features in JSON format and returning the predicted species (setosa, versicolor, virginica).", bold_prefix="3. Predict Endpoint: ")
    add_body_paragraph(
        doc,
        "Defensive input validation is strictly implemented: requests without valid JSON, missing the 'features' key, containing non-numeric values, or having feature counts != 4 are cleanly intercepted and returned with HTTP 400 Bad Request and detailed error descriptions."
    )

    # 7. Dockerfile Architecture
    add_heading_1(doc, "6. Dockerfile Architecture & Instructions")
    add_body_paragraph(
        doc,
        "The Dockerfile packages the Python application and model into a standardized container image:"
    )
    dockerfile_code = (
        "# Step 1: Use an official lightweight Python image\n"
        "FROM python:3.11-slim\n\n"
        "# Step 2: Set working directory in container\n"
        "WORKDIR /app\n\n"
        "# Prevent Python from writing .pyc files and buffer output\n"
        "ENV PYTHONDONTWRITEBYTECODE=1\n"
        "ENV PYTHONUNBUFFERED=1\n\n"
        "# Step 3: Copy requirements first to leverage Docker layer caching\n"
        "COPY requirements.txt .\n\n"
        "# Step 4: Install dependencies\n"
        "RUN pip install --no-cache-dir -r requirements.txt\n\n"
        "# Step 5: Copy application code and serialized model\n"
        "COPY app.py .\n"
        "COPY model.joblib .\n\n"
        "# Step 6: Expose port 5000 for Flask API\n"
        "EXPOSE 5000\n\n"
        "# Step 7: Command to run application on container start\n"
        "CMD [\"python\", \"app.py\"]"
    )
    add_code_block(doc, dockerfile_code)

    add_heading_2(doc, "Explanation of Instructions:")
    add_bullet_point(doc, "Specifies python:3.11-slim as base OS to minimize vulnerability footprint and image size.", bold_prefix="FROM: ")
    add_bullet_point(doc, "Sets /app as the active execution context for all commands.", bold_prefix="WORKDIR: ")
    add_bullet_point(doc, "Transfers requirements.txt first to exploit Docker layer caching when application code changes.", bold_prefix="COPY (Requirements): ")
    add_bullet_point(doc, "Installs dependencies with --no-cache-dir to prevent wheel caching bloat.", bold_prefix="RUN: ")
    add_bullet_point(doc, "Copies app.py and model.joblib into the container.", bold_prefix="COPY (Application & Model): ")
    add_bullet_point(doc, "Documents port 5000 as the network listening port.", bold_prefix="EXPOSE: ")
    add_bullet_point(doc, "Specifies the runtime entrypoint executing 'python app.py'.", bold_prefix="CMD: ")

    # 8. Testing & Results
    add_heading_1(doc, "7. API Testing & Experimental Results")
    add_body_paragraph(
        doc,
        "The REST API was validated against both the local test suite and containerized deployment:"
    )
    test_results_text = (
        "[1] GET http://localhost:5000/\n"
        "Response: {\"message\": \"Iris Model API is running\"} (HTTP 200)\n\n"
        "[2] GET http://localhost:5000/health\n"
        "Response: {\"classes\": [\"setosa\", \"versicolor\", \"virginica\"], \"model_loaded\": true, \"status\": \"healthy\"} (HTTP 200)\n\n"
        "[3] POST http://localhost:5000/predict (Setosa Input: [5.1, 3.5, 1.4, 0.2])\n"
        "Response: {\"prediction\": \"setosa\"} (HTTP 200)\n\n"
        "[4] POST http://localhost:5000/predict (Versicolor Input: [6.0, 2.7, 5.1, 1.6])\n"
        "Response: {\"prediction\": \"versicolor\"} (HTTP 200)\n\n"
        "[5] POST http://localhost:5000/predict (Virginica Input: [6.7, 3.3, 5.7, 2.5])\n"
        "Response: {\"prediction\": \"virginica\"} (HTTP 200)\n\n"
        "[6] POST http://localhost:5000/predict (Invalid Input: [5.1, 3.5])\n"
        "Response: {\"error\": \"Invalid feature length: Expected exactly 4 numerical features...\"} (HTTP 400 Bad Request)"
    )
    add_code_block(doc, test_results_text)

    # 9. Screenshots Section
    add_heading_1(doc, "8. Verification Screenshots")
    add_body_paragraph(
        doc,
        "The following screenshots verify each stage of the MLOps containerization and deployment process:"
    )
    ss_folder = os.path.join(DOC_DIR, "screenshots")
    add_figure(doc, os.path.join(ss_folder, "01_model_training.png"), "Figure 1: Model Training, 90.00% Accuracy & model.joblib Serialization")
    add_figure(doc, os.path.join(ss_folder, "02_docker_build.png"), "Figure 2: Docker Image Build Process (iris-model-api:1.0)")
    add_figure(doc, os.path.join(ss_folder, "03_docker_images.png"), "Figure 3: Output of docker images command showing created image")
    add_figure(doc, os.path.join(ss_folder, "04_docker_ps.png"), "Figure 4: Output of docker ps showing running iris-container on port 5000")
    add_figure(doc, os.path.join(ss_folder, "05_browser_root.png"), "Figure 5: Web Browser verifying GET / root endpoint")
    add_figure(doc, os.path.join(ss_folder, "06_health_endpoint.png"), "Figure 6: Verification of GET /health endpoint")
    add_figure(doc, os.path.join(ss_folder, "07_predict_setosa.png"), "Figure 7: Successful POST /predict response returning 'setosa'")
    add_figure(doc, os.path.join(ss_folder, "08_predict_invalid_input.png"), "Figure 8: Error handling returning HTTP 400 Bad Request for invalid inputs")
    add_figure(doc, os.path.join(ss_folder, "09_docker_logs.png"), "Figure 9: Docker container logs showing incoming inference traffic")

    # 10. GitHub Repository Link
    add_heading_1(doc, "9. GitHub Repository")
    add_body_paragraph(
        doc,
        "The entire project, source code, Dockerfile, tests, and documentation are hosted on GitHub at:",
    )
    add_body_paragraph(
        doc,
        "https://github.com/GaurangJagtap/A6",
        bold_prefix="Repository URL: "
    )

    # 11. Conclusion
    add_heading_1(doc, "10. Conclusion")
    add_body_paragraph(
        doc,
        "In this practical assignment, we successfully realized an end-to-end MLOps pipeline: training a Random Forest classifier to 90% accuracy, building a production-grade Flask REST API with defensive input validation, authoring an optimized Dockerfile, containerizing the application, and verifying live inference. Containerization eliminates environment drift, establishing a reliable, reproducible, and horizontally scalable deployment unit for modern cloud infrastructures."
    )

    # Save to primary and alternate locations
    out_path_1 = os.path.join(DOC_DIR, REPORT_FILENAME)
    out_path_2 = os.path.join(DOC_DIR, REPORT_ALT_FILENAME)
    out_path_3 = os.path.join(ALT_DOC_DIR, REPORT_FILENAME)
    out_path_4 = os.path.join(ALT_DOC_DIR, REPORT_ALT_FILENAME)

    doc.save(out_path_1)
    doc.save(out_path_2)
    os.makedirs(ALT_DOC_DIR, exist_ok=True)
    doc.save(out_path_3)
    doc.save(out_path_4)

    print(f"[SUCCESS] Report saved to:\n - {out_path_1}\n - {out_path_2}\n - {out_path_3}\n - {out_path_4}")


if __name__ == "__main__":
    build_document()
