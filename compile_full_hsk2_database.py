import sys, pymupdf, re, json, os, pypinyin

sys.stdout.reconfigure(encoding='utf-8')

from test_extract_and_validate import extract_answers, extract_listening_transcripts, H21006_LISTENING
from generate_full_hsk2_dataset import tokenize_chinese, tokens_to_ruby_html, VI_DICT

# Add extra vocab to VI_DICT
EXTRA_VI = {
    "九": "chín", "八": "tám", "七": "bảy", "六": "sáu", "五": "năm", "四": "bốn", "三": "ba", "两": "hai", "二": "hai", "一": "một", "零": "không",
    "十": "mười", "百": "trăm", "千": "nghìn",
    "九百": "chín trăm", "两千": "hai nghìn", "三千": "ba nghìn", "五千八": "năm nghìn tám",
    "不到": "chưa tới, không đến", "一千": "một nghìn", "一元店": "cửa hàng đồng giá 1 tệ",
    "好好学习": "học tập thật tốt", "天天向上": "ngày ngày tiến bộ", "真多": "thật nhiều",
    "听话": "nghe lời, ngoan", "洗衣机": "máy giặt", "出问题": "gặp trục trặc, có vấn đề",
    "慢跑": "chạy chậm, chạy bộ", "笑一笑": "cười một cái nào",
    "做错": "làm sai", "回答": "câu trả lời, trả lời", "长": "lâu, dài",
    "个": "cái, chiếc (lượng từ chung)", "部": "bộ, chiếc",
}
VI_DICT.update(EXTRA_VI)

