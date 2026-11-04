import sys, pymupdf, re, json, pypinyin

sys.stdout.reconfigure(encoding='utf-8')

# Comprehensive Vietnamese dictionary for HSK 1 and HSK 2 vocabulary
VI_DICT = {
    # Pronouns & People
    "我": "tôi, mình", "你": "bạn, anh, chị", "您": "ngài, ông, bà (kính trọng)", "他": "anh ấy, cậu ấy", "她": "cô ấy, chị ấy", "它": "nó (con vật, đồ vật)",
    "我们": "chúng tôi, chúng ta", "你们": "các bạn", "他们": "họ, bọn họ", "她们": "các cô ấy", "大家": "mọi người",
    "老师": "thầy/cô giáo", "学生": "học sinh", "同学": "bạn học", "朋友": "bạn bè", "朋友们": "các bạn bè",
    "爸爸": "bố, cha", "妈妈": "mẹ", "儿子": "con trai", "女儿": "con gái", "哥哥": "anh trai", "弟弟": "em trai",
    "姐姐": "chị gái", "妹妹": "em gái", "丈夫": "chồng", "妻子": "vợ", "先生": "ông, ngài, chồng", "小姐": "cô, tiểu thư",
    "服务员": "nhân viên phục vụ", "医生": "bác sĩ", "孩子": "trẻ con, con cái", "孩子们": "các con, các cháu",
    "女孩子": "bé gái, cô gái", "女孩儿": "bé gái, cô gái", "男人": "đàn ông", "女人": "phụ nữ",
    "李先生": "ông Lý", "王小姐": "cô Vương", "小王": "tiểu Vương", "小张": "tiểu Trương", "小刘": "tiểu Lưu",
    "李哥": "anh Lý", "赵老师": "thầy Triệu", "小白": "tiểu Bạch", "高小姐": "cô Cao", "杨笑笑": "Dương Tiếu Tiếu",
    
    # Nouns
    "手机": "điện thoại di động", "电脑": "máy tính", "电视": "ti vi", "电影": "phim điện ảnh", "电影票": "vé xem phim",
    "书": "sách", "报纸": "báo chí", "汉字": "chữ Hán", "汉语": "tiếng Hán, tiếng Trung", "课": "tiết học, bài học",
    "桌子": "cái bàn", "椅子": "cái ghế", "门": "cửa", "房间": "căn phòng", "家": "nhà", "房子": "ngôi nhà",
    "衣服": "quần áo", "件": "chiếc, cái (lượng từ quần áo)", "水": "nước", "茶": "trà", "咖啡": "cà phê",
    "牛奶": "sữa bò", "苹果": "quả táo", "西瓜": "dưa hấu", "水果": "trái cây, hoa quả", "米饭": "cơm",
    "羊肉": "thịt cừu", "鱼": "cá", "鸡蛋": "trứng gà", "菜": "món ăn, rau", "药": "thuốc", "茶馆儿": "quán trà",
    "猫": "con mèo", "小猫": "mèo con", "狗": "con chó", "小狗": "chó con", "小鱼": "cá nhỏ",
    "飞机": "máy bay", "飞机场": "sân bay", "机场": "sân bay", "火车": "tàu hỏa", "火车站": "ga tàu hỏa",
    "出租车": "xe taxi", "公共汽车": "xe buýt", "船": "thuyền, tàu thủy", "自行车": "xe đạp", "车": "xe", "车票": "vé xe",
    "学校": "trường học", "大学": "đại học", "中学": "trung học", "教室": "lớp học, phòng học", "公司": "công ty",
    "医院": "bệnh viện", "饭店": "nhà hàng, khách sạn", "饭馆儿": "quán ăn", "商店": "cửa hàng", "药店": "tiệm thuốc",
    "北京": "Bắc Kinh", "上海": "Thượng Hải", "中国": "Trung Quốc",
    "路": "đường", "前面": "phía trước", "后面": "phía sau", "左边": "bên trái", "右边": "bên phải",
    "旁边": "bên cạnh", "里面": "bên trong", "外面": "bên ngoài", "上": "trên", "下": "dưới", "里": "trong",
    "今天": "hôm nay", "明天": "ngày mai", "昨天": "hôm qua", "早上": "buổi sáng sớm", "上午": "buổi sáng",
    "中午": "buổi trưa", "下午": "buổi chiều", "晚上": "buổi tối", "现在": "bây giờ", "时候": "lúc, khi",
    "年": "năm", "月": "tháng", "日": "ngày", "号": "ngày, số", "点": "giờ", "分": "phút", "分钟": "phút",
    "小时": "tiếng, giờ đồng hồ", "星期": "tuần, thứ", "星期六": "thứ bảy", "星期日": "chủ nhật", "生日": "sinh nhật",
    "天气": "thời tiết", "晴天": "ngày nắng", "阴天": "trời râm", "雪": "tuyết", "雨": "mưa",
    "身体": "sức khỏe, cơ thể", "眼睛": "mắt", "事情": "sự việc, chuyện", "东西": "đồ vật, thứ",
    "钱": "tiền", "块": "đồng, tệ (khẩu ngữ)", "元": "tệ (đồng)", "斤": "cân (0.5 kg)", "百": "trăm", "千": "nghìn",
    "问题": "câu hỏi, vấn đề", "意思": "ý nghĩa", "名字": "tên", "题": "câu hỏi, đề bài",
    
    # Verbs
    "买": "mua", "卖": "bán", "是": "là", "有": "có", "在": "ở, đang", "去": "đi", "来": "đến",
    "吃": "ăn", "喝": "uống", "看": "xem, nhìn, đọc", "听": "nghe", "说": "nói", "读": "đọc", "写": "viết",
    "做": "làm", "坐": "ngồi, đi (xe)", "住": "sống, ở", "叫": "gọi, tên là", "学习": "học tập", "学": "học",
    "工作": "làm việc", "起床": "thức dậy", "睡觉": "ngủ", "跑步": "chạy bộ", "游泳": "bơi lội", "踢足球": "đá bóng",
    "打篮球": "chơi bóng rổ", "跳舞": "khiêu vũ, múa", "唱歌": "ca hát", "运动": "vận động, thể thao",
    "旅游": "du lịch", "开": "mở, lái (xe)", "完": "xong, hoàn thành", "进": "vào", "出": "ra", "回": "về",
    "送": "tặng, tiễn", "给": "cho, tặng", "找": "tìm, tìm kiếm", "懂": "hiểu", "会": "biết (kỹ năng), sẽ",
    "能": "có thể", "可以": "có thể, được", "想": "muốn, nhớ, nghĩ", "喜欢": "thích", "爱": "yêu, thích",
    "认识": "quen biết", "知道": "biết", "觉得": "cảm thấy", "希望": "hy vọng", "帮助": "giúp đỡ",
    "回答": "trả lời", "告诉": "nói cho, bảo", "穿": "mặc", "笑": "cười", "生病": "bị ốm, bị bệnh",
    "休息": "nghỉ ngơi", "介绍": "giới thiệu", "准备": "chuẩn bị", "开始": "bắt đầu", "帮助": "giúp đỡ",
    "走": "đi, rời đi", "到": "đến, tới", "出院": "xuất viện", "洗": "rửa, giặt",
    
    # Adjectives & Adverbs
    "好": "tốt, đẹp, xong", "大": "to, lớn", "小": "nhỏ, bé", "多": "nhiều, hơn", "少": "ít",
    "冷": "lạnh", "热": "nóng", "高": "cao", "贵": "đắt, quý", "便宜": "rẻ", "长": "dài, lâu",
    "远": "xa", "近": "gần", "快": "nhanh, sắp", "慢": "chậm", "忙": "bận", "累": "mệt",
    "高兴": "vui vẻ", "快乐": "hạnh phúc, vui sướng", "漂亮": "xinh đẹp", "红": "đỏ", "红色": "màu đỏ",
    "黑": "đen", "黑色": "màu đen", "白": "trắng", "白色": "màu trắng", "新": "mới",
    "很": "rất", "太": "quá, lắm", "非常": "vô cùng, rất", "真": "thật sự", "最": "nhất",
    "不": "không", "没": "chưa, không có", "别": "đừng", "也": "cũng", "都": "đều",
    "就": "thì, ngay, liền", "再": "lại, thêm nữa", "还": "còn, vẫn", "已经": "đã", "一起": "cùng nhau",
    "可能": "có thể, có lẽ", "正在": "đang",
    
    # Particles & Measure words & Conjunctions
    "的": "của, đích (trợ từ)", "了": "rồi (trợ từ ngữ khí)", "吗": "không? (hỏi)", "呢": "nhé, nhỉ, đang",
    "吧": "đi, nhé, nha (đề nghị)", "得": "được, đến mức (trợ từ kết cấu)", "过": "qua, từng (trợ từ kinh nghiệm)",
    "着": "đang (trợ từ tiếp diễn)", "和": "và", "因为": "bởi vì", "所以": "cho nên", "但是": "nhưng",
    "虽然": "tuy rằng", "比": "so với", "向": "hướng về, tới", "从": "từ", "离": "cách (khoảng cách)",
    "个": "cái, chiếc (lượng từ chung)", "张": "tờ, bức (lượng từ)", "本": "quyển, cuốn (lượng từ)",
    "杯": "ly, cốc (lượng từ)", "些": "một vài, một ít", "点儿": "một chút, một ít", "次": "lần, chuyến",
    "岁": "tuổi", "对不起": "xin lỗi", "没关系": "không có gì, không sao", "谢谢": "cảm ơn", "不客气": "không có gì khách sáo",
    "再见": "tạm biệt", "欢迎": "hoan nghênh, chào mừng", "请": "xin mời, vui lòng", "喂": "a lô (nghe điện)",
}

