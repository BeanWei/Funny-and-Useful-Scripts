"""
利用 PIL 生成 6位 简单验证码图片
"""

from PIL import Image, ImageDraw, ImageFont
import random

vcode = Image.new(mode='RGB', size=(120, 30), color=(255, 255, 255))

draws = ImageDraw.Draw(vcode, mode='RGB')

fonts = ImageFont.truetype('./ttf/times.ttf', 28)

for i in range(6):
    # 65到90为字母的ASCII码,使用chr把生成的ASCII码转换成字符
    thechar = random.choice([chr(random.randint(65, 90)), str(random.randint(0, 9))])

    # 生成随机颜色(三原色)
    thecolor = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    # 字符绘制在图片上
    # args: 坐标，字符，颜色， 字体
    draws.text([ i * 20, 0], thechar, thecolor, font=fonts)

# 保存图片
# with open('simplecode.png', 'wb') as f:
#     vcode.save(f, format='png')

# 展示图片
import matplotlib.pyplot as plt
plt.axis('off')
plt.imshow(vcode)
plt.show()
