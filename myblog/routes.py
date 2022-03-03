import os
import secrets
from PIL import Image
from flask import render_template, url_for, request, json, redirect, send_from_directory,make_response
from myblog import app, mysql
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
from datetime import datetime

@app.route("/")
@app.route("/home")
def home():
    name = request.cookies.get('userID')
    con = mysql.connect()
    cursor = con.cursor()
    cursor.callproc('login_nv',(name,))
    data = cursor.fetchall()
    if len(data) > 0:
        return render_template('index.html', data = data[0][7], quyen_nv = data[0][2])
    else:
        con = mysql.connect()
        cursor = con.cursor()
        cursor.callproc('login_kh',(name,))
        data = cursor.fetchall()
        if len(data) > 0:
            con3 = mysql.connect()
            cursor3 = con3.cursor()
            cursor3.callproc('tong_sp',(name,))
            sp3 = cursor3.fetchall()
            return render_template('index.html', data = data[0][4], sp3=sp3)
        else:
            return render_template('index.html')

@app.route('/introduce')
def introduce():
    name = request.cookies.get('userID')
    con = mysql.connect()
    cursor = con.cursor()
    cursor.callproc('login_nv',(name,))
    data = cursor.fetchall()
    if len(data) > 0:
        return render_template('introduce.html', data = data[0][7], quyen_nv = data[0][2])
    else:
        cursor.callproc('login_kh',(name,))
        data = cursor.fetchall()
        if len(data) > 0:
            con3 = mysql.connect()
            cursor3 = con3.cursor()
            cursor3.callproc('tong_sp',(name,))
            sp3 = cursor3.fetchall()
            return render_template('introduce.html', data = data[0][4], sp3 = sp3)
        else:
            return render_template('introduce.html')

@app.route("/store", methods=['GET'])
def store():
    name = request.cookies.get('userID')
    con = mysql.connect()
    cursor = con.cursor()
    cursor.callproc('login_nv',(name,))
    data = cursor.fetchall()
    if len(data) > 0:
        if request.method == 'GET':
            id_loai1 = request.args.get('id_loai')
            con = mysql.connect()
            cursor = con.cursor()
            cursor.callproc('sp_store',(id_loai1,))
            data_sp = cursor.fetchall()
            # return str(data_sp)
            ten_loai = data_sp[0][5]
            # return str(ten_loai)
            return render_template("store.html", sp_loai1 = data_sp, data = data[0][7], ten_loai = ten_loai, quyen_nv = data[0][2])
    else:
        cursor.callproc('login_kh',(name,))
        data = cursor.fetchall()
        if len(data) > 0:
            if request.method == 'GET':
                id_loai1 = request.args.get('id_loai')
                con = mysql.connect()
                cursor = con.cursor()
                cursor.callproc('sp_store',(id_loai1,))
                data_sp = cursor.fetchall()
                ten_loai = data_sp[0][5]
                # return str(ten_loai)

                con3 = mysql.connect()
                cursor3 = con3.cursor()
                cursor3.callproc('tong_sp',(name,))
                sp3 = cursor3.fetchall()
                return render_template("store.html", sp_loai1 = data_sp, data = data[0][4], ten_loai = ten_loai, sp3=sp3)
        else:
            if request.method == 'GET':
                id_loai1 = request.args.get('id_loai')
                con = mysql.connect()
                cursor = con.cursor()
                cursor.callproc('sp_store',(id_loai1,))
                data_sp = cursor.fetchall()
                ten_loai = data_sp[0][5]
                # return str(ten_loai)
                return render_template("store.html", sp_loai1 = data_sp, ten_loai = ten_loai)

@app.route("/khuyenmai")
def khuyenmai():
    name = request.cookies.get('userID')
    con = mysql.connect()
    cursor = con.cursor()
    cursor.callproc('login_nv',(name,))
    data = cursor.fetchall()
    if len(data) > 0:
        id_ch = 1
        con1 = mysql.connect()
        cursor1 = con1.cursor()
        cursor1.callproc('km_show',())
        data1 = cursor1.fetchall()
        if len(data1) > 0:
            return render_template("khuyenmai.html", data1=data1,data=data[0][7], quyen_nv = data[0][2])

