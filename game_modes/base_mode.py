#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
游戏模式基类，提供所有游戏模式通用的功能
"""

import pygame
import time
import random
from keyboard.keyboard_renderer import KeyboardRenderer
from data.storage import StorageManager
from font_loader import load_font

class BaseMode:
    """游戏模式基类"""
    
    def __init__(self, scene):
        """
        初始化游戏模式
        
        参数:
        - scene: 游戏场景
        """
        self.scene = scene
        self.app = scene.app
        self.config = self.app.config
        self.audio_manager = self.app.audio_manager
        
        # 创建键盘渲染器
        self.keyboard_renderer = KeyboardRenderer(self.config)
        
        # 创建存储管理器
        self.storage_manager = StorageManager(self.config)
        
        # 游戏状态
        self.running = False
        self.start_time = 0
        self.end_time = 0
        
        # 游戏数据
        self.score = 0
        self.accuracy = 0.0
        self.correct_count = 0
        self.total_count = 0
        
        # 鼓励语列表
        self.encouragements = [
            "太棒了！",
            "做得好！",
            "真不错！",
            "继续保持！",
            "你真厉害！",
            "好样的！",
            "非常好！",
            "哇！好快！",
            "真准！",
            "你在进步！"
        ]
    
    def start(self):
        """开始游戏"""
        self.running = True
        self.start_time = time.time()
        self.reset_game_data()
    
    def reset_game_data(self):
        """重置游戏数据"""
        self.score = 0
        self.accuracy = 0.0
        self.correct_count = 0
        self.total_count = 0
    
    def update(self):
        """更新游戏状态"""
        if not self.running:
            return
        
        # 计算游戏时间
        current_time = time.time()
        self.game_time = current_time - self.start_time
    
    def render(self, screen):
        """渲染游戏画面"""
        if not self.running:
            return
        
        # 渲染键盘
        self.keyboard_renderer.render(screen)
        
        # 渲染游戏信息
        self.render_game_info(screen)
    
    def render_game_info(self, screen):
        """渲染游戏信息"""
        font = load_font(20, font_dir=self.config.FONTS_DIR)

        # 顶部功能区均匀排列
        y = 10
        items = [
            ("分数", f"分数: {self.score}"),
            ("准确率", f"准确率: {self.accuracy:.1%}"),
            ("时间", f"时间: {int(self.game_time)}秒")
        ]
        spacing = self.config.SCREEN_WIDTH // (len(items) + 1)
        for i, (_, text) in enumerate(items, start=1):
            surface = font.render(text, True, self.config.TEXT_COLOR)
            rect = surface.get_rect(center=(spacing * i, y + surface.get_height() // 2))
            screen.blit(surface, rect)
    
    def handle_event(self, event):
        """处理游戏事件"""
        if not self.running:
            return
        
        # 处理键盘事件
        if event.type == pygame.KEYDOWN:
            # ESC/End键：放弃游戏并返回主菜单（不计分）
            if event.key in (pygame.K_ESCAPE, pygame.K_END):
                self.abort_game()
            else:
                self.handle_key_down(event.key)
    
    def handle_key_down(self, key):
        """处理键盘按下事件"""
        pass
    
    def calculate_score(self):
        """计算得分"""
        pass
    
    def calculate_accuracy(self):
        """计算准确率"""
        if self.total_count > 0:
            self.accuracy = self.correct_count / self.total_count
        else:
            self.accuracy = 0.0
    
    def calculate_stars(self):
        """计算星级评价"""
        # 根据分数计算星级
        score_percentage = self.score / self.get_max_score()
        
        # 使用配置中的星级阈值
        for i, threshold in enumerate(self.config.STAR_THRESHOLDS):
            if score_percentage * 100 < threshold:
                return i
        
        return len(self.config.STAR_THRESHOLDS) - 1
    
    def get_max_score(self):
        """获取最大可能分数"""
        return 100
    
    def get_encouragement(self):
        """获取随机鼓励语"""
        return random.choice(self.encouragements)
    
    def play_encouragement(self):
        """播放鼓励音效"""
        self.audio_manager.play_sound("encouragement")
    
    def play_correct_sound(self):
        """播放正确音效"""
        self.audio_manager.play_sound("correct")
    
    def play_error_sound(self):
        """播放错误音效"""
        self.audio_manager.play_sound("error")
    
    def end_game(self):
        """结束游戏"""
        if not self.running:
            return
        
        self.running = False
        self.end_time = time.time()
        
        # 计算最终数据
        self.calculate_accuracy()
        self.calculate_score()
        stars = self.calculate_stars()
        
        # 检查是否创造新纪录
        is_new_record = self.check_new_record()
        
        # 保存成绩
        self.save_record()
        
        # 播放结束音效
        self.audio_manager.play_sound("game_over")
        
        # 跳转到结果场景
        self.scene.end_game(self.score, self.accuracy, stars, is_new_record)
    
    def abort_game(self):
        """放弃游戏（不计分）"""
        if not self.running:
            return
        
        self.running = False
        
        # 不保存成绩，不播放结束音效，直接返回主菜单
        # 返回主菜单
        from scene_manager import MainMenuScene
        self.scene.scene_manager.change_scene(MainMenuScene(self.scene.scene_manager))
    
    def check_new_record(self):
        """检查是否创造新纪录"""
        # 加载现有记录
        data = self.storage_manager.load_data()
        
        # 获取当前模式的记录
        mode_name = self.get_mode_name().lower()
        if mode_name not in data:
            return True
        
        # 检查分数是否高于现有记录
        if self.score > data[mode_name].get("best_score", 0):
            return True
        
        return False
    
    def save_record(self):
        """保存成绩记录"""
        # 加载现有数据
        data = self.storage_manager.load_data()
        
        # 获取当前模式名称
        mode_name = self.get_mode_name().lower()
        
        # 如果当前模式没有记录，创建新记录
        if mode_name not in data:
            data[mode_name] = {
                "best_score": self.score,
                "best_accuracy": self.accuracy,
                "stars": self.calculate_stars(),
                "record_holder": "玩家",
                "total_sessions": 1,
                "recent_results": []
            }
        else:
            # 更新记录
            mode_data = data[mode_name]
            
            # 更新最佳分数和准确率
            if self.score > mode_data.get("best_score", 0):
                mode_data["best_score"] = self.score
                mode_data["best_accuracy"] = self.accuracy
                mode_data["stars"] = self.calculate_stars()
                mode_data["record_holder"] = "玩家"
            
            # 更新总游戏次数
            mode_data["total_sessions"] = mode_data.get("total_sessions", 0) + 1
            
            # 添加最近结果
            if "recent_results" not in mode_data:
                mode_data["recent_results"] = []
            
            # 添加当前结果
            mode_data["recent_results"].append({
                "score": self.score,
                "accuracy": self.accuracy,
                "stars": self.calculate_stars(),
                "date": time.strftime("%Y-%m-%d %H:%M:%S")
            })
            
            # 只保留最近10条记录
            if len(mode_data["recent_results"]) > 10:
                mode_data["recent_results"] = mode_data["recent_results"][-10:]
        
        # 保存数据
        self.storage_manager.save_data(data)
    
    def get_mode_name(self):
        """获取游戏模式名称"""
        return "基础模式"