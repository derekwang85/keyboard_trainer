#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
文本渲染组件
"""

import pygame
from font_loader import load_font

class Text:
    """文本渲染类"""
    
    def __init__(self, text, font_size, color, pos, font_name=None, align="center", font_dir=None):
        """
        初始化文本
        
        参数:
        - text: 要显示的文本
        - font_size: 字体大小
        - color: 文本颜色
        - pos: 文本位置 (x, y)
        - font_name: 字体名称，默认为None（使用系统默认字体）
        - align: 文本对齐方式，可选值："center", "left", "right"
        - font_dir: 字体目录
        """
        self.text = text
        self.font_size = font_size
        self.color = color
        self.pos = pos
        self.font_name = font_name
        self.align = align
        self.font_dir = font_dir
        
        # 加载字体
        self.load_font()
        
        # 渲染文本
        self.render_text()
    
    def load_font(self):
        """加载字体"""
        # 使用统一的字体加载器
        self.font = load_font(self.font_size, font_dir=self.font_dir)
    
    def render_text(self):
        """渲染文本"""
        self.text_surface = self.font.render(self.text, True, self.color)
        
        # 根据对齐方式设置文本矩形
        if self.align == "center":
            self.text_rect = self.text_surface.get_rect(center=self.pos)
        elif self.align == "left":
            self.text_rect = self.text_surface.get_rect(topleft=self.pos)
        elif self.align == "right":
            self.text_rect = self.text_surface.get_rect(topright=self.pos)
    
    def set_text(self, text):
        """设置文本内容"""
        self.text = text
        self.render_text()
    
    def set_color(self, color):
        """设置文本颜色"""
        self.color = color
        self.render_text()
    
    def render(self, screen):
        """渲染文本到屏幕"""
        screen.blit(self.text_surface, self.text_rect)