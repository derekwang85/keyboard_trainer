# 字体文件说明

此目录用于存放项目中使用的中文字体文件，以解决跨环境字体乱码问题。

## 推荐字体文件

请在此目录放置以下任意一个中文字体文件：

### 1. Noto Sans SC (推荐)
- 文件名: `NotoSansSC-Regular.ttf`
- 下载地址: https://github.com/googlefonts/noto-fonts/raw/main/hinted/ttf/NotoSansSC/NotoSansSC-Regular.ttf
- 说明: Google 开源中文字体，支持简体中文，体积适中

### 2. Source Han Sans CN (思源黑体)
- 文件名: `SourceHanSansCN-Regular.otf`
- 下载地址: https://github.com/adobe-fonts/source-han-sans/raw/release/OTF/SimplifiedChinese/SourceHanSansCN-Regular.otf
- 说明: Adobe 开源中文字体，支持完整中文

### 3. Noto Sans SC Medium (粗体)
- 文件名: `NotoSansSC-Medium.ttf`
- 下载地址: https://github.com/googlefonts/noto-fonts/raw/main/hinted/ttf/NotoSansSC/NotoSansSC-Medium.ttf
- 说明: Noto Sans SC 的粗体版本

## 使用说明

1. 将下载的字体文件放入此目录
2. 重启程序，程序会自动使用此目录中的字体
3. 如果没有字体文件，程序会尝试使用系统字体

## 注意事项

- 字体文件较大，建议只放入必需的字体
- 程序会自动检测并使用找到的第一个可用字体
- 如果系统已有中文字体，此目录可以为空
