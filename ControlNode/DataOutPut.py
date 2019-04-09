# coding:utf-8
import codecs
import time


class DataOutput(object):
    def __init__(self):
        self.file_path = 'novel_{}.html'.format(time.strftime(r"%Y_%m_%d_%H_%M_%S", time.
                                                              localtime()))
        self.output_head()
        self.datas = []

    def store_data(self, data, num=100):
        if data is None:
            return
        self.datas.append(data)
        if len(self.datas) > num:
            self.output_html()
            self.datas = []
        return

    def output_head(self):
        """
        将 HTML 头写进去
        :return:
        """
        fout = codecs.open(self.file_path, 'w', encoding='utf-8')
        fout.write("<html>")
        fout.write("<head>")
        fout.write('''<style>table,table tr th, table tr td {
                border:1px solid #0094ff;}</style>''')
        fout.write('<meta charset="UTF-8">')
        fout.write('''<meta name="viewport", content="width=device-width,
                initial-scale=1.0">''')
        fout.write('<meta http-equiv="X-UA-Compatible" content="ie=edge">')
        fout.write('<title>Document</title>')
        fout.write("</head>")
        fout.write("<body>")
        fout.write("""<table style='border-color:
            #b6ff00; border-collapse: collapse;'>""")
        fout.close()
        return

    def output_html(self):
        """
        将数据写入 HTML 文件中
        :param path: 文件路径
        :return:
        """
        fout_file = codecs.open(self.file_path, 'a', encoding='utf-8')
        for data in self.datas:
            fout_file.write("<tr>")
            fout_file.write("<td>%s</td>" % data['url'])
            fout_file.write("<td>%s</td>" % data['title'])
            fout_file.write("<td>%s</td>" % data['summary'])
            fout_file.write("</tr>")
            # self.datas.remove(data)
        fout_file.close()
        return

    def ouput_end(self):
        """
        输出 HTML 结束
        :param path: 文件存储路径
        :return:
        """
        fout = codecs.open(self.file_path, 'a', encoding='utf-8')
        fout.write("</table>")
        fout.write("</body>")
        fout.write("</html>")
        fout.close()
        return