# Reading Canonical Data for all 6 exams
READING_DATA = {
    "h20901": {
        "p1_options": {"A": "Cô gái khiêu vũ", "B": "Trời tuyết lạnh", "C": "Hai người bắt tay", "D": "Chơi bóng rổ", "E": "Đọc sách mỏi mắt", "F": "Cá bơi lội"},
        "p1": {
            36: "给 您 介绍 一下， 这 是 我们 公司 的 李 先生。",
            37: "看 书 时间 长 了， 眼睛 得 休息 休息。",
            38: "那 是 我 孩子， 她 爱 跳舞。",
            39: "今天 下 雪 了， 天气 很 冷。",
            40: "因为 我 不 会 游泳， 所以， 小鱼， 你 好！"
        },
        "p2_options": {"A": "完", "B": "进", "C": "过", "D": "千", "E": "贵", "F": "自行车"},
        "p2": {
            41: "这个 船 非常 大， 可以 坐 几（   ） 人。",
            42: "请（   ）， 这 就 是 我 的 房间。",
            43: "昨天 的 考试 题 太 多， 我 没有 做（   ）。",
            44: "我 没 去（   ） 中国， 我 希望 今年 能 去 中国 旅游。",
            45: "女： 对不起， 我 不 能 和 你 一起 去 买（   ） 了。\n男： 没 关系， 我 知道 你 很 忙。"
        },
        "p3": {
            46: {"ctx": "我 上午 去 外面 买了 个 新 手机， 九百 多 块 钱， 很 便宜。", "stmt": "那个 手机 不 到 一千 元。"},
            47: {"ctx": "时间 过 得 真 快， 我 来 北京 10 年 了。 我 女儿 已经 5 岁 多 了， 都 开始 学习 写 汉字 了。", "stmt": "我 有 两 个 孩子。"},
            48: {"ctx": "今天 是 7 月 12 日， 再 有 三 天 就 是 我 爸爸 的 生日 了。 我 想 送 他 一 个 电脑。", "stmt": "7 月 15 日 是 我 的 生日。"},
            49: {"ctx": "喂， 姐， 我 的 飞机 是 十 点 零 七 的， 再 有 20 分钟 我 就 到 机场 了。 我们 下午 见。", "stmt": "我 在 去 机场 的 路 上。"},
            50: {"ctx": "昨天 和 朋友们 在 外面 玩儿了 一 个 晚上， 很 累， 但是 很 高兴。", "stmt": "昨天 玩儿 得 不 高兴。"}
        },
        "p4_5155_options": {
            "A": "它 不 认识 你。",
            "B": "很 近， 走 几 分钟 就 到。",
            "C": "谢谢！",
            "D": "我 认识 他， 他 比 我 小 4 岁。",
            "E": "你 怎么 还 没 吃 完？",
            "F": "我 去 药店 买 些 药。"
        },
        "p4_5155": {
            51: "我们 要 向 您 学习！",
            52: "火车站 离 这儿 远 吗？",
            53: "已经 快 8 点 了， 你 还 出去 做 什么？",
            54: "小狗 怎么 了？ 为 什么 不 吃 东西？",
            55: "但是， 你 知道， 你 没有 他 高。"
        },
        "p4_5660_options": {
            "A": "他 是 我 弟弟 的 中学 同学。",
            "B": "谢谢 您。",
            "C": "我 知道， 我 马上 去。",
            "D": "欢迎 您 来 我们 学校！",
            "E": "快 进， 喝 杯 水。",
            "F": "没 关系， 我 听 得 懂。"
        },
        "p4_5660": {
            56: "大家 好！ 我 姓 王， 是 新 来 的 汉语 老师。",
            57: "这个 月 真 的 非常 忙。",
            58: "开 门， 快 开 门。",
            59: "她 笑着 对 我 说：“ 不 客气。”",
            60: "我 的 天！ 你们 认识？ 这 怎么 可能？"
        }
    },
    "h20902": {
        "p1_options": {"A": "Trái cây trong tủ lạnh", "B": "Chào nhau ở văn phòng", "C": "Hai vợ chồng", "D": "Chơi bóng rổ", "E": "Lớp học, nghe giảng", "F": "Mẹ chăm sóc con ốm"},
        "p1": {
            36: "同学们， 你们 听 懂 了 吗？",
            37: "里面 有 你 最 爱 吃 的 水果。",
            38: "喂， 儿子 生病 了， 你 什么 时候 能 回来？",
            39: "我 来 介绍 一下， 这 是 我 丈夫。",
            40: "现在 快 6 点 了， 我 20 分钟 后 去 公司 找 你。"
        },
        "p2_options": {"A": "房间", "B": "旁边", "C": "认识", "D": "完", "E": "贵", "F": "等"},
        "p2": {
            41: "这些 题 你 什么 时候 能 做（   ）？",
            42: "快 点儿， 大家 都 在（   ） 你 吃 饭 呢。",
            43: "别 找 了， 手机 在 桌子 上 呢， 电脑（   ）。",
            44: "我 来 北京 的 第一 天 就（   ） 他 了。",
            45: "男： （   ） 里 有 人 吗？\n女： 请 进， 先生， 您 找 谁？"
        },
        "p3": {
            46: {"ctx": "我 知道 她 的 名字， 她 姓 杨， 叫 杨 笑笑， 她 姐姐 是 我 同学。", "stmt": "我 认识 杨 笑笑 的 姐姐。"},
            47: {"ctx": "我 的 一 个 朋友 正在 找 房子， 希望 住 得 离 公司 近 一些， 这样 他 每 天 早上 就 可以 7 点 起床， 比 现在 多 睡 一 个 小时。", "stmt": "朋友 现在 每 天 7 点 起床。"},
            48: {"ctx": "我 喜欢 猫， 但是 丈夫 不 喜欢， 所以 到 现在 家 里 也 没有 猫。 我 希望 有 一 天 能 有 一 个 小猫。", "stmt": "我 丈夫 想 要 一 个 小猫。"},
            49: {"ctx": "从 我 家 到 北京， 坐 火车 就 5 个 小时， 比 坐 飞机 便宜 很 多。 所以， 明天 我 准备 坐 火车 去。", "stmt": "我 明天 去 北京。"},
            50: {"ctx": "李哥， 赵 老师 让 我 告诉 你， 你 的 电影票 买到 了。", "stmt": "李哥 正在 看 电影。"}
        },
        "p4_5155_options": {
            "A": "别 笑 了， 我 说 的 是 真 的。",
            "B": "还 可以， 不 到 100 元。",
            "C": "这儿 有 商店 吗？ 我 想 去 买 点儿 东西。",
            "D": "是 吗？ 我 的 手表 慢 了？",
            "E": "他 在 哪儿 呢？ 你 看见 他 了 吗？",
            "F": "那 我 和 你 一起 去。"
        },
        "p4_5155": {
            51: "9 点？ 现在 已经 9 点 25 了。",
            52: "我 家 的 狗 喜欢 吃 苹果。",
            53: "你 的 自行车 是 白色 的？ 真 漂亮， 贵 吗？",
            54: "鸡蛋 吃 完 了， 下午 我 再 买 一些。",
            55: "向 前 走， 就 在 那儿。"
        },
        "p4_5660_options": {
            "A": "我 从 您 这儿 学了 很 多。",
            "B": "新年 快乐！",
            "C": "我 弟弟 在 北京 大学 读 书， 今年 是 第三 年 了。",
            "D": "听说 他 病 了， 我们 找 时间 去 看看 他 吧。",
            "E": "这个 是 下午 送， 送 到 哪儿？",
            "F": "没 关系， 我 听 得 懂。"
        },
        "p4_5660": {
            56: "今天 是 1 月 1 日。",
            57: "等 一下， 我 打 电话 问 一下。",
            58: "他 会 说 汉语？",
            59: "星期六 怎么样？",
            60: "希望 我 的 回答 能 对 你 有 帮助。"
        }
    },
    "h21003": {
        "p1_options": {"A": "Chạy bộ sáng sớm", "B": "Cười chụp ảnh", "C": "Điện thoại mới", "D": "Chơi bóng rổ", "E": "Chào mừng đến công ty", "F": "Trời tạnh mưa, nắng ráo"},
        "p1": {
            36: "雨 不 下 了， 天 晴 了。",
            37: "他 给 女 朋友 买了 一 个 新 手机。",
            38: "准备 好 了 吗？ 好， 笑一笑。",
            39: "非常 欢迎 你 来 我们 公司 工作。",
            40: "每 天 早上 她 都 要 慢 跑 一 小时。"
        },
        "p2_options": {"A": "一起", "B": "西瓜", "C": "题", "D": "号", "E": "贵", "F": "雪"},
        "p2": {
            41: "天 阴 了， 可能 要 下（   ）。",
            42: "我 要 睡觉 了， 那些（   ） 明天 再 做 吧。",
            43: "我 希望 能 和 你 在（   ）。",
            44: "我 今年 14 岁， 我 的 生日 是 6 月 7 （   ）。",
            45: "男： 现在（   ） 多少 钱 一 斤？\n女： 我 看看， 这儿 写着 呢， 5 元 一 斤。"
        },
        "p3": {
            46: {"ctx": "您 请 进， 这 就 是 我 的 家。 这个 房间 是 我 和 我 丈夫 的， 旁边 那个 小 的 是 孩子 的 房间。", "stmt": "我们 的 房间 比 孩子 的 大。"},
            47: {"ctx": "我 爸爸 不 爱 喝 咖啡， 他 喜欢 喝 茶， 每 天 上午 都 会 喝 几 杯 热 茶。", "stmt": "爸爸 觉得 茶 不 好喝。"},
            48: {"ctx": "他 在 火车站 工作， 每 天 都 很 忙， 但 他 很 少 说 累， 他 觉得 能 帮助 人们 是 他 最大 的 快乐。", "stmt": "他 很 喜欢 他 的 工作。"},
            49: {"ctx": "这些 桌子 和 椅子 都 是 100 多 年 前 做 的， 所以 比 现在 的 要 贵 很 多。", "stmt": "这些 桌子、 椅子 都 很 新。"},
            50: {"ctx": "他 做 的 菜 比 我 做 的 好吃， 但是 因为 工作 忙， 他 很 少 做。", "stmt": "他 不 会 做 菜。"}
        },
        "p4_5155_options": {
            "A": "对不起， 再 给 我 一 天 时间。",
            "B": "王 老师， 你 的 电话。",
            "C": "一 个 鸡蛋， 喝了 些 牛奶。",
            "D": "你 出去 的 时候 多 穿 些 衣服。",
            "E": "他 在 哪儿 呢？ 你 看见 他 了 吗？",
            "F": "这 船 是 从 上海 开 来 的。"
        },
        "p4_5155": {
            51: "外面 天气 非常 冷。",
            52: "今天 早上 吃 什么 了？",
            53: "李 先生 在 吗？ 接 一下 电话。",
            54: "那个 苹果 我 已经 洗 了。",
            55: "这 件 事情 你 准备 什么 时候 告诉 他？"
        },
        "p4_5660_options": {
            "A": "这个 名字 很 有 意思。",
            "B": "太 多 了 吧？ 这 是 药！",
            "C": "你 姐姐 真 高， 这么 漂亮， 她 有 男 朋友 了 吗？",
            "D": "在 门 后面 玩儿 呢。",
            "E": "您 看 了 吗？ 没 什么 问题 吧？",
            "F": "没 关系， 我 听 得 懂。"
        },
        "p4_5660": {
            56: "我 弟弟 的 狗 呢？",
            57: "一 次 吃 三 块儿？",
            58: "大家 都 叫 他 “大高”。",
            59: "我 已经 看了 两 次 了， 非常 好。",
            60: "她 已经 结婚 了， 丈夫 是 我 哥哥。"
        }
    },
    "h21004": {
        "p1_options": {"A": "Chơi bóng rổ", "B": "Hai người nói chuyện vui vẻ", "C": "Hai người ngắm cảnh", "D": "Bóng rổ ví dụ", "E": "Chào tạm biệt ở sân bay", "F": "Bác sĩ khám bệnh"},
        "p1": {
            36: "再见， 祝 你 一路 平安！",
            37: "他 在 哪儿 呢？ 你 看见 他 了 吗？",
            38: "他们 在 谈论 今天 的 新闻。",
            39: "医生 正在 给他 看病。",
            40: "我们 一起 去 散步 吧。"
        },
        "p2_options": {"A": "新", "B": "百", "C": "小时", "D": "回答", "E": "贵", "F": "牛奶"},
        "p2": {
            41: "别 说话， 听听 他 怎么 （   ） 这个 题。",
            42: "你 好， 这个 篮球 卖 三（   ） 块 钱 吗？",
            43: "喝（   ） 前， 先 吃 个 鸡蛋 吧。",
            44: "你 知道 吗？ 一 年 有 8700 多 个（   ）。",
            45: "女： 你（   ） 买 的 车 是 什么 颜色 的？\n男： 黑色 的。"
        },
        "p3": {
            46: {"ctx": "唱歌 是一件 让 人 高兴 的 事情， 每 年 生日 我 都 会和 朋友们 去 唱歌。", "stmt": "我 爱 唱歌。"},
            47: {"ctx": "你 看， 这 就 是 我 家 的 猫， 眼睛 漂亮 不？ 它 是 我 妹妹 送 给 我们 的。", "stmt": "猫 是 弟弟 家 的。"},
            48: {"ctx": "中国人 喜欢 说 “好好 学习， 天天 向上”， 意思 是 希望 孩子们 从 小 爱 学习， 多 学 东西。", "stmt": "中国人 希望 孩子 多 学习。"},
            49: {"ctx": "你 去过 “一 元 店” 吗？ 在 这样 的 商店 里， 一 块 钱 就 可以 买 一 件 东西。", "stmt": "“一 元 店” 的 东西 很 贵。"},
            50: {"ctx": "水果 中， 我 最 爱 吃 苹果 和 西瓜。 我 每 天 都 要 吃 一 个 苹果， 医生 说， 多 吃 苹果 对 身体 好。", "stmt": "我 觉得 西瓜 很 好吃。"}
        },
        "p4_5155_options": {
            "A": "那 本 书 我 已经 看 完 了。",
            "B": "船 快 开 了， 你 回去 吧。",
            "C": "我 想 买 500 斤 大米， 你们 能 帮 我 送 一下 吗？",
            "D": "这 两 件 我 都 喜欢。",
            "E": "他 还 在 教室 里 学习。",
            "F": "服务员， 我 想 要 杯 热 水， 谢谢 你。"
        },
        "p4_5155": {
            51: "怎么 这么 快？ 有 意思 吗？",
            52: "你 觉得 红色 的 和 白色 的 哪个 好？",
            53: "好， 再见， 到了 给 我 来 个 电话。",
            54: "可以， 您 住 哪儿？",
            55: "星期日， 她 和 丈夫 在 饭店 吃 晚饭。"
        },
        "p4_5660_options": {
            "A": "就 知道 他 姓 张。",
            "B": "没 关系， 你们 坐 出租车 去 吧。",
            "C": "好 的， 谢谢 你们。",
            "D": "哥， 明天 天气 怎么样？ 是 阴天？",
            "E": "同学们， 今天 我们 开始 学习 第五 课。",
            "F": "没 关系， 我 听 得 懂。"
        },
        "p4_5660": {
            56: "那个 医生 没 告诉 我 他 的 名字。",
            57: "晴天， 但是 很 冷， 你 出 门 多 穿 点儿。",
            58: "火车站 离 这儿 很 远。",
            59: "慢 走， 欢迎 您 下 次 再 来。",
            60: "请 你 读 一下 这 几 个 汉字。"
        }
    },
    "h21005": {
        "p1_options": {"A": "Hai bạn đọc sách", "B": "Cô gái nằm giường xem tivi", "C": "Hỏi thăm ở lớp học", "D": "Bóng rổ ví dụ", "E": "Đón khách vui mừng", "F": "Gọi điện thoại"},
        "p1": {
            36: "李 老师， 这个 教室 能 坐 多少 人？",
            37: "你 好， 欢迎， 非常 欢迎！",
            38: "她 还 没 睡觉， 正在 床 上 看 电视 呢。",
            39: "请 告诉 我 您 的 电话 是 多少。",
            40: "同学们， 请 大家 和 我 一起 读。"
        },
        "p2_options": {"A": "认识", "B": "从", "C": "鱼", "D": "为什么", "E": "贵", "F": "介绍"},
        "p2": {
            41: "我 妹妹 的 孩子 最 喜欢 问（   ）。",
            42: "这个 工作 是 朋友 帮 我（   ） 的。",
            43: "我 已经（   ） 家 里 出来 了， 10 分钟 后 到。",
            44: "小猫 你 别 叫 了， 这些（   ） 都 是 给 你 准备 的。",
            45: "女： 小王 旁边 那个 女孩儿 是 谁？ 你（   ） 吗？\n男： 是 他 女朋友。"
        },
        "p3": {
            46: {"ctx": "今天 太 累 了， 我 不 想 做 饭 了， 我们 去 外面 吃 吧， 你 想 吃 什么？", "stmt": "他们 想 在 家 吃 饭。"},
            47: {"ctx": "不 要 在 公共汽车 上 看 书、 看 报纸， 因为 那样 对 眼睛 不 好。", "stmt": "坐 公共汽车 对 眼睛 不 好。"},
            48: {"ctx": "我 从 11 岁 开始 踢 足球， 已经 踢 了 10 年 了， 我 踢进 了 很多 球， 每次 进球 的 时候 我 都 非常 快乐。", "stmt": "他 爱 踢 足球。"},
            49: {"ctx": "从 学校 到 机场， 坐 出租车 要 一 小时， 我们 10 点 的 飞机， 8 点 从 学校 走 可以 吗？", "stmt": "他们 坐 8 点 的 飞机。"},
            50: {"ctx": "我 每 天 早上 都 要 出去 跑步。 昨天 是 阴天， 跑着跑着， 开始 下雨 了。 等 我 跑 回 家 时， 天 晴 了。", "stmt": "昨天 下雨 了。"}
        },
        "p4_5155_options": {
            "A": "我 是 新 来 的， 所以 您 可能 没 见过 我。",
            "B": "怎么样？ 现在 可以 开始 了 吗？",
            "C": "明天 要 考试， 考完 试 再 去 看 吧。",
            "D": "这 是 我 第二 次 来 北京。",
            "E": "他 还 在 教室 里 学习。",
            "F": "这 件 衣服 的 颜色， 我 不 喜欢。"
        },
        "p4_5155": {
            51: "对不起， 请 等 一下， 王 小姐 还 没 到。",
            52: "你 是 这里 的 服务员 吗？",
            53: "晚上 去 不 去 看 电影？",
            54: "希望 这 次 你 能 在 这儿 多 住 几 天。",
            55: "好， 没 关系， 我们 再 去 别的 商店 看看。"
        },
        "p4_5660_options": {
            "A": "我 也 不 知道， 你 问问 小刘 吧。",
            "B": "这儿 离 火车站 不 远， 很 近。",
            "C": "妻子 让 他 每 天 早上 起床 后 喝 一 杯 水。",
            "D": "我们 玩儿 得 很 高兴， 还 学会 了 一些 汉语。",
            "E": "他 打 我 电话 时 我 正在 洗 水果。",
            "F": "没 关系， 我 听 得 懂。"
        },
        "p4_5660": {
            56: "那 两 个 字 是 什么 意思？",
            57: "就 在 前面， 走 七 八 分钟 就 到 了。",
            58: "去年 6 月， 我 和 丈夫 去 中国 旅游 了。",
            59: "您 找 我 什么 事？",
            60: "医生 说 这样 对 身体 好。"
        }
    },
    "h21006": {
        "p1_options": {"A": "Học sinh chào tạm biệt", "B": "Cúi sát đọc sách mỏi mắt", "C": "Phục vụ bàn đưa thực đơn", "D": "Bóng rổ ví dụ", "E": "Đọc tờ báo của công ty", "F": "Khiêu vũ"},
        "p1": {
            36: "这 张 报纸 上 有 我们 公司 的 介绍。",
            37: "这样 看 书 对 眼睛 不 好。",
            38: "服务员， 你们 这儿 有 什么 好吃 的 菜？",
            39: "你 也 爱 跳舞？ 太 好 了。",
            40: "明天 上午 学校 见， 再见。"
        },
        "p2_options": {"A": "大家", "B": "知道", "C": "手机", "D": "旁边", "E": "贵", "F": "离"},
        "p2": {
            41: "孩子 做错 了 事情， 你 要 让 他（   ） 错 在 哪儿 了。",
            42: "她 家（   ） 公司 很 近， 每 天 中午 都 回 家 吃 饭。",
            43: "我 住 345 房间， 就 在 你（   ）。",
            44: "他 的 回答 很 有 意思， （   ） 都 笑 了。",
            45: "女： 这个（   ） 还 有 什么 颜色 的？\n男： 还 有 红色 和 黑色 的。"
        },
        "p3": {
            46: {"ctx": "我 现在 在 出租车 上， 很 快 就 到 火车站 了。 你 找 我 什么 事？", "stmt": "他 已经 到 火车站 了。"},
            47: {"ctx": "一 年 有 365 天， 每 天 都 会 有 高兴 的 事， 每 天 找 一点儿 快乐， 我们 就 会 有 很 多 快乐。", "stmt": "快乐 就 在 我们 身边。"},
            48: {"ctx": "那儿 有 一 家 新 开 的 商店， 我 昨天 去了 一 次， 衣服 很 便宜， 下班 后 我们 去 看看？", "stmt": "她们 正在 买 衣服。"},
            49: {"ctx": "我 喜欢 喝 咖啡， 但是 今天 太 晚 了， 给 我 来 一 杯 牛牛奶 好 了， 谢谢。", "stmt": "她 要 喝 咖啡。"},
            50: {"ctx": "对不起， 那个 人 我 也 不 认识， 您 可以 问问 小张， 他 在 这儿 工作 的 时间 长， 认识 的 人 多。", "stmt": "小张 可能 认识 那个 人。"}
        },
        "p4_5155_options": {
            "A": "坐 公共汽车 去， 20 分钟 就 能 到。",
            "B": "没 问题， 您 有 什么 事？",
            "C": "没 关系， 慢慢 来。",
            "D": "今天 玩儿 得 很 高兴， 谢谢！",
            "E": "他 在 哪儿 呢？ 你 看见 他 了 吗？",
            "F": "那 打 电话 告诉 他 别 去 踢 足球 了， 明天 再 去。"
        },
        "p4_5155": {
            51: "不 客气， 欢迎 您 下 次 再 来。",
            52: "一 个 星期 了， 弟弟 还 没 学 会 游泳 呢。",
            53: "从 这儿 到 机场 远 吗？",
            54: "我 觉得 今天 天气 不 太 好， 很 可能 会 下 雨。",
            55: "喂？ 请 问， 你 会 说 汉语 吗？"
        },
        "p4_5660_options": {
            "A": "不， 我 去年 去过 北京。",
            "B": "别 睡 了， 起床， 我们 去 跑步。",
            "C": "那 是 我 丈夫 和 女儿， 我们 准备 一起 去 看 电影。",
            "D": "这 门 课 什么 时候 考试？",
            "E": "您 是 第一 次 来 中国 吗？",
            "F": "天气 这么 热， 我们 吃 块儿 西瓜 吧。"
        },
        "p4_5660": {
            56: "不， 我 去年 去过 北京。",
            57: "太 冷 了， 明天 再 说 吧。",
            58: "外面 有 两 个 人， 是 在 等 你 吗？",
            59: "听说 是 6 月 7 号。",
            60: "你们 要不要 喝 点儿 茶？"
        }
    }
}

