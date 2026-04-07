#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
场景管理器，负责管理游戏的不同场景和场景切换
"""

import pygame
from ui.button import Button
from ui.text import Text
from game_modes.beginner_mode import BeginnerMode
from game_modes.intermediate_mode import IntermediateMode
from game_modes.advanced_mode import AdvancedMode
from game_modes.master_mode import MasterMode
from data.storage import StorageManager
from audio.audio_manager import AudioManager
from font_loader import load_font, log_font_diagnosis

class Scene:
    """场景基类"""
    
    def __init__(self, scene_manager):
        """初始化场景"""
        self.scene_manager = scene_manager
        self.app = scene_manager.app
        self.config = self.app.config
        self.audio_manager = self.app.audio_manager
    
    def handle_event(self, event):
        """处理事件"""
        pass
    
    def update(self):
        """更新场景"""
        pass
    
    def render(self, screen):
        """渲染场景"""
        pass

class MainMenuScene(Scene):
    """主菜单场景"""
    
    def __init__(self, scene_manager):
        """初始化主菜单场景"""
        super().__init__(scene_manager)
        
        # 创建标题文本
        self.title = Text(
            "儿童键盘练习小游戏",
            self.config.TITLE_FONT_SIZE,
            self.config.PRIMARY_COLOR,
            (self.config.SCREEN_WIDTH // 2, 100),
            font_dir=self.config.FONTS_DIR
        )
        
        # 创建按钮
        button_width = self.config.BUTTON_WIDTH
        button_height = self.config.BUTTON_HEIGHT
        button_margin = self.config.BUTTON_MARGIN
        center_x = self.config.SCREEN_WIDTH // 2
        
        # 开始游戏按钮
        self.start_button = Button(
            "开始游戏",
            button_width,
            button_height,
            (center_x, 250),
            self.config.PRIMARY_COLOR,
            self.config.LIGHT_TEXT,
            self.config.NORMAL_FONT_SIZE,
            self.start_game,
            font_dir=self.config.FONTS_DIR
        )
        
        # 成绩档案按钮
        self.records_button = Button(
            "成绩档案",
            button_width,
            button_height,
            (center_x, 250 + button_height + button_margin),
            self.config.PRIMARY_COLOR,
            self.config.LIGHT_TEXT,
            self.config.NORMAL_FONT_SIZE,
            self.show_records,
            font_dir=self.config.FONTS_DIR
        )
        
        # 设置按钮
        self.settings_button = Button(
            "设置",
            button_width,
            button_height,
            (center_x, 250 + 2 * (button_height + button_margin)),
            self.config.PRIMARY_COLOR,
            self.config.LIGHT_TEXT,
            self.config.NORMAL_FONT_SIZE,
            self.show_settings,
            font_dir=self.config.FONTS_DIR
        )
        
        # 退出按钮
        self.exit_button = Button(
            "退出",
            button_width,
            button_height,
            (center_x, 250 + 3 * (button_height + button_margin)),
            self.config.ERROR_COLOR,
            self.config.LIGHT_TEXT,
            self.config.NORMAL_FONT_SIZE,
            self.exit_game,
            font_dir=self.config.FONTS_DIR
        )
    
    def handle_event(self, event):
        """处理事件"""
        self.start_button.handle_event(event)
        self.records_button.handle_event(event)
        self.settings_button.handle_event(event)
        self.exit_button.handle_event(event)
    
    def update(self):
        """更新场景"""
        pass
    
    def render(self, screen):
        """渲染场景"""
        # 渲染标题
        self.title.render(screen)
        
        # 渲染按钮
        self.start_button.render(screen)
        self.records_button.render(screen)
        self.settings_button.render(screen)
        self.exit_button.render(screen)
    
    def start_game(self):
        """开始游戏"""
        self.scene_manager.change_scene(ModeSelectScene(self.scene_manager))
    
    def show_records(self):
        """显示成绩档案"""
        self.scene_manager.change_scene(RecordsScene(self.scene_manager))
    
    def show_settings(self):
        """显示设置"""
        self.scene_manager.change_scene(SettingsScene(self.scene_manager))
    
    def exit_game(self):
        """退出游戏"""
        self.app.running = False

class ModeSelectScene(Scene):
    """模式选择场景"""
    
    def __init__(self, scene_manager):
        """初始化模式选择场景"""
        super().__init__(scene_manager)
        
        # 创建标题文本
        self.title = Text(
            "选择游戏模式",
            self.config.HEADER_FONT_SIZE,
            self.config.PRIMARY_COLOR,
            (self.config.SCREEN_WIDTH // 2, 100)
        )
        
        # 创建按钮
        button_width = self.config.BUTTON_WIDTH
        button_height = self.config.BUTTON_HEIGHT
        button_margin = self.config.BUTTON_MARGIN
        center_x = self.config.SCREEN_WIDTH // 2
        
        # 初级模式按钮
        self.beginner_button = Button(
            "初级模式",
            button_width,
            button_height,
            (center_x, 200),
            self.config.PRIMARY_COLOR,
            self.config.LIGHT_TEXT,
            self.config.NORMAL_FONT_SIZE,
            self.start_beginner_mode
        )
        
        # 中级模式按钮
        self.intermediate_button = Button(
            "中级模式",
            button_width,
            button_height,
            (center_x, 200 + button_height + button_margin),
            self.config.PRIMARY_COLOR,
            self.config.LIGHT_TEXT,
            self.config.NORMAL_FONT_SIZE,
            self.start_intermediate_mode
        )
        
        # 高级模式按钮
        self.advanced_button = Button(
            "高级模式",
            button_width,
            button_height,
            (center_x, 200 + 2 * (button_height + button_margin)),
            self.config.PRIMARY_COLOR,
            self.config.LIGHT_TEXT,
            self.config.NORMAL_FONT_SIZE,
            self.start_advanced_mode
        )
        
        # 大师模式按钮
        self.master_button = Button(
            "大师模式",
            button_width,
            button_height,
            (center_x, 200 + 3 * (button_height + button_margin)),
            self.config.PRIMARY_COLOR,
            self.config.LIGHT_TEXT,
            self.config.NORMAL_FONT_SIZE,
            self.start_master_mode
        )
        
        # 返回按钮
        self.back_button = Button(
            "返回",
            button_width,
            button_height,
            (center_x, 200 + 4 * (button_height + button_margin)),
            self.config.SECONDARY_COLOR,
            self.config.LIGHT_TEXT,
            self.config.NORMAL_FONT_SIZE,
            self.back_to_menu
        )
    
    def handle_event(self, event):
        """处理事件"""
        self.beginner_button.handle_event(event)
        self.intermediate_button.handle_event(event)
        self.advanced_button.handle_event(event)
        self.master_button.handle_event(event)
        self.back_button.handle_event(event)
    
    def update(self):
        """更新场景"""
        pass
    
    def render(self, screen):
        """渲染场景"""
        # 渲染标题
        self.title.render(screen)
        
        # 渲染按钮
        self.beginner_button.render(screen)
        self.intermediate_button.render(screen)
        self.advanced_button.render(screen)
        self.master_button.render(screen)
        self.back_button.render(screen)
    
    def start_beginner_mode(self):
        """开始初级模式"""
        self.scene_manager.change_scene(GameScene(self.scene_manager, "beginner"))
    
    def start_intermediate_mode(self):
        """开始中级模式"""
        self.scene_manager.change_scene(IntermediateLevelSelectScene(self.scene_manager))
    
    def start_advanced_mode(self):
        """开始高级模式"""
        self.scene_manager.change_scene(GameScene(self.scene_manager, "advanced"))
    
    def start_master_mode(self):
        """开始大师模式"""
        self.scene_manager.change_scene(GameScene(self.scene_manager, "master"))
    
    def back_to_menu(self):
        """返回主菜单"""
        self.scene_manager.change_scene(MainMenuScene(self.scene_manager))

class IntermediateLevelSelectScene(Scene):
    """中级模式级别选择场景"""

    def __init__(self, scene_manager):
        """初始化中级模式级别选择场景"""
        super().__init__(scene_manager)

        # 创建标题文本
        self.title = Text(
            "选择训练内容",
            self.config.HEADER_FONT_SIZE,
            self.config.PRIMARY_COLOR,
            (self.config.SCREEN_WIDTH // 2, 100)
        )

        # 创建按钮
        button_width = self.config.BUTTON_WIDTH
        button_height = self.config.BUTTON_HEIGHT
        button_margin = self.config.BUTTON_MARGIN
        center_x = self.config.SCREEN_WIDTH // 2

        # 单词训练按钮
        self.words_button = Button(
            "单词训练",
            button_width,
            button_height,
            (center_x, 200),
            self.config.PRIMARY_COLOR,
            self.config.LIGHT_TEXT,
            self.config.NORMAL_FONT_SIZE,
            lambda: self.start_intermediate_mode(0)
        )

        # 短语训练按钮
        self.phrases_button = Button(
            "短语训练",
            button_width,
            button_height,
            (center_x, 200 + button_height + button_margin),
            self.config.PRIMARY_COLOR,
            self.config.LIGHT_TEXT,
            self.config.NORMAL_FONT_SIZE,
            lambda: self.start_intermediate_mode(1)
        )

        # 句子训练按钮
        self.sentences_button = Button(
            "句子训练",
            button_width,
            button_height,
            (center_x, 200 + 2 * (button_height + button_margin)),
            self.config.PRIMARY_COLOR,
            self.config.LIGHT_TEXT,
            self.config.NORMAL_FONT_SIZE,
            lambda: self.start_intermediate_mode(2)
        )

        # 返回按钮
        self.back_button = Button(
            "返回",
            button_width,
            button_height,
            (center_x, 200 + 3 * (button_height + button_margin)),
            self.config.SECONDARY_COLOR,
            self.config.LIGHT_TEXT,
            self.config.NORMAL_FONT_SIZE,
            self.back_to_mode_select
        )

    def handle_event(self, event):
        """处理事件"""
        self.words_button.handle_event(event)
        self.phrases_button.handle_event(event)
        self.sentences_button.handle_event(event)
        self.back_button.handle_event(event)

    def update(self):
        """更新场景"""
        pass

    def render(self, screen):
        """渲染场景"""
        # 渲染标题
        self.title.render(screen)

        # 渲染按钮
        self.words_button.render(screen)
        self.phrases_button.render(screen)
        self.sentences_button.render(screen)
        self.back_button.render(screen)

    def start_intermediate_mode(self, level):
        """开始中级模式指定级别"""
        game_scene = GameScene(self.scene_manager, "intermediate")
        game_scene.game_mode.level = level
        game_scene.game_mode.load_content()
        game_scene.game_mode.set_next_content()
        self.scene_manager.change_scene(game_scene)

    def back_to_mode_select(self):
        """返回模式选择"""
        self.scene_manager.change_scene(ModeSelectScene(self.scene_manager))

class GameScene(Scene):
    """游戏场景"""

    def __init__(self, scene_manager, mode):
        """初始化游戏场景"""
        super().__init__(scene_manager)
        self.mode = mode

        # 根据模式创建游戏实例
        if mode == "beginner":
            self.game_mode = BeginnerMode(self)
        elif mode == "intermediate":
            self.game_mode = IntermediateMode(self)
        elif mode == "advanced":
            self.game_mode = AdvancedMode(self)
        elif mode == "master":
            self.game_mode = MasterMode(self)

        # 游戏是否暂停
        self.paused = False

        # 初/中级不显示暂停按钮
        if mode not in ("beginner", "intermediate"):
            self.pause_button = Button(
                "暂停",
                100,
                50,
                (self.config.SCREEN_WIDTH - 230, 20),
                self.config.SECONDARY_COLOR,
                self.config.LIGHT_TEXT,
                self.config.SMALL_FONT_SIZE,
                self.toggle_pause
            )
        else:
            self.pause_button = None

        # 创建返回主菜单按钮
        self.exit_button = Button(
            "退出",
            100,
            50,
            (self.config.SCREEN_WIDTH - 120, 20),
            self.config.ERROR_COLOR,
            self.config.LIGHT_TEXT,
            self.config.SMALL_FONT_SIZE,
            self.return_to_menu
        )

        # 启动当前模式，确保键盘渲染与计时开始
        self.game_mode.start()
    
    def handle_event(self, event):
        """处理事件"""
        if not self.paused:
            self.game_mode.handle_event(event)
        else:
            # 暂停状态下仍允许退出按钮事件
            self.exit_button.handle_event(event)
            if self.pause_button:
                self.pause_button.handle_event(event)
            return

        if self.pause_button:
            self.pause_button.handle_event(event)
        self.exit_button.handle_event(event)
    
    def update(self):
        """更新场景"""
        if not self.paused:
            self.game_mode.update()
    
    def render(self, screen):
        """渲染场景"""
        # 渲染游戏
        self.game_mode.render(screen)
        
        # 渲染暂停按钮（仅高级/大师）
        if self.pause_button:
            self.pause_button.render(screen)
        
        # 渲染退出按钮
        self.exit_button.render(screen)
    
    def toggle_pause(self):
        """切换暂停状态"""
        self.paused = not self.paused
        if self.pause_button:
            if self.paused:
                self.pause_button.set_text("继续")
            else:
                self.pause_button.set_text("暂停")
    
    def return_to_menu(self):
        """返回主菜单（放弃游戏，不计分）"""
        # 调用游戏模式的abort_game方法
        self.game_mode.abort_game()
    
    def end_game(self, score, accuracy, stars, is_new_record=False):
        """结束游戏"""
        self.scene_manager.change_scene(
            ResultScene(
                self.scene_manager,
                score,
                accuracy,
                stars,
                is_new_record,
                self.game_mode.get_mode_name(),
                self.mode
            )
        )

class ResultScene(Scene):
    """游戏结果场景"""
    
    def __init__(self, scene_manager, score, accuracy, stars, is_new_record, mode_name, mode_key="beginner"):
        """初始化结果场景"""
        super().__init__(scene_manager)
        
        # 游戏结果数据
        self.score = score
        self.accuracy = accuracy
        self.stars = stars
        self.is_new_record = is_new_record
        self.mode_name = mode_name
        self.mode_key = mode_key
        
        # 创建标题文本
        self.title = Text(
            f"{mode_name} - 游戏结束",
            self.config.HEADER_FONT_SIZE,
            self.config.PRIMARY_COLOR,
            (self.config.SCREEN_WIDTH // 2, 100)
        )
        
        # 创建分数文本
        self.score_text = Text(
            f"得分: {score}",
            self.config.NORMAL_FONT_SIZE,
            self.config.TEXT_COLOR,
            (self.config.SCREEN_WIDTH // 2, 200)
        )
        
        # 创建准确率文本
        self.accuracy_text = Text(
            f"准确率: {accuracy:.1%}",
            self.config.NORMAL_FONT_SIZE,
            self.config.TEXT_COLOR,
            (self.config.SCREEN_WIDTH // 2, 250)
        )
        
        # 创建星级显示
        self.stars_text = Text(
            f"星级评价: {'★' * stars}",
            self.config.HEADER_FONT_SIZE,
            self.config.SECONDARY_COLOR,
            (self.config.SCREEN_WIDTH // 2, 320)
        )
        
        # 创建新纪录文本（如果是新纪录）
        if is_new_record:
            self.new_record_text = Text(
                "恭喜！你创造了新纪录！",
                self.config.NORMAL_FONT_SIZE,
                self.config.SUCCESS_COLOR,
                (self.config.SCREEN_WIDTH // 2, 380)
            )
        
        # 创建鼓励语
        self.encouragement_text = Text(
            self.get_encouragement(),
            self.config.NORMAL_FONT_SIZE,
            self.config.PRIMARY_COLOR,
            (self.config.SCREEN_WIDTH // 2, 450)
        )
        
        # 创建按钮
        button_width = self.config.BUTTON_WIDTH
        button_height = self.config.BUTTON_HEIGHT
        center_x = self.config.SCREEN_WIDTH // 2
        
        # 再玩一次按钮
        self.play_again_button = Button(
            "再玩一次",
            button_width,
            button_height,
            (center_x, 520),
            self.config.PRIMARY_COLOR,
            self.config.LIGHT_TEXT,
            self.config.NORMAL_FONT_SIZE,
            self.play_again
        )
        
        # 返回主菜单按钮
        self.menu_button = Button(
            "返回主菜单",
            button_width,
            button_height,
            (center_x, 520 + button_height + self.config.BUTTON_MARGIN),
            self.config.SECONDARY_COLOR,
            self.config.LIGHT_TEXT,
            self.config.NORMAL_FONT_SIZE,
            self.back_to_menu
        )
    
    def handle_event(self, event):
        """处理事件"""
        self.play_again_button.handle_event(event)
        self.menu_button.handle_event(event)
    
    def update(self):
        """更新场景"""
        pass
    
    def render(self, screen):
        """渲染场景"""
        # 渲染标题
        self.title.render(screen)
        
        # 渲染分数和准确率
        self.score_text.render(screen)
        self.accuracy_text.render(screen)
        
        # 渲染星级
        self.stars_text.render(screen)
        
        # 渲染新纪录文本（如果是新纪录）
        if self.is_new_record:
            self.new_record_text.render(screen)
        
        # 渲染鼓励语
        self.encouragement_text.render(screen)
        
        # 渲染按钮
        self.play_again_button.render(screen)
        self.menu_button.render(screen)
    
    def get_encouragement(self):
        """获取鼓励语"""
        # 根据星级选择不同的鼓励语
        encouragements = [
            [
                "今天也认真练习了，继续加油！",
                "每一次练习都在帮你变熟练！",
                "别着急，你已经在前进了！"
            ],
            [
                "不错哦，再练一会儿会更棒！",
                "你正在进步，继续努力！",
                "很好！坚持练习会越来越好！"
            ],
            [
                "你掌握得越来越稳了！",
                "做得不错，继续保持！",
                "很好！你的手指越来越灵活了！"
            ],
            [
                "真厉害，再试一次可能就是满星！",
                "太棒了！你离打字高手越来越近了！",
                "非常好！你的进步真明显！"
            ],
            [
                "你已经像小小打字高手了！",
                "太棒了！你是打字小天才！",
                "哇！完美表现！你真的很有天赋！"
            ]
        ]

        import random
        star_index = max(0, min(self.stars - 1, 4))
        return random.choice(encouragements[star_index])
    
    def play_again(self):
        """再玩一次"""
        self.scene_manager.change_scene(GameScene(self.scene_manager, self.mode_key))
    
    def back_to_menu(self):
        """返回主菜单"""
        self.scene_manager.change_scene(MainMenuScene(self.scene_manager))

class RecordsScene(Scene):
    """成绩档案场景"""
    
    def __init__(self, scene_manager):
        """初始化成绩档案场景"""
        super().__init__(scene_manager)
        
        # 创建标题文本
        self.title = Text(
            "成绩档案",
            self.config.HEADER_FONT_SIZE,
            self.config.PRIMARY_COLOR,
            (self.config.SCREEN_WIDTH // 2, 50)
        )
        
        # 加载成绩数据
        self.storage_manager = StorageManager(self.config)
        self.records = self.storage_manager.load_data()
        
        # 创建返回按钮
        self.back_button = Button(
            "返回",
            150,
            50,
            (self.config.SCREEN_WIDTH // 2, self.config.SCREEN_HEIGHT - 50),
            self.config.SECONDARY_COLOR,
            self.config.LIGHT_TEXT,
            self.config.NORMAL_FONT_SIZE,
            self.back_to_menu
        )
    
    def handle_event(self, event):
        """处理事件"""
        self.back_button.handle_event(event)
    
    def update(self):
        """更新场景"""
        pass
    
    def render(self, screen):
        """渲染场景"""
        # 渲染标题
        self.title.render(screen)
        
        # 渲染各模式的最佳成绩
        y_pos = 120
        line_height = 40
        
        # 初级模式
        if "beginner" in self.records:
            beginner_data = self.records["beginner"]
            Text(
                f"初级模式 - 最佳分数: {beginner_data.get('best_score', 0)} "
                f"(准确率: {beginner_data.get('best_accuracy', 0):.1%}) "
                f"{'★' * beginner_data.get('stars', 0)}",
                self.config.NORMAL_FONT_SIZE,
                self.config.TEXT_COLOR,
                (self.config.SCREEN_WIDTH // 2, y_pos)
            ).render(screen)
            if "record_holder" in beginner_data:
                Text(
                    f"纪录保持者: {beginner_data['record_holder']}",
                    self.config.SMALL_FONT_SIZE,
                    self.config.TEXT_COLOR,
                    (self.config.SCREEN_WIDTH // 2, y_pos + 25)
                ).render(screen)
            y_pos += line_height + 20
        
        # 中级模式
        if "intermediate" in self.records and "levels" in self.records["intermediate"]:
            intermediate_data = self.records["intermediate"]["levels"]
            
            Text(
                "中级模式:",
                self.config.NORMAL_FONT_SIZE,
                self.config.PRIMARY_COLOR,
                (self.config.SCREEN_WIDTH // 2, y_pos)
            ).render(screen)
            y_pos += line_height
            
            for level, data in intermediate_data.items():
                level_name = {"words": "单词", "phrases": "短语", "sentences": "句子"}.get(level, level)
                Text(
                    f"- {level_name}: 最佳准确率 {data.get('best_accuracy', 0):.1%}, "
                    f"最快时间 {data.get('best_time', 0):.1f}秒, "
                    f"{'★' * data.get('stars', 0)}",
                    self.config.SMALL_FONT_SIZE,
                    self.config.TEXT_COLOR,
                    (self.config.SCREEN_WIDTH // 2, y_pos)
                ).render(screen)
                y_pos += line_height - 10
            
            y_pos += 10
        
        # 高级模式
        if "advanced" in self.records:
            advanced_data = self.records["advanced"]
            Text(
                f"高级模式 - 最高分数: {advanced_data.get('best_score', 0)} "
                f"(准确率: {advanced_data.get('best_accuracy', 0):.1%}, "
                f"最大连击: {advanced_data.get('max_combo', 0)}) "
                f"{'★' * advanced_data.get('stars', 0)}",
                self.config.NORMAL_FONT_SIZE,
                self.config.TEXT_COLOR,
                (self.config.SCREEN_WIDTH // 2, y_pos)
            ).render(screen)
            if "record_holder" in advanced_data:
                Text(
                    f"纪录保持者: {advanced_data['record_holder']}",
                    self.config.SMALL_FONT_SIZE,
                    self.config.TEXT_COLOR,
                    (self.config.SCREEN_WIDTH // 2, y_pos + 25)
                ).render(screen)
            y_pos += line_height + 20
        
        # 大师模式
        if "master" in self.records:
            master_data = self.records["master"]
            Text(
                f"大师模式 - 最高分数: {master_data.get('best_score', 0)} "
                f"(准确率: {master_data.get('best_accuracy', 0):.1%}) "
                f"{'★' * master_data.get('stars', 0)}",
                self.config.NORMAL_FONT_SIZE,
                self.config.TEXT_COLOR,
                (self.config.SCREEN_WIDTH // 2, y_pos)
            ).render(screen)
            if "record_holder" in master_data:
                Text(
                    f"纪录保持者: {master_data['record_holder']}",
                    self.config.SMALL_FONT_SIZE,
                    self.config.TEXT_COLOR,
                    (self.config.SCREEN_WIDTH // 2, y_pos + 25)
                ).render(screen)
        
        # 渲染返回按钮
        self.back_button.render(screen)
    
    def back_to_menu(self):
        """返回主菜单"""
        self.scene_manager.change_scene(MainMenuScene(self.scene_manager))

class SettingsScene(Scene):
    """设置场景"""
    
    def __init__(self, scene_manager):
        """初始化设置场景"""
        super().__init__(scene_manager)
        
        # 创建标题文本
        self.title = Text(
            "设置",
            self.config.HEADER_FONT_SIZE,
            self.config.PRIMARY_COLOR,
            (self.config.SCREEN_WIDTH // 2, 50)
        )
        
        # 音效开关
        self.sound_enabled = True
        
        # 创建音效开关按钮
        self.sound_button = Button(
            "音效: 开",
            200,
            50,
            (self.config.SCREEN_WIDTH // 2, 150),
            self.config.PRIMARY_COLOR,
            self.config.LIGHT_TEXT,
            self.config.NORMAL_FONT_SIZE,
            self.toggle_sound
        )
        
        # 音量控制
        self.volume = self.config.SOUND_VOLUME
        
        # 创建音量文本
        self.volume_text = Text(
            f"音量: {int(self.volume * 100)}%",
            self.config.NORMAL_FONT_SIZE,
            self.config.TEXT_COLOR,
            (self.config.SCREEN_WIDTH // 2, 220)
        )
        
        # 创建音量增加按钮
        self.volume_up_button = Button(
            "+",
            50,
            50,
            (self.config.SCREEN_WIDTH // 2 + 100, 220),
            self.config.PRIMARY_COLOR,
            self.config.LIGHT_TEXT,
            self.config.NORMAL_FONT_SIZE,
            self.increase_volume
        )
        
        # 创建音量减少按钮
        self.volume_down_button = Button(
            "-",
            50,
            50,
            (self.config.SCREEN_WIDTH // 2 - 100, 220),
            self.config.PRIMARY_COLOR,
            self.config.LIGHT_TEXT,
            self.config.NORMAL_FONT_SIZE,
            self.decrease_volume
        )
        
        # 创建返回按钮
        self.back_button = Button(
            "返回",
            150,
            50,
            (self.config.SCREEN_WIDTH // 2, self.config.SCREEN_HEIGHT - 50),
            self.config.SECONDARY_COLOR,
            self.config.LIGHT_TEXT,
            self.config.NORMAL_FONT_SIZE,
            self.back_to_menu
        )
    
    def handle_event(self, event):
        """处理事件"""
        self.sound_button.handle_event(event)
        self.volume_up_button.handle_event(event)
        self.volume_down_button.handle_event(event)
        self.back_button.handle_event(event)
    
    def update(self):
        """更新场景"""
        pass
    
    def render(self, screen):
        """渲染场景"""
        # 渲染标题
        self.title.render(screen)
        
        # 渲染音效开关
        self.sound_button.render(screen)
        
        # 渲染音量控制
        self.volume_text.render(screen)
        self.volume_up_button.render(screen)
        self.volume_down_button.render(screen)
        
        # 渲染返回按钮
        self.back_button.render(screen)
    
    def toggle_sound(self):
        """切换音效开关"""
        self.sound_enabled = not self.sound_enabled
        self.sound_button.set_text(f"音效: {'开' if self.sound_enabled else '关'}")
        self.audio_manager.set_sound_enabled(self.sound_enabled)
    
    def increase_volume(self):
        """增加音量"""
        self.volume = min(1.0, self.volume + 0.1)
        self.volume_text.set_text(f"音量: {int(self.volume * 100)}%")
        self.audio_manager.set_volume(self.volume)
    
    def decrease_volume(self):
        """减少音量"""
        self.volume = max(0.0, self.volume - 0.1)
        self.volume_text.set_text(f"音量: {int(self.volume * 100)}%")
        self.audio_manager.set_volume(self.volume)
    
    def back_to_menu(self):
        """返回主菜单"""
        self.scene_manager.change_scene(MainMenuScene(self.scene_manager))

class SceneManager:
    """场景管理器"""
    
    def __init__(self, app):
        """初始化场景管理器"""
        self.app = app
        self.config = app.config
        
        # 创建音频管理器
        self.app.audio_manager = AudioManager(self.config)
        
        # 初始场景为主菜单
        self.current_scene = MainMenuScene(self)
    
    def change_scene(self, scene):
        """切换场景"""
        self.current_scene = scene
    
    def handle_event(self, event):
        """处理事件"""
        self.current_scene.handle_event(event)
    
    def update(self):
        """更新场景"""
        self.current_scene.update()
    
    def render(self, screen):
        """渲染场景"""
        self.current_scene.render(screen)