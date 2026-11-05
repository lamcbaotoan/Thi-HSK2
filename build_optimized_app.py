import sys, json, os, re
sys.stdout.reconfigure(encoding='utf-8')

from verify_and_build_all import OFFICIAL_LEXICON, CONTEXT_OVERRIDES

# Read the compact database from hsk2_full_database.js
with open('hsk2_full_database.js', 'r', encoding='utf-8') as f:
    text = f.read()

start = text.find('{')
end = text.rfind('}') + 1
full_db = json.loads(text[start:end])

# Create ultra-clean database without precomputed ruby HTML strings
optimized_db = {}
for exam_id, exam in full_db.items():
    clean_questions = []
    for q in exam['questions']:
        cq = {}
        for k, v in q.items():
            if k in ['ruby', 'contextRuby', 'statementRuby']:
                continue
            if k == 'options' and isinstance(v, dict):
                clean_opts = {}
                for l, opt in v.items():
                    if isinstance(opt, dict) and 'text' in opt:
                        clean_opts[l] = opt['text']
                    else:
                        clean_opts[l] = opt
                cq['options'] = clean_opts
            else:
                cq[k] = v
        clean_questions.append(cq)
    optimized_db[exam_id] = {
        'id': exam['id'],
        'name': exam['name'],
        'questions': clean_questions
    }

print("Raw questions optimized!")
opt_db_json = json.dumps(optimized_db, ensure_ascii=False)
print("Optimized DB size:", len(opt_db_json), "bytes")

# Lexicon and Overrides
lexicon_json = json.dumps(OFFICIAL_LEXICON, ensure_ascii=False)
overrides_json = json.dumps(CONTEXT_OVERRIDES, ensure_ascii=False)

# Read current update_index_html_dual_voice.py to get the UI template
with open('update_index_html_dual_voice.py', 'r', encoding='utf-8') as f:
    template_code = f.read()

# Extract HTML portion up to line <!-- JAVASCRIPT LOGIC
idx_split = template_code.find('<!-- JAVASCRIPT LOGIC')
html_top = template_code[template_code.find('<!DOCTYPE html>'):idx_split]

# Create JavaScript Engine
js_engine = f"""
  <!-- ============================================================== -->
  <!-- JAVASCRIPT LOGIC & HSK 2 ULTRA-FAST ENGINE -->
  <!-- ============================================================== -->
  <script>
    // 1. Authoritative HSK 2 Lexicon & Polyphone Overrides
    const HSK2_LEXICON = {lexicon_json};
    const HSK2_OVERRIDES = {overrides_json};
    const HSK2_SORTED_KEYS = Object.keys(HSK2_LEXICON).sort((a, b) => b.length - a.length);

    // Dynamic Ruby Generator
    function matchPrefixIgnoringSpaces(str, target) {{
      let sIdx = 0, tIdx = 0;
      while (sIdx < str.length && tIdx < target.length) {{
        if (/\\s/.test(str[sIdx])) {{
          sIdx++;
          continue;
        }}
        if (str[sIdx] === target[tIdx]) {{
          sIdx++;
          tIdx++;
        }} else {{
          return 0;
        }}
      }}
      return (tIdx === target.length) ? sIdx : 0;
    }}

    function formatRuby(sentence) {{
      if (!sentence) return '';
      const cleanS = sentence.trim();
      let i = 0;
      let html = '';

      while (i < cleanS.length) {{
        // Whitespace
        if (/\\s/.test(cleanS[i])) {{
          html += '<span class="punct"> </span>';
          i++;
          continue;
        }}
        // Newline
        if (cleanS[i] === '\\n') {{
          html += '<br/>';
          i++;
          continue;
        }}
        // Context Overrides (Polyphones like 眼睛得休息, 买了个新手机, 笑着)
        let matchedOverride = false;
        for (const ctxPhrase in HSK2_OVERRIDES) {{
          const matchLen = matchPrefixIgnoringSpaces(cleanS.substring(i), ctxPhrase);
          if (matchLen > 0) {{
            const tokens = HSK2_OVERRIDES[ctxPhrase];
            for (const t of tokens) {{
              const hz = t[0], py = t[1], vi = t[2];
              html += `<ruby class="ruby-item" data-vi="${{vi}}">${{hz}}<rt>${{py}}</rt><span class="tooltip-text">${{vi}}</span></ruby>`;
            }}
            i += matchLen;
            matchedOverride = true;
            break;
          }}
        }}
        if (matchedOverride) continue;

        // Standard Lexicon
        let matchedLex = false;
        for (const word of HSK2_SORTED_KEYS) {{
          const matchLen = matchPrefixIgnoringSpaces(cleanS.substring(i), word);
          if (matchLen > 0) {{
            const [py, vi] = HSK2_LEXICON[word];
            html += `<ruby class="ruby-item" data-vi="${{vi}}">${{word}}<rt>${{py}}</rt><span class="tooltip-text">${{vi}}</span></ruby>`;
            i += matchLen;
            matchedLex = true;
            break;
          }}
        }}
        if (matchedLex) continue;

        // Fallback
        const c = cleanS[i];
        if (c >= '\\u4e00' && c <= '\\u9fff') {{
          html += `<ruby class="ruby-item">${{c}}<rt></rt></ruby>`;
        }} else {{
          html += `<span class="punct">${{c}}</span>`;
        }}
        i++;
      }}
      return html;
    }}

    // 2. Official 6-Exam Database (Ultra-Compact)
    const HSK2_FULL_DATABASE = {opt_db_json};
"""

# Extract the rest of the JS logic from update_index_html_dual_voice.py (STATE, startExam, SpeechSynthesis, etc.)
idx_state = template_code.find('const STATE = {')
idx_end_script = template_code.rfind('</script>')
rest_js = template_code[idx_state:idx_end_script]

# Replace old ruby references in rest_js:
# q.ruby -> formatRuby(q.audioText || q.text)
rest_js = rest_js.replace('${q.ruby}', '${formatRuby(q.audioText || q.text)}')
rest_js = rest_js.replace('${q.contextRuby}', '${formatRuby(q.context)}')
rest_js = rest_js.replace('${q.statementRuby}', '${formatRuby(q.statement)}')
rest_js = rest_js.replace('${opt.ruby || opt.text}', '${formatRuby(typeof opt === "string" ? opt : (opt.text || ""))}')

full_html = html_top + js_engine + "\n" + rest_js + "\n  </script>\n</body>\n</html>"

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(full_html)

print("Saved optimized index.html! New file size:", os.path.getsize('index.html'), "bytes")

# Also save optimized hsk2_full_database.js
with open('hsk2_full_database.js', 'w', encoding='utf-8') as f:
    f.write(f"const HSK2_FULL_DATABASE = {opt_db_json};\n")
print("Saved optimized hsk2_full_database.js! New file size:", os.path.getsize('hsk2_full_database.js'), "bytes")