@app.route("/edit_km", methods=['GET'])
def edit_km():
    if request.method == 'GET':
        id_km = request.args.get('id_km')
        con = mysql.connect()
        cursor = con.cursor()
        cursor.callproc('km',(id_km,))
        data = cursor.fetchall()
        if len(data) > 0:
            return render_template("edit_km.html", data = data)

@app.route("/editKM", methods=['POST'])
def editKM():
    if request.method == 'POST':
        id_km = request.form['id_km']
        ngay_bd = request.form['ngay_bd']
        ngay_kt = request.form['ngay_kt']

        con = mysql.connect()
        cursor = con.cursor()
        cursor.callproc('edit_km',(id_km, ngay_bd, ngay_kt))
        data = cursor.fetchall()
        if len(data) is 0:
            con.commit()
            return redirect(url_for('khuyenmai'))

@app.route("/add_km")
def add_km():
    return render_template("add_km.html")

@app.route("/addKM", methods=['POST'])
def addKM():
    if request.method == 'POST':
        muc_km = request.form['muc_km']
        ngay_bd = request.form['ngay_bd']
        ngay_kt = request.form['ngay_kt']

        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.callproc('add_km',(muc_km, ngay_bd, ngay_kt))
        data = cursor.fetchall()
        if len(data) is 0:
            conn.commit()
            return redirect(url_for('khuyenmai'))

@app.route("/cart")
def cart():
    name = request.cookies.get('userID')
    con = mysql.connect()
    cursor = con.cursor()
    cursor.callproc('login_kh',(name,))
    data = cursor.fetchall()
    # return str(data)
    if len(data) > 0:
        con = mysql.connect()
        cursor = con.cursor()
        cursor.callproc('sp_cart',(name,))
        sp = cursor.fetchall()
        # return str(sp)
        if len(sp) is 0:
            # return 'Khác rỗng'
            return render_template("cart.html", data = data[0][4])
        else:
            # return "rỗng"
            con3 = mysql.connect()
            cursor3 = con3.cursor()
            cursor3.callproc('tong_sp',(name,))
            sp3 = cursor3.fetchall()
            # return str(sp3)
            return render_template("cart_sp.html", data = data[0][4], sp=sp, sp3=sp3)
    else:
        return render_template("cart.html")

@app.route("/product_if", methods=['GET'])
def product_if():
    name = request.cookies.get('userID')
    con = mysql.connect()
    cursor = con.cursor()
    cursor.callproc('login_nv',(name,))
    data = cursor.fetchall()
    if len(data) > 0:
        if request.method == 'GET':
            id_sp = request.args.get('id_sp')
            id = int(id_sp)
            con = mysql.connect()
            cursor = con.cursor()
            cursor.callproc('sp',(id,))
            sp = cursor.fetchall()
            if len(sp) > 0:
                return render_template("product_information.html", sp = sp, data = data[0][7], quyen_nv = data[0][2])
    else:
        cursor.callproc('login_kh',(name,))
        data = cursor.fetchall()
        if len(data) > 0:
            if request.method == 'GET':
                id_sp = request.args.get('id_sp')
                id = int(id_sp)
                con = mysql.connect()
                cursor = con.cursor()
                cursor.callproc('sp',(id,))
                sp = cursor.fetchall()
                # return str(sp)
                if len(sp) > 0:
                    con3 = mysql.connect()
                    cursor3 = con3.cursor()
                    cursor3.callproc('tong_sp',(name,))
                    sp3 = cursor3.fetchall()
                    return render_template("product_information.html", sp = sp, data = data[0][4], sp3=sp3)
        else:
            return render_template("login.html")

