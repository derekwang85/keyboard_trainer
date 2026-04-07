"""
统一字体加载器
解决跨环境字体乱码问题：优先使用自带字体，其次系统字体，最后回退默认字体
"""
import os
import pygame

# 自带字体文件名（按优先级排序）
DEFAULT_FONT_CANDIDATES = [
    "NotoSansSC-Regular.ttf",
    "SourceHanSansCN-Regular.otf",
    "NotoSansSC-Medium.ttf",
    "SourceHanSansCN-Medium.otf",
]

# 系统中文字体名列表（跨平台）
SYSTEM_CHINESE_FONTS = [
    # Windows 常见中文字体
    "msyh", "msyhbd", "simhei", "simsun", "dengxian", "fangsong", "kaiti",
    "yahei", "microsoftyahei", "simkai", "simfang",
    # macOS 常见中文字体
    "pingfang", "pingfangtc", "pingfanghk", "pingfangsc",
    "hiraginosansgb", "stheitilight", "stheitimedium", "stheiti",
    "heiti", "stsong", "stkaiti", "stfangsong",
    # Linux 常见中文字体
    "notosanscjksc", "notosanscjk", "sourcehansans",
    "wqy-zenhei", "wqy-microhei", "wenquanyizenhei",
    # 通用 Unicode 字体
    "arialunicodems", "dejavusans", "freesans",
]

# 字体缓存 {(size, bold, font_dir): font}
_font_cache = {}

# 当前使用的字体路径（用于调试）
_current_font_path = None


def set_font_dir(font_dir):
    """设置字体文件目录（在程序初始化时调用）"""
    global _font_dir
    _font_dir = font_dir


def get_current_font_path():
    """获取当前使用的字体路径（用于调试）"""
    return _current_font_path


def load_font(size, bold=False, font_dir=None):
    """
    加载字体（带缓存）
    
    Args:
        size: 字体大小
        bold: 是否加粗
        font_dir: 自带字体目录（如果为None，则尝试从全局设置获取）
    
    Returns:
        pygame.font.Font 对象
    """
    global _font_cache, _current_font_path
    
    key = (size, bold, font_dir)
    if key in _font_cache:
        return _font_cache[key]
    
    font = None
    font_source = None
    
    # 1) 尝试自带字体文件
    if font_dir:
        for fname in DEFAULT_FONT_CANDIDATES:
            font_path = os.path.join(font_dir, fname)
            if os.path.exists(font_path):
                try:
                    font = pygame.font.Font(font_path, size)
                    if bold:
                        font.set_bold(bold)
                    
                    # 验证字体能否渲染中文字符
                    if _can_render_chinese(font):
                        font_source = font_path
                        break
                except Exception as e:
                    # 加载失败，尝试下一个字体
                    continue
    
    # 2) 尝试系统中文字体
    if font is None:
        for font_name in SYSTEM_CHINESE_FONTS:
            font_path = pygame.font.match_font(font_name, bold=bold)
            if font_path:
                try:
                    font = pygame.font.Font(font_path, size)
                    if bold:
                        font.set_bold(bold)
                    
                    # 验证字体能否渲染中文字符
                    if _can_render_chinese(font):
                        font_source = f"系统: {font_name}"
                        break
                except Exception as e:
                    continue
    
    # 3) 兜底：pygame 默认字体
    if font is None:
        font = pygame.font.Font(None, size)
        if bold:
            font.set_bold(bold)
        font_source = "默认"
    
    # 记录当前使用的字体
    if font_source and _current_font_path is None:
        _current_font_path = font_source
    
    # 缓存字体
    _font_cache[key] = font
    return font


def _can_render_chinese(font):
    """验证字体能否渲染中文字符"""
    try:
        rendered = font.render("中", True, (0, 0, 0))
        # 如果渲染结果宽度为0，说明字体不支持中文
        return rendered.get_width() > 0
    except Exception:
        return False


def diagnose_fonts():
    """
    诊断当前环境的字体情况
    返回诊断信息字典
    """
    info = {
        "available_fonts": pygame.font.get_fonts(),
        "available_count": len(pygame.font.get_fonts()),
        "matched_chinese_fonts": [],
        "can_render_default_chinese": False,
    }
    
    # 检查哪些中文字体可用
    for font_name in SYSTEM_CHINESE_FONTS:
        matched = pygame.font.match_font(font_name)
        if matched:
            info["matched_chinese_fonts"].append({
                "name": font_name,
                "path": matched
            })
    
    # 检查默认字体能否渲染中文
    try:
        default_font = pygame.font.Font(None, 16)
        if _can_render_chinese(default_font):
            info["can_render_default_chinese"] = True
    except Exception:
        pass
    
    return info


def clear_cache():
    """清空字体缓存（用于测试或重新加载字体）"""
    global _font_cache, _current_font_path
    _font_cache.clear()
    _current_font_path = None


def log_font_diagnosis():
    """输出字体诊断信息到控制台"""
    print("=" * 60)
    print("字体诊断信息")
    print("=" * 60)
    
    info = diagnose_fonts()
    print(f"系统可用字体数量: {info['available_count']}")
    print(f"匹配到的中文字体: {len(info['matched_chinese_fonts'])} 个")
    
    if info['matched_chinese_fonts']:
        print("\n可用的中文字体:")
        for font_info in info['matched_chinese_fonts'][:10]:  # 只显示前10个
            print(f"  - {font_info['name']}")
        if len(info['matched_chinese_fonts']) > 10:
            print(f"  ... 还有 {len(info['matched_chinese_fonts']) - 10} 个")
    
    print(f"\n默认字体支持中文: {'是' if info['can_render_default_chinese'] else '否'}")
    
    # 测试当前加载的字体
    test_font = load_font(20)
    test_rendered = test_font.render("中文测试 Chinese Test", True, (0, 0, 0))
    print(f"\n当前使用字体: {_current_font_path}")
    print(f"测试文本渲染: 成功" if test_rendered.get_width() > 0 else "失败")
    print("=" * 60)
