from PIL import Image

# 打开图片
pic_path = r"C:\Users\Administrator\PycharmProjects\XJZX\static\timg.jpg"
im = Image.open(pic_path, 'r')
# Image.open返回一个Image对象，该对象有size,format,mode等属性;
# 其中size表示图像的宽度和高度(像素表示);format表示图像的格式,常见的包括JPEG,PNG等格式;
# mode表示图像的模式，定义了像素类型还有图像深度等，常见的有RGB,HSV等;
# 一般来说'L'(luminance)表示灰度图像,'RGB'表示真彩图像,'CMYK'表示预先压缩的图像。
# 一旦你得到了打开的Image对象之后，就可以使用其众多的方法对图像进行处理了，比如使用im.show()可以展示上面得到的图像。
print(im.size, im.format, im.mode)
# im.show()
# 保存指定格式的图像
im.save(r"C:\Users\Administrator\PycharmProjects\XJZX\static\V.png", 'png')
