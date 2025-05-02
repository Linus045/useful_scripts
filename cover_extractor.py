import os
import zipfile
import argparse
from tqdm import tqdm

# extracts covers from cbz and epub files
# CBZ: will extract the first few image files
# EPUB: will extract the 'cover.jpg' and searches for everything that has 'cover' in its name as well an extract it

def extract_cover_from_cbz(cbz_path, output_dir):
    try:
        with zipfile.ZipFile(cbz_path, 'r') as zip_ref:
            namelist = zip_ref.namelist()

            image_extensions = ['.jpg', '.jpeg', '.png']

            # Filter image files only
            image_files = [name for name in namelist if os.path.splitext(name)[1].lower() in image_extensions]
            image_files.sort()  # Ensure consistent order

            # Get the base name of the cbz file without extension
            cbz_name = os.path.splitext(os.path.basename(cbz_path))[0]

            # Extract up to the first 3 images
            for i, image_file in enumerate(image_files[:3]):
                # Read the file from the archive
                with zip_ref.open(image_file) as source:
                    # Build output file path
                    ext = os.path.splitext(image_file)[1]
                    output_filename = f"{cbz_name}_{i+1}{ext}"
                    output_path = os.path.join(output_dir, output_filename)

                    # Write to the output file
                    with open(output_path, 'wb') as target:
                        target.write(source.read())
    except zipfile.BadZipFile:
        print(f"[WARN] Skipping file (not a valid zip): {cbz_path}")

    return None

def extract_cover_from_epub(epub_path, output_dir):
    image_extensions = ['.jpg', '.jpeg', '.png']
    epub_name = os.path.splitext(os.path.basename(epub_path))[0]

    # Step 1: Check for a "cover.jpg" in the same directory as the .epub
    dir_of_epub = os.path.dirname(epub_path)
    local_cover_path = os.path.join(dir_of_epub, 'cover.jpg')
    if os.path.isfile(local_cover_path):
        ext = os.path.splitext(local_cover_path)[1]
        output_filename = f"{epub_name}_cover0{ext}"
        output_path = os.path.join(output_dir, output_filename)
        with open(local_cover_path, 'rb') as src, open(output_path, 'wb') as dst:
            dst.write(src.read())
        # print(f"[INFO] Copied external cover: {local_cover_path}")

    # Step 2: Search inside the EPUB for any images with "cover" in the name
    try:
        with zipfile.ZipFile(epub_path, 'r') as zip_ref:
            candidates = [
                name for name in zip_ref.namelist()
                if 'cover' in name.lower() and os.path.splitext(name)[1].lower() in image_extensions
            ]
            if not candidates:
                print(f"[WARN] No internal cover image found in: {epub_path}")
                return

            for i, image_file in enumerate(candidates):
                with zip_ref.open(image_file) as source:
                    ext = os.path.splitext(image_file)[1]
                    output_filename = f"{epub_name}_cover{i+1}{ext}"
                    output_path = os.path.join(output_dir, output_filename)
                    with open(output_path, 'wb') as target:
                        target.write(source.read())
            # print(f"[INFO] Extracted cover(s) from: {epub_path}")
    except zipfile.BadZipFile:
        print(f"[WARN] Skipping invalid EPUB (not a zip): {epub_path}")


if __name__ == '__main__':
    # make output direcotyr
    output_dir = 'output_covers'
    parser = argparse.ArgumentParser(description='Extract covers from cbz or epub files.')
    parser.add_argument('path', type=str, help='Path to the directory or file to extract covers from.')
    parser.add_argument('--output', type=str, default='covers', help='Output directory for extracted covers.')
    parser.add_argument('--overwrite', action='store_true', help='Overwrite existing covers.')


    args = parser.parse_args()
    if args.output:
        output_dir = args.output

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    cbz_files = []
    epub_files = []

    for root, dirs, files in os.walk(args.path):
        for file in files:
            if file.endswith('.cbz'):
                cbz_files.append(os.path.join(root, file))
            elif file.endswith('.epub'):
                epub_files.append(os.path.join(root, file))

    for cbz_file in tqdm(cbz_files, desc="CBZ", unit="file"):
        extract_cover_from_cbz(cbz_file, output_dir)
    for epub_file in tqdm(epub_files, desc="EPUB", unit="file"):
        extract_cover_from_epub(epub_file, output_dir)
