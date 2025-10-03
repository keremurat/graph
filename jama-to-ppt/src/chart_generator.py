"""
Chart Generator for JAMA Open PowerPoint
Creates statistical charts and visualizations
"""

from typing import Dict, List, Tuple, Optional
import re
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend
import matplotlib.pyplot as plt
import numpy as np


class ChartGenerator:
    """Generate statistical charts for PowerPoint slides"""

    # JAMA Open color scheme
    COLORS = {
        'primary': '#E91383',      # Magenta
        'secondary': '#990066',    # Dark magenta
        'gray': '#646464',
        'light_gray': '#F0F0F0',
        'error_bar': '#323232',
    }

    @staticmethod
    def extract_comparison_data(text: str) -> Optional[Dict]:
        """
        Extract comparison data from text
        Example: "Enhanced support: ~1.0, Foundational support: ~1.0"
        """
        patterns = {
            'group_values': r'(\w+(?:\s+\w+)*)\s*:?\s*[~≈]?\s*([0-9.]+)',
            'mean_diff': r'[Mm]ean\s+difference.*?([0-9.-]+)',
            'ci': r'95%\s*CI[,:]?\s*([0-9.-]+)\s+to\s+([0-9.-]+)',
            'p_value': r'[Pp]\s*=\s*\.?([0-9.]+)',
        }

        data = {}

        # Extract group values
        matches = re.findall(patterns['group_values'], text, re.IGNORECASE)
        if matches:
            groups = []
            values = []
            for group, value in matches:
                if 'support' in group.lower() or 'group' in group.lower():
                    groups.append(group.strip())
                    values.append(float(value))

            if groups and values:
                data['groups'] = groups
                data['values'] = values

        # Extract mean difference
        md_match = re.search(patterns['mean_diff'], text)
        if md_match:
            data['mean_diff'] = float(md_match.group(1))

        # Extract CI
        ci_match = re.search(patterns['ci'], text)
        if ci_match:
            data['ci_lower'] = float(ci_match.group(1))
            data['ci_upper'] = float(ci_match.group(2))

        # Extract p-value
        p_match = re.search(patterns['p_value'], text)
        if p_match:
            data['p_value'] = float(p_match.group(1))

        return data if data else None

    @classmethod
    def create_comparison_chart(cls, text: str, width: int = 600, height: int = 400) -> Optional[BytesIO]:
        """
        Create a bar chart comparing groups
        Returns image as BytesIO buffer
        """
        data = cls.extract_comparison_data(text)

        if not data or 'groups' not in data:
            return None

        # Set up the plot
        plt.figure(figsize=(width/100, height/100), dpi=100)
        plt.style.use('seaborn-v0_8-whitegrid')

        groups = data['groups']
        values = data['values']

        # Shorten group names for display
        display_groups = [cls._shorten_label(g) for g in groups]

        # Create bar chart
        x_pos = np.arange(len(groups))
        bars = plt.bar(x_pos, values, color=cls.COLORS['primary'], alpha=0.8, width=0.6)

        # Add error bars if CI available
        if 'ci_lower' in data and 'ci_upper' in data:
            ci_range = (data['ci_upper'] - data['ci_lower']) / 2
            errors = [ci_range] * len(values)
            plt.errorbar(x_pos, values, yerr=errors, fmt='none',
                        ecolor=cls.COLORS['error_bar'], capsize=5, capthick=2)

        # Customize plot
        plt.xlabel('', fontsize=10)
        plt.ylabel('Mean penetration (95% CI)', fontsize=10)
        plt.xticks(x_pos, display_groups, fontsize=9, rotation=0)
        plt.ylim(0, max(values) * 1.3)

        # Add value labels on bars
        for i, (bar, val) in enumerate(zip(bars, values)):
            plt.text(bar.get_x() + bar.get_width()/2, val + 0.05,
                    f'{val:.1f}', ha='center', va='bottom', fontsize=9, fontweight='bold')

        # Add p-value if available
        if 'p_value' in data:
            p_val = data['p_value']
            plt.text(0.95, 0.95, f'P = {p_val:.2f}',
                    transform=plt.gca().transAxes,
                    ha='right', va='top', fontsize=10,
                    bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

        plt.tight_layout()

        # Save to buffer
        buf = BytesIO()
        plt.savefig(buf, format='png', dpi=150, bbox_inches='tight', facecolor='white')
        buf.seek(0)
        plt.close()

        return buf

    @staticmethod
    def _shorten_label(label: str) -> str:
        """Shorten long labels for display"""
        # Remove common words
        label = label.replace('support', '').replace('group', '').strip()

        # Capitalize first letter
        if label:
            label = label[0].upper() + label[1:]

        return label

    @classmethod
    def create_forest_plot(cls, text: str, width: int = 600, height: int = 300) -> Optional[BytesIO]:
        """
        Create a forest plot for effect sizes and confidence intervals
        """
        data = cls.extract_comparison_data(text)

        if not data or 'mean_diff' not in data:
            return None

        # Set up the plot
        fig, ax = plt.subplots(figsize=(width/100, height/100), dpi=100)

        mean_diff = data.get('mean_diff', 0)
        ci_lower = data.get('ci_lower', mean_diff - 0.5)
        ci_upper = data.get('ci_upper', mean_diff + 0.5)

        # Plot the effect
        ax.plot([mean_diff], [0], 'o', color=cls.COLORS['primary'], markersize=12)
        ax.plot([ci_lower, ci_upper], [0, 0], '-', color=cls.COLORS['secondary'], linewidth=3)

        # Add vertical line at null effect (0)
        ax.axvline(x=0, color='black', linestyle='--', linewidth=1, alpha=0.5)

        # Labels
        ax.set_xlabel('Mean Difference (95% CI)', fontsize=10)
        ax.set_yticks([])
        ax.spines['left'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        # Add text annotation
        text_str = f'{mean_diff:.1f} ({ci_lower:.1f} to {ci_upper:.1f})'
        ax.text(mean_diff, 0.1, text_str, ha='center', va='bottom', fontsize=9)

        if 'p_value' in data:
            ax.text(0.95, 0.05, f'P = {data["p_value"]:.2f}',
                   transform=ax.transAxes, ha='right', va='bottom', fontsize=9)

        plt.tight_layout()

        # Save to buffer
        buf = BytesIO()
        plt.savefig(buf, format='png', dpi=150, bbox_inches='tight', facecolor='white')
        buf.seek(0)
        plt.close()

        return buf

    @classmethod
    def create_simple_icon(cls, icon_type: str, width: int = 200, height: int = 200) -> BytesIO:
        """
        Create simple vector-style icons using PIL
        """
        # Create image with transparent background
        img = Image.new('RGBA', (width, height), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)

        color = cls._hex_to_rgb(cls.COLORS['primary'])

        if icon_type == 'people':
            # Draw three simple person silhouettes
            for i in range(3):
                x_offset = 30 + i * 60
                # Head
                draw.ellipse([x_offset, 50, x_offset+40, 90], fill=color)
                # Body
                draw.rectangle([x_offset-10, 95, x_offset+50, 150], fill=color)

        elif icon_type == 'hospital':
            # Simple building with cross
            draw.rectangle([50, 80, 150, 180], fill=color)
            # Cross
            cross_color = (255, 255, 255, 255)
            draw.rectangle([85, 40, 115, 90], fill=cross_color)
            draw.rectangle([60, 55, 140, 75], fill=cross_color)

        elif icon_type == 'chart':
            # Simple bar chart
            heights = [60, 100, 80]
            for i, h in enumerate(heights):
                x = 40 + i * 50
                draw.rectangle([x, 160-h, x+35, 160], fill=color)

        elif icon_type == 'target':
            # Target/bullseye
            draw.ellipse([40, 40, 160, 160], fill=color)
            draw.ellipse([70, 70, 130, 130], fill=(255, 255, 255, 255))
            draw.ellipse([90, 90, 110, 110], fill=color)

        # Save to buffer
        buf = BytesIO()
        img.save(buf, format='PNG')
        buf.seek(0)

        return buf

    @staticmethod
    def _hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
        """Convert hex color to RGB tuple"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
