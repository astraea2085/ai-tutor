import os
import json
import re
from pathlib import Path
import argparse
import sys

def chunk_text(text, target_length=600):
    """
    Split text into chunks of approximately `target_length` characters.
    Tries to split on paragraphs or strong punctuation to keep semantic meaning intact.
    """
    # First, try splitting by double newlines (paragraphs)
    paragraphs = re.split(r'\n\s*\n', text)
    
    chunks = []
    current_chunk = ""
    
    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
            
        # If adding this paragraph exceeds the target significantly, save the current chunk
        if len(current_chunk) + len(para) > target_length and len(current_chunk) > target_length * 0.5:
            chunks.append(current_chunk.strip())
            current_chunk = para
        else:
            if current_chunk:
                current_chunk += "\n\n" + para
            else:
                current_chunk = para
                
    if current_chunk:
        chunks.append(current_chunk.strip())
        
    return chunks

def process_file(input_path, output_dir):
    """
    Reads a raw .txt file, chunks it, and saves it as a JSON array.
    """
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {input_path}: {e}")
        return False

    if not content.strip():
        print(f"File {input_path} is empty. Skipping.")
        return False

    chunks = chunk_text(content)
    
    # Metadata for the course
    filename = Path(input_path).stem
    course_data = {
        "course_id": filename,
        "total_chunks": len(chunks),
        "chunks": chunks
    }
    
    output_path = os.path.join(output_dir, f"{filename}.json")
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(course_data, f, ensure_ascii=False, indent=2)
        print(f"✅ Successfully processed '{filename}': {len(chunks)} chunks generated.")
        print(f"   Saved to: {output_path}")
        return True
    except Exception as e:
        print(f"Error saving {output_path}: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="AI Tutor: Parse raw TXT materials into JSON chunks for Socratic teaching.")
    parser.add_argument('--raw-dir', type=str, default=os.path.expanduser("~/.openclaw/workspace/knowledge/ai-tutor/raw"), 
                        help="Directory containing raw .txt files")
    parser.add_argument('--out-dir', type=str, default=os.path.expanduser("~/.openclaw/workspace/knowledge/ai-tutor/materials"), 
                        help="Directory to save the parsed .json files")
    
    args = parser.parse_args()
    
    raw_dir = Path(args.raw_dir)
    out_dir = Path(args.out_dir)
    
    if not raw_dir.exists():
        print(f"❌ Raw directory not found: {raw_dir}")
        sys.exit(1)
        
    out_dir.mkdir(parents=True, exist_ok=True)
    
    txt_files = list(raw_dir.glob("*.txt"))
    if not txt_files:
        print(f"ℹ️ No .txt files found in {raw_dir}. Please drop some transcripts there.")
        return

    print(f"Found {len(txt_files)} file(s). Processing...")
    
    success_count = 0
    for txt_file in txt_files:
        if process_file(txt_file, out_dir):
            success_count += 1
            
    print(f"\n🎉 Done! {success_count}/{len(txt_files)} files processed successfully.")

if __name__ == "__main__":
    main()