H21004_LISTEN_OPTS = {
    21: {"A": "下雨", "B": "太忙了", "C": "要考试了"},
    22: {"A": "今天", "B": "明天", "C": "后天"},
    23: {"A": "很高", "B": "做妈妈了", "C": "没男朋友"},
    24: {"A": "没开机", "B": "找不到了", "C": "快没电了"},
    25: {"A": "教室", "B": "公司", "C": "医院"},
    26: {"A": "家里", "B": "商店", "C": "饭馆儿"},
    27: {"A": "多运动", "B": "少吃肉", "C": "多吃水果"},
    28: {"A": "在右边", "B": "有两张", "C": "还没看见"},
    29: {"A": "5分钟", "B": "10分钟", "C": "15分钟"},
    30: {"A": "菜", "B": "身体", "C": "茶馆儿"},
    31: {"A": "机场", "B": "路上", "C": "飞机上"},
    32: {"A": "5点", "B": "6点", "C": "7点"},
    33: {"A": "8月1号", "B": "10月1号", "C": "10月2号"},
    34: {"A": "手表", "B": "电脑", "C": "自行车"},
    35: {"A": "妻子", "B": "同学", "C": "学生"},
}

H21005_LISTEN_OPTS = {
    21: {"A": "路上", "B": "船上", "C": "飞机上"},
    22: {"A": "生病了", "B": "很高兴", "C": "有点儿忙"},
    23: {"A": "大一些", "B": "小一些", "C": "高一些"},
    24: {"A": "姐姐的", "B": "哥哥的", "C": "朋友的"},
    25: {"A": "医院", "B": "饭馆儿", "C": "家里"},
    26: {"A": "65", "B": "70", "C": "75"},
    27: {"A": "累了", "B": "没听懂", "C": "不想休息"},
    28: {"A": "女儿没来", "B": "女儿姓王", "C": "女儿在那儿"},
    29: {"A": "吃药", "B": "喝咖啡", "C": "去上课"},
    30: {"A": "一起来的", "B": "打过电话", "C": "看见车了"},
    31: {"A": "200元", "B": "300元", "C": "400元"},
    32: {"A": "学校", "B": "机场", "C": "商店"},
    33: {"A": "要喝水", "B": "要吃米饭", "C": "要吃苹果"},
    34: {"A": "工作", "B": "学习", "C": "运动"},
    35: {"A": "14号", "B": "16号", "C": "17号"},
}

