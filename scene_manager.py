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
        self.scene_manager.change_scene(AdvancedLevelSelectScene(self.scene_manager))
    
    def start_master_mode(self):
        """开始大师模式（纯汉字输入，无虚拟键盘提示）"""
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
        level_keys = ["words", "phrases", "sentences"]
        mode_key = f"intermediate_{level_keys[level]}"
        game_scene = GameScene(self.scene_manager, mode_key)
        game_scene.game_mode.load_content()
        game_scene.game_mode.set_next_content()
        self.scene_manager.change_scene(game_scene)

    def back_to_mode_select(self):
        """返回模式选择"""
        self.scene_manager.change_scene(ModeSelectScene(self.scene_manager))

class AdvancedLevelSelectScene(Scene):
    """高级模式级别选择场景"""

    def __init__(self, scene_manager):
        """初始化高级模式级别选择场景"""
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

        # 高级字母训练按钮（原高级模式）
        self.letters_button = Button(
            "高级字母",
            button_width,
            button_height,
            (center_x, 200),
            self.config.PRIMARY_COLOR,
            self.config.LIGHT_TEXT,
            self.config.NORMAL_FONT_SIZE,
            self.start_advanced_letters
        )

        # 高级拼音训练按钮（原大师模式，但保留键盘提示）
        self.pinyin_button = Button(
            "高级拼音",
            button_width,
            button_height,
            (center_x, 200 + button_height + button_margin),
            self.config.PRIMARY_COLOR,
            self.config.LIGHT_TEXT,
            self.config.NORMAL_FONT_SIZE,
            self.start_advanced_pinyin
        )

        # 返回按钮
        self.back_button = Button(
            "返回",
            button_width,
            button_height,
            (center_x, 200 + 2 * (button_height + button_margin)),
            self.config.SECONDARY_COLOR,
            self.config.LIGHT_TEXT,
            self.config.NORMAL_FONT_SIZE,
            self.back_to_mode_select
        )

    def handle_event(self, event):
        """处理事件"""
        self.letters_button.handle_event(event)
        self.pinyin_button.handle_event(event)
        self.back_button.handle_event(event)

    def update(self):
        """更新场景"""
        pass

    def render(self, screen):
        """渲染场景"""
        # 渲染标题
        self.title.render(screen)

        # 渲染按钮
        self.letters_button.render(screen)
        self.pinyin_button.render(screen)
        self.back_button.render(screen)

    def start_advanced_letters(self):
        """开始高级字母模式（原高级模式）"""
        self.scene_manager.change_scene(GameScene(self.scene_manager, "advanced"))

    def start_advanced_pinyin(self):
        """开始高级拼音模式（原大师模式，保留键盘提示）"""
        # 使用统一的模式标识
        self.scene_manager.change_scene(GameScene(self.scene_manager, "advanced_pinyin"))

    def back_to_mode_select(self):
        """返回模式选择"""
        self.scene_manager.change_scene(ModeSelectScene(self.scene_manager))

