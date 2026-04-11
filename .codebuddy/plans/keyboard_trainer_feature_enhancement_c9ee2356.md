---
name: keyboard_trainer_feature_enhancement
overview: 为键盘训练游戏添加两项功能改进：1) 初级/中级模式添加指法示意图（显示正确手指）；2) 高级/大师模式增加动态速度调节机制（连续错误减速，速度过低结束游戏）
design:
  fontSystem:
    fontFamily: PingFang SC
    heading:
      size: 24px
      weight: 600
    subheading:
      size: 18px
      weight: 500
    body:
      size: 16px
      weight: 400
  colorSystem:
    primary:
      - "#4682B4"
      - "#FFA500"
    background:
      - "#F0F8FF"
      - "#FFFFFF"
    text:
      - "#1E1E1E"
      - "#FFFFFF"
    functional:
      - "#32CD32"
      - "#DC143C"
      - "#FFD700"
todos:
  - id: finger-guide-renderer
    content: 在 keyboard_renderer.py 中实现 FingerGuide 渲染器，包含 _draw_hand/_draw_finger 像素绘图方法和 render_finger_guide 主渲染方法，支持 active_finger 参数控制高亮
    status: completed
  - id: beginner-finger-integration
    content: 在 beginner_mode.py 的 render() 方法末尾调用 finger_guide 渲染，传入 target_key 对应的手指名称作为高亮参数
    status: completed
    dependencies:
      - finger-guide-renderer
  - id: intermediate-finger-integration
    content: 在 intermediate_mode.py 的 render() 方法末尾调用 finger_guide 渲染，根据 current_content[current_index] 获取对应手指并高亮
    status: completed
    dependencies:
      - finger-guide-renderer
  - id: advanced-dynamic-speed
    content: 在 advanced_mode.py 中新增 consecutive_errors 计数器和 speed_penalty 因子，修改 update()/handle_key_down() 中的错误处理逻辑实现连续错误降速和速度下限结束机制
    status: completed
  - id: master-dynamic-speed
    content: 在 master_mode.py 中同步实现相同的动态速度调节机制（consecutive_errors 计数、降速规则、下限结束），并在 submit_pinyin() 和落地检测中加入错误计数
    status: completed
  - id: speed-ui-indicator
    content: 在高级模式和大师模式的 render_game_info() 中添加速度倍率百分比和连续错误数的可视化显示，含颜色警告梯度
    status: completed
    dependencies:
      - advanced-dynamic-speed
      - master-dynamic-speed
  - id: 2c3d8f75
    content: 完成修改后对程序进行单元测试和功能测试，如果在测试过程中发现错误，即使修正，修正后继续进行测试，直到可以保证程序正确运行
    status: completed
---

## 产品概述

为儿童键盘练习游戏添加两项功能改进：(1) 在初级和中级模式的虚拟键盘下方添加标准指法示意图，敲击按键时显示对应手指标识；(2) 为高级和大师模式增加动态速度调节机制，连续错误时降低下落速度，速度过低时自动结束游戏。

## 核心功能

### 功能一：指法示意图（初级/中级模式）

- **位置**：在虚拟键盘下方（键盘底部边缘以下约10-15像素间距），屏幕底部安全区域内绘制
- **触发条件**：当有目标按键被高亮时，自动显示该目标键对应的手指标识
- **视觉设计**：用像素绘制的简笔手形图形表示10个手指（左手5指+右手5指），指尖朝上
- **高亮逻辑**：当前目标键对应的手指用其专属颜色高亮显示，其余手指用灰色显示
- **手指名称**：在高亮手指旁显示中文标签（如"右手食指"）
- **不重叠保证**：位于键盘下方独立区域，与现有所有UI元素无冲突
- **涉及文件**：`keyboard/keyboard_renderer.py` 新增 `FingerGuide` 渲染器；`game_modes/beginner_mode.py` 和 `game_modes/intermediate_mode.py` 的 render 方法调用

### 功能二：动态速度调节机制（高级/大师模式）

- **保留现有逻辑**：保留基于时间的速度递增公式 `current_speed = base_speed + (game_time/duration) * speed_increment`
- **连续错误计数**：新增 `consecutive_errors` 计数器，跟踪连续未命中次数
- **降速规则**：每累计 2 次连续错误（包括按错键未命中、目标落地漏失），将当前速度乘以 0.95
- **速度下限**：当实际速度降至初始速度（base_speed）的 0.5 倍时，自动调用 `end_game()` 结束并结算
- **重置条件**：成功击中目标时重置 `consecutive_errors` 为 0
- **UI反馈**：在游戏信息面板中显示当前速度倍率和连续错误计数
- **涉及文件**：`game_modes/advanced_mode.py` 和 `game_modes/master_mode.py`

## Tech Stack

- **语言**：Python 3.12 + Pygame 2.x
- **现有架构**：场景管理器模式，BaseMode 基类 → 各游戏模式子类，KeyboardRenderer 独立渲染键盘

## 实现方案

### 功能一：指法示意图 - 技术方案

**核心设计思路**：
在 `keyboard/keyboard_renderer.py` 中新增一个 `FingerGuide` 类或直接在 `KeyboardRenderer` 上扩展方法，使用 pygame 的基础绘图原语（椭圆、矩形、线条、多边形）绘制像素风格的简笔手形。利用已有的 `finger_colors` 颜色映射和 `key_to_finger` 按键-手指映射表实现联动。