def get_listening_opts_generic(doc):
    txt = doc[5].get_text() + '\n' + doc[6].get_text()
    opts = {}
    for q in range(21, 36):
        m = re.search(rf'{q}\s*[．\.](.*?)(?=(?:{q+1})\s*[．\.]|第四部分|H2|\Z)', txt, re.DOTALL)
        if m:
            raw = m.group(1)
            mA = re.search(r'A\s*(.*?)(?=B|\Z)', raw, re.DOTALL)
            mB = re.search(r'B\s*(.*?)(?=C|\Z)', raw, re.DOTALL)
            mC = re.search(r'C\s*(.*?)(?=\Z)', raw, re.DOTALL)
            if mA and mB and mC:
                clean_A = ''.join(c for c in mA.group(1) if '\u4e00' <= c <= '\u9fff' or c in '0123456789 ')
                clean_B = ''.join(c for c in mB.group(1) if '\u4e00' <= c <= '\u9fff' or c in '0123456789 ')
                clean_C = ''.join(c for c in mC.group(1) if '\u4e00' <= c <= '\u9fff' or c in '0123456789 ')
                opts[q] = {
                    "A": " ".join(clean_A.split()),
                    "B": " ".join(clean_B.split()),
                    "C": " ".join(clean_C.split())
                }
    return opts

