import jieba.analyse
from PIL import Image, ImageSequence
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator

l = ''
f = open('短评.txt', 'r',encoding='utf-8')  # 这个就是你的数据源，打开数据时和数据进行截取可以使用结巴分词器
for i in f:
	l += f.read()

result = jieba.analyse.textrank(l, topK=250, withWeight=True)
keyworlds = dict()
for i in result:
	keyworlds[i[0]] = i[1]

# print(keyworlds)

image = Image.open('tim.jpg')  # 这个就是你的背景，想要好看的，背景图颜色多一点
graph = np.array(image)
wc = WordCloud(font_path='simhei.ttf', background_color='White', max_font_size=170, mask=graph)
wc.generate_from_frequencies(keyworlds)
image_color = ImageColorGenerator(graph)
plt.imshow(wc)
# plt.imshow(wc.recolor(color_func=image_color))
plt.axis('off')
plt.show()
wc.to_file('1.png')