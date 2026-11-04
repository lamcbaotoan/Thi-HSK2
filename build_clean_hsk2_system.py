import sys, pymupdf, re, json, os

sys.stdout.reconfigure(encoding='utf-8')

from test_extract_and_validate import extract_answers, extract_listening_transcripts, H21006_LISTENING
from compile_full_hsk2_database import READING_DATA, H21004_LISTEN_OPTS, H21005_LISTEN_OPTS, get_listening_opts_generic
from verify_and_build_all import clean_sentence_pinyin

def tokens_to_ruby(tokens):
    html_parts = []
    for t in tokens:
        if not t["py"]:
            if t["hz"] == '\n':
                html_parts.append('<br/>')
            else:
                html_parts.append(f'<span class="punct">{t["hz"]}</span>')
        else:
            vi_tooltip = f'<span class="tooltip-text">{t["vi"]}</span>' if t["vi"] else ''
            html_parts.append(f'<ruby class="ruby-item" data-vi="{t["vi"]}">{t["hz"]}<rt>{t["py"]}</rt>{vi_tooltip}</ruby>')
    return "".join(html_parts)

def process_cjk_ruby(text):
    tokens = clean_sentence_pinyin(text)
    ruby_html = tokens_to_ruby(tokens)
    return {"text": text, "ruby": ruby_html}

EXAM_BANK = {}