@app.route("/capnhat_dh", methods=['GET', 'POST'])
def capnhat_dh():
    name = request.cookies.get('userID')
    # return name
    con5 = mysql.connect()
    cursor5 = con5.cursor()
    cursor5.callproc('trangthai_dh',(name,))
    data5 = cursor5.fetchall()
    # return str(data5)
    if len(data5) > 0:
        if request.method == 'POST':
            sl = request.form['quantity']
            id_sp = request.args.get('id_sp')
            # return str(id_sp)

            con = mysql.connect()
            cursor = con.cursor()
            cursor.callproc('sp_in_cart',(id_sp, name))
            data = cursor.fetchall()
            # return str(data)
            
            if len(data) > 0:
                con = mysql.connect()
                cursor = con.cursor()
                cursor.callproc('sp_in_cart_update',(id_sp, sl, data[0][0]))
                data1 = cursor.fetchall()
                con.commit()
                # return str(data1)
                if len(data1) is 0:
                    con = mysql.connect()
                    cursor = con.cursor()
                    cursor.callproc('sp_cart',(name,))
                    sp = cursor.fetchall()
                    # return str(sp)

                    con3 = mysql.connect()
                    cursor3 = con3.cursor()
                    cursor3.callproc('tong_sp',(name,))
                    sp3 = cursor3.fetchall()
                    # return "Cập nhật lại"

                    con6 = mysql.connect()
                    cursor6 = con6.cursor()
                    cursor6.callproc('kt_slsp',(id_sp,sl))
                    sp4 = cursor6.fetchall()
                    # return str(sp4)
                    error = ""

                    if len(sp4) is 0:
                        error = "Hết Hàng"

                    return render_template("cart_sp.html", data = data5[0][4], sp=sp, sp3=sp3, error = error)
            else:
                con = mysql.connect()
                cursor = con.cursor()
                cursor.callproc('sp_order',(id_sp, sl))
                sp = cursor.fetchall()
                # return str(sp)
                if len(sp) > 0:
                    con2 = mysql.connect()
                    cursor2 = con2.cursor()
                    cursor2.callproc('ct_dathang',(sp[0][4], sp[0][3], sp[0][2], data5[0][7], sp[0][1]))
                    sp2 = cursor2.fetchall()
                    con2.commit()

                    con1 = mysql.connect()
                    cursor1 = con1.cursor()
                    cursor1.callproc('sp_cart',(name,))
                    sp1 = cursor1.fetchall()

                    con3 = mysql.connect()
                    cursor3 = con3.cursor()
                    cursor3.callproc('tong_sp',(name,))
                    sp3 = cursor3.fetchall()
                    # return str(data5[0][0])
                    return render_template("cart_sp.html", data = data5[0][4], sp=sp1, sp3=sp3)
    else:
        # return "chua có đonn hàng"
        con = mysql.connect()
        cursor = con.cursor()
        cursor.callproc('login_kh',(name,))
        data = cursor.fetchall()
        if len(data) > 0:
            if request.method == 'POST':
                sl = request.form['quantity']
                id_sp = request.args.get('id_sp')

                con = mysql.connect()
                cursor = con.cursor()
                cursor.callproc('sp_order',(id_sp, sl))
                sp = cursor.fetchall()
                # return str(sp[0][6])
                if len(sp) > 0:
                    today = datetime.now()
                    con1 = mysql.connect()
                    cursor1 = con1.cursor()
                    cursor1.callproc('dathang',(data[0][0], today, data[0][2]))
                    sp1 = cursor1.fetchall()
                    con1.commit()
                    # return str(sp1)
                    if len(sp1) > 0:
                        con2 = mysql.connect()
                        cursor2 = con2.cursor()
                        cursor2.callproc('ct_dathang',(sp[0][4], sp[0][3], sp[0][2], sp1[0][0], sp[0][1]))
                        sp2 = cursor2.fetchall()
                        con2.commit()
                        # return str(sp[0][1])

                        con3 = mysql.connect()
                        cursor3 = con3.cursor()
                        cursor3.callproc('tong_sp',(name,))
                        sp3 = cursor3.fetchall()


                        con4 = mysql.connect()
                        cursor4 = con4.cursor()
                        cursor4.callproc('sp_cart',(name,))
                        sp4 = cursor4.fetchall()

                        # return str(sp3)
                        return render_template("cart_sp.html", data = data[0][4], sp=sp4, sp3=sp3)
                
