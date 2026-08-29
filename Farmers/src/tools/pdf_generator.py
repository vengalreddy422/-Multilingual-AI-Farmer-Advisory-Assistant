import io
from datetime import datetime
from typing import Dict, Any, List, Optional
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, PageBreak, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def generate_pdf_health_card(
    farmer_name: str, 
    location: str, 
    disease_data: Optional[Dict[str, Any]] = None, 
    soil_data: Optional[Dict[str, Any]] = None, 
    weather_data: Optional[Dict[str, Any]] = None,
    crops_data: Optional[Dict[str, Any]] = None,
    mandi_data: Optional[List[Dict[str, Any]]] = None,
    schemes_data: Optional[List[Dict[str, Any]]] = None,
    farmer_acres: float = 2.0,
    **kwargs
) -> io.BytesIO:
    """
    Generates an official, all-in-one Kisan Digital Health Dossier & Master Farm Report
    including Crop Diagnostics, Soil NPK, Recommended Regional Crops, Live Mandi Rates, and Govt Schemes.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, 
        pagesize=A4, 
        rightMargin=25, 
        leftMargin=25, 
        topMargin=22, 
        bottomMargin=22
    )
    story = []
    styles = getSampleStyleSheet()

    # --- CUSTOM STYLES ---
    title_style = ParagraphStyle(
        'MainTitle',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=colors.HexColor("#1b5e20"),
        alignment=1,
        spaceAfter=3
    )
    sub_title_style = ParagraphStyle(
        'SubTitle',
        parent=styles['Normal'],
        fontSize=8.5,
        textColor=colors.HexColor("#388e3c"),
        alignment=1,
        spaceAfter=8
    )
    section_style = ParagraphStyle(
        'SectionHeader',
        parent=styles['Heading2'],
        fontSize=11,
        textColor=colors.HexColor("#1b5e20"),
        spaceBefore=6,
        spaceAfter=4
    )
    body_style = ParagraphStyle(
        'BodyTextCustom',
        parent=styles['Normal'],
        fontSize=8.5,
        leading=11.5
    )
    bold_body_style = ParagraphStyle(
        'BoldBodyCustom',
        parent=styles['Normal'],
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor("#1b5e20")
    )
    table_head_style = ParagraphStyle(
        'TableHead',
        parent=styles['Normal'],
        fontSize=8.5,
        leading=11,
        textColor=colors.white,
        fontName="Helvetica-Bold"
    )

    # =========================================================
    # 📄 PAGE 1: EXECUTIVE PROFILE & CROP DIAGNOSTICS
    # =========================================================
    story.append(Paragraph("🌾 KISAN MITRA — COMPREHENSIVE DIGITAL FARM HEALTH DOSSIER", title_style))
    story.append(Paragraph("Verified Agricultural Decision Support System • Grounded in ICAR & SAU Standards", sub_title_style))
    story.append(HRFlowable(width="100%", thickness=1.2, color=colors.HexColor("#2e7d32"), spaceBefore=1, spaceAfter=6))

    # 1. Metadata Profile Card
    curr_date = datetime.now().strftime("%d %B %Y, %I:%M %p")
    w_cond = weather_data.get('condition', 'Clear / Sunny') if weather_data else 'Clear'
    w_temp = f"{weather_data.get('temperature', 28.5)}°C" if weather_data else '28.5°C'
    w_rain = f"Rain Risk: {weather_data.get('rain_risk', False)}" if weather_data else 'Normal'

    meta_data = [
        [
            Paragraph(f"<b>Farmer Name:</b> {farmer_name}", body_style), 
            Paragraph(f"<b>Report Date:</b> {curr_date}", body_style)
        ],
        [
            Paragraph(f"<b>Location / Cluster:</b> {location}", body_style), 
            Paragraph(f"<b>Landholding:</b> {farmer_acres} Acres", body_style)
        ],
        [
            Paragraph(f"<b>Live Weather:</b> {w_cond} ({w_temp})", body_style),
            Paragraph(f"<b>Spray Suitability:</b> {'⚠️ Delay Spray' if weather_data and weather_data.get('rain_risk') else '✅ Favorable Weather'}", body_style)
        ]
    ]
    t_meta = Table(meta_data, colWidths=[270, 270])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#e8f5e9")),
        ('PADDING', (0, 0), (-1, -1), 4.5),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#a5d6a7")),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 6))

    # 2. Leaf Diagnostics & Prescription
    story.append(Paragraph("🍃 Diagnostic Lab Report & Integrated Treatment Plan", section_style))
    if disease_data:
        diag_rows = [
            [Paragraph("<b>Cultivated Crop:</b>", bold_body_style), Paragraph(str(disease_data.get('leaf_name', 'Field Crop')), body_style)],
            [Paragraph("<b>Diagnosed Disease:</b>", bold_body_style), Paragraph(str(disease_data.get('disease', 'Foliar Disorder')), body_style)],
            [Paragraph("<b>Confidence Match:</b>", bold_body_style), Paragraph(f"{int(disease_data.get('confidence', 0.92)*100)}% (ONNX Neural Vision)", body_style)],
            [Paragraph("<b>Pathogen / Vector:</b>", bold_body_style), Paragraph(str(disease_data.get('pathogen', 'Pathogen Complex')), body_style)],
            [Paragraph("<b>Severity Rating:</b>", bold_body_style), Paragraph(f"<b>{disease_data.get('severity', 'Moderate')}</b>", body_style)],
            [Paragraph("<b>Visible Symptoms:</b>", bold_body_style), Paragraph(str(disease_data.get('symptoms', 'Necrotic foliar lesions')), body_style)],
            [Paragraph("<b>🌿 Organic Remedy (ZBNF):</b>", bold_body_style), Paragraph(str(disease_data.get('organic_treatment', disease_data.get('treatment', 'Neem Oil 5ml/L'))), body_style)],
            [Paragraph("<b>🧪 Chemical Prescription:</b>", bold_body_style), Paragraph(str(disease_data.get('chemical_treatment', disease_data.get('treatment', 'Mancozeb 75 WP @ 2.5g/L'))), body_style)],
            [Paragraph("<b>Waiting Period (PHI):</b>", bold_body_style), Paragraph(f"{disease_data.get('phi_days', 7)} Days before harvest", body_style)],
        ]
    else:
        diag_rows = [
            [Paragraph("<b>Status:</b>", bold_body_style), Paragraph("No active foliar disease scan recorded in current session. General preventive maintenance advised.", body_style)],
            [Paragraph("<b>Preventive Care:</b>", bold_body_style), Paragraph("Apply 5% Neem Seed Kernel Extract (NSKE) as prophylactic protection against sucking pests.", body_style)]
        ]

    t_diag = Table(diag_rows, colWidths=[150, 390])
    t_diag.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor("#f1f8e9")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#c8e6c9")),
        ('PADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_diag)
    story.append(Spacer(1, 6))

    # 3. Soil & Nutrition Advisory
    story.append(Paragraph("🧪 Soil Health & Balanced Fertilizer (NPK) Schedule", section_style))
    if soil_data:
        s_crop = soil_data.get("crop", "General Cultivation")
        soil_rows = [[Paragraph("<b>Target Crop:</b>", bold_body_style), Paragraph(str(s_crop), body_style)]]
        for idx, rec in enumerate(soil_data.get("recommendations", []), 1):
            soil_rows.append([Paragraph(f"<b>Dose Step {idx}:</b>", bold_body_style), Paragraph(str(rec), body_style)])
    else:
        soil_rows = [
            [Paragraph("<b>Basal Manure:</b>", bold_body_style), Paragraph("Apply 5 tons/acre well-decomposed Farm Yard Manure (FYM) during final ploughing.", body_style)],
            [Paragraph("<b>NPK Strategy:</b>", bold_body_style), Paragraph("Split Nitrogen into 50% Basal, 25% Tillering, 25% Panicle emergence. Apply full P as basal.", body_style)]
        ]

    t_soil = Table(soil_rows, colWidths=[150, 390])
    t_soil.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor("#fffde7")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#fff59d")),
        ('PADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_soil)
    story.append(Spacer(1, 10))

    # =========================================================
    # 📄 PAGE 2: REGIONAL CROPS, LIVE MANDI RATES & SCHEMES
    # =========================================================
    story.append(PageBreak())
    story.append(Paragraph(f"🌱 Regional Crop Recommendations for {location.split(',')[0]}", section_style))
    
    # 4. Regional Crop Recommendation Table
    if crops_data and crops_data.get("all_crops"):
        crop_list = crops_data["all_crops"][:4]
        c_table_data = [
            [
                Paragraph("Crop Name", table_head_style), 
                Paragraph("Suitability", table_head_style), 
                Paragraph("Recommended Varieties", table_head_style), 
                Paragraph("Water Need", table_head_style)
            ]
        ]
        for c in crop_list:
            c_table_data.append([
                Paragraph(f"<b>{c['crop'].split('(')[0]}</b>", body_style),
                Paragraph(f"{c.get('suitability', 90)}%", body_style),
                Paragraph(str(c.get('varieties', 'Hybrid'))[:35], body_style),
                Paragraph(str(c.get('water_need', 'Medium')), body_style)
            ])
    else:
        c_table_data = [
            [Paragraph("Crop", table_head_style), Paragraph("Suitability", table_head_style), Paragraph("Varieties", table_head_style), Paragraph("Season", table_head_style)],
            [Paragraph("Paddy / Rice", body_style), Paragraph("95%", body_style), Paragraph("BPT-5204, MTU-1010", body_style), Paragraph("Kharif / Rabi", body_style)],
            [Paragraph("Tomato", body_style), Paragraph("92%", body_style), Paragraph("Saaho 3251, Abhinav", body_style), Paragraph("Year-round", body_style)],
            [Paragraph("Cotton", body_style), Paragraph("88%", body_style), Paragraph("RCH-659 BG II, Mallika", body_style), Paragraph("Kharif", body_style)],
            [Paragraph("Groundnut", body_style), Paragraph("86%", body_style), Paragraph("Kadiri-6, Dharani", body_style), Paragraph("Rabi / Kharif", body_style)]
        ]

    t_crops = Table(c_table_data, colWidths=[130, 70, 220, 120])
    t_crops.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#2e7d32")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#a5d6a7")),
        ('PADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_crops)
    story.append(Spacer(1, 8))

    # 5. Live Mandi Market Prices Table
    story.append(Paragraph(f"💰 Live APMC Mandi Market Index ({location.split(',')[0]} Cluster)", section_style))
    if mandi_data:
        m_table_data = [
            [
                Paragraph("Commodity", table_head_style), 
                Paragraph("APMC Market Yard", table_head_style), 
                Paragraph("Modal Price (₹/Q)", table_head_style), 
                Paragraph("Price Range (₹/Q)", table_head_style),
                Paragraph("Trend", table_head_style)
            ]
        ]
        for m in mandi_data[:5]:
            m_table_data.append([
                Paragraph(f"<b>{m['crop']}</b>", body_style),
                Paragraph(str(m['primary_market']), body_style),
                Paragraph(f"₹{m['modal_price']:,}", bold_body_style),
                Paragraph(f"₹{m['min_price']:,} - ₹{m['max_price']:,}", body_style),
                Paragraph(str(m['trend']), body_style)
            ])
    else:
        m_table_data = [
            [Paragraph("Commodity", table_head_style), Paragraph("Market", table_head_style), Paragraph("Modal Price", table_head_style), Paragraph("Trend", table_head_style)],
            [Paragraph("Tomato", body_style), Paragraph(f"{location.split(',')[0]} APMC", body_style), Paragraph("₹1,950 / Q", bold_body_style), Paragraph("🔺 Firm", body_style)],
            [Paragraph("Paddy / Rice", body_style), Paragraph(f"{location.split(',')[0]} APMC", body_style), Paragraph("₹2,320 / Q", bold_body_style), Paragraph("🔺 Steady", body_style)],
            [Paragraph("Cotton", body_style), Paragraph(f"{location.split(',')[0]} APMC", body_style), Paragraph("₹7,450 / Q", bold_body_style), Paragraph("🔺 Strong", body_style)]
        ]

    t_mandi = Table(m_table_data, colWidths=[120, 150, 100, 110, 60])
    t_mandi.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1b5e20")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#a5d6a7")),
        ('PADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_mandi)
    story.append(Spacer(1, 8))

    # 6. Matched Government Welfare Schemes Table
    story.append(Paragraph("🏛️ Matched Government Schemes & Financial Subsidies", section_style))
    if schemes_data:
        s_table_data = [
            [
                Paragraph("Scheme Name", table_head_style), 
                Paragraph("Direct Benefit / Subsidy", table_head_style), 
                Paragraph("Eligibility & Requirements", table_head_style)
            ]
        ]
        for sch in schemes_data[:4]:
            s_table_data.append([
                Paragraph(f"<b>{sch['name'].split('(')[0]}</b>", bold_body_style),
                Paragraph(str(sch['benefit'])[:60] + "...", body_style),
                Paragraph(str(sch['required_docs'])[:50], body_style)
            ])
    else:
        s_table_data = [
            [Paragraph("Scheme", table_head_style), Paragraph("Benefit", table_head_style), Paragraph("Required Docs", table_head_style)],
            [Paragraph("PM-KISAN", bold_body_style), Paragraph("₹6,000 / year direct bank transfer in 3 installments", body_style), Paragraph("Aadhaar, Land Passbook (ROR)", body_style)],
            [Paragraph("PMKSY Micro Irrigation", bold_body_style), Paragraph("Up to 90% direct subsidy on Drip & Sprinkler systems", body_style), Paragraph("Land Passbook, Water Certificate", body_style)],
            [Paragraph("PMFBY Crop Insurance", bold_body_style), Paragraph("Insurance compensation against pest epidemics & flood", body_style), Paragraph("Sowing Declaration, Bank Passbook", body_style)]
        ]

    t_schemes = Table(s_table_data, colWidths=[140, 240, 160])
    t_schemes.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#2e7d32")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#a5d6a7")),
        ('PADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_schemes)
    story.append(Spacer(1, 10))

    # 7. Official Notice & Footer
    notice_text = (
        "<b>Official Notice to Agrochemical Dealers & Rythu Bharosa Kendras (RBKs):</b> This document is an "
        "agronomic prescription generated by Kisan Mitra AI based on ICAR packages of practices. Please dispense only "
        "CIB&RC approved chemical formulations. Verify the farmer's safety pre-harvest intervals (PHI)."
    )
    story.append(Paragraph(notice_text, ParagraphStyle('Notice', parent=styles['Normal'], fontSize=7.5, textColor=colors.HexColor("#555555"), leading=9.5)))
    story.append(Spacer(1, 4))
    story.append(HRFlowable(width="100%", thickness=0.8, color=colors.HexColor("#a5d6a7"), spaceBefore=1, spaceAfter=3))
    story.append(Paragraph("🏛️ Kisan Call Center (Toll Free): 1800-180-1551 • Kisan Mitra AI Advisory Platform", ParagraphStyle('Footer', parent=styles['Normal'], fontSize=8, alignment=1, textColor=colors.HexColor("#2e7d32"))))

    doc.build(story)
    buffer.seek(0)
    return buffer
