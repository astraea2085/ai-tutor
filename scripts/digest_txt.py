import os
import json
import re
from pathlib import Path
import argparse
import sys

def chunk_text(text, target_length=600, overlap=50):
    """
    Split text into chunks of approximately `target_length` characters.
    Tries to split on paragraphs or strong punctuation to keep semantic meaning intact.
    Includes an `overlap` of characters from the previous chunk to maintain context.
    """
    # Split into sentences or smaller semantic blocks using regex
    # Match Chinese and English sentence enders
    blocks = re.split(r'(?<=[。！？!?\n])\s*', text)
    
    chunks = []
    current_chunk = ""
    
    for block in blocks:
        block = block.strip()
        if not block:
            continue
            
        if len(current_chunk) + len(block) > target_length and len(current_chunk) > target_length * 0.5:
            chunks.append(current_chunk.strip())
            # Keep the overlap from the end of the current chunk for the next one
            overlap_text = current_chunk[-overlap:] if len(current_chunk) > overlap else current_chunk
            # Find the first full sentence in the overlap if possible
            overlap_match = re.search(r'[^。！？!?\n]+[。！？!?\n]+\s*$', overlap_text)
            if overlap_match:
                overlap_text = overlap_match.group(0)
            
            current_chunk = overlap_text + " " + block if overlap_text else block
        else:
            if current_chunk:
                current_chunk += " " + block
            else:
                current_chunk = block
                
    if current_chunk:
        chunks.append(current_chunk.strip())
        
    return chunks

def update_state(course_id, total_chunks):
    """
    Automatically registers the course into the state machine.
    """
    state_path = os.path.expanduser("~/.openclaw/workspace/memory/ai-tutor-state.json")
    state_dir = os.path.dirname(state_path)
    if not os.path.exists(state_dir):
        os.makedirs(state_dir, exist_ok=True)
        
    state = {"active_course": "", "courses": {}}
    if os.path.exists(state_path):
        try:
            with open(state_path, 'r', encoding='utf-8') as f:
                state = json.load(f)
        except Exception:
            pass
            
    if "courses" not in state:
        state["courses"] = {}
        
    if course_id not in state["courses"]:
        state["courses"][course_id] = {
            "current_chunk": 0,
            "total_chunks": total_chunks,
            "last_interaction": "",
            "review_queue": []
        }
    else:
        state["courses"][course_id]["total_chunks"] = total_chunks
        if "review_queue" not in state["courses"][course_id]:
            state["courses"][course_id]["review_queue"] = []
            
    if not state.get("active_course"):
        state["active_course"] = course_id
        
    try:
        with open(state_path, 'w', encoding='utf-8') as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
        print(f"   State updated: '{course_id}' registered in ai-tutor-state.json")
    except Exception as e:
        print(f"Error updating state: {e}")

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
        update_state(filename, len(chunks))
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