@app.route("/delete_sp_cart", methods=['GET', 'POST'])
def delete_sp_cart():
    name = request.cookies.get('userID')
    con = mysql.connect()
    cursor = con.cursor()
    cursor.callproc('login_kh',(name,))
    data = cursor.fetchall()
    if request.method == 'GET':
        id_sp = request.args.get('id_sp')
        id_dh = request.args.get('id_dh')
        
        con1 = mysql.connect()
        cursor1 = con1.cursor()
        cursor1.callproc('delete_sp_cart',(id_dh, id_sp))
        data1 = cursor1.fetchall()
        con1.commit()
        if len(data1) is 0:
            con3 = mysql.connect()
            cursor3 = con3.cursor()
            cursor3.callproc('tong_sp',(name,))
            sp3 = cursor3.fetchall()

            con4 = mysql.connect()
            cursor4 = con4.cursor()
            cursor4.callproc('sp_cart',(name,))
            sp4 = cursor4.fetchall()
            # return str(sp4)

            return render_template("cart_sp.html", data = data[0][4], sp=sp4, sp3=sp3)

@app.route("/dathang")
def dathang():
    name = request.cookies.get('userID')
    con = mysql.connect()
    cursor = con.cursor()
    cursor.callproc('login_kh',(name,))
    data = cursor.fetchall()
    if len(data) > 0:
        con = mysql.connect()
        cursor = con.cursor()
        cursor.callproc('sp_cart',(name,))
        sp = cursor.fetchall()
        # return str(sp)
        if len(sp) != None:
            # return "rỗng"
            con3 = mysql.connect()
            cursor3 = con3.cursor()
            cursor3.callproc('tong_sp',(name,))
            sp3 = cursor3.fetchall()
            # return str(sp3)
            return render_template("order.html", data = data, sp=sp, sp3=sp3)

@app.route("/dathang_tc", methods=['GET', 'POST'])
def dathang_tc():
    name = request.cookies.get('userID')
    con = mysql.connect()
    cursor = con.cursor()
    cursor.callproc('login_kh',(name,))
    data = cursor.fetchall()
    if len(data) > 0:
        if request.method == 'POST':
            id_dh = request.args.get('id_dh')
            con1 = mysql.connect()
            cursor1 = con1.cursor()
            cursor1.callproc('capnhat_trangthai',(id_dh,))
            data1 = cursor1.fetchall()
            con1.commit()

            if len(data1) is 0:
                # return "thành công"
                con = mysql.connect()
                cursor = con.cursor()
                cursor.callproc('dh_danggiao',(name,))
                sp = cursor.fetchall()

                for i in range(len(sp)):
                    con2 = mysql.connect()
                    cursor2 = con2.cursor()
                    cursor2.callproc('soluongsp_conlai',(sp[i][4], sp[i][3], id_dh))
                    sp2 = cursor2.fetchall()
                    con2.commit()

                if len(sp) != None:
                # return "rỗng"
                    con3 = mysql.connect()
                    cursor3 = con3.cursor()
                    cursor3.callproc('tong_sp_dadat',(name,))
                    sp3 = cursor3.fetchall()
                    # return str(sp3)

                    con4 = mysql.connect()
                    cursor4 = con4.cursor()
                    cursor4.callproc('tong_sp',(name,))
                    sp4 = cursor4.fetchall()
                    return render_template("dh_dadat.html", data = data[0][4], sp=sp, sp3=sp3, sp4=sp4)
        
@app.route("/dh_danggiao")
def dh_danggiao():
    name = request.cookies.get('userID')
    con = mysql.connect()
    cursor = con.cursor()
    cursor.callproc('login_kh',(name,))
    data = cursor.fetchall()
    if len(data) > 0:
        con = mysql.connect()
        cursor = con.cursor()
        cursor.callproc('dh_danggiao',(name,))
        sp = cursor.fetchall()
        # return str(sp)
        if len(sp) != None:
            con3 = mysql.connect()
            cursor3 = con3.cursor()
            cursor3.callproc('tong_sp_dadat',(name,))
            sp3 = cursor3.fetchall()
            # return str(sp3)

            con4 = mysql.connect()
            cursor4 = con4.cursor()
            cursor4.callproc('tong_sp',(name,))
            sp4 = cursor4.fetchall()

            return render_template("dh_dadat.html", data = data[0][4], sp=sp, sp3=sp3, sp4=sp4)
        else:
            return "Không có đơn hàng"

@app.route("/product_add")
def product_add():
    # name = request.cookies.get('userID')
    return render_template("add_product.html")

