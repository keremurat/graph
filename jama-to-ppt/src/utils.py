"""
Utility Functions
"""

import re
from typing import Dict


class IconSelector:
    """
    Automatic icon selection based on article keywords
    """

    KEYWORDS_TO_ICON = {
        'cardiology': ['cardiac', 'heart', 'cardiovascular', 'myocardial', 'ECG', 'echocardiography', 'coronary'],
        'neurology': ['brain', 'neurological', 'cognitive', 'alzheimer', 'stroke', 'dementia', 'parkinson', 'seizure'],
        'oncology': ['cancer', 'tumor', 'tumour', 'chemotherapy', 'radiation', 'malignant', 'carcinoma', 'metastasis'],
        'respiratory': ['lung', 'copd', 'asthma', 'pneumonia', 'ventilation', 'respiratory', 'pulmonary', 'bronchial'],
        'diabetes': ['diabetes', 'diabetic', 'glucose', 'insulin', 'hba1c', 'glycemic', 'hyperglycemia'],
        'infectious': ['covid', 'viral', 'bacterial', 'sepsis', 'antibiotic', 'infection', 'influenza', 'pandemic'],
        'mental_health': ['depression', 'anxiety', 'psychiatric', 'ptsd', 'mental health', 'psychological', 'suicide'],
        'pediatric': ['children', 'pediatric', 'paediatric', 'infant', 'adolescent', 'neonatal', 'child']
    }

    @classmethod
    def select_icon(cls, article_data: Dict[str, str], verbose: bool = False) -> str:
        """
        Select appropriate icon type based on article content
        Returns icon type string (e.g., 'cardiology', 'neurology', etc.)
        """
        # Combine all text fields for keyword search
        search_text = ' '.join([
            article_data.get('title', ''),
            article_data.get('population', ''),
            article_data.get('intervention', ''),
            article_data.get('setting', ''),
            article_data.get('primary_outcome', ''),
            article_data.get('finding_1', ''),
            article_data.get('finding_2', '')
        ]).lower()

        # Count matches for each category
        matches = {}
        for category, keywords in cls.KEYWORDS_TO_ICON.items():
            count = sum(1 for keyword in keywords if keyword in search_text)
            if count > 0:
                matches[category] = count

        # Return category with most matches
        if matches:
            best_match = max(matches.items(), key=lambda x: x[1])
            if verbose:
                print(f"🎯 İkon seçildi: {best_match[0]} ({best_match[1]} eşleşme)")
            return best_match[0]

        if verbose:
            print("🎯 İkon seçildi: medical (varsayılan)")
        return 'medical'


def sanitize_filename(filename: str) -> str:
    """
    Clean filename for safe file system usage
    """
    # Remove invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    # Replace spaces and multiple underscores
    filename = re.sub(r'\s+', '_', filename)
    filename = re.sub(r'_+', '_', filename)
    # Limit length
    if len(filename) > 100:
        filename = filename[:100]
    return filename.strip('_')
