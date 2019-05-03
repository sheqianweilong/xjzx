from flask import Blueprint, make_response, jsonify, redirect
from flask import current_app
from flask import request
from flask import session
from models import db, UserInfo

user_blueprint = Blueprint('user', __name__, url_prefix='/user')


@user_blueprint.route('/image_yzm')
def image_yzm():
    from utils.captcha.captcha import captcha
    name, yzm, image = captcha.generate_captcha()
    # yzm表示随机生成的验证码字符串
    # 将数据进行保存，方便方面对比
    session['image_yzm'] = yzm
    # image表示图片的二进制数据
    response = make_response(image)
    # 默认浏览器将数据作为text/html解析
    # 需要告诉浏览器当前数据的类型为image/png
    response.mimetype = 'image/png'
    return response


@user_blueprint.route('/sms_yzm')
def sms_yzm():
    # 接收数据：手机号，图片验证码
    dict1 = request.args
    mobile = dict1.get('mobile')
    yzm = dict1.get('yzm')

    # 对比图片验证码
    if yzm != session['image_yzm']:
        return jsonify(result=1)

    # 随机生成一个4位的验证码
    import random
    yzm2 = random.randint(1000, 9999)

    # 将短信验证码进行保存，用于验证
    session['sms_yzm'] = yzm2

    # 发送短信
    from utils.ytx_sdk.ytx_send import sendTemplateSMS
    # sendTemplateSMS(mobile,{yzm2,5},1)
    print(yzm2)

    return jsonify(result=2)


@user_blueprint.route('/register', methods=['POST'])
def register():
    # 接收数据
    register_info = request.form
    mobile = register_info.get('mobile')
    yzm_image = register_info.get('yzm_image')
    yzm_sms = register_info.get('yzm_sms')
    pwd = register_info.get('pwd')

    # 验证数据的有效性
    # 保证所有的数据都被填写,列表中只要有一个值为False,则结果为False
    if not all([mobile, yzm_image, yzm_sms, pwd]):
        return jsonify(result=1)
    # 对比图片验证码
    if yzm_image != session['image_yzm']:
        return jsonify(result=2)
    # 对比短信验证码
    if int(yzm_sms) != session['sms_yzm']:
        return jsonify(result=3)
    # 判断密码的长度
    import re
    if not re.match(r'[a-zA-Z0-9_]{6,20}', pwd):
        return jsonify(result=4)
    # 验证mobile是否存在
    mobile_count = UserInfo.query.filter_by(mobile=mobile).count()
    if mobile_count > 0:
        return jsonify(result=5)

    # 创建对象
    user = UserInfo()
    user.nick_name = mobile
    user.mobile = mobile
    user.password = pwd

    # 提交到数据库
    try:
        db.session.add(user)
        db.session.commit()
    except:
        current_app.logger_xjzx.error('用户注册访问数据库失败')
        return jsonify(result=7)

    # 返回响应
    return jsonify(result=6)


@user_blueprint.route('/login', methods=['POST'])
def login():
    # 接收数据
    login_info = request.form
    mobile = login_info.get("mobile")
    password = login_info.get("password")
    # 检查所有参数
    if not all([mobile, password]):
        return jsonify(result=1)
    # # 判断手机号是否合法
    # import re
    # check_mobile = re.compile(r"^1[2-9]\d{9}$")
    # check_mobile = check_mobile.match(mobile)
    # if not check_mobile:
    #     return jsonify(result=2)
    # 查询数据库中是否存在该用户
    user = UserInfo.query.filter_by(mobile=mobile).first()
    if user:
        if user.check_pwd(password):  # flask提供了对应的解密算法
            # 密码正确，则表示用户可以登录，做状态保持
            # session 默认存储在cookies中
            session["user_id"] = user.id
            return jsonify(result=4, avatar=user.avatar, nick_name=user.nick_name)
        else:
            return jsonify(result=3)
    else:
        return jsonify(result=2)


@user_blueprint.route('/logout', methods=['POST'])
def logout():
    del session['user_id']
    return jsonify(result=1)


@user_blueprint.route('/show')
def show():
    if 'user_id' in session:
        return 'ok'
    else:
        return 'no'