@app.route("/add", methods=['POST'])
def add():
    UPLOAD_FOLDER = 'myblog/static/sanpham/'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    if request.method == 'POST':
        nhacungcap = request.form['nhacungcap']
        khuyenmai = request.form['khuyenmai']
        loai_sp = request.form['loai_sp']
        ten_sp = request.form['ten_sp']
        thongtin_sp = request.form['thongtin_sp']
        hinhanh_sp = request.files['hinhanh_sp']
        gia_sp = request.form['gia_sp']
        soluong_sp = request.form['soluong_sp']

        img_name = secure_filename(hinhanh_sp.filename)
        saved_path = os.path.join(app.config['UPLOAD_FOLDER'], img_name)
        app.logger.info("saving {}".format(saved_path))
        hinhanh_sp.save(saved_path)

        # return json.dumps({'filename':saved_path})
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.callproc('sp_add',(nhacungcap,khuyenmai,1,loai_sp,ten_sp,thongtin_sp,'static/sanpham/'+img_name,gia_sp, soluong_sp))
        data = cursor.fetchall()
        if len(data) is 0:
            conn.commit()
            return redirect(url_for('total_product'))

@app.route("/total_product")
def total_product():
    name = request.cookies.get('userID')
    con = mysql.connect()
    cursor = con.cursor()
    cursor.callproc('login_nv',(name,))
    data = cursor.fetchall()
    if len(data) > 0:
        id_ch = 1
        con1 = mysql.connect()
        cursor1 = con1.cursor()
        cursor1.callproc('sp_show',(id_ch,))
        data1 = cursor1.fetchall()
        if len(data1) > 0:
            return render_template("total_product.html", data1=data1,data=data[0][7], quyen_nv = data[0][2])
            
@app.route("/delete_sp", methods=['GET'])
def delete_sp():
    if request.method == 'GET':
        id_sp = request.args.get('id_sp')
        id = int(id_sp)
        con = mysql.connect()
        cursor = con.cursor()
        cursor.callproc('sp_delete',(id,))
        data = cursor.fetchall()
        if len(data) is 0:
            con.commit()
            return redirect(url_for('total_product'))

@app.route("/edit_product", methods=['GET'])
def edit_product():
    if request.method == 'GET':
        id_sp = request.args.get('id_sp')
        id = int(id_sp)
        con = mysql.connect()
        cursor = con.cursor()
        cursor.callproc('sp',(id,))
        data = cursor.fetchall()
        if len(data) > 0:
            return render_template("edit.html", data = data)

@app.route("/edit", methods=['POST'])
def edit():
    UPLOAD_FOLDER = 'myblog/static/sanpham/'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    if request.method == 'POST':
        nhacungcap = request.form['nhacungcap']
        khuyenmai = request.form['khuyenmai']
        loai_sp = request.form['loai_sp']
        id_sp = request.form['id_sp']
        ten_sp = request.form['ten_sp']
        thongtin_sp = request.form['thongtin_sp']
        hinhanh_sp = request.files['hinhanh_sp']
        gia_sp = request.form['gia_sp']
        soluong_sp = request.form['soluong_sp']

        return str(hinhanh_sp)
        img_name = secure_filename(hinhanh_sp.filename)
        saved_path = os.path.join(app.config['UPLOAD_FOLDER'], img_name)
        app.logger.info("saving {}".format(saved_path))
        hinhanh_sp.save(saved_path)

        return 'static/sanpham/'+img_name
        con = mysql.connect()
        cursor = con.cursor()
        cursor.callproc('sp_edit',(id_sp, nhacungcap, khuyenmai, loai_sp, ten_sp, thongtin_sp, 'static/sanpham/'+img_name, gia_sp, soluong_sp))
        data = cursor.fetchall()
        if len(data) is 0:
            con.commit()
            return redirect(url_for('total_product'))

@app.route("/account")
def account():
    name = request.cookies.get('userID')
    if name:
        con = mysql.connect()
        cursor = con.cursor()
        cursor.callproc('login_nv',(name,))
        data = cursor.fetchall()
        if len(data) > 0:
            return render_template('account.html', data=data, quyen_nv = data[0][2])
        else:
            con = mysql.connect()
            cursor = con.cursor()
            cursor.callproc('login_kh',(name,))
            data = cursor.fetchall()
            if len(data) > 0:
                con3 = mysql.connect()
                cursor3 = con3.cursor()
                cursor3.callproc('tong_sp',(name,))
                sp3 = cursor3.fetchall()
                return render_template('account.html', data=data, sp3=sp3)