class GameScene(Scene):
    """游戏场景"""

    def __init__(self, scene_manager, mode):
        """初始化游戏场景"""
        super().__init__(scene_manager)
        
        # 处理可能的复合模式键（如 intermediate_words）
        self.mode = mode
        self.level_key = None
        
        actual_mode = mode
        if mode.startswith("intermediate_"):
            actual_mode = "intermediate"
            self.level_key = mode.replace("intermediate_", "")
        
        # 根据模式创建游戏实例（按需导入，避免循环导入）
        if actual_mode == "beginner":
            from game_modes.beginner_mode import BeginnerMode
            self.game_mode = BeginnerMode(self)
        elif actual_mode == "intermediate":
            from game_modes.intermediate_mode import IntermediateMode
            self.game_mode = IntermediateMode(self)
            if self.level_key:
                # 转换 key 为 index
                level_map = {"words": 0, "phrases": 1, "sentences": 2}
                self.game_mode.level = level_map.get(self.level_key, 0)
        elif actual_mode == "advanced":
            from game_modes.advanced_mode import AdvancedMode
            self.game_mode = AdvancedMode(self)
        elif actual_mode == "master":
            from game_modes.master_mode import MasterMode
            self.game_mode = MasterMode(self)
            self.game_mode.set_variant("master")
        elif actual_mode == "advanced_pinyin":
            from game_modes.master_mode import MasterMode
            self.game_mode = MasterMode(self)
            self.game_mode.set_variant("advanced_pinyin")

        # 游戏是否暂停
        self.paused = False

        # 初/中级不显示暂停按钮
        if actual_mode not in ("beginner", "intermediate"):
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
        
        # 用户名输入状态
        self.waiting_for_username = is_new_record
        self.username_input = ""
        self.input_active = True
        self.username_submitted = False
        self.storage_manager = StorageManager(self.config)
        self._toggle_text_input(self.waiting_for_username)
        
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
        
        # 创建鼓励语（仅在非输入状态显示）
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
        
        # 再玩一次按钮（初始隐藏，输入完成后显示）
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
        
        # 确认按钮（用于用户名输入）
        self.confirm_button = Button(
            "确认",
            button_width,
            button_height,
            (center_x, 520),
            self.config.SUCCESS_COLOR,
            self.config.LIGHT_TEXT,
            self.config.NORMAL_FONT_SIZE,
            self.confirm_username
        )
    
    def _toggle_text_input(self, enabled):
        """开启或关闭系统文本输入"""
        if not hasattr(pygame.key, "start_text_input"):
            return
        try:
            if enabled:
                pygame.key.start_text_input()
            else:
                pygame.key.stop_text_input()
        except pygame.error:
            pass

    def _append_username_text(self, text):
        """向用户名输入框追加合法字符"""
        if not text:
            return
        for char in text:
            if len(self.username_input) >= 10:
                break
            if char.isalnum() or '\u4e00' <= char <= '\u9fff':
                self.username_input += char

    def handle_event(self, event):
        """处理事件"""
        if self.waiting_for_username:
            if event.type == pygame.TEXTINPUT:
                self._append_username_text(event.text)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.confirm_username()
                elif event.key == pygame.K_BACKSPACE:
                    self.username_input = self.username_input[:-1]
                elif event.key == pygame.K_ESCAPE:
                    self.skip_username()
            elif event.type == pygame.MOUSEBUTTONDOWN and self.username_input:
                self.confirm_button.handle_event(event)
        else:
            self.play_again_button.handle_event(event)
            self.menu_button.handle_event(event)
    
    def update(self):
        """更新场景"""
        pass
    
    def render(self, screen):
        """渲染场景"""
        self.title.render(screen)
        self.score_text.render(screen)
        self.accuracy_text.render(screen)
        self.stars_text.render(screen)
        
        if self.is_new_record:
            self.new_record_text.render(screen)
        
        if self.waiting_for_username:
            self._render_username_input(screen)
        else:
            self.encouragement_text.render(screen)
            self.play_again_button.render(screen)
            self.menu_button.render(screen)
    
    def _render_username_input(self, screen):
        """渲染用户名输入界面"""
        import pygame
        
        hint_font = load_font(24, font_dir=self.config.FONTS_DIR)
        hint_text = "请输入您的名字（按Enter确认，ESC跳过）："
        hint_surface = hint_font.render(hint_text, True, self.config.TEXT_COLOR)
        hint_rect = hint_surface.get_rect(center=(self.config.SCREEN_WIDTH // 2, 430))
        screen.blit(hint_surface, hint_rect)
        
        input_rect = pygame.Rect(
            self.config.SCREEN_WIDTH // 2 - 150,
            460,
            300,
            40
        )
        pygame.draw.rect(screen, (50, 55, 65), input_rect, border_radius=8)
        pygame.draw.rect(screen, self.config.PRIMARY_COLOR, input_rect, 2, border_radius=8)
        
        input_font = load_font(28, font_dir=self.config.FONTS_DIR)
        input_surface = input_font.render(self.username_input, True, self.config.TEXT_COLOR)
        screen.blit(input_surface, (input_rect.x + 10, input_rect.y + 8))
        
        if pygame.time.get_ticks() % 1000 < 500:
            cursor_x = input_rect.x + 10 + input_font.size(self.username_input)[0]
            pygame.draw.line(
                screen,
                self.config.PRIMARY_COLOR,
                (cursor_x, input_rect.y + 8),
                (cursor_x, input_rect.y + 32),
                2
            )
        
        if self.username_input:
            self.confirm_button.render(screen)
        
        skip_text = "按 ESC 跳过"
        skip_surface = hint_font.render(skip_text, True, self.config.TEXT_MUTED)
        skip_rect = skip_surface.get_rect(center=(self.config.SCREEN_WIDTH // 2, 600))
        screen.blit(skip_surface, skip_rect)
    
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
        self._toggle_text_input(False)
        self.scene_manager.change_scene(GameScene(self.scene_manager, self.mode_key))
    
    def back_to_menu(self):
        """返回主菜单"""
        self._toggle_text_input(False)
        self.scene_manager.change_scene(MainMenuScene(self.scene_manager))
    
    def confirm_username(self):
        """确认用户名"""
        if self.username_submitted:
            return
        
        username = self.username_input.strip()
        if not username:
            return
        
        self.username_submitted = True
        self._toggle_text_input(False)
        
        # 更新排行榜
        self.storage_manager.update_leaderboard(
            self.mode_key,
            username,
            self.score
        )
        
        # 更新玩家名称
        self.storage_manager.set_player_name(username)
        
        # 结束输入状态
        self.waiting_for_username = False
    
    def skip_username(self):
        """跳过用户名输入"""
        if self.username_submitted:
            return
        
        self.username_submitted = True
        self._toggle_text_input(False)
        
        # 使用默认名称更新排行榜
        self.storage_manager.update_leaderboard(
            self.mode_key,
            "匿名玩家",
            self.score
        )
        
        # 结束输入状态
        self.waiting_for_username = False

class RecordsScene(Scene):
    """成绩档案场景 - 分模式排行榜"""
    
    # 模式名称映射
    MODE_NAMES = {
        'beginner': '初级模式',
        'advanced': '高级字母',
        'advanced_pinyin': '高级拼音',
        'master': '大师模式',
        'intermediate_words': '中级-单词',
        'intermediate_phrases': '中级-短语',
        'intermediate_sentences': '中级-句子'
    }
    
    # 模式显示顺序
    MODE_ORDER = ['beginner', 'intermediate_words', 'intermediate_phrases', 'intermediate_sentences', 
                  'advanced', 'advanced_pinyin', 'master']
    
    def __init__(self, scene_manager):
        """初始化成绩档案场景"""
        super().__init__(scene_manager)
        
        # 创建标题文本
        self.title = Text(
            "排行榜",
            self.config.HEADER_FONT_SIZE,
            self.config.PRIMARY_COLOR,
            (self.config.SCREEN_WIDTH // 2, 40)
        )
        
        # 加载成绩数据
        self.storage_manager = StorageManager(self.config)
        self.all_data = self.storage_manager.load_data()
        
        # 当前选中的模式标签
        self.current_mode_index = 0
        
        # 标签按钮区域
        self.tab_buttons = []
        self._create_tab_buttons()
        
        # 创建返回按钮
        self.back_button = Button(
            "返回",
            150,
            50,
            (self.config.SCREEN_WIDTH // 2, self.config.SCREEN_HEIGHT - 40),
            self.config.SECONDARY_COLOR,
            self.config.LIGHT_TEXT,
            self.config.NORMAL_FONT_SIZE,
            self.back_to_menu
        )
        
        # 左右切换按钮
        self.prev_button = Button(
            "<",
            50,
            40,
            (80, 40),
            self.config.SECONDARY_COLOR,
            self.config.LIGHT_TEXT,
            self.config.NORMAL_FONT_SIZE,
            self.prev_mode
        )
        self.next_button = Button(
            ">",
            50,
            40,
            (self.config.SCREEN_WIDTH - 80, 40),
            self.config.SECONDARY_COLOR,
            self.config.LIGHT_TEXT,
            self.config.NORMAL_FONT_SIZE,
            self.next_mode
        )
    
    def _create_tab_buttons(self):
        """创建模式标签按钮"""
        self.tab_buttons = []
        start_x = 140
        tab_width = 100
        tab_gap = 10
        
        for i, mode_key in enumerate(self.MODE_ORDER):
            mode_name = self.MODE_NAMES.get(mode_key, mode_key)
            btn = Button(
                mode_name,
                tab_width,
                35,
                (start_x + i * (tab_width + tab_gap), 85),
                self.config.PRIMARY_COLOR if i == self.current_mode_index else self.config.SECONDARY_COLOR,
                self.config.LIGHT_TEXT,
                self.config.SMALL_FONT_SIZE,
                lambda idx=i: self.select_mode(idx)
            )
            self.tab_buttons.append(btn)
    
    def select_mode(self, index):
        """选择模式"""
        self.current_mode_index = index
        self._create_tab_buttons()  # 重建按钮以更新高亮
    
    def prev_mode(self):
        """上一个模式"""
        self.current_mode_index = (self.current_mode_index - 1) % len(self.MODE_ORDER)
        self._create_tab_buttons()
    
    def next_mode(self):
        """下一个模式"""
        self.current_mode_index = (self.current_mode_index + 1) % len(self.MODE_ORDER)
        self._create_tab_buttons()
    
    def handle_event(self, event):
        """处理事件"""
        self.back_button.handle_event(event)
        self.prev_button.handle_event(event)
        self.next_button.handle_event(event)
        for btn in self.tab_buttons:
            btn.handle_event(event)
    
    def update(self):
        """更新场景"""
        pass
    
    def render(self, screen):
        """渲染场景"""
        # 渲染标题
        self.title.render(screen)
        
        # 渲染左右切换按钮
        self.prev_button.render(screen)
        self.next_button.render(screen)
        
        # 渲染标签按钮
        for btn in self.tab_buttons:
            btn.render(screen)
        
        # 获取当前模式的排行榜数据
        current_mode = self.MODE_ORDER[self.current_mode_index]
        leaderboard = self._get_leaderboard(current_mode)
        
        # 渲染排行榜标题
        mode_name = self.MODE_NAMES.get(current_mode, current_mode)
        title_font = load_font(28, font_dir=self.config.FONTS_DIR)
        title_surface = title_font.render(f"{mode_name} 排行榜", True, self.config.PRIMARY_COLOR)
        title_rect = title_surface.get_rect(center=(self.config.SCREEN_WIDTH // 2, 145))
        screen.blit(title_surface, title_rect)
        
        # 渲染排行榜列表
        if leaderboard:
            self._render_leaderboard(screen, leaderboard)
        else:
            self._render_empty_leaderboard(screen)
        
        # 渲染返回按钮
        self.back_button.render(screen)
    
    def _get_leaderboard(self, mode_key):
        """获取指定模式的排行榜"""
        # 处理中级模式的子级别
        if mode_key.startswith('intermediate_'):
            level = mode_key.replace('intermediate_', '')
            return self.storage_manager.get_leaderboard('intermediate', level)
        else:
            return self.storage_manager.get_leaderboard(mode_key)
    
    def _render_leaderboard(self, screen, leaderboard):
        """渲染排行榜列表"""
        entry_font = load_font(22, font_dir=self.config.FONTS_DIR)
        rank_font = load_font(24, font_dir=self.config.FONTS_DIR)
        
        # 表头
        header_y = 180
        headers = ["排名", "用户名", "分数", "时间"]
        header_x_positions = [self.config.SCREEN_WIDTH // 2 - 200, 
                              self.config.SCREEN_WIDTH // 2 - 80,
                              self.config.SCREEN_WIDTH // 2 + 40,
                              self.config.SCREEN_WIDTH // 2 + 150]
        
        for i, header in enumerate(headers):
            header_surface = entry_font.render(header, True, self.config.TEXT_SECONDARY)
            header_rect = header_surface.get_rect(center=(header_x_positions[i], header_y))
            screen.blit(header_surface, header_rect)
        
        # 分隔线
        pygame.draw.line(
            screen,
            self.config.PRIMARY_COLOR,
            (self.config.SCREEN_WIDTH // 2 - 250, header_y + 20),
            (self.config.SCREEN_WIDTH // 2 + 250, header_y + 20),
            2
        )
        
        # 排行榜条目
        for i, entry in enumerate(leaderboard[:10]):  # 最多显示10条
            rank = i + 1
            y_pos = header_y + 45 + i * 35
            
            # 排名（前三名特殊颜色）
            rank_color = self.config.TEXT_COLOR
            if rank == 1:
                rank_color = (255, 215, 0)  # 金色
            elif rank == 2:
                rank_color = (192, 192, 192)  # 银色
            elif rank == 3:
                rank_color = (205, 127, 50)  # 铜色
            
            rank_text = f"#{rank}"
            rank_surface = rank_font.render(rank_text, True, rank_color)
            rank_rect = rank_surface.get_rect(center=(header_x_positions[0], y_pos))
            screen.blit(rank_surface, rank_rect)
            
            # 用户名
            username = entry.get('username', '匿名')
            username_surface = entry_font.render(username, True, self.config.TEXT_COLOR)
            username_rect = username_surface.get_rect(center=(header_x_positions[1], y_pos))
            screen.blit(username_surface, username_rect)
            
            # 分数
            score = entry.get('score', 0)
            score_surface = entry_font.render(str(score), True, self.config.TEXT_COLOR)
            score_rect = score_surface.get_rect(center=(header_x_positions[2], y_pos))
            screen.blit(score_surface, score_rect)
            
            # 时间
            date = entry.get('date', '')
            # 只显示日期部分
            if len(date) > 10:
                date = date[:10]
            date_surface = entry_font.render(date, True, self.config.TEXT_MUTED)
            date_rect = date_surface.get_rect(center=(header_x_positions[3], y_pos))
            screen.blit(date_surface, date_rect)
    
    def _render_empty_leaderboard(self, screen):
        """渲染空排行榜提示"""
        empty_font = load_font(24, font_dir=self.config.FONTS_DIR)
        empty_text = "暂无记录，快来创造第一个记录吧！"
        empty_surface = empty_font.render(empty_text, True, self.config.TEXT_MUTED)
        empty_rect = empty_surface.get_rect(center=(self.config.SCREEN_WIDTH // 2, 300))
        screen.blit(empty_surface, empty_rect)
    
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
    
    def create_main_menu_scene(self):
        """创建主菜单场景"""
        return MainMenuScene(self)
    
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