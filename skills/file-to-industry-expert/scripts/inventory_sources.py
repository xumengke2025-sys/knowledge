"""Inventory only: document extraction and semantic reading are separate work."""
import argparse
import hashlib
import json
import os
from pathlib import Path

IMAGES = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.emf', '.tif', '.tiff'}
DOCUMENTS = {'.pdf', '.doc', '.docx', '.ppt', '.pptx', '.xls', '.xlsx', '.csv', '.tsv', '.txt', '.md', '.rtf', '.html', '.xml'}
RECORDINGS = {'.mp3', '.mp4', '.wav', '.m4a', '.aac', '.wma', '.wmv', '.webm'}


def inventory(source, exclude_images=False):
    entries, hashes = [], {}
    def walk_error(error):
        entries.append({'path': str(error.filename), 'status': 'read_error', 'error': str(error)})
    for folder, dirs, files in os.walk(source, followlinks=False, onerror=walk_error):
        dirs.sort()
        for filename in sorted(files):
            p = Path(folder) / filename
            rel = p.relative_to(source).as_posix()
            record = {'path': rel, 'extension': p.suffix.lower()}
            if p.is_symlink():
                record['status'] = 'symlink_not_followed'
                entries.append(record)
                continue
            try:
                before = p.stat()
                digest = hashlib.sha256()
                with p.open('rb') as stream:
                    for block in iter(lambda: stream.read(1024 * 1024), b''):
                        digest.update(block)
                after = p.stat()
                if (before.st_size, before.st_mtime_ns) != (after.st_size, after.st_mtime_ns):
                    raise OSError('File changed during hashing; retry this file')
                sha = digest.hexdigest()
                record.update(size=after.st_size, sha256=sha, source_id='src-' + sha[:16])
                ext = p.suffix.lower()
                if exclude_images and ext in IMAGES:
                    record['status'] = 'excluded_images_per_user'
                elif sha in hashes:
                    record.update(status='duplicate_content', duplicate_of=hashes[sha])
                else:
                    record['status'] = ('archive_pending' if ext in {'.zip', '.rar', '.7z'}
                        else 'recording_pending' if ext in RECORDINGS or ext.startswith('.wem')
                        else 'extraction_pending' if ext in DOCUMENTS
                        else 'image_pending' if ext in IMAGES else 'classification_pending')
                if record['status'] != 'excluded_images_per_user':
                    hashes.setdefault(sha, rel)
            except OSError as error:
                record.update(status='read_error', error=str(error))
            entries.append(record)
        for dirname in dirs[:]:
            p = Path(folder) / dirname
            if p.is_symlink():
                entries.append({'path': p.relative_to(source).as_posix(), 'status': 'symlink_directory_not_followed'})
                dirs.remove(dirname)
    return entries


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--exclude-images', action='store_true')
    args = parser.parse_args()
    source, output = args.source.resolve(), args.output.resolve()
    if not source.is_dir():
        parser.error('Source must be an existing directory')
    if output.is_relative_to(source):
        parser.error('Keep inventory output outside the source directory')
    entries = inventory(source, args.exclude_images)
    counts = {}
    for entry in entries:
        counts[entry['status']] = counts.get(entry['status'], 0) + 1
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps({'source_root': str(source), 'counts': counts, 'entries': entries,
        'notice': 'Inventory only; extraction, archive members and semantic reading remain pending.'}, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'entries': len(entries), 'counts': counts}, ensure_ascii=False))


if __name__ == '__main__':
    main()