@app.route("/account_update_kh", methods=['POST'])
def account_update_kh():
    if request.method == 'POST':
        name = request.cookies.get('userID')
        ten = request.form['ten']
        diachi = request.form['diachi']
        sdt = request.form['sdt']
        con = mysql.connect()
        cursor = con.cursor()
        cursor.callproc('update_kh',(ten,diachi,sdt,name,))
        data = cursor.fetchall()
        if len(data) is 0:
            con.commit()
            return redirect(url_for('account'))

@app.route("/account_update_nv", methods=['POST'])
def account_update_nv():
    if request.method == 'POST':
        name = request.cookies.get('userID')
        ten = request.form['ten']
        diachi = request.form['diachi']
        sdt = request.form['sdt']
        email = request.form['email']

        con = mysql.connect()
        cursor = con.cursor()
        cursor.callproc('update_nv',(ten,diachi,sdt,email,name,))
        data = cursor.fetchall()
        if len(data) is 0:
            con.commit()
            return redirect(url_for('account'))

@app.route('/showlogin')
def showlogin():
    return render_template("login.html")

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        name = request.form['username']
        password = request.form['password']
        if name  and password:
            con = mysql.connect()
            cursor = con.cursor()
            cursor.callproc('login_nv',(name,))
            data = cursor.fetchall()
            error = None
            error1 = None
            if len(data) > 0:
                # if check_password_hash(str(data[0][9]),password):
                if str(data[0][9]) == password:
                    resp = make_response(render_template('index.html', data = data[0][7], quyen_nv = data[0][2]))
                    resp.set_cookie('userID', name)
                    return resp
                else:
                    error1 = 'Sai mật khẩu'
                    return  render_template('login.html',error1 = error1)
            else:
                con = mysql.connect()
                cursor = con.cursor()
                cursor.callproc('login_kh',(name,))
                data = cursor.fetchall()
                if len(data) > 0:
                    if check_password_hash(str(data[0][6]),password):
                        con3 = mysql.connect()
                        cursor3 = con3.cursor()
                        cursor3.callproc('tong_sp',(name,))
                        sp3 = cursor3.fetchall()
                        resp = make_response(render_template('index.html', data = data[0][4], sp3=sp3, quyen_nv=data[0][2]))
                        resp.set_cookie('userID', name)
                        return resp
                    else:
                        error1 = 'Sai mật khẩu'
                        return  render_template('login.html',error1 = error1)
                else:
                    error = 'Tên đăng nhập không tồn tại'
                    return render_template('login.html', error = error)

@app.route("/showregister")
def showregister():
    return render_template("register.html")

@app.route("/register", methods=['POST'])
def register(): 
    name = request.form['username']
    password = request.form['password']
    re_password = request.form['re_password']

    error = None
    error1 = None

    if name:
        con = mysql.connect()
        cursor = con.cursor()
        cursor.callproc('login_nv',(name,))
        data = cursor.fetchall()
        if len(data) > 0:
            error = 'Tên đăng ký đã tồn tại'
            return render_template('register.html', error=error)
        else:
            con = mysql.connect()
            cursor = con.cursor()
            cursor.callproc('login_kh',(name,))
            data = cursor.fetchall()
            if len(data) > 0:
                error = 'Tên đăng ký đã tồn tại'
                return render_template('register.html', error=error)
            else:
                if password == re_password:
                    p_name = request.cookies.get('userID')
                    if p_name != None:
                        con1 = mysql.connect()
                        cursor1 = con1.cursor()
                        cursor1.callproc('login_nv',(p_name,))
                        data1 = cursor1.fetchall()
                        if data1[0][2] == 1:  
                            conn = mysql.connect()
                            cursor = conn.cursor()
                            cursor.callproc('register_nv',(name, password, 1, 2, 1))
                            data = cursor.fetchall()
                            if len(data) is 0:
                                conn.commit()
                                return render_template('login.html')
                    else:
                        conn = mysql.connect()
                        cursor = conn.cursor()
                        _hashed_password = generate_password_hash(password)
                        cursor.callproc('register_kh',(name, _hashed_password))
                        data = cursor.fetchall()
                        if len(data) is 0:
                            conn.commit()
                            return render_template('login.html')
                else:
                    error1 = 'Mật khẩu không trùng khớp'
                    return render_template('register.html', error1=error1)

