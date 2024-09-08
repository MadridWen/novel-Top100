from wordcloud import WordCloud
import matplotlib.pyplot as plt
from PIL import Image
import jieba
import re


def file_read(c_path, c_isbytes=False):
    with open(c_path, mode="rb") if c_isbytes else open(c_path, mode='r', encoding="utf-8") as f:
        return f.read()

def file_write(c_path, c_data, c_isbytes=False):
    with open(c_path, mode="wb") if c_isbytes else open(c_path, mode='a', encoding="utf-8") as f:
        f.write(c_data)

data_content = file_read('result.txt')

stringList = jieba.lcut(data_content)

data_dict = {}
for item in stringList :

    item = re.sub("\W+","",item)

    if(len(item) < 2):
        continue

    if(item != ''):
        data_dict[item] = data_dict.get(item,0) + 1

data_dict = dict(sorted(data_dict.items(), key=lambda x: x[1],reverse=True))

print("--------------排名 100----------------")
for count,item in enumerate(data_dict.keys()):
    if(count < 100):
        print(f"排名:{ count+1 } \t关键字:{ item } \t出现次数:{data_dict[item]}")
        file_write('word_top100.txt',f"排名:{ count+1 } \t关键字:{ item } \t出现次数:{data_dict[item]}\n")

        
def color_func(word,/,font_size,position,random_state,**kwargs):
    if position[0]<60:
        r=random_state.randint(10,40)
    else:
        r=random_state.randint(100,150)
    if position[1]<310:
        g=random_state.randint(0,40)
    else:
        g=random_state.randint(100,150)
    if font_size < 0:
        b=random_state.randint(0,40)
    else:
        b=random_state.randint(100,150)
 
    return (r,g,b)

save_img_path = 'xiaoshuo_wordcloud_result.jpg'

# classmMask = np.array(Image.open(classpath))

cloud_content = ' '.join(data_dict.keys())

imdb_wordcloud = WordCloud(width=900,height=700,background_color='White',color_func=color_func,font_path='msyh.ttf').generate(cloud_content)

imdb_wordcloud.to_file(save_img_path)

imgobj = Image.open(save_img_path)

plt.title('WorldCloud')
plt.imshow(imgobj)
plt.show()