# Special multi-character phrases
PHRASES = sorted(list(VI_DICT.keys()), key=lambda x: -len(x))

def tokenize_chinese(text):
    """Segment Chinese text and add pinyin and vietnamese definition"""
    tokens = []
    i = 0
    clean_text = text.strip()
    while i < len(clean_text):
        matched = False
        # Try matching longest known phrase
        for phrase in PHRASES:
            if clean_text[i:i+len(phrase)] == phrase:
                pys = pypinyin.pinyin(phrase, style=pypinyin.Style.TONE)
                # Specific tone fixes
                if phrase == "个": py_str = "ge"
                elif phrase == "了": py_str = "le"
                elif phrase == "的": py_str = "de"
                elif phrase == "吗": py_str = "ma"
                elif phrase == "呢": py_str = "ne"
                elif phrase == "吧": py_str = "ba"
                else: py_str = "'".join([p[0] for p in pys])
                
                tokens.append({
                    "hz": phrase,
                    "py": py_str,
                    "vi": VI_DICT.get(phrase, "")
                })
                i += len(phrase)
                matched = True
                break
        if not matched:
            char = clean_text[i]
            if '\u4e00' <= char <= '\u9fff':
                pys = pypinyin.pinyin(char, style=pypinyin.Style.TONE)
                py_str = pys[0][0] if pys else ""
                if char == "个": py_str = "ge"
                elif char == "了": py_str = "le"
                elif char == "的": py_str = "de"
                tokens.append({
                    "hz": char,
                    "py": py_str,
                    "vi": VI_DICT.get(char, "")
                })
            else:
                tokens.append({
                    "hz": char,
                    "py": "",
                    "vi": ""
                })
            i += 1
    return tokens

def tokens_to_ruby_html(tokens):
    html_parts = []
    for t in tokens:
        if not t["py"]:
            # Punctuation or space
            if t["hz"] == '\n':
                html_parts.append('<br/>')
            else:
                html_parts.append(f'<span class="punct">{t["hz"]}</span>')
        else:
            vi_tooltip = f'<span class="tooltip-text">{t["vi"]}</span>' if t["vi"] else ''
            html_parts.append(f'<ruby class="ruby-item" data-vi="{t["vi"]}">{t["hz"]}<rt>{t["py"]}</rt>{vi_tooltip}</ruby>')
    return "".join(html_parts)

print("Tokenizer ready!")

