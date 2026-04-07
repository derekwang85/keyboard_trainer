#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
儿童键盘练习小游戏主程序入口
"""

import pygame
import sys
from scene_manager import SceneManager
from config import Config
from font_loader import log_font_diagnosis

class GameApp:
    """游戏主应用类"""
    
    def __init__(self):
        """初始化游戏"""
        # 初始化pygame
        pygame.init()
        pygame.font.init()
        pygame.mixer.init()
        
        # 设置窗口标题
        pygame.display.set_caption("儿童键盘练习小游戏")
        
        # 创建配置实例
        self.config = Config()
        
        # 输出字体诊断信息（帮助调试字体问题）
        log_font_diagnosis()
        
        # 设置窗口大小和显示模式
        self.screen = pygame.display.set_mode(
            (self.config.SCREEN_WIDTH, self.config.SCREEN_HEIGHT)
        )
        
        # 创建时钟对象，用于控制游戏帧率
        self.clock = pygame.time.Clock()
        
        # 创建场景管理器
        self.scene_manager = SceneManager(self)
        
        # 游戏是否运行
        self.running = True
    
    def handle_events(self):
        """处理游戏事件"""
        for event in pygame.event.get():
            # 退出游戏
            if event.type == pygame.QUIT:
                self.running = False
            
            # 将事件传递给场景管理器
            self.scene_manager.handle_event(event)
    
    def update(self):
        """更新游戏状态"""
        self.scene_manager.update()
    
    def render(self):
        """渲染游戏画面"""
        # 填充背景色
        self.screen.fill(self.config.BACKGROUND_COLOR)
        
        # 渲染当前场景
        self.scene_manager.render(self.screen)
        
        # 更新屏幕显示
        pygame.display.flip()
    
    def run(self):
        """运行游戏主循环"""
        while self.running:
            # 处理事件
            self.handle_events()
            
            # 更新游戏状态
            self.update()
            
            # 渲染游戏画面
            self.render()
            
            # 控制帧率
            self.clock.tick(self.config.FPS)
        
        # 退出游戏
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    # 创建游戏实例并运行
    game = GameApp()
    game.run()