**手形布局设计**：

- 整体宽度约 300px，高度约 80px
- 水平排列两只手掌的俯视/斜视图，左手在左，右手在右
- 每只手由 1 个手掌矩形 + 5 个手指椭圆形组成
- 手指尖端朝向屏幕上方（12点钟方向）
- 位置居中于键盘正下方，Y坐标为 `self.keyboard_y + self.keyboard_height + 15`

**渲染流程**：

1. `BeginnerMode.render()` / `IntermediateMode.render()` 调用 `super().render(screen)` 后
2. 获取当前 `target_key`（初级）或当前目标字符对应的手指（中级）
3. 调用 `self.keyboard_renderer.render_finger_guide(screen, active_finger)`
4. `render_finger_guide` 绘制全部10根手指，active_finger 用高亮色+文字标注

### 功能二：动态速度调节 - 技术方案

**核心设计思路**：
在 AdvancedMode 和 MasterMode 中引入"有效速度"(effective_speed)的概念。原有的时间递增公式计算的是基准速度基准值，而实际使用的下落速度在此基础上叠加错误惩罚因子。

**速度公式变更**：

```
# 原有（保留不变）
base_current_speed = base_speed + (game_time / game_duration) * speed_increment

# 新增：错误惩罚因子（初始1.0，每次连续2次错误乘以0.95）
speed_penalty = 0.95 ^ error_penalty_count

# 最终实际速度
effective_current_speed = base_current_speed * speed_penalty
```

**触发点设计**：

- **高级模式**：`handle_key_down()` 中 `not hit_any` 分支 → `consecutive_errors += 1`；落地检测 `if letter.landed:` → `consecutive_errors += 1`
- **大师模式**：`submit_pinyin()` 中 `not hit_any` 分支 → `consecutive_errors += 1`；落地检测 `if char.landed:` → `consecutive_errors += 1`
- **两模式共同**：击中成功时 `consecutive_errors = 0`

**结束判定**：在 `update()` 末尾检查 `effective_current_speed < base_speed * 0.5` 时调用 `end_game()`

## 关键实现细节

### 目录结构

```
project-root/
├── keyboard/
│   └── keyboard_renderer.py    # [MODIFY] 新增 render_finger_guide 方法和 _draw_finger 辅助方法
├── game_modes/
│   ├── beginner_mode.py        # [MODIFY] render() 中调用指法渲染
│   ├── intermediate_mode.py    # [MODIFY] render() 中调用指法渲染
│   ├── advanced_mode.py        # [MODIFY] 新增连续错误计数和动态速度逻辑
│   └── master_mode.py          # [MODIFY] 新增连续错误计数和动态速度逻辑
```

### 性能考虑

- 指法手形使用静态 Surface 缓存（首次绘制后存为 surface，后续只 blit），避免每帧重建绘图原语
- 速度计算仅涉及简单浮点运算，无性能开销

### 向后兼容性

- 所有修改仅在各自模式内部进行，不影响其他模式
- `keyboard_renderer.py` 的改动是纯增量式（新增方法），不修改已有接口

本项目是基于 Pygame 的桌面游戏应用，不涉及 Web UI 框架。此处的 design 标签主要描述游戏内的 UI 组件视觉设计规范。

### 指法示意图视觉设计

#### 整体布局

- 位于虚拟键盘正下方，水平居中
- 两只手并排显示（左手 | 右手），呈微微张开的姿态
- 手掌采用俯视角度（略带倾斜），使手指自然向上伸展

#### 手形绘制规格

- **手掌**：圆角矩形（50x40px），浅肤色填充(255,224,189)，深色边框
- **手指**：细长椭圆形（8x30px），连接在手掌上缘，指尖朝上
- **拇指**：稍短稍粗（10x20px），向外侧偏转约30度
- **间距**：相邻手指间隔6px

#### 高亮状态

- **默认状态**：所有手指用浅灰色(180,180,180)填充，表示非激活
- **激活状态**：目标手指使用其专属颜色填充（复用 finger_colors 映射表），并在手指上方/旁边显示中文标签
- **标签样式**：18px 字体，白色文字 + 半透明深色背景圆角矩形，避免与手指颜色冲突
- **过渡动画**：激活时可选轻微脉冲效果（透明度在0.8~1.0间交替）

#### 尺寸约束

- 总宽度不超过键盘宽度的70%（约560px内），避免超出屏幕边界
- 总高度控制在80px以内，确保在768px屏幕高度内有足够空间
- Y坐标起始位置：keyboard_y + keyboard_height + 15（留出与键盘的间隙）

### 动态速度指示器设计

在高级/大师模式的游戏信息面板中新增两个指标：

1. **速度倍率**：以百分比形式显示当前有效速度相对于初始速度的比例（如 "85%"）
2. **连续错误数**：显示当前的连续错误计数（如 "连错: 2"）
3. 当速度低于初始速度的75%时，速度倍率数字变为橙色警告色
4. 当速度低于初始速度的60%时，变为红色危险色

## Agent Extensions

### SubAgent

- **code-explorer**
- Purpose: 用于在实施过程中快速定位需要修改的具体代码行和验证文件依赖关系
- Expected outcome: 精确定位每个修改点的上下文，确保修改不会破坏现有功能