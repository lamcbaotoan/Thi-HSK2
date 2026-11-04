import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

from playwright.sync_api import sync_playwright

def verify_app():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        
        # Listen for console errors
        errors = []
        page.on("pageerror", lambda err: errors.append(str(err)))
        page.on("console", lambda msg: errors.append(f"Console {msg.type}: {msg.text}") if msg.type == "error" else None)
        
        index_url = f"file:///{os.path.abspath('index.html').replace(os.sep, '/')}"
        print(f"Loading {index_url}...")
        page.goto(index_url, wait_until="networkidle")
        
        # Check title
        title = page.title()
        print(f"Page Title: {title}")
        
        # Check source radio options
        h20901_radio = page.query_selector('input[name="exam-source"][value="h20901"]')
        print(f"H20901 option found: {h20901_radio is not None}")
        
        # Select H20901 and Study Mode
        h20901_radio.click()
        study_radio = page.query_selector('input[name="exam-mode"][value="study"]')
        study_radio.click()
        
        # Click start exam
        print("Clicking Start Exam...")
        page.click('button:has-text("Bắt Đầu Làm Bài")')
        page.wait_for_timeout(1000)
        
        # Check number of rendered question cards (1 to 60)
        cards = page.query_selector_all('div[id^="q-card-"]')
        print(f"Total question cards rendered: {len(cards)}")
        assert len(cards) == 60, f"Expected 60 questions, got {len(cards)}"
        
        # Check if Listening Audio buttons exist
        dual_audio_btns = page.query_selector_all('button:has-text("Phát 2 lần")')
        female_btns = page.query_selector_all('button:has-text("👩 Nữ")')
        male_btns = page.query_selector_all('button:has-text("👨 Nam")')
        print(f"Dual-Voice Audio buttons: {len(dual_audio_btns)}")
        print(f"Female buttons: {len(female_btns)}")
        print(f"Male buttons: {len(male_btns)}")
        assert len(dual_audio_btns) >= 35, f"Expected at least 35 dual audio buttons, got {len(dual_audio_btns)}"
        
        # Check if "例如 (Ví dụ)" cards exist
        example_headings = page.query_selector_all('span:has-text("例如 (Ví dụ)")')
        print(f"Total Example cards (例如): {len(example_headings)}")
        assert len(example_headings) >= 8, f"Expected at least 8 example cards (4 listening + 4 reading), got {len(example_headings)}"
        
        # Verify text of Q46 in H20901: should have 个 (ge) and no internal apostrophes like shǒu'jī
        content = page.content()
        assert "个<rt>ge</rt>" in content, "Q46 should contain 个 with pinyin ge"
        assert "手机<rt>shǒujī</rt>" in content, "Q46 should contain 手机 with clean pinyin shǒujī"
        assert "shǒu'jī" not in content, "Content should not contain shǒu'jī"
        assert "pián'yi" not in content, "Content should not contain pián'yi"
        print("Pinyin check passed: No unwanted apostrophes found! Correct '个 (ge)' and '手机 (shǒujī)' confirmed.")
        
        # Test clicking an audio button
        first_audio_btn = dual_audio_btns[0]
        print("Clicking first dual-voice audio button...")
        first_audio_btn.click()
        page.wait_for_timeout(500)
        
        # Check floating audio player visibility
        floating_player = page.query_selector("#floating-audio-player")
        if floating_player:
            is_visible = floating_player.is_visible()
            print(f"Floating audio player visible: {is_visible}")
            player_text = floating_player.inner_text()
            print(f"Floating audio status text: {player_text}")
        
        # Take a screenshot of the top section (Listening Part 1 + Example)
        os.makedirs("screenshots", exist_ok=True)
        page.screenshot(path="screenshots/dual_voice_exam_p1.png")
        print("Saved screenshots/dual_voice_exam_p1.png")
        
        # Scroll to Reading Part 1 (Q36)
        page.evaluate("() => { const q36 = document.getElementById('q-card-36'); if (q36) q36.scrollIntoView(); }")
        page.wait_for_timeout(500)
        page.screenshot(path="screenshots/dual_voice_reading_p1.png")
        print("Saved screenshots/dual_voice_reading_p1.png")
        
        # Scroll to Q46 (Reading Part 2 with 买了个新手机)
        page.evaluate("() => { const q46 = document.getElementById('q-card-46'); if (q46) q46.scrollIntoView(); }")
        page.wait_for_timeout(500)
        page.screenshot(path="screenshots/dual_voice_q46_check.png")
        print("Saved screenshots/dual_voice_q46_check.png")
        
        if errors:
            print(f"Warning: Found {len(errors)} errors/warnings:")
            for e in errors:
                print("  -", e)
        else:
            print("Zero console errors detected!")
            
        browser.close()

if __name__ == "__main__":
    verify_app()
