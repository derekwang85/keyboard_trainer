#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
指法合规性追踪器
用于追踪用户的指法使用情况，分析指法是否正确
"""

class FingerComplianceTracker:
    """指法合规性追踪器"""
    
    def __init__(self):
        """初始化追踪器"""
        # 按键使用统计
        self.key_usage_count = {}  # {char: count}
        
        # 手指使用统计
        self.finger_usage_count = {
            'left_pinkie': 0,
            'left_ring': 0,
            'left_middle': 0,
            'left_index': 0,
            'left_thumb': 0,
            'both_thumbs': 0,
            'right_thumb': 0,
            'right_index': 0,
            'right_middle': 0,
            'right_ring': 0,
            'right_pinkie': 0,
        }
        
        # 正确/错误统计
        self.correct_presses = []  # [(char, finger, timestamp), ...]
        self.incorrect_presses = []  # [(char, pressed_finger, correct_finger, timestamp), ...]
        
        # 统计数据
        self.total_presses = 0
        self.correct_presses_count = 0
        self.incorrect_presses_count = 0
        
        # 指法映射（从键盘渲染器获取）
        self.key_to_finger_map = {}
    
    def set_key_finger_map(self, key_to_finger_map):
        """设置按键到手指的映射"""
        self.key_to_finger_map = key_to_finger_map
    
    def record_key_press(self, char, finger_used, is_correct):
        """
        记录一次按键
        
        参数:
        - char: 按键字符
        - finger_used: 使用的手指
        - is_correct: 是否正确
        """
        import time
        timestamp = time.time()
        
        # 更新统计
        self.total_presses += 1
        self.key_usage_count[char] = self.key_usage_count.get(char, 0) + 1
        
        # 更新手指使用统计
        finger_key = finger_used if finger_used else 'unknown'
        if finger_key in self.finger_usage_count:
            self.finger_usage_count[finger_key] += 1
        
        if is_correct:
            self.correct_presses_count += 1
            self.correct_presses.append((char, finger_used, timestamp))
        else:
            self.incorrect_presses_count += 1
            correct_finger = self.get_correct_finger(char)
            self.incorrect_presses.append((char, finger_used, correct_finger, timestamp))
    
    def get_correct_finger(self, char):
        """获取按键对应的正确手指"""
        char_lower = char.lower() if len(char) == 1 else char
        return self.key_to_finger_map.get(char_lower, 'unknown')
    
    def get_compliance_rate(self):
        """获取指法合规率"""
        if self.total_presses == 0:
            return 0.0
        return self.correct_presses_count / self.total_presses
    
    def get_finger_usage_stats(self):
        """获取手指使用统计"""
        total = sum(self.finger_usage_count.values())
        if total == 0:
            return {}
        
        stats = {}
        for finger, count in self.finger_usage_count.items():
            stats[finger] = {
                'count': count,
                'percentage': (count / total * 100) if total > 0 else 0
            }
        return stats
    
    def get_most_used_finger(self):
        """获取使用最多的手指"""
        if not self.finger_usage_count:
            return None
        return max(self.finger_usage_count.items(), key=lambda x: x[1])
    
    def get_least_used_finger(self):
        """获取使用最少的手指"""
        # 过滤掉使用次数为0的手指
        active_fingers = {k: v for k, v in self.finger_usage_count.items() if v > 0}
        if not active_fingers:
            return None
        return min(active_fingers.items(), key=lambda x: x[1])
    
    def get_finger_balance_score(self):
        """
        获取手指使用均衡分数（0-100）
        100表示完美均衡，0表示严重不均衡
        """
        active_fingers = [v for v in self.finger_usage_count.values() if v > 0]
        if not active_fingers:
            return 100
        
        total = sum(active_fingers)
        if total == 0:
            return 100
        
        # 计算标准差
        mean = total / len(active_fingers)
        variance = sum((x - mean) ** 2 for x in active_fingers) / len(active_fingers)
        std_dev = variance ** 0.5
        
        # 将标准差转换为分数
        # 假设理想状态下每个手指使用次数相同
        max_std_dev = mean * 2  # 设定一个合理的最大标准差
        if max_std_dev == 0:
            return 100
        
        score = max(0, 100 - (std_dev / max_std_dev * 100))
        return int(score)
    
    def get_wrong_finger_report(self):
        """获取错误手指使用报告"""
        report = []
        for char, pressed_finger, correct_finger in self.incorrect_presses:
            if pressed_finger != correct_finger:
                report.append({
                    'char': char,
                    'pressed_finger': pressed_finger,
                    'correct_finger': correct_finger,
                    'finger_name_cn': self._get_finger_name_cn(pressed_finger),
                    'correct_finger_name_cn': self._get_finger_name_cn(correct_finger)
                })
        return report
    
    def _get_finger_name_cn(self, finger):
        """获取手指中文名称"""
        names = {
            'left_pinkie': '左手小指',
            'left_ring': '左手无名指',
            'left_middle': '左手中指',
            'left_index': '左手食指',
            'left_thumb': '左手拇指',
            'both_thumbs': '双拇指',
            'right_thumb': '右手拇指',
            'right_index': '右手食指',
            'right_middle': '右手中指',
            'right_ring': '右手无名指',
            'right_pinkie': '右手小指',
            'unknown': '未知'
        }
        return names.get(finger, finger)
    
    def get_summary(self):
        """获取统计摘要"""
        return {
            'total_presses': self.total_presses,
            'correct_count': self.correct_presses_count,
            'incorrect_count': self.incorrect_presses_count,
            'compliance_rate': self.get_compliance_rate(),
            'finger_balance_score': self.get_finger_balance_score(),
            'most_used_finger': self.get_most_used_finger(),
            'least_used_finger': self.get_least_used_finger(),
            'finger_usage': self.get_finger_usage_stats()
        }
    
    def reset(self):
        """重置追踪器"""
        self.__init__()
