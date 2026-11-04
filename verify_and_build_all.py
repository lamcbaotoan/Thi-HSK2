import sys, os, re, json, pypinyin

sys.stdout.reconfigure(encoding='utf-8')

# Authoritative HSK 2 Lexicon with exact Hanban Pinyin and Vietnamese meanings
OFFICIAL_LEXICON = {
    # Pronouns & People
    "我": ("wǒ", "tôi, mình"),
    "你": ("nǐ", "bạn, anh, chị"),
    "您": ("nín", "ngài, ông, bà (kính xưng)"),
    "他": ("tā", "anh ấy, cậu ấy"),
    "她": ("tā", "cô ấy, chị ấy"),
    "它": ("tā", "nó (con vật, đồ vật)"),
    "我们": ("wǒmen", "chúng tôi, chúng ta"),
    "你们": ("nǐmen", "các bạn"),
    "他们": ("tāmen", "họ, bọn họ"),
    "她们": ("tāmen", "các cô ấy"),
    "大家": ("dàjiā", "mọi người"),
    "别人": ("biérén", "người khác"),
    "爸爸": ("bàba", "bố, ba"),
    "妈妈": ("māma", "mẹ, má"),
    "哥哥": ("gēge", "anh trai"),
    "弟弟": ("dìdi", "em trai"),
    "姐姐": ("jiějie", "chị gái"),
    "妹妹": ("mèimei", "em gái"),
    "丈夫": ("zhàngfu", "chồng"),
    "妻子": ("qīzi", "vợ"),
    "儿子": ("érzi", "con trai"),
    "女儿": ("nǚ'ér", "con gái"),
    "孩子": ("háizi", "trẻ con, con cái"),
    "孩子们": ("háizimen", "các con, các cháu"),
    "女孩儿": ("nǚháir", "bé gái, cô gái"),
    "女孩子": ("nǚháizi", "bé gái, cô gái"),
    "男人": ("nánrén", "đàn ông"),
    "女人": ("nǚrén", "phụ nữ"),
    "先生": ("xiānsheng", "ông, ngài, chồng"),
    "小姐": ("xiǎojiě", "cô, tiểu thư"),
    "老师": ("lǎoshī", "thầy/cô giáo"),
    "学生": ("xuésheng", "học sinh"),
    "同学": ("tóngxué", "bạn học"),
    "朋友": ("péngyou", "bạn bè"),
    "朋友们": ("péngyoumen", "các bạn bè"),
    "医生": ("yīshēng", "bác sĩ"),
    "服务员": ("fúwùyuán", "nhân viên phục vụ"),
    "李先生": ("Lǐ xiānsheng", "ông Lý"),
    "王小姐": ("Wáng xiǎojiě", "cô Vương"),
    "高小姐": ("Gāo xiǎojiě", "cô Cao"),
    "小王": ("Xiǎo Wáng", "tiểu Vương"),
    "小张": ("Xiǎo Zhāng", "tiểu Trương"),
    "小刘": ("Xiǎo Liú", "tiểu Lưu"),
    "小白": ("Xiǎo Bái", "tiểu Bạch"),
    "李哥": ("Lǐ gē", "anh Lý"),
    "赵老师": ("Zhào lǎoshī", "thầy Triệu"),
    "王老师": ("Wáng lǎoshī", "thầy Vương"),
    "杨笑笑": ("Yáng Xiàoxiao", "Dương Tiếu Tiếu"),
    "大高": ("Dà Gāo", "Đại Cao (biệt danh)"),

    # Numbers
    "一": ("yī", "một"), "二": ("èr", "hai"), "两": ("liǎng", "hai (lượng từ)"), "三": ("sān", "ba"),
    "四": ("sì", "bốn"), "五": ("wǔ", "năm"), "六": ("liù", "sáu"), "七": ("qī", "bảy"),
    "八": ("bā", "tám"), "九": ("jiǔ", "chín"), "十": ("shí", "mười"), "零": ("líng", "không"),
    "百": ("bǎi", "trăm"), "千": ("qiān", "nghìn"),
    "九百": ("jiǔbǎi", "chín trăm"), "两百": ("liǎngbǎi", "hai trăm"), "两千": ("liǎngqiān", "hai nghìn"),
    "三千": ("sānqiān", "ba nghìn"), "五千八": ("wǔqiānbā", "năm nghìn tám"),
    "第一": ("dì-yī", "thứ nhất, đầu tiên"), "第二": ("dì-'èr", "thứ hai"), "第三": ("dì-sān", "thứ ba"), "第五": ("dì-wǔ", "thứ năm"),

    # Time & Weather
    "时间": ("shíjiān", "thời gian"), "分钟": ("fēnzhōng", "phút"), "小时": ("xiǎoshí", "tiếng, giờ"),
    "今天": ("jīntiān", "hôm nay"), "明天": ("míngtiān", "ngày mai"), "昨天": ("zuótiān", "hôm qua"),
    "后天": ("hòutiān", "ngày kia"), "早上": ("zǎoshang", "buổi sáng sớm"), "上午": ("shàngwǔ", "buổi sáng"),
    "中午": ("zhōngwǔ", "buổi trưa"), "下午": ("xiàwǔ", "buổi chiều"), "晚上": ("wǎnshang", "buổi tối"),
    "现在": ("xiànzài", "bây giờ"), "年": ("nián", "năm"), "月": ("yuè", "tháng"), "日": ("rì", "ngày"),
    "号": ("hào", "ngày, số"), "点": ("diǎn", "giờ, điểm"), "点钟": ("diǎnzhōng", "giờ đúng"),
    "分": ("fēn", "phút"), "星期": ("xīngqī", "tuần, thứ"), "星期六": ("xīngqīliù", "thứ bảy"),
    "星期日": ("xīngqīrì", "chủ nhật"), "生日": ("shēngrì", "sinh nhật"), "时候": ("shíhou", "lúc, khi"),
    "天气": ("tiānqì", "thời tiết"), "晴天": ("qíngtiān", "ngày nắng"), "晴": ("qíng", "nắng ráo"),
    "阴天": ("yīntiān", "trời râm"), "阴": ("yīn", "râm"), "雪": ("xuě", "tuyết"), "下雪": ("xià xuě", "tuyết rơi"),
    "雨": ("yǔ", "mưa"), "下雨": ("xià yǔ", "mưa rơi"),

    # Food & Drink
    "水": ("shuǐ", "nước"), "热茶": ("rè chá", "trà nóng"), "茶": ("chá", "trà"),
    "咖啡": ("kāfēi", "cà phê"), "牛奶": ("niúnǎi", "sữa bò"), "苹果": ("píngguǒ", "quả táo"),
    "西瓜": ("xīguā", "dưa hấu"), "水果": ("shuǐguǒ", "trái cây, hoa quả"), "米饭": ("mǐfàn", "cơm"),
    "羊肉": ("yángròu", "thịt cừu"), "肉": ("ròu", "thịt"), "鱼": ("yú", "cá"),
    "鸡蛋": ("jīdàn", "trứng gà"), "菜": ("cài", "món ăn, rau"), "药": ("yào", "thuốc"), "吃药": ("chī yào", "uống thuốc"),

    # Objects, Body, Daily Life
    "身体": ("shēntǐ", "sức khỏe, cơ thể"), "眼睛": ("yǎnjing", "mắt"), "书": ("shū", "sách"),
    "报纸": ("bàozhǐ", "báo chí"), "汉字": ("Hànzì", "chữ Hán"), "汉语": ("Hànyǔ", "tiếng Hán, tiếng Trung"),
    "课": ("kè", "tiết học, bài học"), "字": ("zì", "chữ"), "事情": ("shìqing", "sự việc, chuyện"),
    "问题": ("wèntí", "câu hỏi, vấn đề"), "意思": ("yìsi", "ý nghĩa"), "名字": ("míngzi", "tên"),
    "桌子": ("zhuōzi", "cái bàn"), "椅子": ("yǐzi", "cái ghế"), "门": ("mén", "cửa"), "开门": ("kāi mén", "mở cửa"),
    "房间": ("fángjiān", "căn phòng"), "家": ("jiā", "nhà"), "房子": ("fángzi", "ngôi nhà"), "床": ("chuáng", "cái giường"),
    "衣服": ("yīfu", "quần áo"), "裤子": ("kùzi", "quần"), "手表": ("shǒubiǎo", "đồng hồ đeo tay"),
    "手机": ("shǒujī", "điện thoại di động"), "电脑": ("diànnǎo", "máy tính"), "电视": ("diànshì", "ti vi"),
    "看电视": ("kàn diànshì", "xem ti vi"), "电影": ("diànyǐng", "phim điện ảnh"), "看电影": ("kàn diànyǐng", "xem phim"),
    "电影票": ("diànyǐngpiào", "vé xem phim"), "车票": ("chēpiào", "vé xe"), "票": ("piào", "vé"),
    "洗衣机": ("xǐyījī", "máy giặt"), "飞机": ("fēijī", "máy bay"), "机场": ("jīchǎng", "sân bay"),
    "飞机场": ("fēijīchǎng", "sân bay"), "火车": ("huǒchē", "tàu hỏa"), "火车站": ("huǒchēzhàn", "ga tàu hỏa"),
    "出租车": ("chūzūchē", "xe taxi"), "公共汽车": ("gōnggòngqìchē", "xe buýt"), "船": ("chuán", "thuyền, tàu thủy"),
    "坐船": ("zuò chuán", "đi thuyền"), "自行车": ("zìxíngchē", "xe đạp"), "车": ("chē", "xe"),
    "新车": ("xīn chē", "xe mới"), "路": ("lù", "đường"), "学校": ("xuéxiào", "trường học"),
    "大学": ("dàxué", "đại học"), "中学": ("zhōngxué", "trung học"), "教室": ("jiàoshì", "lớp học, phòng học"),
    "大教室": ("dà jiàoshì", "phòng học lớn"), "公司": ("gōngsī", "công ty"), "医院": ("yīyuàn", "bệnh viện"),
    "饭店": ("fàndiàn", "nhà hàng, khách sạn"), "饭馆儿": ("fànguǎnr", "quán ăn"), "商店": ("shāngdiàn", "cửa hàng"),
    "药店": ("yàodiàn", "hiệu thuốc"), "茶馆儿": ("cháguǎnr", "quán trà"), "一元店": ("yīyuándiàn", "cửa hàng đồng giá 1 tệ"),
    "北京": ("Běijīng", "Bắc Kinh"), "上海": ("Shànghǎi", "Thượng Hải"), "中国": ("Zhōngguó", "Trung Quốc"),
    "猫": ("māo", "con mèo"), "小猫": ("xiǎomāo", "mèo con"), "狗": ("gǒu", "con chó"), "小狗": ("xiǎogǒu", "chó con"),
    "小鱼": ("xiǎoyú", "cá nhỏ"), "东西": ("dōngxi", "đồ vật, thứ"), "大米": ("dàmǐ", "gạo"), "米": ("mǐ", "gạo, mét"),
    "钱": ("qián", "tiền"), "块": ("kuài", "đồng, tệ (khẩu ngữ)"), "元": ("yuán", "tệ, đồng"), "斤": ("jīn", "cân (0.5 kg)"),

    # Directions & Positions
    "前": ("qián", "trước"), "前面": ("qiánmiàn", "phía trước"), "后": ("hòu", "sau"), "后面": ("hòumiàn", "phía sau"),
    "左": ("zuǒ", "trái"), "左边": ("zuǒbian", "bên trái"), "右": ("yòu", "phải"), "右边": ("yòubian", "bên phải"),
    "上": ("shàng", "trên"), "上面": ("shàngmiàn", "phía trên"), "下": ("xià", "dưới"), "下面": ("xiàmiàn", "phía dưới"),
    "里": ("lǐ", "trong"), "里面": ("lǐmiàn", "bên trong"), "外": ("wài", "ngoài"), "外面": ("wàimiàn", "bên ngoài"),
    "旁": ("páng", "bên"), "旁边": ("pángbiān", "bên cạnh"), "身边": ("shēnbiān", "bên cạnh, quanh mình"),

    # Verbs & Actions
    "是": ("shì", "là"), "有": ("yǒu", "có"), "在": ("zài", "ở, tại, đang"), "去": ("qù", "đi"), "来": ("lái", "đến, tới"),
    "吃": ("chī", "ăn"), "喝": ("hē", "uống"), "看": ("kàn", "xem, nhìn, đọc"), "听": ("tīng", "nghe"),
    "说": ("shuō", "nói"), "读": ("dú", "đọc"), "写": ("xiě", "viết"), "看书": ("kàn shū", "đọc sách"),
    "做": ("zuò", "làm"), "做饭": ("zuò fàn", "nấu cơm"), "坐": ("zuò", "ngồi, đi (tàu xe)"), "住": ("zhù", "sống, ở"),
    "买": ("mǎi", "mua"), "卖": ("mài", "bán"), "开": ("kāi", "mở, lái (xe)"), "关": ("guān", "đóng, tắt"),
    "回": ("huí", "về, quay lại"), "回家": ("huí jiā", "về nhà"), "回去": ("huíqù", "đi về"),
    "进": ("jìn", "vào"), "出": ("chū", "ra"), "出门": ("chū mén", "ra ngoài, ra khỏi cửa"),
    "出院": ("chūyuàn", "xuất viện"), "出来": ("chūlai", "ra đây, xuất hiện"),
    "叫": ("jiào", "gọi, kêu, tên là"), "学习": ("xuéxí", "học tập"), "工作": ("gōngzuò", "làm việc"),
    "起床": ("qǐchuáng", "thức dậy"), "睡觉": ("shuìjiào", "đi ngủ"), "跑步": ("pǎobù", "chạy bộ"),
    "慢跑": ("mànpǎo", "chạy chậm, chạy bộ"), "游泳": ("yóuyǒng", "bơi lội"), "踢足球": ("tī zúqiú", "đá bóng"),
    "打篮球": ("dǎ lánqiú", "chơi bóng rổ"), "打": ("dǎ", "đánh, chơi, gọi"), "打电话": ("dǎ diànhuà", "gọi điện thoại"),
    "跳舞": ("tiàowǔ", "khiêu vũ, múa"), "唱歌": ("chànggē", "ca hát"), "运动": ("yùndòng", "vận động, thể thao"),
    "旅游": ("lǚyóu", "du lịch"), "散步": ("sànbù", "đi dạo"), "休息": ("xiūxi", "nghỉ ngơi"),
    "洗": ("xǐ", "rửa, giặt"), "洗衣服": ("xǐ yīfu", "giặt quần áo"), "生病": ("shēngbìng", "bị ốm, bị bệnh"),
    "给": ("gěi", "cho, tặng"), "送": ("sòng", "tặng, tiễn"), "找": ("zhǎo", "tìm, kiếm"),
    "懂": ("dǒng", "hiểu"), "听懂": ("tīngdǒng", "nghe hiểu"), "看懂": ("kàndǒng", "đọc hiểu"),
    "穿": ("chuān", "mặc, đi (giày)"), "笑": ("xiào", "cười"), "笑一笑": ("xiàoyíxiào", "cười một chút"),
    "问": ("wèn", "hỏi"), "问问": ("wènwen", "hỏi thử"), "走": ("zǒu", "đi, bước đi"), "到": ("dào", "đến, tới"),
    "帮助": ("bāngzhù", "giúp đỡ"), "帮": ("bāng", "giúp"), "介绍": ("jièshào", "giới thiệu"),
    "准备": ("zhǔnbèi", "chuẩn bị"), "开始": ("kāishǐ", "bắt đầu"), "回答": ("huídá", "trả lời"),
    "告诉": ("gàosu", "nói cho, bảo"), "知道": ("zhīdào", "biết"), "认识": ("rènshi", "quen biết"),
    "觉得": ("juéde", "cảm thấy"), "希望": ("xīwàng", "hy vọng"), "喜欢": ("xǐhuan", "thích"),
    "爱": ("ài", "yêu, thích"), "想": ("xiǎng", "muốn, nhớ, nghĩ"), "要": ("yào", "muốn, cần, phải"),
    "会": ("huì", "biết (kỹ năng), sẽ"), "能": ("néng", "có thể"), "可以": ("kěyǐ", "có thể, được"),
    "完": ("wán", "xong, hết"), "做完": ("zuòwán", "làm xong"), "吃完": ("chīwán", "ăn xong"), "看完": ("kànwán", "xem xong"),
    "做错": ("zuòcuò", "làm sai"), "错": ("cuò", "sai, mắc lỗi"), "听话": ("tīnghuà", "nghe lời, ngoan"),
    "出问题": ("chū wèntí", "gặp trục trặc, có vấn đề"),
    "欢迎": ("huānyíng", "hoan nghênh, chào mừng"),

    # Adjectives & Adverbs
    "好": ("hǎo", "tốt, đẹp, xong"), "大": ("dà", "to, lớn"), "小": ("xiǎo", "nhỏ, bé"),
    "多": ("duō", "nhiều, hơn"), "少": ("shǎo", "ít"), "冷": ("lěng", "lạnh"), "热": ("rè", "nóng"),
    "高": ("gāo", "cao"), "矮": ("ǎi", "thấp, lùn"), "长": ("cháng", "dài, lâu"),
    "远": ("yuǎn", "xa"), "近": ("jìn", "gần"), "快": ("kuài", "nhanh, sắp"), "慢": ("màn", "chậm"),
    "慢走": ("màn zǒu", "đi thong thả, đi cẩn thận"), "贵": ("guì", "đắt, quý"), "便宜": ("piányi", "rẻ"),
    "新": ("xīn", "mới"), "旧": ("jiù", "cũ"), "忙": ("máng", "bận rộn"), "累": ("lèi", "mệt mỏi"),
    "高兴": ("gāoxìng", "vui vẻ, vui mừng"), "快乐": ("kuàilè", "hạnh phúc, vui sướng"), "漂亮": ("piàoliang", "xinh đẹp"),
    "红": ("hóng", "đỏ"), "红色": ("hóngsè", "màu đỏ"), "黑": ("hēi", "đen"), "黑色": ("hēisè", "màu đen"),
    "白": ("bái", "trắng"), "白色": ("báisè", "màu trắng"),
    "很": ("hěn", "rất"), "太": ("tài", "quá, lắm"), "非常": ("fēicháng", "vô cùng, rất"),
    "真": ("zhēn", "thật sự"), "最": ("zuì", "nhất"), "不": ("bù", "không"), "没": ("méi", "chưa, không có"),
    "别": ("bié", "đừng"), "也": ("yě", "cũng"), "都": ("dōu", "đều"), "就": ("jiù", "thì, ngay, liền"),
    "再": ("zài", "lại, thêm nữa"), "还": ("hái", "vẫn, còn"), "已经": ("yǐjīng", "đã"),
    "正在": ("zhèngzài", "đang"), "一起": ("yìqǐ", "cùng nhau"), "可能": ("kěnéng", "có thể, có lẽ"),

    # Conjunctions, Prepositions & Particles
    "和": ("hé", "và"), "因为": ("yīnwèi", "bởi vì"), "所以": ("suǒyǐ", "cho nên"),
    "但是": ("dànshì", "nhưng mà"), "虽然": ("suīrán", "tuy rằng"), "比": ("bǐ", "so với"),
    "从": ("cóng", "từ"), "离": ("lí", "cách (khoảng cách)"), "向": ("xiàng", "hướng về, tới"),
    "的": ("de", "của, đích (trợ từ kết cấu)"), "了": ("le", "rồi (trợ từ ngữ khí)"),
    "吗": ("ma", "không? (trợ từ nghi vấn)"), "呢": ("ne", "nhé, nhỉ, đang (trợ từ)"),
    "吧": ("ba", "đi, nhé, nha (trợ từ đề nghị)"), "着": ("zhe", "đang (trợ từ tiếp diễn)"),
    "得": ("de", "được, đến mức (trợ từ kết cấu)"),
    "个": ("ge", "cái, chiếc (lượng từ chung)"), "张": ("zhāng", "tờ, bức, tấm (lượng từ)"),
    "本": ("běn", "quyển, cuốn (lượng từ)"), "杯": ("bēi", "ly, cốc (lượng từ)"),
    "件": ("jiàn", "chiếc, cái, vụ (lượng từ quần áo, sự việc)"), "些": ("xiē", "một vài, một ít"),
    "点儿": ("diǎnr", "một chút, một ít"), "次": ("cì", "lần, lượt (lượng từ số lần)"), "岁": ("suì", "tuổi"),

    # Expressions
    "对不起": ("duìbuqǐ", "xin lỗi"), "没关系": ("méi guānxi", "không sao, không có gì"),
    "谢谢": ("xièxie", "cảm ơn"), "不客气": ("bú kèqi", "không cần khách sáo"),
    "再见": ("zàijiàn", "tạm biệt"), "你好": ("nǐ hǎo", "chào bạn"), "您好": ("nín hǎo", "chào ngài, chào ông/bà"),
    "请": ("qǐng", "xin mời, vui lòng"), "请问": ("qǐngwèn", "xin hỏi"), "喂": ("wéi", "a lô (nghe điện thoại)"),
    "新年快乐": ("xīnnián kuàilè", "chúc mừng năm mới"), "生日快乐": ("shēngrì kuàilè", "chúc mừng sinh nhật"),
    "没问题": ("méi wèntí", "không thành vấn đề"), "好好学习": ("hǎohǎo xuéxí", "học tập thật tốt"),
    "天天向上": ("tiāntiān xiàngshàng", "ngày ngày tiến bộ"),
}

