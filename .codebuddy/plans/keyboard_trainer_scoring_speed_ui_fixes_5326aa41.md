---
name: keyboard_trainer_scoring_speed_ui_fixes
overview: 修复键盘练习游戏中的记分与排行榜串栏/重复问题，补齐中英文用户名与排除测试账号逻辑，同时调整手指示意图拇指位置和高级/拼音模式的真实加速机制，并把加速上限提高到 5.0。
todos:
  - id: unify-mode-identity
    content: 统一 scene_manager.py 与 base_mode.py 的模式标识
    status: completed
  - id: normalize-storage
    content: 重构 storage.py 迁移旧存档并去重过滤排行榜
    status: completed
    dependencies:
      - unify-mode-identity
  - id: fix-ranking-flow
    content: 修正结果页与排行榜页的排行读写链路
    status: completed
    dependencies:
      - unify-mode-identity
      - normalize-storage
  - id: adjust-hand-layout
    content: 重排 keyboard_renderer.py 手型示意图拇指位置
    status: completed
  - id: fix-speed-bonus
    content: 修复 advanced/master 实时加速并上调 speed_bonus_max
    status: completed
  - id: regression-verify
    content: 回归测试串档、黑名单用户名、手型和加速
    status: completed
    dependencies:
      - normalize-storage
      - fix-ranking-flow
      - adjust-hand-layout
      - fix-speed-bonus
---

## User Requirements

修复现有训练模式中的几个关键问题：高级拼音的成绩不能再写到其他项目下，单次游玩也不能产生多条排名；用户名需要正常支持中文、英文及混合输入，但当用户名为“admin”或“tester”时不进入排行榜；手指示意图需要重新摆正，拇指应与四指明显拉开，并位于左手手掌右侧、右手手掌左侧；加速效果需要真正生效，且加速上限改为 5.0。

## Product Overview

成绩系统应表现为“模式归属准确、单局写入一次、排行榜稳定可读”；手型示意图应更接近真实手掌结构；高级和大师类玩法中的加速应有明显体感变化，当前屏幕中的下落对象也能立即体现速度变化。

## Core Features

- 按模式准确归档成绩与排行榜，修复高级拼音串档问题
- 单局成绩只写入一次，避免一次游玩出现多条排名
- 支持中英文用户名输入与展示，并过滤 admin/tester 排名
- 修正左右手示意图中拇指与四指的真实相对位置
- 让加速对当前下落对象即时生效，并将上限提升到 5.0

## Tech Stack Selection

- 现有项目栈：Python 3 + Pygame
- 数据持久化：本地 JSON 存档，入口在 `data/storage.py`
- 场景与模式结构：`scene_manager.py` 调度场景，`game_modes/*.py` 负责玩法逻辑，`keyboard/keyboard_renderer.py` 负责键盘与手型示意图

## Implementation Approach

核心方案是把“显示名称”和“存储标识”彻底分离，并让 `StorageManager` 成为成绩与排行榜的唯一写入口。当前问题的根源已确认有两类：一是“高级拼音”只是 `master` 的子类型，但场景层仍以 `master` 作为结果模式键；二是 `BaseMode` 仍按中文模式名直接往顶层 JSON 写数据，导致 `modes.*` 结构与顶层中文键并存。最佳修复方式不是继续补丁式判断，而是统一为规范模式标识：`beginner`、`intermediate + level`、`advanced`、`advanced_pinyin`、`master`，并由场景、结果页、排行榜页、存储层共同使用。

实现上建议把 `advanced_pinyin` 提升为场景层的一等模式入口，仍复用 `MasterMode` 的玩法实现，但不再依赖“先创建 master 再改 subtype”的临时写法。这样可以同时修复成绩归档、排行榜归档、结果页重玩回到错误模式等连锁问题。`BaseMode` 的新纪录判断与成绩保存也应改为调用 `StorageManager` 的统一接口，不再直接按 `get_mode_name().lower()` 读写 JSON。

排行榜部分需要同时解决“旧数据兼容”和“单局重复写入”。建议在 `StorageManager.ensure_data_structure()` 中加入一次性规范化逻辑：把历史顶层中文模式键迁移并合并到 `data['modes']` 的规范路径中，去重重复记录，清理黑名单用户名，并保证旧存档不会继续把错误结构写回。用户名过滤采用大小写无关、去首尾空格后的比较，屏蔽 `admin` 与 `tester`。为避免一局重复入榜，结果场景还应增加单次提交保护，防止回车和点击重复触发。

加速问题的根因也已明确：当前 `speed_bonus` 虽然会增长，但 `FallingLetter` 和 `FallingChineseChar` 在创建时就把速度固化到了对象实例上，后续已在屏幕中的对象不会同步提速，所以体感很弱。应改为在模式 `update()` 循环中把当帧 `current_speed` 同步到所有存活对象，或让对象更新直接读取外部实时速度。这样复杂度仍是每帧 O(n) 遍历活动对象，和现有更新循环同级，不会引入额外性能瓶颈。排行榜排序与去重的数据量很小，时间复杂度保持在 O(k log k) 且 k 实际远小于 10。

## Implementation Notes

- 优先复用现有 `StorageManager`，不要继续在 `BaseMode` 或场景层直接拼 JSON 路径。
- 旧存档迁移要尽量“合并而非覆盖”，避免用户已有最好成绩被新结构清空。
- 黑名单过滤不仅要拦截新写入，也要清理现有排行榜中的 `admin/tester`。
- 结果页需要防止重复确认提交，避免一次游戏写多条榜单。
- 加速修复应控制在现有玩法循环内完成，避免无关重构或改变原有计分规则。

## Architecture Design

当前修改应保持现有分层，只收敛数据入口和模式标识：

场景层负责提供准确模式键，模式层负责产生成绩，存储层负责规范化保存与读取，结果页和排行榜页只消费规范数据。这样可以把“模式串档”“重复写入”“旧存档分叉”三个问题一起收口到同一条数据链路中。

## Directory Structure

## Directory Structure Summary

本次修改以“统一模式标识、统一成绩入口、修正手型布局、修复实时加速”为主，全部基于现有文件增量调整。

```text
/Users/derekwang/CodeBuddy/keyboard_trainer/
├── scene_manager.py              # [MODIFY] 统一高级拼音的场景模式键；修正结果页传参与重玩逻辑；收敛 ResultScene/RecordsScene 的排行入口
├── game_modes/base_mode.py       # [MODIFY] 移除按中文模式名直写顶层 JSON 的逻辑，改走 StorageManager 统一记录接口
├── game_modes/intermediate_mode.py # [MODIFY] 提供中级模式级别到规范存储键的映射，避免排行榜与记录路径分裂
├── game_modes/master_mode.py     # [MODIFY] 让 advanced_pinyin 与 master 的存储标识可区分；修复实时加速对在场对象生效
├── game_modes/advanced_mode.py   # [MODIFY] 修复实时加速链路，使 speed_bonus 立即影响当前下落字母
├── data/storage.py               # [MODIFY] 规范化旧存档、统一排行榜/记录读写、去重、黑名单过滤、用户名校验
├── keyboard/keyboard_renderer.py # [MODIFY] 重新布局左右手示意图，调整拇指与四指的相对位置和间距
├── config.py                     # [MODIFY] 将 SPEED_BONUS_MAX 调整为 5.0，并同步相关加速参数说明
└── data/game_data.json           # [MODIFY] 清理当前仓库内示例存档的错误模式键与测试账号排行，验证迁移结果
```