#!/bin/bash

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到Python3。请先安装Python 3.8或更高版本。"
    exit 1
fi

# 检查Python版本
PYTHON_VERSION=$(python3 --version | awk '{print $2}')
REQUIRED_VERSION="3.8"

if [[ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]]; then
    echo "警告: Python版本 $PYTHON_VERSION 可能低于推荐的版本 $REQUIRED_VERSION"
    echo "游戏可能无法正常运行，建议升级Python版本。"
fi

# 检查Pygame是否安装
if ! python3 -c "import pygame" &> /dev/null; then
    echo "未找到Pygame库，正在安装..."
    pip3 install pygame
    if [ $? -ne 0 ]; then
        echo "错误: 安装Pygame失败。请手动安装: pip3 install pygame"
        exit 1
    fi
fi

# 确保音效目录存在
mkdir -p resources/sounds

# 创建占位音效文件（如果不存在）
SOUND_FILES=("correct.wav" "error.wav" "encouragement.wav" "game_over.wav" "new_record.wav" "button_click.wav" "level_up.wav" "combo.wav")
for file in "${SOUND_FILES[@]}"; do
    if [ ! -f "resources/sounds/$file" ]; then
        echo "创建占位音效文件: $file"
        # 创建一个空的WAV文件作为占位符
        python3 -c "import wave; import struct; f = wave.open('resources/sounds/$file', 'w'); f.setparams((1, 2, 44100, 0, 'NONE', 'not compressed')); f.writeframes(struct.pack('h', 0)); f.close()"
    fi
done

# 运行游戏
echo "启动儿童键盘练习小游戏..."
python3 main.py