import sys, json, os

sys.stdout.reconfigure(encoding='utf-8')

print("Reading hsk2_full_database.js...")
with open("hsk2_full_database.js", "r", encoding="utf-8") as f:
    db_content = f.read()

# We also have REAL_IMAGES for reading Part 1 if needed as base64, or images/ folder
# Let's check images folder
print("Database loaded. Size:", len(db_content), "chars")

HTML_TEMPLATE = r'''<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Thi Thử HSK 2 Chuẩn Hanban - Đầy Đủ 60 Câu (Nghe & Đọc)</title>
  <!-- Tailwind CSS CDN -->
  <script src="https://cdn.tailwindcss.com"></script>
  <!-- Google Fonts: Noto Serif SC for authentic paper exam aesthetic -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Ma+Shan+Zheng&family=Noto+Serif+SC:wght@400;600;700&family=Playfair+Display:ital,wght@0,600;1,600&display=swap" rel="stylesheet">
  <script>
    tailwind.config = {
      theme: {
        extend: {
          fontFamily: {
            serif: ['"Noto Serif SC"', 'SimSun', 'STSong', 'KaiTi', 'serif'],
            display: ['"Playfair Display"', 'Georgia', 'serif'],
            calligraphy: ['"Ma Shan Zheng"', 'cursive']
          },
          colors: {
            hanban: {
              red: '#C8102E',
              darkRed: '#9B0D23',
              gold: '#D4AF37',
              paper: '#FAF7F2',
              ink: '#1F2421',
              border: '#E5DFD5'
            }
          }
        }
      }
    }
  </script>
  <style>
    /* Paper texture & exam styling */
    body {
      background-color: #F4F1EA;
      color: #1F2421;
      font-family: "Noto Serif SC", "SimSun", "STSong", "KaiTi", serif;
      -webkit-font-smoothing: antialiased;
    }
    
    .paper-sheet {
      background-color: #FFFFFF;
      box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.08), 0 2px 6px -1px rgba(0, 0, 0, 0.04);
      border: 1px solid #E5DFD5;
    }

    /* Ruby Pinyin styling */
    ruby {
      display: inline-flex;
      flex-direction: column-reverse;
      vertical-align: bottom;
      line-height: 1.1;
      position: relative;
      margin: 0 2px;
      cursor: pointer;
    }

    rt {
      display: block;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      font-size: 0.68rem;
      font-weight: 500;
      color: #78350F; /* warm amber */
      text-align: center;
      line-height: 1.1;
      user-select: none;
      padding-bottom: 2px;
    }

    /* Tooltip for Study Mode */
    .study-mode ruby:hover .tooltip-text,
    .study-mode ruby:focus .tooltip-text,
    .review-mode ruby:hover .tooltip-text {
      visibility: visible;
      opacity: 1;
      transform: translateY(0);
    }

    .tooltip-text {
      visibility: hidden;
      opacity: 0;
      position: absolute;
      bottom: -32px;
      left: 50%;
      transform: translateX(-50%) translateY(4px);
      background-color: #1F2937;
      color: #F9FAFB;
      text-align: center;
      padding: 3px 8px;
      border-radius: 4px;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      font-size: 0.75rem;
      white-space: nowrap;
      z-index: 50;
      box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
      transition: opacity 0.15s ease, transform 0.15s ease;
      pointer-events: none;
    }

    .tooltip-text::after {
      content: "";
      position: absolute;
      top: -4px;
      left: 50%;
      margin-left: -4px;
      border-width: 4px;
      border-style: solid;
      border-color: transparent transparent #1F2937 transparent;
    }

    /* Exam mode overrides: no tooltip */
    .exam-mode .tooltip-text {
      display: none !important;
    }

    /* Audio playing wave animation */
    @keyframes wave {
      0%, 100% { height: 4px; }
      50% { height: 16px; }
    }
    .wave-bar {
      animation: wave 1s infinite ease-in-out;
    }
    .wave-bar:nth-child(2) { animation-delay: 0.2s; }
    .wave-bar:nth-child(3) { animation-delay: 0.4s; }

    /* Custom radio buttons */
    .option-btn {
      transition: all 0.15s ease;
    }
    .option-btn.selected {
      background-color: #FEF3C7;
      border-color: #D97706;
      color: #92400E;
      font-weight: 600;
    }
  </style>
</head>
<body class="min-h-screen flex flex-col antialiased">

  <!-- Top Global Header -->
  <header class="bg-hanban-red text-white shadow-md sticky top-0 z-40">
    <div class="max-w-5xl mx-auto px-4 py-3 flex items-center justify-between">
      <div class="flex items-center space-x-3 cursor-pointer" onclick="goToHome()">
        <div class="w-9 h-9 rounded-full bg-white text-hanban-red flex items-center justify-center font-bold text-lg shadow-inner">
          汉
        </div>
        <div>
          <h1 class="text-lg font-bold tracking-wide flex items-center gap-2">
            HSK 2 模拟考试系统
            <span class="text-xs bg-yellow-400 text-red-900 font-semibold px-2 py-0.5 rounded-full uppercase tracking-wider">Chuẩn Hanban 60 Câu</span>
          </h1>
          <p class="text-xs text-red-100 hidden sm:block">Mô phỏng 100% đề thi chính thức: Nghe (1-35) & Đọc (36-60)</p>
        </div>
      </div>

      <!-- Action buttons & timer in header -->
      <div class="flex items-center space-x-3">
        <!-- Timer Badge (visible when test is active) -->
        <div id="header-timer" class="hidden items-center space-x-2 bg-red-900/80 border border-red-700/60 px-3 py-1 rounded-full text-sm font-mono font-bold text-yellow-300">
          <svg class="w-4 h-4 animate-pulse text-yellow-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
          </svg>
          <span id="timer-display">50:00</span>
        </div>

        <!-- Quick navigation toggle -->
        <button id="btn-show-grid" class="hidden sm:hidden items-center px-2.5 py-1 text-xs bg-red-800 hover:bg-red-700 rounded text-white" onclick="toggleNavDrawer()">
          Danh sách câu
        </button>

        <button id="btn-header-submit" class="hidden bg-yellow-400 hover:bg-yellow-500 text-red-900 font-bold px-3.5 py-1 text-sm rounded shadow transition" onclick="submitExam(true)">
          Nộp bài
        </button>
      </div>
    </div>
  </header>

  <!-- Main Container -->
  <main class="flex-1 max-w-5xl w-full mx-auto p-4 sm:p-6">

    <!-- ========================================== -->
    <!-- 1. SCREEN: SETUP & EXAM SELECTION (HOME) -->
    <!-- ========================================== -->
    <div id="screen-home" class="space-y-6">
      
      <!-- Welcome Banner -->
      <div class="paper-sheet rounded-xl p-6 sm:p-8 border-l-4 border-l-hanban-red bg-gradient-to-r from-white via-amber-50/20 to-orange-50/30">
        <div class="flex flex-col md:flex-row md:items-center justify-between gap-6">
          <div>
            <div class="inline-flex items-center gap-2 px-2.5 py-0.5 rounded-full bg-red-100 text-red-800 text-xs font-semibold mb-3">
              ★ Đề thi HSK 2 chuẩn Quốc tế Hanban
            </div>
            <h2 class="text-2xl sm:text-3xl font-bold text-gray-900 mb-2">
              Luyện Thi Thử HSK Cấp 2 Trực Tuyến
            </h2>
            <p class="text-gray-600 text-sm sm:text-base leading-relaxed max-w-2xl">
              Hệ thống mô phỏng chính xác cấu trúc đề thi giấy thật của Hanban với đầy đủ <b>60 câu hỏi</b> (35 câu Nghe + 25 câu Đọc), có hiển thị Pinyin chuẩn trên chữ Hán, phát âm Audio giọng đọc phổ thông, tra từ điển nghĩa Tiếng Việt tương tác và chấm điểm tự động.
            </p>
          </div>
          <div class="shrink-0 flex sm:flex-col gap-2 text-center text-xs text-gray-500">
            <div class="bg-gray-50 border border-gray-200 rounded-lg p-3">
              <span class="block text-xl font-bold text-hanban-red">6</span>
              Đề thi chính thức
            </div>
            <div class="bg-gray-50 border border-gray-200 rounded-lg p-3">
              <span class="block text-xl font-bold text-hanban-red">360</span>
              Tổng số câu hỏi
            </div>
          </div>
        </div>
      </div>

      <!-- Config Options Card -->
      <div class="paper-sheet rounded-xl p-6 sm:p-8 space-y-6">
        <h3 class="text-lg font-bold text-gray-900 border-b pb-3 flex items-center gap-2">
          <span>⚙️</span> Thiết Lập Bài Thi
        </h3>

        <!-- 1. Scope Selection -->
        <div>
          <label class="block text-sm font-bold text-gray-700 mb-2">1. Chọn phần thi (Phạm vi câu hỏi):</label>
          <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
            <label class="relative flex flex-col p-4 border-2 rounded-xl cursor-pointer hover:bg-amber-50/30 transition has-[:checked]:border-hanban-red has-[:checked]:bg-amber-50/50">
              <input type="radio" name="exam-scope" value="full" class="sr-only" checked onchange="updateScopeInfo()">
              <div class="flex items-center justify-between mb-1">
                <span class="font-bold text-gray-900 text-base">Toàn Bộ Đề Thi</span>
                <span class="text-xs bg-red-100 text-red-800 font-bold px-2 py-0.5 rounded">60 Câu</span>
              </div>
              <p class="text-xs text-gray-500 mt-1">Câu 1 - 60 (Nghe 1-35 & Đọc 36-60). Chuẩn 50 phút, 200 điểm.</p>
            </label>

            <label class="relative flex flex-col p-4 border-2 rounded-xl cursor-pointer hover:bg-amber-50/30 transition has-[:checked]:border-hanban-red has-[:checked]:bg-amber-50/50">
              <input type="radio" name="exam-scope" value="reading" class="sr-only" onchange="updateScopeInfo()">
              <div class="flex items-center justify-between mb-1">
                <span class="font-bold text-gray-900 text-base">Phần Đọc Hiểu</span>
                <span class="text-xs bg-amber-100 text-amber-800 font-bold px-2 py-0.5 rounded">25 Câu</span>
              </div>
              <p class="text-xs text-gray-500 mt-1">Câu 36 - 60 (Đọc hiểu 4 phần). Chuẩn 22 phút, 100 điểm.</p>
            </label>

            <label class="relative flex flex-col p-4 border-2 rounded-xl cursor-pointer hover:bg-amber-50/30 transition has-[:checked]:border-hanban-red has-[:checked]:bg-amber-50/50">
              <input type="radio" name="exam-scope" value="listening" class="sr-only" onchange="updateScopeInfo()">
              <div class="flex items-center justify-between mb-1">
                <span class="font-bold text-gray-900 text-base">Phần Nghe Hiểu</span>
                <span class="text-xs bg-blue-100 text-blue-800 font-bold px-2 py-0.5 rounded">35 Câu</span>
              </div>
              <p class="text-xs text-gray-500 mt-1">Câu 1 - 35 (Nghe hiểu 4 phần). Chuẩn 25 phút, 100 điểm.</p>
            </label>
          </div>
        </div>

        <!-- 2. Source Selection -->
        <div>
          <label class="block text-sm font-bold text-gray-700 mb-2">2. Chọn nguồn đề thi:</label>
          <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-3">
            <label class="flex items-center gap-3 p-3 border-2 rounded-xl cursor-pointer hover:bg-amber-50/30 transition has-[:checked]:border-hanban-red has-[:checked]:bg-amber-50/50">
              <input type="radio" name="exam-source" value="random" class="text-hanban-red" checked>
              <div>
                <span class="font-bold text-sm text-gray-900 block">🎲 Đề Trộn Ngẫu Nhiên</span>
                <span class="text-xs text-gray-500">Bốc từ 360 câu hỏi</span>
              </div>
            </label>

            <label class="flex items-center gap-3 p-3 border-2 rounded-xl cursor-pointer hover:bg-amber-50/30 transition has-[:checked]:border-hanban-red has-[:checked]:bg-amber-50/50">
              <input type="radio" name="exam-source" value="h20901" class="text-hanban-red">
              <div>
                <span class="font-bold text-sm text-gray-900 block">Đề thi H20901</span>
                <span class="text-xs text-gray-500">Đề chính thức Hanban</span>
              </div>
            </label>

            <label class="flex items-center gap-3 p-3 border-2 rounded-xl cursor-pointer hover:bg-amber-50/30 transition has-[:checked]:border-hanban-red has-[:checked]:bg-amber-50/50">
              <input type="radio" name="exam-source" value="h20902" class="text-hanban-red">
              <div>
                <span class="font-bold text-sm text-gray-900 block">Đề thi H20902</span>
                <span class="text-xs text-gray-500">Đề chính thức Hanban</span>
              </div>
            </label>

            <label class="flex items-center gap-3 p-3 border-2 rounded-xl cursor-pointer hover:bg-amber-50/30 transition has-[:checked]:border-hanban-red has-[:checked]:bg-amber-50/50">
              <input type="radio" name="exam-source" value="h21003" class="text-hanban-red">
              <div>
                <span class="font-bold text-sm text-gray-900 block">Đề thi H21003</span>
                <span class="text-xs text-gray-500">Đề chính thức Hanban</span>
              </div>
            </label>

            <label class="flex items-center gap-3 p-3 border-2 rounded-xl cursor-pointer hover:bg-amber-50/30 transition has-[:checked]:border-hanban-red has-[:checked]:bg-amber-50/50">
              <input type="radio" name="exam-source" value="h21004" class="text-hanban-red">
              <div>
                <span class="font-bold text-sm text-gray-900 block">Đề thi H21004</span>
                <span class="text-xs text-gray-500">Đề chính thức Hanban</span>
              </div>
            </label>

            <label class="flex items-center gap-3 p-3 border-2 rounded-xl cursor-pointer hover:bg-amber-50/30 transition has-[:checked]:border-hanban-red has-[:checked]:bg-amber-50/50">
              <input type="radio" name="exam-source" value="h21005" class="text-hanban-red">
              <div>
                <span class="font-bold text-sm text-gray-900 block">Đề thi H21005</span>
                <span class="text-xs text-gray-500">Đề chính thức Hanban</span>
              </div>
            </label>

            <label class="flex items-center gap-3 p-3 border-2 rounded-xl cursor-pointer hover:bg-amber-50/30 transition has-[:checked]:border-hanban-red has-[:checked]:bg-amber-50/50">
              <input type="radio" name="exam-source" value="h21006" class="text-hanban-red">
              <div>
                <span class="font-bold text-sm text-gray-900 block">Đề thi H21006</span>
                <span class="text-xs text-gray-500">Đề chính thức Hanban</span>
              </div>
            </label>
          </div>
        </div>

        <!-- 3. Mode Selection -->
        <div>
          <label class="block text-sm font-bold text-gray-700 mb-2">3. Chọn chế độ làm bài:</label>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <label class="flex items-start gap-3 p-4 border-2 rounded-xl cursor-pointer hover:bg-amber-50/30 transition has-[:checked]:border-amber-600 has-[:checked]:bg-amber-50/50">
              <input type="radio" name="exam-mode" value="study" class="mt-1 text-amber-600" checked>
              <div>
                <span class="font-bold text-base text-gray-900 block flex items-center gap-2">
                  <span>📖</span> Chế Độ Luyện Tập (Study Mode)
                </span>
                <ul class="text-xs text-gray-600 mt-2 space-y-1">
                  <li>• <b>Không giới hạn thời gian</b> làm bài.</li>
                  <li>• <b>Pinyin hiển thị sẵn</b> trên toàn bộ chữ Hán.</li>
                  <li>• <b>Hover hoặc chạm</b> vào chữ để xem nghĩa tiếng Việt (Tooltip).</li>
                  <li>• Nút nghe Audio đàm thoại, xem ngay giải thích khi cần.</li>
                </ul>
              </div>
            </label>

            <label class="flex items-start gap-3 p-4 border-2 rounded-xl cursor-pointer hover:bg-red-50/30 transition has-[:checked]:border-hanban-red has-[:checked]:bg-red-50/50">
              <input type="radio" name="exam-mode" value="exam" class="mt-1 text-hanban-red">
              <div>
                <span class="font-bold text-base text-gray-900 block flex items-center gap-2">
                  <span>⏱️</span> Chế Độ Thi Thật (Exam Mode)
                </span>
                <ul class="text-xs text-gray-600 mt-2 space-y-1">
                  <li>• <b>Đồng hồ đếm ngược</b> ghim trên màn hình. Hết giờ tự động nộp bài.</li>
                  <li>• <b>Vẫn hiển thị Pinyin</b> (đúng chuẩn đề thi giấy HSK 2 chính thức).</li>
                  <li>• <b>Ẩn nghĩa tiếng Việt</b> để rèn luyện phản xạ đọc hiểu mặt chữ.</li>
                  <li>• Chấm điểm chuẩn và phân tích chi tiết sau khi bấm Nộp bài.</li>
                </ul>
              </div>
            </label>
          </div>
        </div>

        <!-- Start Button -->
        <div class="pt-4 border-t flex flex-col sm:flex-row items-center justify-between gap-4">
          <div id="scope-summary-text" class="text-sm text-gray-600">
            Thời gian: <b>50 phút</b> | Số câu: <b>60 câu</b> | Thang điểm: <b>200 điểm</b>
          </div>
          <button onclick="startExam()" class="w-full sm:w-auto px-8 py-3.5 bg-hanban-red hover:bg-hanban-darkRed text-white font-bold text-lg rounded-xl shadow-lg hover:shadow-xl transition transform active:scale-95 flex items-center justify-center gap-2">
            <span>Bắt Đầu Làm Bài</span>
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"></path>
            </svg>
          </button>
        </div>

      </div>

    </div>

    <!-- ========================================== -->
    <!-- 2. SCREEN: EXAM TAKING -->
    <!-- ========================================== -->
    <div id="screen-exam" class="hidden space-y-6">

      <!-- Exam Sub-header Card -->
      <div class="paper-sheet rounded-xl p-4 sm:p-5 flex flex-wrap items-center justify-between gap-3 sticky top-16 z-30 bg-white/95 backdrop-blur-sm shadow-sm">
        <div class="flex items-center gap-3">
          <span id="current-exam-title" class="font-bold text-gray-900 text-sm sm:text-base">
            HSK 2 - Đề H20901
          </span>
          <span id="badge-mode-indicator" class="text-xs px-2.5 py-0.5 rounded-full font-bold bg-amber-100 text-amber-800">
            Chế độ Luyện tập
          </span>
        </div>

        <!-- Navigation helper & progress -->
        <div class="flex items-center gap-3 text-xs sm:text-sm">
          <span class="text-gray-500 font-medium">Đã làm: <b id="progress-text" class="text-hanban-red font-bold">0 / 60</b></span>
          <button onclick="toggleNavDrawer()" class="px-3 py-1.5 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-lg font-semibold flex items-center gap-1.5 border border-gray-300">
            <span>📋</span> Bảng câu hỏi
          </button>
          <button onclick="submitExam(true)" class="px-4 py-1.5 bg-hanban-red hover:bg-hanban-darkRed text-white font-bold rounded-lg shadow transition">
            Nộp bài
          </button>
        </div>
      </div>

      <!-- Question Drawer / Floating Panel -->
      <div id="nav-drawer" class="hidden paper-sheet rounded-xl p-5 border border-gray-200 shadow-xl transition-all">
        <div class="flex items-center justify-between border-b pb-2 mb-3">
          <h4 class="font-bold text-gray-800 text-sm flex items-center gap-2">
            <span>📌</span> Danh sách câu hỏi (Bấm để nhảy tới câu)
          </h4>
          <button onclick="toggleNavDrawer()" class="text-gray-400 hover:text-gray-600 text-xl font-bold">&times;</button>
        </div>
        <div id="nav-grid" class="flex flex-wrap gap-2 max-h-60 overflow-y-auto p-1">
          <!-- Populated by JS -->
        </div>
      </div>

      <!-- Container for all questions -->
      <div id="questions-container" class="space-y-8">
        <!-- Rendered by JS -->
      </div>

      <!-- Bottom Submit Bar -->
      <div class="paper-sheet rounded-xl p-6 text-center space-y-3">
        <p class="text-gray-600 text-sm">Hãy kiểm tra kỹ toàn bộ câu trả lời trước khi nộp bài.</p>
        <button onclick="submitExam(true)" class="px-10 py-3.5 bg-hanban-red hover:bg-hanban-darkRed text-white font-bold text-lg rounded-xl shadow-lg transition transform active:scale-95">
          Hoàn Thành & Nộp Bài Thi
        </button>
      </div>

    </div>

    <!-- ========================================== -->
    <!-- 3. SCREEN: RESULT & REVIEW -->
    <!-- ========================================== -->
    <div id="screen-result" class="hidden space-y-6">

      <!-- Score Summary Banner -->
      <div class="paper-sheet rounded-xl p-6 sm:p-8 text-center space-y-4 border-t-4 border-t-hanban-red">
        <div id="result-status-badge" class="inline-flex items-center gap-2 px-3 py-1 rounded-full text-sm font-bold bg-green-100 text-green-800">
          🎉 CHÚC MỪNG BẠN ĐÃ ĐẠT ĐIỂM ĐỖ!
        </div>
        
        <h2 class="text-3xl sm:text-4xl font-extrabold text-gray-900">
          Kết Quả Bài Thi HSK 2
        </h2>
        
        <div class="flex items-center justify-center gap-2">
          <span class="text-6xl sm:text-7xl font-extrabold text-hanban-red font-mono" id="score-total">180</span>
          <span class="text-2xl text-gray-400 font-bold self-end mb-2" id="score-max">/ 200</span>
        </div>

        <!-- Section Breakdown -->
        <div class="grid grid-cols-2 max-w-md mx-auto gap-4 pt-2">
          <div class="bg-gray-50 border border-gray-200 rounded-xl p-3 text-center">
            <span class="text-xs text-gray-500 font-semibold block uppercase">Phần Nghe Hiểu</span>
            <span class="text-xl font-bold text-blue-700" id="score-listen">90 / 100</span>
          </div>
          <div class="bg-gray-50 border border-gray-200 rounded-xl p-3 text-center">
            <span class="text-xs text-gray-500 font-semibold block uppercase">Phần Đọc Hiểu</span>
            <span class="text-xl font-bold text-amber-700" id="score-read">90 / 100</span>
          </div>
        </div>

        <div class="text-sm text-gray-600 space-x-4 pt-2">
          <span>Đúng: <b id="stat-correct" class="text-green-600 font-bold">45</b> câu</span>
          <span>Sai: <b id="stat-incorrect" class="text-red-600 font-bold">10</b> câu</span>
          <span>Chưa làm: <b id="stat-unanswered" class="text-gray-500 font-bold">5</b> câu</span>
          <span>Thời gian: <b id="stat-time" class="font-bold">32:15</b></span>
        </div>

        <div class="pt-4 flex flex-wrap justify-center gap-3">
          <button onclick="goToHome()" class="px-6 py-2.5 bg-gray-200 hover:bg-gray-300 text-gray-800 font-bold rounded-xl transition">
            🔄 Làm Bài Thi Khác
          </button>
          <button onclick="retakeCurrentExam()" class="px-6 py-2.5 bg-hanban-red hover:bg-hanban-darkRed text-white font-bold rounded-xl shadow transition">
            🔁 Làm Lại Đề Này
          </button>
        </div>
      </div>

      <!-- Detailed Review Section -->
      <div class="paper-sheet rounded-xl p-6 sm:p-8 space-y-6 review-mode">
        <div class="flex items-center justify-between border-b pb-3">
          <h3 class="text-lg font-bold text-gray-900 flex items-center gap-2">
            <span>📝</span> Xem Lại Chi Tiết Toàn Bộ Đề & Lời Giải
          </h3>
          <span class="text-xs text-gray-500 italic">Di chuột vào chữ Hán để xem nghĩa tiếng Việt</span>
        </div>

        <div id="review-container" class="space-y-8">
          <!-- Rendered by JS -->
        </div>
      </div>

    </div>

  </main>

  <!-- Image Lightbox Modal for Full-size Paper Illustrations -->
  <div id="image-modal" class="fixed inset-0 z-50 bg-black/80 hidden items-center justify-center p-4 backdrop-blur-sm cursor-zoom-out" onclick="closeImageModal()">
    <div class="relative max-w-3xl max-h-[90vh] bg-white rounded-2xl p-2 shadow-2xl overflow-hidden" onclick="event.stopPropagation()">
      <button class="absolute top-3 right-3 bg-black/60 hover:bg-black/90 text-white w-8 h-8 rounded-full flex items-center justify-center font-bold text-lg z-10 transition" onclick="closeImageModal()">
        &times;
      </button>
      <img id="modal-img-src" src="" alt="Hình ảnh đề thi phóng to" class="max-h-[85vh] w-auto mx-auto object-contain rounded-xl">
      <div id="modal-img-caption" class="text-center text-xs text-gray-600 py-2 font-medium"></div>
    </div>
  </div>

  <!-- Audio Playing Indicator (Floating mini player) -->
  <div id="floating-audio-player" class="fixed bottom-4 right-4 z-40 bg-gray-900/95 text-white px-4 py-2.5 rounded-full shadow-2xl border border-gray-700 hidden items-center gap-3 backdrop-blur-md">
    <div class="flex items-center gap-1 h-4">
      <span class="w-1 bg-yellow-400 rounded-full wave-bar"></span>
      <span class="w-1 bg-yellow-400 rounded-full wave-bar"></span>
      <span class="w-1 bg-yellow-400 rounded-full wave-bar"></span>
    </div>
    <span class="text-xs font-semibold tracking-wide" id="audio-player-status">Đang phát audio câu...</span>
    <button onclick="stopAudio()" class="text-gray-400 hover:text-white text-base font-bold ml-1">&times;</button>
  </div>

  <!-- ============================================================== -->
  <!-- JAVASCRIPT LOGIC & HSK 2 DATABASE -->
  <!-- ============================================================== -->
  <script>
    // Embedded Complete 6-Exam Database
    ''' + db_content + r'''

    // Application State
    const STATE = {
      scope: 'full',      // 'full' (60), 'reading' (25), 'listening' (35)
      source: 'random',   // 'random' or 'h20901', 'h20902', etc.
      mode: 'study',      // 'study' or 'exam'
      questions: [],
      userAnswers: {},
      examDurationSeconds: 50 * 60,
      secondsRemaining: 50 * 60,
      timerInterval: null,
      examStartTime: null,
      examEndTime: null
    };

    // Speech Synthesis for Audio
    let currentUtterance = null;
    let synth = window.speechSynthesis;

    function playAudio(text, repeatCount = 2, rate = 0.9) {
      if (!synth) {
        alert("Trình duyệt của bạn không hỗ trợ Web Speech Synthesis.");
        return;
      }
      stopAudio();

      const floatingPlayer = document.getElementById('floating-audio-player');
      const statusText = document.getElementById('audio-player-status');
      if (floatingPlayer) {
        floatingPlayer.classList.remove('hidden');
        floatingPlayer.classList.add('flex');
        statusText.innerText = `Đang đọc: "${text.substring(0, 18)}..."`;
      }

      let playCount = 0;
      function speakOnce() {
        if (playCount >= repeatCount) {
          stopAudio();
          return;
        }
        playCount++;
        currentUtterance = new SpeechSynthesisUtterance(text);
        currentUtterance.lang = 'zh-CN';
        currentUtterance.rate = rate;
        currentUtterance.onend = () => {
          if (playCount < repeatCount) {
            setTimeout(speakOnce, 1200); // 1.2s pause between repeats just like real HSK
          } else {
            stopAudio();
          }
        };
        currentUtterance.onerror = () => {
          stopAudio();
        };
        synth.speak(currentUtterance);
      }
      speakOnce();
    }

    function stopAudio() {
      if (synth) {
        synth.cancel();
      }
      currentUtterance = null;
      const floatingPlayer = document.getElementById('floating-audio-player');
      if (floatingPlayer) {
        floatingPlayer.classList.add('hidden');
        floatingPlayer.classList.remove('flex');
      }
    }

    // Lightbox modal for images
    function openImageModal(src, caption = '') {
      const modal = document.getElementById('image-modal');
      const img = document.getElementById('modal-img-src');
      const cap = document.getElementById('modal-img-caption');
      img.src = src;
      cap.innerText = caption;
      modal.classList.remove('hidden');
      modal.classList.add('flex');
    }

    function closeImageModal() {
      const modal = document.getElementById('image-modal');
      modal.classList.add('hidden');
      modal.classList.remove('flex');
    }

    // Navigation and screen switching
    function showScreen(screenId) {
      ['screen-home', 'screen-exam', 'screen-result'].forEach(id => {
        document.getElementById(id).classList.add('hidden');
      });
      document.getElementById(screenId).classList.remove('hidden');
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    function goToHome() {
      if (STATE.timerInterval) clearInterval(STATE.timerInterval);
      stopAudio();
      document.getElementById('header-timer').classList.add('hidden');
      document.getElementById('btn-header-submit').classList.add('hidden');
      document.getElementById('btn-show-grid').classList.add('hidden');
      document.body.classList.remove('exam-mode', 'study-mode');
      showScreen('screen-home');
    }

    function updateScopeInfo() {
      const scope = document.querySelector('input[name="exam-scope"]:checked').value;
      const summary = document.getElementById('scope-summary-text');
      if (scope === 'full') {
        summary.innerHTML = 'Thời gian: <b>50 phút</b> | Số câu: <b>60 câu</b> (Nghe 1-35, Đọc 36-60) | Thang điểm: <b>200 điểm</b>';
      } else if (scope === 'reading') {
        summary.innerHTML = 'Thời gian: <b>22 phút</b> | Số câu: <b>25 câu</b> (Câu 36 - 60) | Thang điểm: <b>100 điểm</b>';
      } else if (scope === 'listening') {
        summary.innerHTML = 'Thời gian: <b>25 phút</b> | Số câu: <b>35 câu</b> (Câu 1 - 35) | Thang điểm: <b>100 điểm</b>';
      }
    }

    // Toggle navigation drawer
    function toggleNavDrawer() {
      const drawer = document.getElementById('nav-drawer');
      drawer.classList.toggle('hidden');
    }

    // Start Exam Setup
    function startExam() {
      STATE.scope = document.querySelector('input[name="exam-scope"]:checked').value;
      STATE.source = document.querySelector('input[name="exam-source"]:checked').value;
      STATE.mode = document.querySelector('input[name="exam-mode"]:checked').value;
      STATE.userAnswers = {};

      // Prepare questions
      prepareExamQuestions();

      // Configure timer & mode
      if (STATE.scope === 'full') {
        STATE.examDurationSeconds = 50 * 60;
      } else if (STATE.scope === 'reading') {
        STATE.examDurationSeconds = 22 * 60;
      } else {
        STATE.examDurationSeconds = 25 * 60;
      }
      STATE.secondsRemaining = STATE.examDurationSeconds;

      document.body.classList.remove('exam-mode', 'study-mode');
      if (STATE.mode === 'exam') {
        document.body.classList.add('exam-mode');
        document.getElementById('header-timer').classList.remove('hidden');
        document.getElementById('header-timer').classList.add('flex');
        startTimer();
      } else {
        document.body.classList.add('study-mode');
        document.getElementById('header-timer').classList.remove('hidden');
        document.getElementById('header-timer').classList.add('flex');
        startStopwatch();
      }

      document.getElementById('btn-header-submit').classList.remove('hidden');
      document.getElementById('btn-show-grid').classList.remove('hidden');
      document.getElementById('btn-show-grid').classList.add('flex');

      // Update badge
      const badge = document.getElementById('badge-mode-indicator');
      if (STATE.mode === 'exam') {
        badge.className = 'text-xs px-2.5 py-0.5 rounded-full font-bold bg-red-100 text-red-800';
        badge.innerText = 'Chế độ Thi thật (Đếm ngược)';
      } else {
        badge.className = 'text-xs px-2.5 py-0.5 rounded-full font-bold bg-amber-100 text-amber-800';
        badge.innerText = 'Chế độ Luyện tập (Tự do)';
      }

      const titleEl = document.getElementById('current-exam-title');
      if (STATE.source === 'random') {
        titleEl.innerText = 'HSK 2 - Đề Trộn Ngẫu Nhiên';
      } else {
        titleEl.innerText = HSK2_FULL_DATABASE[STATE.source].name;
      }

      // Render Questions
      renderQuestions();
      updateProgress();
      buildNavGrid();

      STATE.examStartTime = new Date();
      showScreen('screen-exam');
    }

    function prepareExamQuestions() {
      const examKeys = Object.keys(HSK2_FULL_DATABASE);

      if (STATE.source !== 'random') {
        // Specific Exam
        const fullList = HSK2_FULL_DATABASE[STATE.source].questions;
        if (STATE.scope === 'full') {
          STATE.questions = [...fullList];
        } else if (STATE.scope === 'listening') {
          STATE.questions = fullList.filter(q => q.section === 'listening');
        } else if (STATE.scope === 'reading') {
          STATE.questions = fullList.filter(q => q.section === 'reading');
        }
      } else {
        // Random Exam: Pick questions part-by-part across exams to preserve accurate structure
        let finalQuestions = [];

        if (STATE.scope === 'full' || STATE.scope === 'listening') {
          // Listen Part 1 (1-10): pick one exam or shuffle 10 questions
          const randExamP1 = examKeys[Math.floor(Math.random() * examKeys.length)];
          const p1 = HSK2_FULL_DATABASE[randExamP1].questions.filter(q => q.section === 'listening' && q.part === 1);
          finalQuestions.push(...p1);

          // Listen Part 2 (11-20): pick one exam to keep coherent pictures A-F
          const randExamP2 = examKeys[Math.floor(Math.random() * examKeys.length)];
          const p2 = HSK2_FULL_DATABASE[randExamP2].questions.filter(q => q.section === 'listening' && q.part === 2);
          finalQuestions.push(...p2);

          // Listen Part 3 (21-30): pick one exam
          const randExamP3 = examKeys[Math.floor(Math.random() * examKeys.length)];
          const p3 = HSK2_FULL_DATABASE[randExamP3].questions.filter(q => q.section === 'listening' && q.part === 3);
          finalQuestions.push(...p3);

          // Listen Part 4 (31-35): pick one exam
          const randExamP4 = examKeys[Math.floor(Math.random() * examKeys.length)];
          const p4 = HSK2_FULL_DATABASE[randExamP4].questions.filter(q => q.section === 'listening' && q.part === 4);
          finalQuestions.push(...p4);
        }

        if (STATE.scope === 'full' || STATE.scope === 'reading') {
          // Reading Part 1 (36-40): pick one exam
          const randExamR1 = examKeys[Math.floor(Math.random() * examKeys.length)];
          const r1 = HSK2_FULL_DATABASE[randExamR1].questions.filter(q => q.section === 'reading' && q.part === 1);
          finalQuestions.push(...r1);

          // Reading Part 2 (41-45): pick one exam
          const randExamR2 = examKeys[Math.floor(Math.random() * examKeys.length)];
          const r2 = HSK2_FULL_DATABASE[randExamR2].questions.filter(q => q.section === 'reading' && q.part === 2);
          finalQuestions.push(...r2);

          // Reading Part 3 (46-50): pick one exam
          const randExamR3 = examKeys[Math.floor(Math.random() * examKeys.length)];
          const r3 = HSK2_FULL_DATABASE[randExamR3].questions.filter(q => q.section === 'reading' && q.part === 3);
          finalQuestions.push(...r3);

          // Reading Part 4 (51-60): pick one exam
          const randExamR4 = examKeys[Math.floor(Math.random() * examKeys.length)];
          const r4 = HSK2_FULL_DATABASE[randExamR4].questions.filter(q => q.section === 'reading' && q.part === 4);
          finalQuestions.push(...r4);
        }

        STATE.questions = finalQuestions;
      }
    }

    // Timer Logic
    function startTimer() {
      if (STATE.timerInterval) clearInterval(STATE.timerInterval);
      const display = document.getElementById('timer-display');
      displayTimer(STATE.secondsRemaining);

      STATE.timerInterval = setInterval(() => {
        STATE.secondsRemaining--;
        displayTimer(STATE.secondsRemaining);

        if (STATE.secondsRemaining <= 0) {
          clearInterval(STATE.timerInterval);
          alert("⏱️ ĐÃ HẾT GIỜ LÀM BÀI! Hệ thống sẽ tự động thu bài và chấm điểm.");
          submitExam(false);
        }
      }, 1000);
    }

    function startStopwatch() {
      if (STATE.timerInterval) clearInterval(STATE.timerInterval);
      let elapsed = 0;
      const display = document.getElementById('timer-display');
      display.innerText = "00:00";

      STATE.timerInterval = setInterval(() => {
        elapsed++;
        const mins = String(Math.floor(elapsed / 60)).padStart(2, '0');
        const secs = String(elapsed % 60).padStart(2, '0');
        display.innerText = `${mins}:${secs}`;
      }, 1000);
    }

    function displayTimer(totalSecs) {
      const display = document.getElementById('timer-display');
      const mins = String(Math.floor(totalSecs / 60)).padStart(2, '0');
      const secs = String(totalSecs % 60).padStart(2, '0');
      display.innerText = `${mins}:${secs}`;
    }

    // Render Exam Questions
    function renderQuestions() {
      const container = document.getElementById('questions-container');
      container.innerHTML = '';

      let currentSection = '';
      let currentPartTitle = '';

      STATE.questions.forEach((q, idx) => {
        // Section Header if changed
        if (q.sectionName !== currentSection) {
          currentSection = q.sectionName;
          const secHeader = document.createElement('div');
          secHeader.className = 'bg-stone-800 text-amber-300 px-5 py-3 rounded-xl font-bold text-lg sm:text-xl tracking-wider shadow';
          secHeader.innerHTML = `<h3>${q.sectionName}</h3>`;
          container.appendChild(secHeader);
        }

        // Part Header if changed
        if (q.partTitle !== currentPartTitle) {
          currentPartTitle = q.partTitle;
          const partHeader = document.createElement('div');
          partHeader.className = 'border-b-2 border-stone-300 pb-2 pt-2';
          partHeader.innerHTML = `
            <h4 class="font-bold text-base sm:text-lg text-gray-900">${q.partTitle}</h4>
            <p class="text-xs text-gray-500 italic mt-0.5">${getPartInstruction(q)}</p>
          `;
          container.appendChild(partHeader);

          // If Part 1 or Part 2 has shared Image Options or Word Options, render the reference panel
          const refPanel = getPartReferencePanel(q);
          if (refPanel) {
            container.appendChild(refPanel);
          }
        }

        // Question Card
        const qCard = createQuestionElement(q, idx);
        container.appendChild(qCard);
      });
    }

    function getPartInstruction(q) {
      if (q.section === 'listening') {
        if (q.part === 1) return 'Ví dụ: 我们家有三个人。(√) / 我每天坐公共汽车去上班。(×). Nghe câu và chọn Đúng (√) hoặc Sai (×).';
        if (q.part === 2) return 'Ví dụ: 你喜欢什么运动？- 我最喜欢踢足球。(D). Nghe đối thoại và chọn bức tranh tương ứng từ A đến F.';
        if (q.part === 3) return 'Ví dụ: 小王，这里有几个杯子，哪个是你的？- 左边那个红色的是我的。(A 红色). Nghe đối thoại ngắn và chọn A, B, C.';
        if (q.part === 4) return 'Ví dụ: 请在这儿写您的名字。(A 名字). Nghe đối thoại dài và chọn đáp án đúng A, B, C.';
      } else {
        if (q.part === 1) return 'Ví dụ: 每个星期六，我都去打篮球。(D). Chọn bức tranh tương ứng từ A đến F.';
        if (q.part === 2) return 'Ví dụ: 这儿的羊肉很好吃，但是也很（ E 贵 ）。 Chọn từ thích hợp điền vào chỗ trống.';
        if (q.part === 3) return 'Ví dụ: 现在是11点30分，他们已经游了20分钟了。★ 他们11点10分开始游泳。(√). Đọc đoạn văn và chọn Đúng (√) hoặc Sai (×).';
        if (q.part === 4) return 'Ví dụ: 他还在教室里学习。(E). Ghép đôi câu hỏi và câu đáp thích hợp.';
      }
      return '';
    }

    function getPartReferencePanel(q) {
      // 1. Reading Part 1 (36-40): 6 Images A - F
      if (q.section === 'reading' && q.part === 1 && q.imageOptions) {
        const div = document.createElement('div');
        div.className = 'paper-sheet rounded-xl p-4 bg-stone-50 border border-stone-200';
        let imgsHtml = '<div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-6 gap-3">';
        ['A', 'B', 'C', 'D', 'E', 'F'].forEach(letter => {
          const imgSrc = q.imageOptions[letter] || '';
          imgsHtml += `
            <div class="border rounded-lg bg-white p-2 text-center shadow-sm cursor-pointer hover:border-amber-600 transition" onclick="openImageModal('${imgSrc}', 'Hình ảnh ${letter}')">
              <span class="inline-block w-6 h-6 rounded-full bg-stone-800 text-white font-bold text-xs leading-6 mb-1">${letter}</span>
              <img src="${imgSrc}" alt="${letter}" class="h-24 w-full object-contain mx-auto rounded" onerror="this.src='https://placehold.co/150x100?text=${letter}'">
            </div>
          `;
        });
        imgsHtml += '</div>';
        div.innerHTML = imgsHtml;
        return div;
      }

      // 2. Reading Part 2 (41-45): Options A - F
      if (q.section === 'reading' && q.part === 2 && q.options) {
        const div = document.createElement('div');
        div.className = 'paper-sheet rounded-xl p-4 bg-stone-50 border border-stone-200';
        let optsHtml = '<div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-6 gap-2 text-center">';
        ['A', 'B', 'C', 'D', 'E', 'F'].forEach(letter => {
          const opt = q.options[letter] || { text: '', ruby: '' };
          optsHtml += `
            <div class="border rounded-lg bg-white p-2 shadow-sm">
              <span class="font-bold text-hanban-red mr-1">${letter}.</span>
              <span class="text-base">${opt.ruby || opt.text}</span>
            </div>
          `;
        });
        optsHtml += '</div>';
        div.innerHTML = optsHtml;
        return div;
      }

      // 3. Listening Part 2 (11-20): Images A - F
      if (q.section === 'listening' && q.part === 2 && q.imageOptions) {
        const div = document.createElement('div');
        div.className = 'paper-sheet rounded-xl p-4 bg-stone-50 border border-stone-200';
        let imgsHtml = `<div class="text-xs font-bold text-stone-600 mb-2">Tranh lựa chọn (${q.group}):</div><div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-6 gap-3">`;
        Object.keys(q.imageOptions).forEach(letter => {
          const imgSrc = q.imageOptions[letter];
          imgsHtml += `
            <div class="border rounded-lg bg-white p-2 text-center shadow-sm cursor-pointer hover:border-amber-600 transition" onclick="openImageModal('${imgSrc}', 'Hình ảnh ${letter}')">
              <span class="inline-block w-6 h-6 rounded-full bg-stone-800 text-white font-bold text-xs leading-6 mb-1">${letter}</span>
              <img src="${imgSrc}" alt="${letter}" class="h-24 w-full object-contain mx-auto rounded" onerror="this.src='https://placehold.co/150x100?text=${letter}'">
            </div>
          `;
        });
        imgsHtml += '</div>';
        div.innerHTML = imgsHtml;
        return div;
      }

      // 4. Reading Part 4: Dialogue options A - F
      if (q.section === 'reading' && q.part === 4 && q.options) {
        const div = document.createElement('div');
        div.className = 'paper-sheet rounded-xl p-4 bg-stone-50 border border-stone-200';
        let optsHtml = `<div class="text-xs font-bold text-stone-600 mb-2">Các câu đối thoại lựa chọn (Nhóm ${q.group}):</div><div class="grid grid-cols-1 sm:grid-cols-2 gap-2 text-sm">`;
        Object.keys(q.options).forEach(letter => {
          const opt = q.options[letter];
          optsHtml += `
            <div class="border rounded-lg bg-white p-2 shadow-sm flex items-start gap-2">
              <span class="font-bold text-hanban-red shrink-0">${letter}.</span>
              <span class="text-base">${opt.ruby || opt.text}</span>
            </div>
          `;
        });
        optsHtml += '</div>';
        div.innerHTML = optsHtml;
        return div;
      }

      return null;
    }

    function createQuestionElement(q, idx) {
      const card = document.createElement('div');
      card.id = `q-card-${q.id}`;
      card.className = 'paper-sheet rounded-xl p-5 border border-stone-200 transition-all space-y-4';

      let inner = `
        <div class="flex items-start justify-between gap-3">
          <div class="flex items-center gap-2">
            <span class="w-8 h-8 rounded-full bg-stone-800 text-amber-300 font-bold flex items-center justify-center text-sm shadow shrink-0">
              ${q.id}
            </span>
            <span class="text-xs text-gray-400 uppercase tracking-wide">Câu hỏi số ${q.id}</span>
          </div>
          <!-- Audio Button for Listening Questions -->
          ${q.section === 'listening' ? `
            <button onclick="playAudio('${q.audioText.replace(/'/g, "\\'")}', 2)" class="px-3 py-1.5 bg-amber-600 hover:bg-amber-700 text-white rounded-lg font-bold text-xs flex items-center gap-1.5 shadow transition">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.536 8.464a5 5 0 010 7.072m2.828-9.9a9 9 0 010 12.728M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z"></path></svg>
              <span>🔊 Nghe audio (2 lần)</span>
            </button>
          ` : ''}
        </div>
      `;

      // Question Content Body
      inner += '<div class="space-y-3 pt-1">';

      // 1. Listening Part 1: True / False with image
      if (q.section === 'listening' && q.part === 1) {
        inner += `
          <div class="flex flex-col sm:flex-row items-center gap-4 bg-stone-50 p-3 rounded-lg border border-stone-200">
            <img src="${q.image}" alt="Câu ${q.id}" class="h-32 w-auto object-contain rounded cursor-pointer border bg-white" onclick="openImageModal('${q.image}', 'Hình ảnh câu ${q.id}')" onerror="this.src='https://placehold.co/200x120?text=Tranh+câu+${q.id}'">
            <div class="flex-1 space-y-2 text-center sm:text-left">
              <p class="text-xs text-gray-500">Nghe đoạn thoại và chọn xem nội dung có phù hợp với hình ảnh không:</p>
              ${STATE.mode === 'study' ? `<div class="p-2 bg-white rounded border text-base">${q.ruby}</div>` : '<div class="text-xs text-gray-400 italic">(Nội dung thoại được ẩn trong chế độ thi)</div>'}
            </div>
          </div>
          <div class="flex justify-center sm:justify-start gap-4 pt-2">
            ${renderOptionButton(q.id, '√', '√ Đúng')}
            ${renderOptionButton(q.id, '×', '× Sai')}
          </div>
        `;
      }

      // 2. Listening Part 2: Image Match (A - F)
      else if (q.section === 'listening' && q.part === 2) {
        inner += `
          <div class="space-y-2">
            <p class="text-xs text-gray-500">Nghe đoạn đối thoại và chọn bức tranh tương ứng từ A đến F:</p>
            ${STATE.mode === 'study' ? `<div class="p-2 bg-stone-50 rounded border text-base">${q.ruby}</div>` : '<div class="text-xs text-gray-400 italic">(Nội dung thoại được ẩn trong chế độ thi)</div>'}
            <div class="flex flex-wrap gap-2 pt-2">
              ${['A', 'B', 'C', 'D', 'E', 'F'].filter(l => q.imageOptions[l]).map(l => renderOptionButton(q.id, l, l)).join('')}
            </div>
          </div>
        `;
      }

      // 3. Listening Part 3 & 4: Multiple Choice (A, B, C)
      else if (q.section === 'listening' && (q.part === 3 || q.part === 4)) {
        inner += `
          <div class="space-y-3">
            ${STATE.mode === 'study' ? `<div class="p-2.5 bg-stone-50 rounded border text-base">${q.ruby}</div>` : '<div class="text-xs text-gray-400 italic">(Nghe đối thoại và câu hỏi qua audio)</div>'}
            <div class="grid grid-cols-1 sm:grid-cols-3 gap-2.5 pt-1">
              ${['A', 'B', 'C'].map(letter => {
                const opt = q.options[letter] || { text: '', ruby: '' };
                return `
                  <button type="button" onclick="selectAnswer(${q.id}, '${letter}')" id="opt-btn-${q.id}-${letter}" class="option-btn text-left p-3 rounded-lg border-2 border-stone-200 hover:border-amber-500 bg-white transition flex items-center gap-2">
                    <span class="w-6 h-6 rounded-full bg-stone-100 font-bold text-xs flex items-center justify-center shrink-0 text-stone-700">${letter}</span>
                    <span class="text-base">${opt.ruby || opt.text}</span>
                  </button>
                `;
              }).join('')}
            </div>
          </div>
        `;
      }

      // 4. Reading Part 1: Sentence matching image
      else if (q.section === 'reading' && q.part === 1) {
        inner += `
          <div class="space-y-3">
            <div class="text-lg sm:text-xl font-medium p-3 bg-stone-50 rounded-lg border border-stone-200 leading-relaxed">
              ${q.ruby}
            </div>
            <div class="flex flex-wrap gap-2 pt-1">
              <span class="text-xs text-gray-500 self-center mr-2">Chọn ảnh:</span>
              ${['A', 'B', 'C', 'D', 'E', 'F'].map(l => renderOptionButton(q.id, l, l)).join('')}
            </div>
          </div>
        `;
      }

      // 5. Reading Part 2: Fill in the blank
      else if (q.section === 'reading' && q.part === 2) {
        inner += `
          <div class="space-y-3">
            <div class="text-lg sm:text-xl font-medium p-3 bg-stone-50 rounded-lg border border-stone-200 leading-relaxed">
              ${q.ruby}
            </div>
            <div class="flex flex-wrap gap-2 pt-1">
              <span class="text-xs text-gray-500 self-center mr-2">Chọn từ điền vào ( ):</span>
              ${['A', 'B', 'C', 'D', 'E', 'F'].map(l => renderOptionButton(q.id, l, l)).join('')}
            </div>
          </div>
        `;
      }

      // 6. Reading Part 3: True / False Passage
      else if (q.section === 'reading' && q.part === 3) {
        inner += `
          <div class="space-y-3 bg-stone-50 p-4 rounded-xl border border-stone-200">
            <div class="text-base sm:text-lg leading-relaxed text-gray-900 border-b border-stone-200 pb-3">
              ${q.contextRuby}
            </div>
            <div class="text-base sm:text-lg font-bold text-amber-900 flex items-start gap-2 pt-1">
              <span class="text-amber-600">★</span>
              <div>${q.statementRuby}</div>
            </div>
          </div>
          <div class="flex justify-center sm:justify-start gap-4 pt-2">
            ${renderOptionButton(q.id, '√', '√ Đúng')}
            ${renderOptionButton(q.id, '×', '× Sai')}
          </div>
        `;
      }

      // 7. Reading Part 4: Dialogue Matching
      else if (q.section === 'reading' && q.part === 4) {
        inner += `
          <div class="space-y-3">
            <div class="text-lg sm:text-xl font-medium p-3 bg-stone-50 rounded-lg border border-stone-200 leading-relaxed">
              ${q.ruby}
            </div>
            <div class="flex flex-wrap gap-2 pt-1">
              <span class="text-xs text-gray-500 self-center mr-2">Chọn câu đối thoại:</span>
              ${['A', 'B', 'C', 'D', 'E', 'F'].map(l => renderOptionButton(q.id, l, l)).join('')}
            </div>
          </div>
        `;
      }

      inner += '</div>';
      card.innerHTML = inner;
      return card;
    }

    function renderOptionButton(qId, val, label) {
      return `
        <button type="button" onclick="selectAnswer(${qId}, '${val}')" id="opt-btn-${qId}-${val}" class="option-btn px-4 py-2 rounded-lg border-2 border-stone-200 hover:border-amber-500 font-bold text-base bg-white transition flex items-center justify-center min-w-[3.5rem]">
          ${label}
        </button>
      `;
    }

    // Handle Answer Selection
    function selectAnswer(qId, value) {
      STATE.userAnswers[qId] = value;

      // Update button styling for this question
      const card = document.getElementById(`q-card-${qId}`);
      if (card) {
        const buttons = card.querySelectorAll('.option-btn');
        buttons.forEach(btn => btn.classList.remove('selected'));
        const selectedBtn = document.getElementById(`opt-btn-${qId}-${value}`);
        if (selectedBtn) {
          selectedBtn.classList.add('selected');
        }
      }

      updateProgress();
      updateNavGridItem(qId);
    }

    function updateProgress() {
      const answeredCount = Object.keys(STATE.userAnswers).length;
      const total = STATE.questions.length;
      document.getElementById('progress-text').innerText = `${answeredCount} / ${total}`;
    }

    function buildNavGrid() {
      const grid = document.getElementById('nav-grid');
      grid.innerHTML = '';
      STATE.questions.forEach(q => {
        const btn = document.createElement('button');
        btn.id = `nav-item-${q.id}`;
        btn.className = 'w-9 h-9 rounded-lg border text-xs font-bold transition flex items-center justify-center bg-gray-50 text-gray-600 border-gray-300 hover:bg-gray-100';
        btn.innerText = q.id;
        btn.onclick = () => {
          const el = document.getElementById(`q-card-${q.id}`);
          if (el) {
            el.scrollIntoView({ behavior: 'smooth', block: 'center' });
            toggleNavDrawer();
          }
        };
        grid.appendChild(btn);
      });
    }

    function updateNavGridItem(qId) {
      const btn = document.getElementById(`nav-item-${qId}`);
      if (btn) {
        btn.className = 'w-9 h-9 rounded-lg border text-xs font-bold transition flex items-center justify-center bg-amber-600 text-white border-amber-700 shadow-sm';
      }
    }

    // Submit Exam
    function submitExam(confirmSubmit = true) {
      if (confirmSubmit) {
        const answered = Object.keys(STATE.userAnswers).length;
        const total = STATE.questions.length;
        if (answered < total) {
          const proceed = confirm(`Bạn mới làm được ${answered}/${total} câu hỏi. Bạn có chắc chắn muốn nộp bài ngay bây giờ?`);
          if (!proceed) return;
        } else {
          const proceed = confirm("Bạn có chắc chắn muốn nộp bài thi để chấm điểm không?");
          if (!proceed) return;
        }
      }

      if (STATE.timerInterval) clearInterval(STATE.timerInterval);
      stopAudio();
      STATE.examEndTime = new Date();

      calculateAndShowResults();
    }

    // Results & Scoring
    function calculateAndShowResults() {
      let correctCount = 0;
      let incorrectCount = 0;
      let unansweredCount = 0;

      let listenCorrect = 0;
      let listenTotal = 0;
      let readCorrect = 0;
      let readTotal = 0;

      STATE.questions.forEach(q => {
        const userAns = STATE.userAnswers[q.id];
        const isCorrect = (userAns === q.answer);

        if (!userAns) {
          unansweredCount++;
        } else if (isCorrect) {
          correctCount++;
        } else {
          incorrectCount++;
        }

        if (q.section === 'listening') {
          listenTotal++;
          if (isCorrect) listenCorrect++;
        } else {
          readTotal++;
          if (isCorrect) readCorrect++;
        }
      });

      // Calculate Scores
      let finalScore = 0;
      let maxScore = 200;
      let listenScore = 0;
      let readScore = 0;

      if (STATE.scope === 'full') {
        maxScore = 200;
        listenScore = listenTotal > 0 ? Math.round((listenCorrect / listenTotal) * 100) : 0;
        readScore = readTotal > 0 ? Math.round((readCorrect / readTotal) * 100) : 0;
        finalScore = listenScore + readScore;
      } else if (STATE.scope === 'reading') {
        maxScore = 100;
        readScore = readTotal > 0 ? Math.round((readCorrect / readTotal) * 100) : 0;
        finalScore = readScore;
      } else {
        maxScore = 100;
        listenScore = listenTotal > 0 ? Math.round((listenCorrect / listenTotal) * 100) : 0;
        finalScore = listenScore;
      }

      // Update UI elements
      document.getElementById('score-total').innerText = finalScore;
      document.getElementById('score-max').innerText = `/ ${maxScore}`;
      document.getElementById('score-listen').innerText = `${listenScore} / 100`;
      document.getElementById('score-read').innerText = `${readScore} / 100`;

      document.getElementById('stat-correct').innerText = correctCount;
      document.getElementById('stat-incorrect').innerText = incorrectCount;
      document.getElementById('stat-unanswered').innerText = unansweredCount;

      // Elapsed time
      const elapsedMs = STATE.examEndTime - STATE.examStartTime;
      const elapsedMins = Math.floor(elapsedMs / 60000);
      const elapsedSecs = Math.floor((elapsedMs % 60000) / 1000);
      document.getElementById('stat-time').innerText = `${String(elapsedMins).padStart(2, '0')}:${String(elapsedSecs).padStart(2, '0')}`;

      // Pass/Fail Badge (Passing is 60% of total score: 120/200 or 60/100)
      const passScore = maxScore * 0.6;
      const isPassed = finalScore >= passScore;
      const statusBadge = document.getElementById('result-status-badge');
      if (isPassed) {
        statusBadge.className = 'inline-flex items-center gap-2 px-4 py-1.5 rounded-full text-sm font-bold bg-green-100 text-green-800 border border-green-300';
        statusBadge.innerText = `🎉 CHÚC MỪNG BẠN ĐÃ THI ĐỖ HSK 2! (Đạt ${finalScore}/${maxScore} điểm)`;
      } else {
        statusBadge.className = 'inline-flex items-center gap-2 px-4 py-1.5 rounded-full text-sm font-bold bg-red-100 text-red-800 border border-red-300';
        statusBadge.innerText = `CỐ GẮNG LÊN! BẠN CẦN THÊM ${Math.round(passScore - finalScore)} ĐIỂM ĐỂ ĐỖ HSK 2 (Điểm đạt: ${passScore}/${maxScore})`;
      }

      // Render Review
      renderReview();

      // Show Result screen
      document.getElementById('header-timer').classList.add('hidden');
      document.getElementById('btn-header-submit').classList.add('hidden');
      document.getElementById('btn-show-grid').classList.add('hidden');
      showScreen('screen-result');
    }

    // Render Review Cards
    function renderReview() {
      const container = document.getElementById('review-container');
      container.innerHTML = '';

      STATE.questions.forEach(q => {
        const userAns = STATE.userAnswers[q.id];
        const isCorrect = (userAns === q.answer);
        const isUnanswered = !userAns;

        const card = document.createElement('div');
        let borderClass = isCorrect ? 'border-green-300 bg-green-50/20' : (isUnanswered ? 'border-gray-300 bg-gray-50/30' : 'border-red-300 bg-red-50/20');
        card.className = `paper-sheet rounded-xl p-5 border-2 ${borderClass} space-y-4 shadow-sm`;

        let statusText = isCorrect ? '<span class="text-xs font-bold bg-green-100 text-green-800 px-2 py-0.5 rounded">✓ Chính xác</span>' :
                         (isUnanswered ? '<span class="text-xs font-bold bg-gray-100 text-gray-700 px-2 py-0.5 rounded">Chưa trả lời</span>' :
                         '<span class="text-xs font-bold bg-red-100 text-red-800 px-2 py-0.5 rounded">✗ Chưa đúng</span>');

        let inner = `
          <div class="flex items-center justify-between border-b pb-2">
            <div class="flex items-center gap-2">
              <span class="w-7 h-7 rounded-full bg-stone-800 text-amber-300 font-bold flex items-center justify-center text-xs">
                ${q.id}
              </span>
              <span class="font-bold text-sm text-gray-900">${q.partTitle}</span>
            </div>
            ${statusText}
          </div>
        `;

        // Content
        if (q.section === 'listening') {
          inner += `
            <div class="space-y-2">
              ${q.image ? `<img src="${q.image}" alt="Câu ${q.id}" class="h-28 w-auto object-contain rounded border bg-white mb-2" onclick="openImageModal('${q.image}', 'Hình ảnh câu ${q.id}')">` : ''}
              <div class="p-3 bg-white rounded border text-base leading-relaxed">
                <span class="text-xs font-bold text-amber-700 block mb-1">Lời thoại phát thanh (听力材料):</span>
                ${q.ruby}
              </div>
            </div>
          `;
        } else {
          if (q.part === 3) {
            inner += `
              <div class="p-3 bg-white rounded border space-y-2 text-base">
                <div>${q.contextRuby}</div>
                <div class="font-bold text-amber-800 flex items-start gap-1">★ ${q.statementRuby}</div>
              </div>
            `;
          } else {
            inner += `
              <div class="p-3 bg-white rounded border text-base">
                ${q.ruby}
              </div>
            `;
          }
        }

        // Answer comparison
        inner += `
          <div class="flex flex-wrap items-center gap-4 text-sm pt-1">
            <span>Đáp án của bạn: <b class="${isCorrect ? 'text-green-700' : 'text-red-700'}">${userAns || 'Chưa chọn'}</b></span>
            <span>Đáp án đúng: <b class="text-green-700 bg-green-100 px-2 py-0.5 rounded">${q.answer}</b></span>
          </div>
        `;

        card.innerHTML = inner;
        container.appendChild(card);
      });
    }

    function retakeCurrentExam() {
      STATE.userAnswers = {};
      STATE.secondsRemaining = STATE.examDurationSeconds;
      startExam();
    }

    // Initialize home page
    updateScopeInfo();
  </script>
</body>
</html>
'''

print("Writing index.html...")
with open("index.html", "w", encoding="utf-8") as f:
    f.write(HTML_TEMPLATE)

print("Generated index.html successfully! Size:", os.path.getsize("index.html"), "bytes")

