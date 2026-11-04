import sys, os
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')
os.makedirs('screenshots', exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1280, "height": 900})
    
    file_path = f"file:///{os.path.abspath('index.html').replace('\\', '/')}"
    print(f"Loading {file_path}...")
    page.goto(file_path)
    page.wait_for_load_state("networkidle")
    
    title = page.title()
    print("Page title:", title)
    assert "HSK 2" in title
    
    # 1. Screenshot of Home Screen
    page.screenshot(path="screenshots/01_home_screen.png")
    print("Saved 01_home_screen.png")
    
    # 2. Select H20901, Full 60 questions, Study Mode
    page.click('input[value="h20901"]')
    page.click('input[value="study"]')
    page.click('text=Bắt Đầu Làm Bài')
    page.wait_for_selector('#questions-container')
    
    # Verify 60 questions are rendered
    cards = page.query_selector_all('[id^="q-card-"]')
    print(f"Rendered question cards: {len(cards)}")
    assert len(cards) == 60, f"Expected 60 questions, got {len(cards)}"
    
    # Screenshot of Exam Screen (Listening Part 1)
    page.screenshot(path="screenshots/02_exam_listening_p1.png")
    print("Saved 02_exam_listening_p1.png")
    
    # 3. Check Question 46 specifically
    q46 = page.query_selector('#q-card-46')
    assert q46 is not None, "Question 46 card not found!"
    q46_text = q46.inner_text()
    print("Question 46 text snippet:", q46_text[:120].replace('\n', ' '))
    assert "个" in q46_text, "Expected '个' in question 46 text!"
    assert "部" not in q46_text, "Found unexpected '部' in question 46 text!"
    
    q46.scroll_into_view_if_needed()
    page.screenshot(path="screenshots/03_question_46_verified_ge.png")
    print("Saved 03_question_46_verified_ge.png")
    
    # 4. Select answers for questions 1, 11, 21, 36, 46, 51
    page.click('#opt-btn-1-×')
    page.click('#opt-btn-46-√')
    
    # Open navigation drawer
    page.click('text=Bảng câu hỏi')
    page.screenshot(path="screenshots/04_nav_drawer.png")
    print("Saved 04_nav_drawer.png")
    page.click('#nav-drawer button:has-text("×")')
    
    # 5. Submit exam
    page.on("dialog", lambda dialog: dialog.accept())
    page.click('button:has-text("Hoàn Thành & Nộp Bài Thi")')
    page.wait_for_selector('#screen-result:not(.hidden)')
    
    total_score = page.inner_text('#score-total')
    print("Result total score:", total_score)
    page.screenshot(path="screenshots/05_result_screen.png")
    print("Saved 05_result_screen.png")

    browser.close()

print("ALL PLAYWRIGHT TESTS PASSED SUCCESSFULLY!")

