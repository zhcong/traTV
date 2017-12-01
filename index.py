#!/usr/bin/env python

import requests, config, io, json
from contextlib import closing
from flask import Flask, render_template, redirect, Response, request
from PIL import Image
import dbm

# 网络代理
if config.proxy_enable:
    proxy = {
        'http': 'http://' + config.proxy_ip + ':' + config.proxy_port,
        'https': 'http://' + config.proxy_ip + ':' + config.proxy_port
    }
else:
    proxy = ''


# 压缩并裁剪照片
def cut_image(data, pic_qua):
    if pic_qua == 'source': return data
    image_data = io.BytesIO(data)
    img = Image.open(image_data)
    img = img.resize((240, 141), Image.ANTIALIAS)
    image_data = io.BytesIO()
    img.save(image_data, format='JPEG')
    return image_data.getvalue()


# 通过get方法获得文本
def get_text(url):
    response = requests.get(url, proxies=proxy, timeout=config.timeout)
    if response.ok:
        return response.text
    else:
        raise Exception('network 404 error.')


# 读取公告
def get_msg():
    try:
        db = dbm.open(config.db_file, 'c')
        msg = db['msg']
        db.close()
        return msg
    except Exception as e:
        return ('').encode()


# 存入新的公告
def set_msg(text):
    db = dbm.open(config.db_file, 'c')
    db['msg'] = text
    db.close()


app = Flask(__name__)

source_url = 'https://iptv.tsinghua.edu.cn/hls/'


@app.route('/')
def index():
    TVlist = []
    # 先抓取节目单
    # https://iptv.tsinghua.edu.cn/channels.json
    # https://iptv.tsinghua.edu.cn/epg/todayepg.json 节目表
    try:
        channels = get_text('https://iptv.tsinghua.edu.cn/channels.json')
        if channels == '': raise Exception
        channels_dict = json.loads(channels.replace(' ', '').replace('\n', ''))
        channels_dict = channels_dict['Categories']
        for channel in channels_dict:
            links = channel['Channels']
            if len(links) > 1:
                area_list = []
                title = channel['Name']
                for link in links:
                    id = link['Vid']
                    area_list.append({
                        'id': id,
                        'title': link['Name'],
                        'url': '/view/' + id + '?title=' + link['Name'],
                        'pic': '/image/' + id + '.jpg',
                    })
                TVlist.append({'title': title, 'list': area_list, 'count': len(area_list)})
        # 模板渲染
        return render_template('index.html', TVlist=TVlist, tip=get_msg().decode())
    except Exception as e:
        app.logger.debug(str(e))
        return redirect(404)


@app.route('/m3u8/<file>', methods=['GET'])
def m3u8(file):
    if file:
        try:
            url = source_url + file
            # 获得m3u8文件，并将地址改成自己的
            m3u8_html = get_text(url)
            m3u8_htmls = m3u8_html.split('\n')
            new_lines = ''
            for line in m3u8_htmls:
                if line:
                    if not line[0] == '#':
                        line = '/stream/' + line
                    new_lines += line + '\n'

            res_headers = {}
            response = requests.head(url, proxies=proxy, timeout=config.timeout)
            if not response.ok: raise Exception('network error.')
            for key, value in response.headers.items():
                if key == 'Host': value = 'TRA TV SERVER'
                res_headers.setdefault(key, value)
            return new_lines, 200, res_headers
        # return Response(generate(), headers=res_headers, direct_passthrough=True)
        except Exception as e:
            return redirect(404), 404
    else:
        return redirect(404)


@app.route('/view/<id>')
def view(id):
    if id:
        try:
            title = id
            if request.args.get('title'): title = request.args.get('title')
            return render_template('view.html', id=id, title=title, tip=get_msg().decode())
        except Exception as e:
            return redirect(404)
    else:
        return redirect(404)


@app.route('/stream/<file>', methods=['GET'])
def stream(file):
    if file:
        try:
            # 这是从清华TV转发视频流
            url = source_url + file

            def generate():
                try:
                    with closing(requests.get(url, stream=True, proxies=proxy, timeout=config.timeout)) as response:
                        if not response.ok: raise Exception('network error.')
                        for data in response.iter_content(chunk_size=512):  # max download limit is 2048??
                            if not response.ok: raise Exception('network error.')
                            yield data
                except Exception as e:
                    app.logger.debug(str(e))
                    return redirect(404)

            response = requests.head(url, proxies=proxy, timeout=config.timeout)
            if not response.status_code == 200: raise Exception('network error.')
            res_headers = {}
            for key, value in response.headers.items():
                if key == 'Host': value = 'TRA TV SERVER'
                res_headers.setdefault(key, value)
            return Response(generate(), headers=res_headers, direct_passthrough=True)
        except Exception as e:
            return redirect(404)
    else:
        return redirect(404)


@app.route('/image/<file>', methods=['GET'])
def image(file):
    if file:
        try:
            # 获取截图
            url = 'https://iptv.tsinghua.edu.cn/snapshot/' + file
            pic_qua = ''
            if request.args.get('quality'): pic_qua = request.args.get('quality')

            def generate():
                response = requests.get(url, proxies=proxy, timeout=config.timeout)
                if not response.ok: raise Exception('network error.')
                return cut_image(response.content, pic_qua)

            res_headers = {}
            response = requests.head(url, proxies=proxy, timeout=config.timeout)
            if not response.ok: raise Exception('network error.')
            for key, value in response.headers.items():
                if key == 'Host': value = 'TRA TV SERVER'
                res_headers.setdefault(key, value)
            return Response(generate(), headers=res_headers, direct_passthrough=True)
        except Exception as e:
            return redirect(404)
    else:
        return redirect(404)


@app.route('/tip', methods=['GET'])
def tip():
    return render_template('tip.html')


# msg = msg_code
@app.route('/tip/<msg>', methods=['GET'])
def set_tip(msg):
    msgs = msg.split('_')
    if len(msgs) == 2:
        if msgs[1] == config.admin_code:
            set_msg(msgs[0])
            return 'ok'
        else:
            return 'bad'
    else:
        return 'bad'


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=config.port, threaded=True, debug=True)
