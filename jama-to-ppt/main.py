#!/usr/bin/env python3
"""
JAMA to PowerPoint Converter - CLI Interface
Converts JAMA Network articles to VA-formatted PowerPoint presentations
"""

import argparse
import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from scraper import JAMAScraper
from extractor import ContentExtractor
from ppt_generator import VAPowerPointGenerator
from ppt_generator_jama_oncology import JAMAOncologyPowerPointGenerator
from utils import IconSelector, sanitize_filename


def main():
    parser = argparse.ArgumentParser(
        description='🎯 JAMA Makale → PowerPoint Dönüştürücü (VA Format)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  %(prog)s https://jamanetwork.com/journals/jama/fullarticle/12345
  %(prog)s <URL> --output my_presentation.pptx
  %(prog)s <URL> --verbose
  %(prog)s <URL> --use-ai --api-key sk-ant-...
        '''
    )

    parser.add_argument(
        'url',
        help='JAMA Network article URL'
    )

    parser.add_argument(
        '-o', '--output',
        help='Output PowerPoint file path (default: auto-generated from title)',
        default=None
    )

    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
    )

    parser.add_argument(
        '--use-ai',
        action='store_true',
        help='Use AI for enhanced content extraction (requires --api-key)'
    )

    parser.add_argument(
        '--api-key',
        help='Anthropic API key for AI features',
        default=None
    )

    parser.add_argument(
        '--format',
        choices=['va', 'jama-oncology'],
        default='jama-oncology',
        help='PowerPoint format (default: jama-oncology - GREEN theme)'
    )

    args = parser.parse_args()

    # Validate URL
    if 'jamanetwork.com' not in args.url:
        print("❌ Hata: Lütfen geçerli bir JAMA Network URL'si girin")
        print("   Örnek: https://jamanetwork.com/journals/jama/fullarticle/...")
        sys.exit(1)

    # Check AI requirements
    if args.use_ai and not args.api_key:
        print("❌ Hata: --use-ai kullanmak için --api-key gereklidir")
        sys.exit(1)

    print("=" * 60)
    print("🎯 JAMA → PowerPoint Dönüştürücü (JAMA Oncology - YEŞİL TEMA)")
    print("=" * 60)
    print()

    try:
        # Step 1: Scrape article
        print("📥 Makale çekiliyor...")
        scraper = JAMAScraper(args.url, verbose=args.verbose)
        html_content = scraper.scrape()
        soup = scraper.get_soup()
        print()

        # Step 2: Extract content
        print("🔍 İçerik çıkarılıyor...")
        extractor = ContentExtractor(soup, verbose=args.verbose)
        article_data = extractor.extract_all()
        print()

        # Display extracted data if verbose
        if args.verbose:
            print("📋 Çıkarılan Veriler:")
            print("-" * 60)
            for key, value in article_data.items():
                print(f"{key:20}: {value[:80]}..." if len(value) > 80 else f"{key:20}: {value}")
            print()

        # Step 3: Select icon
        print("🎨 İkon seçiliyor...")
        icon_type = IconSelector.select_icon(article_data, verbose=args.verbose)
        print()

        # Step 4: Generate PowerPoint
        print("📝 PowerPoint oluşturuluyor...")

        # Determine output path
        if args.output:
            output_path = args.output
        else:
            # Auto-generate from title
            filename = sanitize_filename(article_data['title'])
            if not filename:
                filename = 'jama_article'
            filename = filename[:50]  # Limit filename length
            output_path = f"output/{filename}.pptx"

        # Create output directory if needed
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Generate presentation - SADECE YEŞİL TEMA (JAMA Oncology)
        if args.format == 'jama-oncology':
            generator = JAMAOncologyPowerPointGenerator(article_data, icon_type, verbose=args.verbose)
        else:
            generator = VAPowerPointGenerator(article_data, icon_type, verbose=args.verbose)

        generator.generate(output_path)
        print()

        # Success message
        print("=" * 60)
        print("✨ İşlem Tamamlandı!")
        print("=" * 60)
        print(f"📁 Dosya: {output_path}")
        print(f"🎨 Format: {args.format}")
        print(f"🔧 Yöntem: {scraper.successful_method}")
        print()

    except KeyboardInterrupt:
        print("\n⚠️ İşlem kullanıcı tarafından iptal edildi")
        sys.exit(1)

    except Exception as e:
        print(f"\n❌ Hata oluştu: {str(e)}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
