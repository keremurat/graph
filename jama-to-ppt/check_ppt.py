#!/usr/bin/env python3
"""
Quick script to check PowerPoint content
"""
from pptx import Presentation

prs = Presentation('output/Effect_of_Dexamethasone_on_Ventilator-Free_Days_in.pptx')

for slide_num, slide in enumerate(prs.slides, 1):
    print(f"\n{'='*60}")
    print(f"SLIDE {slide_num}")
    print('='*60)

    for shape in slide.shapes:
        if hasattr(shape, "text") and shape.text:
            print(f"\n{shape.text}")