print("Compiling 6 exams with 100% authoritative Pinyin...")
for pdf in ['h20901.pdf', 'h20902.pdf', 'h21003.pdf', 'h21004.pdf', 'h21005.pdf', 'h21006.pdf']:
    doc = pymupdf.open(pdf)
    exam_id = pdf.replace('.pdf', '')
    ans = extract_answers(doc)
    lt = extract_listening_transcripts(doc, exam_id)
    
    if exam_id == 'h21004':
        lo = H21004_LISTEN_OPTS
    elif exam_id == 'h21005':
        lo = H21005_LISTEN_OPTS
    else:
        lo = get_listening_opts_generic(doc)
        
    rd = READING_DATA[exam_id]
    exam_questions = []
    
    # 1. Listening Part 1 (1 - 10) True/False
    for q in range(1, 11):
        script = lt.get(q, "")
        t_data = process_cjk_ruby(script)
        exam_questions.append({
            "id": q,
            "section": "listening",
            "sectionName": "一、听 力 (Listening)",
            "part": 1,
            "partTitle": "第一部分（第 1 - 10 题）",
            "type": "true_false",
            "image": f"images/listen/{exam_id}_q{q}.png",
            "audioText": script,
            "ruby": t_data["ruby"],
            "answer": ans.get(q, ""),
            "explanation": f"Nội dung audio: {script}"
        })
        
    # 2. Listening Part 2 (11 - 20) Image Match
    for q in range(11, 21):
        script = lt.get(q, "")
        t_data = process_cjk_ruby(script)
        group = "11-15" if q <= 15 else "16-20"
        prefix = f"{exam_id}_1115" if q <= 15 else f"{exam_id}_1620"
        letters = ["A", "B", "C", "D", "E", "F"] if q <= 15 else ["A", "B", "C", "D", "E"]
        image_options = {l: f"images/listen/{prefix}_{l}.png" for l in letters}
        
        exam_questions.append({
            "id": q,
            "section": "listening",
            "sectionName": "一、听 力 (Listening)",
            "part": 2,
            "partTitle": f"第二部分（第 {group} 题）",
            "type": "image_match",
            "group": group,
            "imageOptions": image_options,
            "audioText": script,
            "ruby": t_data["ruby"],
            "answer": ans.get(q, ""),
            "explanation": f"Đoạn đối thoại: {script}"
        })

    # 3. Listening Part 3 (21 - 30) Multiple Choice
    for q in range(21, 31):
        script = lt.get(q, "")
        t_data = process_cjk_ruby(script)
        opts_raw = lo.get(q, {"A": "", "B": "", "C": ""})
        opts_proc = {}
        for l in ["A", "B", "C"]:
            ot = opts_raw.get(l, "")
            opts_proc[l] = process_cjk_ruby(ot)
            
        exam_questions.append({
            "id": q,
            "section": "listening",
            "sectionName": "一、听 力 (Listening)",
            "part": 3,
            "partTitle": "第三部分（第 21 - 30 题）",
            "type": "multiple_choice",
            "audioText": script,
            "ruby": t_data["ruby"],
            "options": opts_proc,
            "answer": ans.get(q, ""),
            "explanation": f"Hội thoại & câu hỏi: {script}"
        })

    # 4. Listening Part 4 (31 - 35) Multiple Choice
    for q in range(31, 36):
        script = lt.get(q, "")
        t_data = process_cjk_ruby(script)
        opts_raw = lo.get(q, {"A": "", "B": "", "C": ""})
        opts_proc = {}
        for l in ["A", "B", "C"]:
            ot = opts_raw.get(l, "")
            opts_proc[l] = process_cjk_ruby(ot)
            
        exam_questions.append({
            "id": q,
            "section": "listening",
            "sectionName": "一、听 力 (Listening)",
            "part": 4,
            "partTitle": "第四部分（第 31 - 35 题）",
            "type": "multiple_choice",
            "audioText": script,
            "ruby": t_data["ruby"],
            "options": opts_proc,
            "answer": ans.get(q, ""),
            "explanation": f"Hội thoại & câu hỏi: {script}"
        })

    # 5. Reading Part 1 (36 - 40) Match image
    p1_imgs = {l: f"images/{exam_id}_{l}.png" for l in ["A", "B", "C", "D", "E", "F"]}
    for q in range(36, 41):
        txt = rd["p1"][q]
        t_data = process_cjk_ruby(txt)
        exam_questions.append({
            "id": q,
            "section": "reading",
            "sectionName": "二、阅 读 (Reading)",
            "part": 1,
            "partTitle": "第一部分（第 36 - 40 题）",
            "type": "image_match",
            "imageOptions": p1_imgs,
            "text": txt,
            "ruby": t_data["ruby"],
            "answer": ans.get(q, ""),
            "explanation": f"Câu văn: {txt}"
        })

    # 6. Reading Part 2 (41 - 45) Fill blank
    p2_opts_proc = {}
    for l, opt_word in rd["p2_options"].items():
        p2_opts_proc[l] = process_cjk_ruby(opt_word)
        
    for q in range(41, 46):
        txt = rd["p2"][q]
        t_data = process_cjk_ruby(txt)
        exam_questions.append({
            "id": q,
            "section": "reading",
            "sectionName": "二、阅 读 (Reading)",
            "part": 2,
            "partTitle": "第二部分（第 41 - 45 题）",
            "type": "fill_blank",
            "options": p2_opts_proc,
            "text": txt,
            "ruby": t_data["ruby"],
            "answer": ans.get(q, ""),
            "explanation": f"Điền từ vào: {txt}"
        })

    # 7. Reading Part 3 (46 - 50) True/False
    for q in range(46, 51):
        p3_item = rd["p3"][q]
        ctx = p3_item["ctx"]
        stmt = p3_item["stmt"]
        ctx_data = process_cjk_ruby(ctx)
        stmt_data = process_cjk_ruby(stmt)
        exam_questions.append({
            "id": q,
            "section": "reading",
            "sectionName": "二、阅 读 (Reading)",
            "part": 3,
            "partTitle": "第三部分（第 46 - 50 题）",
            "type": "true_false_reading",
            "context": ctx,
            "statement": stmt,
            "contextRuby": ctx_data["ruby"],
            "statementRuby": stmt_data["ruby"],
            "answer": ans.get(q, ""),
            "explanation": f"Đoạn văn: {ctx} => Nhận định: {stmt}"
        })

    # 8. Reading Part 4 (51 - 60) Dialogue match
    p4a_opts = {l: process_cjk_ruby(text) for l, text in rd["p4_5155_options"].items()}
    for q in range(51, 56):
        txt = rd["p4_5155"][q]
        t_data = process_cjk_ruby(txt)
        exam_questions.append({
            "id": q,
            "section": "reading",
            "sectionName": "二、阅 读 (Reading)",
            "part": 4,
            "partTitle": "第四部分（第 51 - 55 题）",
            "type": "dialogue_match",
            "group": "51-55",
            "options": p4a_opts,
            "text": txt,
            "ruby": t_data["ruby"],
            "answer": ans.get(q, ""),
            "explanation": f"Câu đối thoại: {txt}"
        })

    p4b_opts = {l: process_cjk_ruby(text) for l, text in rd["p4_5660_options"].items()}
    for q in range(56, 61):
        txt = rd["p4_5660"][q]
        t_data = process_cjk_ruby(txt)
        exam_questions.append({
            "id": q,
            "section": "reading",
            "sectionName": "二、阅 读 (Reading)",
            "part": 4,
            "partTitle": "第四部分（第 56 - 60 题）",
            "type": "dialogue_match",
            "group": "56-60",
            "options": p4b_opts,
            "text": txt,
            "ruby": t_data["ruby"],
            "answer": ans.get(q, ""),
            "explanation": f"Câu đối thoại: {txt}"
        })

    EXAM_BANK[exam_id] = {
        "id": exam_id,
        "name": f"Đề thi HSK 2 - {exam_id.upper()} (Chính thức Hanban)",
        "questions": exam_questions
    }
    print(f"  {exam_id}: compiled 60 questions")

# Save hsk2_full_database.js
js_code = f"const HSK2_FULL_DATABASE = {json.dumps(EXAM_BANK, ensure_ascii=False, indent=2)};\n"
with open("hsk2_full_database.js", "w", encoding="utf-8") as f:
    f.write(js_code)
print("Saved hsk2_full_database.js cleanly! Size:", os.path.getsize("hsk2_full_database.js"))