@app.route("/signout")
def signout():
    resp = make_response(render_template('index.html'))
    resp.delete_cookie('userID', None)
    return resp

@app.route("/dh_khachhang")
def dh_khachhang():
    name = request.cookies.get('userID')
    con = mysql.connect()
    cursor = con.cursor()
    cursor.callproc('login_nv',(name,))
    data = cursor.fetchall()
    if len(data) > 0:
        id_ch = 1
        con1 = mysql.connect()
        cursor1 = con1.cursor()
        cursor1.callproc('dh_khachhang',)
        data1 = cursor1.fetchall()
        # return str(data1)
        if len(data1) > 0:
            return render_template("dh_khachhang.html", data1=data1,data=data[0][7], quyen_nv = data[0][2])
        else:
            return render_template("dh_khachhang.html", data=data[0][7], quyen_nv = data[0][2])

@app.route("/ql_account")
def ql_account():
    name = request.cookies.get('userID')
    if name:
        con = mysql.connect()
        cursor = con.cursor()
        cursor.callproc('login_nv',(name,))
        data = cursor.fetchall()
        if len(data) > 0:
            con1 = mysql.connect()
            cursor1 = con1.cursor()
            cursor1.callproc('ql_account',())
            data1 = cursor1.fetchall()
            return render_template('ql_account.html', data=data[0][7], quyen_nv = data[0][2], data1 = data1)

@app.route("/delete_NV", methods=['GET'])
def delete_NV():
    if request.method == 'GET':
        id_nv = request.args.get('id_nv')
        # return str(id_nv)
        con = mysql.connect()
        cursor = con.cursor()
        cursor.callproc('delete_nv',(id_nv,))
        data = cursor.fetchall()
        if len(data) is 0:
            con.commit()
            return redirect(url_for('ql_account'))

@app.route("/ql_khachhang")
def ql_khachhang():
    name = request.cookies.get('userID')
    if name:
        con = mysql.connect()
        cursor = con.cursor()
        cursor.callproc('login_nv',(name,))
        data = cursor.fetchall()
        if len(data) > 0:
            con1 = mysql.connect()
            cursor1 = con1.cursor()
            cursor1.callproc('ql_khachhang',())
            data1 = cursor1.fetchall()
            return render_template('ql_khachhang.html', data=data[0][7], quyen_nv = data[0][2], data1 = data1)

@app.route("/delete_KH", methods=['GET'])
def delete_KH():
    if request.method == 'GET':
        id_kh = request.args.get('id_kh')
        # return str(id_nv)
        con = mysql.connect()
        cursor = con.cursor()
        cursor.callproc('delete_KH',(id_kh,))
        data = cursor.fetchall()
        if len(data) is 0:
            con.commit()
            return redirect(url_for('ql_khachhang'))