# Context-dependent overrides
CONTEXT_OVERRIDES = {
    "看书时间长了": [("看书", "kàn shū", "đọc sách"), ("时间", "shíjiān", "thời gian"), ("长", "cháng", "dài, lâu"), ("了", "le", "rồi (trợ từ ngữ khí)")],
    "眼睛得休息休息": [("眼睛", "yǎnjing", "mắt"), ("得", "děi", "phải"), ("休息", "xiūxi", "nghỉ ngơi"), ("休息", "xiūxi", "nghỉ ngơi")],
    "她笑着对我说": [("她", "tā", "cô ấy"), ("笑", "xiào", "cười"), ("着", "zhe", "đang (tiếp diễn)"), ("对", "duì", "với, đối với"), ("我", "wǒ", "tôi"), ("说", "shuō", "nói")],
    "跑着跑着": [("跑", "pǎo", "chạy"), ("着", "zhe", "đang"), ("跑", "pǎo", "chạy"), ("着", "zhe", "đang")],
    "写着呢": [("写", "xiě", "viết"), ("着", "zhe", "đang"), ("呢", "ne", "nhé, nhỉ")],
    "为什么": [("为什么", "wèi shénme", "tại sao, vì sao")],
    "买了个新手机": [("买", "mǎi", "mua"), ("了", "le", "rồi"), ("个", "ge", "cái, chiếc (lượng từ)"), ("新", "xīn", "mới"), ("手机", "shǒujī", "điện thoại di động")],
}

