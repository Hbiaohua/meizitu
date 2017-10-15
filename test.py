#构造图片名
url = 'http://mm.chinasareview.com/wp-content/uploads/2017a/07/19/01.jpg'
filename = url.replace('/','')[-15:-1]
print(filename)