@app.route("/dh_daxuly", methods=['GET'])
def dh_daxuly():
    name = request.cookies.get('userID')
    con = mysql.connect()
    cursor = con.cursor()
    cursor.callproc('login_nv',(name,))
    data = cursor.fetchall()
    if request.method == 'GET':
        id_dh = request.args.get('id_dh')
        id_sp = request.args.get('id_sp')
        # return str(id_sp)
        con1 = mysql.connect()
        cursor1 = con1.cursor()
        cursor1.callproc('dh_daxuly',(id_dh, id_sp, name))
        data1 = cursor1.fetchall()
        if len(data1) is 0:
            con1.commit()
            if data[0][2] == 1:
                con2 = mysql.connect()
                cursor2 = con2.cursor()
                cursor2.callproc('dh_khachhang_DXL',())
                data2 = cursor2.fetchall()
                return render_template('dh_daxuly.html', data=data[0][7], quyen_nv = data[0][2], data1 = data2)
            else:
                con1 = mysql.connect()
                cursor1 = con1.cursor()
                cursor1.callproc('dh_khachhang',)
                data1 = cursor1.fetchall()
                # return str(data1)
                if len(data1) > 0:
                    return render_template("dh_khachhang.html", data1=data1,data=data[0][7], quyen_nv = data[0][2])
                else:
                    return render_template("dh_khachhang.html", data=data[0][7], quyen_nv = data[0][2])
    else:
        if data[0][2] == 1:
            con2 = mysql.connect()
            cursor2 = con2.cursor()
            cursor2.callproc('dh_khachhang_DXL',())
            data2 = cursor2.fetchall()
            return render_template('dh_daxuly.html', data=data[0][7], quyen_nv = data[0][2], data1 = data2)
        else:
            con1 = mysql.connect()
            cursor1 = con1.cursor()
            cursor1.callproc('dh_khachhang',)
            data1 = cursor1.fetchall()
            # return str(data1)
            if len(data1) > 0:
                return render_template("dh_khachhang.html", data1=data1,data=data[0][7], quyen_nv = data[0][2])
            else:
                return render_template("dh_khachhang.html", data=data[0][7], quyen_nv = data[0][2])

@app.route("/dh_danhan", methods=['GET'])
def dh_danhan():
    name = request.cookies.get('userID')
    con = mysql.connect()
    cursor = con.cursor()
    cursor.callproc('login_nv',(name,))
    data = cursor.fetchall()
    if request.method == 'GET':
        id_dh = request.args.get('id_dh')
        con1 = mysql.connect()
        cursor1 = con1.cursor()
        cursor1.callproc('dh_danhan',(id_dh,))
        data1 = cursor1.fetchall()
        if len(data1) is 0:
            con1.commit()
            if data[0][2] == 1:
                con2 = mysql.connect()
                cursor2 = con2.cursor()
                cursor2.callproc('dh_kh_danhan',())
                data2 = cursor2.fetchall()
                return render_template('danhan.html', data=data[0][7], quyen_nv = data[0][2], data1 = data2)
            else:
                con1 = mysql.connect()
                cursor1 = con1.cursor()
                cursor1.callproc('dh_khachhang_DXL',)
                data1 = cursor1.fetchall()
                # return str(data1)
                if len(data1) > 0:
                    return render_template("dh_daxuly.html", data1=data1,data=data[0][7], quyen_nv = data[0][2])
                else:
                    return render_template("dh_daxuly.html", data=data[0][7], quyen_nv = data[0][2])
    else:
        if data[0][2] == 1:
            con2 = mysql.connect()
            cursor2 = con2.cursor()
            cursor2.callproc('dh_kh_danhan',())
            data2 = cursor2.fetchall()
            return render_template('dh_daxuly.html', data=data[0][7], quyen_nv = data[0][2], data1 = data2)
        else:
            con1 = mysql.connect()
            cursor1 = con1.cursor()
            cursor1.callproc('dh_khachhang_DXL',)
            data1 = cursor1.fetchall()
            # return str(data1)
            if len(data1) > 0:
                return render_template("dh_daxuly.html", data1=data1,data=data[0][7], quyen_nv = data[0][2])
            else:
                return render_template("dh_daxuly.html", data=data[0][7], quyen_nv = data[0][2])

@app.route("/kh_danhan", methods=['GET'])
def kh_danhan():
    name = request.cookies.get('userID')
    con = mysql.connect()
    cursor = con.cursor()
    cursor.callproc('login_kh',(name,))
    data = cursor.fetchall()
    if len(data) > 0:
        con1 = mysql.connect()
        cursor1 = con1.cursor()
        cursor1.callproc('kh_danhan',(name,))
        data1 = cursor1.fetchall()

        con3 = mysql.connect()
        cursor3 = con3.cursor()
        cursor3.callproc('tong_sp',(name,))
        sp3 = cursor3.fetchall()
        return render_template('kh_danhan.html', data=data[0][4], data1 = data1, sp3=sp3)
    else:
        con3 = mysql.connect()
        cursor3 = con3.cursor()
        cursor3.callproc('tong_sp',(name,))
        sp3 = cursor3.fetchall()
        return render_template('kh_danhan.html', data=data[0][4], sp3=sp3)
            
