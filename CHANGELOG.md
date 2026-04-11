# 更新日志

所有重要的更新和变更都会记录在此文件中。

---

## [v2.0.0] - 2026-04-11

本次更新是一次重大升级，涵盖 UI 重构、指法系统修正和新功能开发。

### 🚀 新增功能

#### 1. 深色主题 UI（参考 type.fun）

**文件**: `config.py`, `keyboard/keyboard_renderer.py`

| 元素 | 旧值 | 新值 |
|------|------|------|
| 背景色 | `(240, 248, 255)` 浅蓝 | `(45, 52, 54)` 深灰蓝 |
| 主色调 | `(70, 130, 180)` 钢蓝 | `(236, 72, 153)` 粉红 |
| 按键背景 | `(200, 200, 200)` 浅灰 | `(61, 79, 95)` 深灰 |
| 圆角半径 | `5px` | `8px` |

**新增颜色定义**:
- `KEY_HIGHLIGHT`: 按键高亮色 `#EC4899`
- `KEY_HOME_POS`: 基准键颜色 `#10B981`
- `KEY_PRESSED`: 按下状态 `#636B78`
- `KEYBOARD_BG`: 键盘背景 `#1A2026`

#### 2. 分阶段训练系统

**文件**: `game_modes/beginner_mode.py`

```python
TRAINING_STAGES = [
    {'id': 1, 'name': '基准键位', 'keys': ['a','s','d','f','j','k','l',';'], 'required_count': 30},
    {'id': 2, 'name': '左手无名指', 'keys': ['2','w','s','x'], 'required_count': 25},
    # ... 共10个阶段
]
```

**特点**:
- 每阶段有最低准确率要求 (60%-70%)
- 未达标自动重练当前阶段
- 阶段切换动画 (1.5秒)
- 进度条显示阶段完成度

#### 3. 指法合规性追踪器

**新文件**: `ui/finger_tracker.py`

```python
class FingerComplianceTracker:
    - record_key_press()    # 记录每次按键
    - get_compliance_rate() # 获取合规率
    - get_finger_balance_score()  # 获取均衡分数
    - get_wrong_finger_report()   # 获取错误报告
```

**集成**: `game_modes/base_mode.py` - 所有模式自动启用追踪

#### 4. 姿势指导模块

**新文件**: `ui/posture_guide.py`

包含4页指导内容：
1. 坐姿要点
2. 手臂姿势
3. 手指放置
4. 基准键位

#### 5. 指法均衡算法

**文件**: `game_modes/advanced_mode.py`

```python
def spawn_letter(self):
    # 80% 概率选择使用最少的手指
    # 20% 概率完全随机
```

### 🔧 Bug 修复

#### P0 - 指法映射严重错误

**文件**: `keyboard/keyboard_renderer.py`

| 按键 | 错误映射 | 正确映射 |
|------|----------|----------|
| `2` | `left_pinkie` | `left_ring` |
| `w` | `left_pinkie` | `left_ring` |
| `s` | `left_pinkie` | `left_ring` |
| `x` | `left_pinkie` | `left_ring` |
| `3` | `left_ring` | `left_middle` |
| `e` | `left_ring` | `left_middle` |
| `d` | `left_ring` | `left_middle` |
| `c` | `left_ring` | `left_middle` |
| `4` | `left_middle` | `left_index` |
| `r` | `left_middle` | `left_index` |
| `f` | `left_middle` | `left_index` |
| `v` | `left_middle` | `left_index` |
| 空格 | `right_thumb` (字典覆盖) | `both_thumbs` |
| `i` | `right_index` | `right_middle` |
| `9` | `right_ring` | `right_middle` |

### 📁 文件变更清单

| 文件 | 操作 | 说明 |
|------|------|------|
| `config.py` | 修改 | 深色主题配色方案 |
| `keyboard/keyboard_renderer.py` | 修改 | 指法映射修正 + 深色UI渲染 |
| `game_modes/base_mode.py` | 修改 | 集成指法追踪器 |
| `game_modes/beginner_mode.py` | 重写 | 10阶段训练系统 |
| `game_modes/advanced_mode.py` | 修改 | 指法均衡算法 |
| `ui/finger_tracker.py` | 新增 | 指法合规性追踪器 |
| `ui/posture_guide.py` | 新增 | 姿势指导模块 |
| `README.md` | 更新 | 文档更新 |

### 🎨 UI 细节改进

1. **键盘渲染**:
   - 圆角按键 (8px radius)
   - 按键内阴影效果
   - 基准键 F/J 底部指示条

2. **手指引导图**:
   - 激活手指发光效果
   - 未激活手指轮廓线
   - 深色主题配色

3. **阶段介绍动画**:
   - 遮罩背景
   - 阶段标题 + 描述
   - 倒计时显示

### 🔍 验证状态

- [x] 所有文件语法检查通过
- [x] 模块导入测试通过
- [x] 游戏可正常启动
- [x] 深色主题渲染正常

---

## [v1.x] - 历史版本

早期版本的详细变更请查看 git log。
