#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
粒子系统，用于实现各种粒子效果
"""

import pygame
import random
import math

class Particle:
    """粒子类"""
    
    def __init__(self, x, y, color, config):
        """
        初始化粒子
        
        参数:
        - x: x坐标
        - y: y坐标
        - color: 粒子颜色
        - config: 游戏配置
        """
        self.x = x
        self.y = y
        self.color = color
        self.config = config
        
        # 粒子大小
        self.size = random.randint(2, 6)
        
        # 粒子速度和方向
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(1, 5)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        
        # 粒子生命周期
        self.life = random.randint(10, 30)
        self.max_life = self.life
        
        # 透明度
        self.alpha = 255
    
    def update(self):
        """更新粒子状态"""
        # 更新位置
        self.x += self.vx
        self.y += self.vy
        
        # 减速
        self.vx *= 0.98
        self.vy *= 0.98
        
        # 增加重力效果
        self.vy += 0.2
        
        # 更新生命周期
        self.life -= 1
        
        # 更新透明度
        self.alpha = int(255 * (self.life / self.max_life))
    
    def render(self, screen):
        """渲染粒子"""
        if self.life > 0:
            # 创建临时表面
            surface = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
            
            # 绘制粒子
            pygame.draw.circle(
                surface,
                (*self.color, self.alpha),
                (self.size, self.size),
                self.size
            )
            
            # 绘制到屏幕
            screen.blit(surface, (self.x - self.size, self.y - self.size))
    
    def is_dead(self):
        """检查粒子是否死亡"""
        return self.life <= 0

class ParticleSystem:
    """粒子系统类"""
    
    def __init__(self, config):
        """
        初始化粒子系统
        
        参数:
        - config: 游戏配置
        """
        self.config = config
        self.particles = []
    
    def update(self):
        """更新所有粒子"""
        # 更新粒子
        for particle in self.particles[:]:
            particle.update()
            
            # 移除死亡的粒子
            if particle.is_dead():
                self.particles.remove(particle)
    
    def render(self, screen):
        """渲染所有粒子"""
        for particle in self.particles:
            particle.render(screen)
    
    def create_explosion(self, x, y, color=None, particle_count=50):
        """
        创建爆炸效果
        
        参数:
        - x: 爆炸中心x坐标
        - y: 爆炸中心y坐标
        - color: 粒子颜色，默认为None（随机颜色）
        - particle_count: 粒子数量
        """
        for _ in range(particle_count):
            # 如果没有指定颜色，使用随机颜色
            if color is None:
                particle_color = (
                    random.randint(100, 255),
                    random.randint(100, 255),
                    random.randint(100, 255)
                )
            else:
                # 在指定颜色基础上添加一些随机变化
                particle_color = (
                    max(0, min(255, color[0] + random.randint(-50, 50))),
                    max(0, min(255, color[1] + random.randint(-50, 50))),
                    max(0, min(255, color[2] + random.randint(-50, 50)))
                )
            
            # 创建粒子
            particle = Particle(x, y, particle_color, self.config)
            self.particles.append(particle)
    
    def create_fountain(self, x, y, color, particle_count=10):
        """
        创建喷泉效果
        
        参数:
        - x: 喷泉中心x坐标
        - y: 喷泉中心y坐标
        - color: 粒子颜色
        - particle_count: 每次创建的粒子数量
        """
        for _ in range(particle_count):
            # 创建向上发射的粒子
            particle = Particle(x, y, color, self.config)
            
            # 调整速度和方向，使其向上发射
            angle = random.uniform(-math.pi/4, math.pi/4)
            speed = random.uniform(3, 7)
            particle.vx = math.cos(angle) * speed
            particle.vy = -math.sin(angle) * speed
            
            # 增加生命周期
            particle.life = random.randint(30, 50)
            particle.max_life = particle.life
            
            self.particles.append(particle)
    
    def create_sparkle(self, x, y, color, particle_count=20):
        """
        创建闪光效果
        
        参数:
        - x: 闪光中心x坐标
        - y: 闪光中心y坐标
        - color: 粒子颜色
        - particle_count: 粒子数量
        """
        for _ in range(particle_count):
            # 创建粒子
            particle = Particle(x, y, color, self.config)
            
            # 调整速度和方向
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 6)
            particle.vx = math.cos(angle) * speed
            particle.vy = math.sin(angle) * speed
            
            # 增加生命周期
            particle.life = random.randint(15, 25)
            particle.max_life = particle.life
            
            # 减小粒子大小
            particle.size = random.randint(1, 3)
            
            self.particles.append(particle)