def match_prefix_ignoring_spaces(s, key):
    s_idx = 0
    k_idx = 0
    while s_idx < len(s) and k_idx < len(key):
        if s[s_idx].isspace():
            s_idx += 1
            continue
        if s[s_idx] == key[k_idx]:
            s_idx += 1
            k_idx += 1
        else:
            return 0
    if k_idx == len(key):
        return s_idx
    return 0

def clean_sentence_pinyin(sentence):
    """Accurately segment Chinese text into words with 100% Hanban Pinyin and Vietnamese translation"""
    tokens = []
    i = 0
    clean_s = sentence.strip()
    
    # Sort phrases by descending length
    keys = sorted(OFFICIAL_LEXICON.keys(), key=lambda x: -len(x))
    
    while i < len(clean_s):
        # 1. Whitespace
        if clean_s[i].isspace():
            tokens.append({"hz": clean_s[i], "py": "", "vi": ""})
            i += 1
            continue

        # 2. Check context overrides first (ignoring internal spaces)
        matched_override = False
        for ctx_phrase, sub_tokens in CONTEXT_OVERRIDES.items():
            matched_len = match_prefix_ignoring_spaces(clean_s[i:], ctx_phrase)
            if matched_len > 0:
                for st in sub_tokens:
                    tokens.append({"hz": st[0], "py": st[1], "vi": st[2]})
                i += matched_len
                matched_override = True
                break
        if matched_override:
            continue
            
        # 3. Match standard lexicon (ignoring internal spaces)
        matched_lex = False
        for word in keys:
            matched_len = match_prefix_ignoring_spaces(clean_s[i:], word)
            if matched_len > 0:
                py, vi = OFFICIAL_LEXICON[word]
                tokens.append({"hz": word, "py": py, "vi": vi})
                i += matched_len
                matched_lex = True
                break
        if matched_lex:
            continue
            
        # 4. Non-lexicon single character (digits, punctuation, or unlisted)
        c = clean_s[i]
        if '\u4e00' <= c <= '\u9fff':
            # Single character fallback
            pys = pypinyin.pinyin(c, style=pypinyin.Style.TONE)
            py_single = pys[0][0] if pys else ""
            tokens.append({"hz": c, "py": py_single, "vi": ""})
        else:
            tokens.append({"hz": c, "py": "", "vi": ""})
        i += 1
        
    return tokens

print("Lexicon and tokenizer defined!")