def process_text_ruby(text):
    tokens = tokenize_chinese(text)
    ruby_html = tokens_to_ruby_html(tokens)
    return {"text": text, "ruby": ruby_html}

EXAM_BANK = {}

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
        t_data = process_text_ruby(script)
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
        t_data = process_text_ruby(script)
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
        t_data = process_text_ruby(script)
        opts_raw = lo.get(q, {"A": "", "B": "", "C": ""})
        opts_proc = {}
        for l in ["A", "B", "C"]:
            ot = opts_raw.get(l, "")
            opts_proc[l] = process_text_ruby(ot)
            
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
        t_data = process_text_ruby(script)
        opts_raw = lo.get(q, {"A": "", "B": "", "C": ""})
        opts_proc = {}
        for l in ["A", "B", "C"]:
            ot = opts_raw.get(l, "")
            opts_proc[l] = process_text_ruby(ot)
            
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
        t_data = process_text_ruby(txt)
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
        p2_opts_proc[l] = process_text_ruby(opt_word)
        
    for q in range(41, 46):
        txt = rd["p2"][q]
        t_data = process_text_ruby(txt)
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
        ctx_data = process_text_ruby(ctx)
        stmt_data = process_text_ruby(stmt)
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
    p4a_opts = {l: process_text_ruby(text) for l, text in rd["p4_5155_options"].items()}
    for q in range(51, 56):
        txt = rd["p4_5155"][q]
        t_data = process_text_ruby(txt)
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

    p4b_opts = {l: process_text_ruby(text) for l, text in rd["p4_5660_options"].items()}
    for q in range(56, 61):
        txt = rd["p4_5660"][q]
        t_data = process_text_ruby(txt)
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
    print(f"Compiled {exam_id}: {len(exam_questions)} questions (1 - 60)")

js_code = f"const HSK2_FULL_DATABASE = {json.dumps(EXAM_BANK, ensure_ascii=False, indent=2)};\n"
with open("hsk2_full_database.js", "w", encoding="utf-8") as f:
    f.write(js_code)

print("Saved hsk2_full_database.js successfully! File size:", os.path.getsize("hsk2_full_database.js"), "bytes")
