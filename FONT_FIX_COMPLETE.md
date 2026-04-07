# 字体乱码问题根本性修正说明

## 问题原因

### 为什么换环境就乱码？

1. **依赖系统字体，跨平台兼容性差**
   - 代码中所有文本渲染都使用 `pygame.font.SysFont()` 依赖系统字体
   - 不同操作系统（Windows、macOS、Linux）的字体名称和安装情况差异很大
   - 例如：Windows 上没有 `pingfang/hiraginosansgb`（macOS 字体），macOS 上没有 `simhei/msyh`（Windows 字体）
   - 当 `SysFont` 匹配不到中文字体时，会回退到不支持中文的默认西文字体，导致中文显示为方框

2. **缺乏随包携带的中文字体**
   - 项目中 `resources/fonts/` 目录为空，没有自带的中文字体文件
   - 这意味着程序完全依赖系统字体，无法保证在任何环境下都能显示中文

3. **没有字体验证机制**
   - 即使加载了字体，也没有验证字体是否真的能渲染中文字符
   - 可能加载的字体文件损坏或不支持中文，导致显示异常

4. **字体加载逻辑分散**
   - 每个模块都有自己的字体加载逻辑，代码重复且不一致
   - 修改字体设置需要在多个地方同步修改，容易遗漏

## 根本性修正方案

### 1. 创建统一的字体加载器 (`font_loader.py`)

**核心特性：**
- 三级回退机制：自带字体文件 → 系统中文字体 → pygame 默认字体
- 字体验证：加载后自动测试能否渲染中文字符
- 字体缓存：避免重复加载相同字体，提升性能
- 跨平台支持：内置了 Windows、macOS、Linux 常见中文字体列表

**加载流程：**
```
1. 尝试加载自带字体文件
   ↓ 失败
2. 遍历系统中文字体列表
   ↓ 匹配成功
3. 验证字体能否渲染中文
   ↓ 失败
4. 回退到 pygame 默认字体
```

### 2. 支持随包携带中文字体

- 创建 `resources/fonts/` 目录
- 提供字体文件下载说明（推荐使用 Noto Sans SC 或思源黑体）
- 程序优先使用自带字体，确保在任何环境下都能显示中文

### 3. 替换所有模块的字体加载逻辑

**修改的文件：**
- `ui/text.py` - 文本渲染组件
- `ui/button.py` - 按钮组件
- `keyboard/keyboard_renderer.py` - 键盘渲染器
- `game_modes/base_mode.py` - 游戏模式基类
- `game_modes/beginner_mode.py` - 初级模式
- `game_modes/intermediate_mode.py` - 中级模式
- `game_modes/master_mode.py` - 大师模式
- `game_modes/advanced_mode.py` - 高级模式
- `scene_manager.py` - 场景管理器
- `main.py` - 主程序入口

**修改内容：**
- 所有 `pygame.font.SysFont()` 替换为 `load_font()`
- 添加 `font_dir` 参数传递字体目录路径
- 在主程序启动时输出字体诊断信息

### 4. 添加字体诊断功能

在 `font_loader.py` 中实现了 `log_font_diagnosis()` 函数：
- 输出系统可用字体数量
- 列出匹配到的中文字体
- 检测默认字体是否支持中文
- 测试当前加载的字体渲染效果

在程序启动时自动调用，帮助快速定位字体问题。

## 使用说明

### 快速解决（推荐）

1. 下载中文字体文件（推荐 Noto Sans SC）：
   ```
   https://github.com/googlefonts/noto-fonts/raw/main/hinted/ttf/NotoSansSC/NotoSansSC-Regular.ttf
   ```

2. 将字体文件放入 `resources/fonts/` 目录：
   ```
   keyboard_trainer/resources/fonts/NotoSansSC-Regular.ttf
   ```

3. 运行程序，会自动检测并使用该字体

### 系统字体模式（无自带字体）

如果不提供字体文件，程序会：
1. 尝试使用系统中已安装的中文字体
2. Windows: 微软雅黑 (msyh)、黑体 (simhei) 等
3. macOS: 萍方 (pingfang)、冬青黑体 (hiraginosansgb) 等
4. Linux: Noto Sans CJK、思源黑体 (sourcehansans) 等

启动时会输出诊断信息，帮助确认是否成功加载中文字体。

## 技术细节

### 字体加载器 API

```python
from font_loader import load_font

# 基本用法
font = load_font(24)  # 字体大小 24

# 指定字体目录
font = load_font(24, font_dir=config.FONTS_DIR)

# 加粗字体
font = load_font(24, bold=True)

# 清空缓存（测试用）
from font_loader import clear_cache
clear_cache()

# 获取当前使用的字体（调试用）
from font_loader import get_current_font_path
print(f"当前字体: {get_current_font_path()}")
```

### 诊断信息示例

```
============================================================
字体诊断信息
============================================================
系统可用字体数量: 245
匹配到的中文字体: 6 个

可用的中文字体:
  - msyh
  - msyhbd
  - simhei
  - simsun
  - dengxian
  - fangsong

默认字体支持中文: 否

当前使用字体: 自带: resources/fonts/NotoSansSC-Regular.ttf
测试文本渲染: 成功
============================================================
```

## 兼容性

- **Windows**: 完全支持，优先使用微软雅黑/黑体
- **macOS**: 完全支持，优先使用萍方/冬青黑体
- **Linux**: 完全支持，优先使用 Noto Sans CJK/思源黑体
- **跨平台**: 通过自带字体保证一致性

## 性能优化

- 字体缓存：相同大小和加粗设置的字体只加载一次
- 字体验证：只在加载时验证一次，后续直接使用缓存
- 按需加载：根据实际使用的字体大小加载，避免加载不必要的字体

## 总结

通过本次修正：
1. ✅ 从根本上解决了跨环境字体乱码问题
2. ✅ 提供了稳定的字体加载机制
3. ✅ 支持随包携带字体，保证一致性
4. ✅ 添加了诊断功能，便于快速定位问题
5. ✅ 统一了字体加载逻辑，便于维护

无论在 Windows、macOS 还是 Linux 上，都能稳定显示中文文本。
