#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
爆炸效果，用于大师模式中击中汉字时的特效
"""

import pygame
import random
import math

class ExplosionEffect:
    """爆炸效果类"""
    
    def __init__(self, x, y, color, config):
        """
        初始化爆炸效果
        
        参数:
        - x: 爆炸中心x坐标
        - y: 爆炸中心y坐标
        - color: 爆炸颜色
        - config: 游戏配置
        """
        self.x = x
        self.y = y
        self.color = color
        self.config = config
        
        # 爆炸波纹
        self.ripples = []
        self.create_ripples()
        
        # 爆炸粒子
        self.particles = []
        self.create_particles()
        
        # 效果持续时间
        self.duration = 30
        self.max_duration = self.duration
        
        # 效果是否完成
        self.finished = False
    
    def create_ripples(self):
        """创建爆炸波纹"""
        for i in range(3):
            ripple = {
                'radius': 10 + i * 10,
                'max_radius': 50 + i * 20,
                'width': 3 - i,
                'alpha': 255
            }
            self.ripples.append(ripple)
    
    def create_particles(self):
        """创建爆炸粒子"""
        # 创建汉字碎片粒子
        for _ in range(20):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 6)
            
            particle = {
                'x': self.x,
                'y': self.y,
                'vx': math.cos(angle) * speed,
                'vy': math.sin(angle) * speed,
                'size': random.randint(4, 10),
                'color': self.color,
                'life': random.randint(20, 40),
                'max_life': random.randint(20, 40),
                'alpha': 255,
                'rotation': random.uniform(0, 2 * math.pi),
                'rotation_speed': random.uniform(-0.1, 0.1)
            }
            self.particles.append(particle)
        
        # 创建火花粒子
        for _ in range(30):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(4, 8)
            
            # 使用更亮的颜色
            particle_color = (
                min(255, self.color[0] + 50),
                min(255, self.color[1] + 50),
                min(255, self.color[2] + 50)
            )
            
            particle = {
                'x': self.x,
                'y': self.y,
                'vx': math.cos(angle) * speed,
                'vy': math.sin(angle) * speed,
                'size': random.randint(2, 4),
                'color': particle_color,
                'life': random.randint(15, 30),
                'max_life': random.randint(15, 30),
                'alpha': 255
            }
            self.particles.append(particle)
    
    def update(self):
        """更新爆炸效果"""
        # 更新持续时间
        self.duration -= 1
        
        # 更新波纹
        for ripple in self.ripples:
            # 扩大波纹
            ripple['radius'] += 2
            
            # 更新透明度
            progress = ripple['radius'] / ripple['max_radius']
            ripple['alpha'] = int(255 * (1 - progress))
        
        # 更新粒子
        for particle in self.particles[:]:
            # 更新位置
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            
            # 减速
            particle['vx'] *= 0.95
            particle['vy'] *= 0.95
            
            # 增加重力效果
            particle['vy'] += 0.2
            
            # 更新生命周期
            particle['life'] -= 1
            
            # 更新透明度
            particle['alpha'] = int(255 * (particle['life'] / particle['max_life']))
            
            # 更新旋转
            if 'rotation' in particle and 'rotation_speed' in particle:
                particle['rotation'] += particle['rotation_speed']
            
            # 移除死亡的粒子
            if particle['life'] <= 0:
                self.particles.remove(particle)
        
        # 检查效果是否完成
        if self.duration <= 0 and len(self.particles) == 0:
            self.finished = True
    
    def render(self, screen):
        """渲染爆炸效果"""
        # 渲染波纹
        for ripple in self.ripples:
            if ripple['alpha'] > 0:
                # 创建临时表面
                surface = pygame.Surface(
                    (ripple['radius'] * 2, ripple['radius'] * 2),
                    pygame.SRCALPHA
                )
                
                # 绘制波纹
                pygame.draw.circle(
                    surface,
                    (*self.color, ripple['alpha']),
                    (ripple['radius'], ripple['radius']),
                    ripple['radius'],
                    ripple['width']
                )
                
                # 绘制到屏幕
                screen.blit(
                    surface,
                    (
                        self.x - ripple['radius'],
                        self.y - ripple['radius']
                    )
                )
        
        # 渲染粒子
        for particle in self.particles:
            if particle['alpha'] > 0:
                # 创建临时表面
                size = particle['size'] * 2
                surface = pygame.Surface((size, size), pygame.SRCALPHA)
                
                # 绘制粒子
                if 'rotation' in particle and 'rotation_speed' in particle:
                    # 绘制旋转的矩形
                    rect = pygame.Rect(0, 0, size, size)
                    pygame.draw.rect(
                        surface,
                        (*particle['color'], particle['alpha']),
                        rect
                    )
                    
                    # 旋转表面
                    rotated_surface = pygame.transform.rotate(
                        surface,
                        math.degrees(particle['rotation'])
                    )
                    
                    # 绘制到屏幕
                    screen.blit(
                        rotated_surface,
                        (
                            particle['x'] - rotated_surface.get_width() / 2,
                            particle['y'] - rotated_surface.get_height() / 2
                        )
                    )
                else:
                    # 绘制圆形粒子
                    pygame.draw.circle(
                        surface,
                        (*particle['color'], particle['alpha']),
                        (particle['size'], particle['size']),
                        particle['size']
                    )
                    
                    # 绘制到屏幕
                    screen.blit(
                        surface,
                        (
                            particle['x'] - particle['size'],
                            particle['y'] - particle['size']
                        )
                    )