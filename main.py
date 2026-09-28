import argparse
from pathlib import Path
from PIL import Image, ImageOps, UnidentifiedImageError

SUPPORTED = {'.png', '.jpg', '.jpeg', '.webp', '.bmp', '.tiff'}


def main():
    p = argparse.ArgumentParser(description='Convertit les images dans un dossier de sortie.')
    p.add_argument('source', type=Path)
    p.add_argument('destination', type=Path)
    p.add_argument('--format', choices=['png', 'jpeg', 'webp'], required=True)
    p.add_argument('--max-width', type=int)
    p.add_argument('--apply', action='store_true')
    args = p.parse_args()
    if not args.source.is_dir() or args.source.resolve() == args.destination.resolve():
        p.error('Choisis un dossier source existant et un dossier de sortie distinct.')
    if args.max_width is not None and args.max_width < 1:
        p.error('--max-width doit être positif.')
    reserved = set()
    for src in sorted(args.source.iterdir()):
        if not src.is_file() or src.is_symlink() or src.suffix.lower() not in SUPPORTED:
            continue
        extension = '.jpg' if args.format == 'jpeg' else '.' + args.format
        dest = args.destination / (src.stem + extension)
        n = 2
        while dest in reserved or dest.exists():
            dest = args.destination / f'{src.stem}_{n}{extension}'
            n += 1
        reserved.add(dest)
        print(f'{src.name} -> {dest}')
        if not args.apply:
            continue
        try:
            with Image.open(src) as opened:
                img = ImageOps.exif_transpose(opened)
                if args.max_width and img.width > args.max_width:
                    img.thumbnail((args.max_width, img.height), Image.Resampling.LANCZOS)
                if args.format == 'jpeg':
                    background = Image.new('RGB', img.size, 'white')
                    if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
                        background.paste(img.convert('RGBA'), mask=img.convert('RGBA').getchannel('A'))
                    else:
                        background.paste(img.convert('RGB'))
                    img = background
                args.destination.mkdir(parents=True, exist_ok=True)
                img.save(dest, format=args.format.upper())
        except (OSError, ValueError, UnidentifiedImageError) as exc:
            print(f'Erreur pour {src}: {exc}')
    if not args.apply:
        print('Aperçu uniquement : ajoute --apply pour convertir.')


if __name__ == '__main__':
    main()
