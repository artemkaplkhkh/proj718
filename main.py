import sys
import sqlite3
import qrcode
from random import choice

from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.colormasks import RadialGradiantColorMask
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer

from PyQt5 import uic
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QDialog, QPushButton, QLabel, QVBoxLayout, QLineEdit


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('sing_in.ui', self)

        self.sing_in.clicked.connect(self.sing_in_func)
        self.sing_up.clicked.connect(self.sing_up_func)
        self.sing_in_admin.clicked.connect(self.sing_adm)

    def sing_adm(self):
        ex.close()
        self.sia = Sing_IN_As_Admin()
        self.sia.show()

    def sing_up_func(self):
        self.suo = Sing_up_one_wind()
        self.suo.show()
        ex.close()

    def sing_in_func(self):
        self.email_sing_in = self.email_edit.text()
        self.password_sing_in = self.password_edit.text()
        con = sqlite3.connect('profsouz.db')
        cur = con.cursor()
        usl = f'SELECT email, password FROM people WHERE email == "{self.email_sing_in}" AND password == "{self.password_sing_in}"'
        res = cur.execute(usl).fetchall()
        if res:
            self.home_wnd = Home_Window()
            self.home_wnd.show()
            ex.close()
        else:
            def ok_pressed():
                self.email_edit.setText('')
                self.password_edit.setText('')
                dialog.close()

            dialog = QDialog()
            dialog.setGeometry(200, 100, 525, 100)
            ok_btn = QPushButton(dialog)
            stat_lab = QLabel(dialog)
            stat_lab.setText('Пользователь с такими данными не найден или введенные данные неверны')
            stat_lab.move(20, 20)
            ok_btn.setText('OK')
            ok_btn.setGeometry(210, 50, 70, 25)
            ok_btn.setStyleSheet('QPushButton {background: rgb(254, 127, 94); color: "white"; '
                                 'border: 2px solid rgb(254, 127, 94); border-radius: 10px} '
                                 'QPushButton:pressed {background: rgb(234, 107, 74)}')
            ok_btn.clicked.connect(ok_pressed)
            dialog.exec_()
        con.close()


class Sing_up_one_wind(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('sing_up_one.ui', self)

        self.next_button.clicked.connect(self.next_func)

    def next_func(self):
        ex.suo.close()
        self.sud = Sing_up_two_wind()
        self.sud.show()


class Sing_up_two_wind(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('sing_up_two.ui', self)

        self.sing_up_button.clicked.connect(self.sing_up_func)

    def sing_up_func(self):
        fio = f'{ex.suo.fam_edit.text()} {ex.suo.name_edit.text()} {ex.suo.father_edit.text()}'
        con = sqlite3.connect('profsouz.db')
        cur = con.cursor()
        usl = f'INSERT INTO people(email, fio, password, number, autent) VALUES("{self.email_edit.text()}", "{fio}", ' \
              f'"{self.password_edit.text()}", "{self.number_edit.text()}", "False")'
        res = cur.execute(usl)
        con.commit()
        con.close()
        ex.suo.sud.close()
        ex.show()


class Home_Window(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('home.ui', self)
        self.profile_btn.clicked.connect(self.profile_func)
        self.qr_button.clicked.connect(self.open_qr_wind)
        con = sqlite3.connect('profsouz.db')
        cur = con.cursor()
        res = list(cur.execute(f'SELECT fio FROM people WHERE email == "{ex.email_sing_in}"'))
        name = res[0][0].split()[1]
        self.hello_lab.setText(f'Здравствуйте, {name}!')
        lgots = cur.execute(f'SELECT lgots FROM people WHERE email == "{ex.email_sing_in}"').fetchall()
        if lgots[0][0]:
            lgots = eval(lgots[0][0])
            lay_lgots = QVBoxLayout()
            for i in lgots:
                lg_lb = QLabel(f'{i[0]} - {i[1]}')
                lg_lb.setStyleSheet('color: rgb(70, 70, 70); border: 0px')
                lg_lb.setFont(QFont('Gill Sans', 18))
                lay_lgots.addWidget(lg_lb)
            wid = QWidget()
            wid.setLayout(lay_lgots)
            self.lgots_area.setWidget(wid)
            self.lgots_area.setWidgetResizable(True)
        else:
            lg_lb = QLabel('    Упс... Похоже, у вас нет партнеров и льгот!')
            lg_lb.setStyleSheet('color: rgb(70, 70, 70); border: 0px')
            lg_lb.setFont(QFont('Gill Sans', 18))
            self.lgots_area.setWidget(lg_lb)
        con.close()

    def profile_func(self):
        ex.home_wnd.close()
        self.profile_wnd = Profile_Window()
        self.profile_wnd.show()

    def exit_func(self):
        ex.home_wnd.close()
        ex.show()

    def open_qr_wind(self):
        con = sqlite3.connect('profsouz.db')
        cur = con.cursor()
        res = list(cur.execute(f'SELECT autent FROM people WHERE email == "{ex.email_sing_in}"'))[0][0]
        if res == 'True':
            ex.home_wnd.close()
            self.qr_wd = QR_Wind()
            self.qr_wd.show()

        else:
            dialog = QDialog()
            dialog.resize(350, 100)
            stat_lab = QLabel(dialog)
            stat_lab.setText('Упс...  Похоже, ваш аккаунт не был подтвержден')
            stat_lab.move(20, 20)
            ok_btn = QPushButton(dialog)
            ok_btn.setText('OK')
            ok_btn.clicked.connect(lambda: dialog.close())
            ok_btn.move(130, 50)
            dialog.exec_()
        cur.close()
        con.close()


class Profile_Window(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('profile_UI.ui', self)
        self.home_btn.clicked.connect(self.back_home)
        self.exit_btn.clicked.connect(self.exit_func)
        self.change_date_btn.clicked.connect(self.change_date_func)
        con = sqlite3.connect('profsouz.db')
        cur = con.cursor()
        res = cur.execute(f'SELECT fio, date_born, date_enter, date_leave, doljnost FROM people '
                          f'WHERE email == "{ex.email_sing_in}"').fetchall()[0]
        self.fio_lab.setText(res[0])
        if res[1]:
            self.date_born_lab.setText(res[1])
            self.change_date_btn.close()
        if res[2]:
            self.date_enter_lab.setText(res[2])
        if res[3]:
            self.pol_lab.setText(res[3])
        if res[4]:
            self.dolj_lab.setText(res[4])
        con.close()

    def back_home(self):
        ex.home_wnd.profile_wnd.close()
        ex.home_wnd.show()

    def exit_func(self):
        ex.home_wnd.profile_wnd.close()
        ex.show()
        ex.email_edit.setText('')
        ex.password_edit.setText('')

    def change_date_func(self):
        def ok_pressed():
            self.date_born_lab.setText(date.text())
            self.change_date_btn.close()
            con = sqlite3.connect('profsouz.db')
            cur = con.cursor()
            res = cur.execute(f'UPDATE people SET date_born = "{date.text()}" WHERE email == "{ex.email_sing_in}"')
            con.commit()
            cur.close()
            con.close()
            dialog.close()

        dialog = QDialog()
        dialog.setGeometry(200, 100, 525, 100)
        ok_btn = QPushButton(dialog)
        stat_lab = QLabel(dialog)
        stat_lab.setText('Введите вашу дату рождения:')
        date = QLineEdit(dialog)
        date.setGeometry(230, 20, 150, 20)
        stat_lab.move(20, 20)
        ok_btn.setText('OK')
        ok_btn.setGeometry(210, 50, 70, 25)
        ok_btn.setStyleSheet('QPushButton {background: rgb(254, 127, 94); color: "white"; '
                             'border: 2px solid rgb(254, 127, 94); border-radius: 10px} '
                             'QPushButton:pressed {background: rgb(234, 107, 74)}')
        ok_btn.clicked.connect(ok_pressed)
        dialog.exec_()


class QR_Wind(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('qr_UI.ui', self)
        self.home_btn.clicked.connect(self.back_home_func)

        qr = qrcode.QRCode(version=1,
                           box_size=5,
                           border=5)
        con = sqlite3.connect('profsouz.db')
        cur = con.cursor()
        res = cur.execute(f'SELECT fio, lgots, doljnost FROM people WHERE email == "{ex.email_sing_in}"').fetchall()[0]
        name = res[0]
        dol = res[-1]
        lst_lg = [f'{i[0]} - {i[1]}' for i in eval(res[1])]
        qr.add_data(f'ФИО: {name}\nДолжность: {dol}\nЛьготы: {choice(lst_lg)}')
        cur.close()
        con.close()
        qr.make(fit=True)
        self.img = qr.make_image(image_factory=StyledPilImage, module_drawer=RoundedModuleDrawer(),
                                 color_mask=RadialGradiantColorMask(edge_color=(249, 101, 58),
                                                                    center_color=(249, 101, 58)))
        self.img.save('qrw.png')
        self.qr_lab.setPixmap(QPixmap('qrw.png'))


    def back_home_func(self):
        ex.home_wnd.qr_wd.close()
        ex.home_wnd.show()


class Sing_IN_As_Admin(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('sing_in_admin.ui', self)

        self.sing_in_admin.clicked.connect(self.sing_admin_func)

    def sing_admin_func(self):
        self.email_sing_in_admin = self.email_edit_admin.text()
        self.password_sing_in_admin = self.password_edit_admin.text()
        con = sqlite3.connect('profsouz.db')
        cur = con.cursor()
        usl = f'SELECT email, password FROM admins WHERE email == "{self.email_sing_in_admin}" AND password == "{self.password_sing_in_admin}"'
        res = cur.execute(usl).fetchall()
        if res:
            ex.sia.close()
            self.auiw = Admin_UI_Work()
            self.auiw.show()
        else:
            def ok_pressed():
                self.email_edit_admin.setText('')
                self.password_edit_admin.setText('')
                dialog.close()

            dialog = QDialog()
            dialog.setGeometry(200, 100, 525, 100)
            ok_btn = QPushButton(dialog)
            stat_lab = QLabel(dialog)
            stat_lab.setText('Администратор с такими данными не найден или введенные данные неверны')
            stat_lab.move(20, 20)
            ok_btn.setText('OK')
            ok_btn.setGeometry(210, 50, 70, 25)
            ok_btn.setStyleSheet('QPushButton {background: rgb(254, 127, 94); color: "white"; '
                                 'border: 2px solid rgb(254, 127, 94); border-radius: 10px} '
                                 'QPushButton:pressed {background: rgb(234, 107, 74)}')
            ok_btn.clicked.connect(ok_pressed)
            dialog.exec_()


class Admin_UI_Work(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('admin_ui_work.ui', self)
        self.show_info_button.clicked.connect(self.show_info_func)
        self.show_part_button.clicked.connect(self.lgots_and_parts_func)
        self.accept_btn.clicked.connect(self.accept_fnc)
        self.delete_btn.clicked.connect(self.delete_fnc)
        self.new_user_btn.clicked.connect(self.new_user_fnc)

        con = sqlite3.connect('profsouz.db')
        cur = con.cursor()
        res = cur.execute(f'SELECT fio FROM people').fetchall()
        self.list_fio = []
        for i in res:
            self.list_fio.append(i[0])
        self.user_name.addItems(self.list_fio)
        cur.close()
        con.close()

    def new_user_fnc(self):
        ex.sia.auiw.close()
        self.nu = New_user_UI()
        self.nu.show()

    def delete_fnc(self):
        def yes_fnc():
            con = sqlite3.connect('profsouz.db')
            cur = con.cursor()
            res = cur.execute(f'DELETE FROM people WHERE fio == "{self.user_name.currentText()}"')
            res = cur.execute(f'SELECT fio FROM people').fetchall()
            self.list_fio = []
            self.user_name.clear()
            for i in res:
                self.list_fio.append(i[0])
            self.user_name.addItems(self.list_fio)
            con.commit()
            cur.close()
            con.close()
            dialog.close()

        dialog = QDialog()
        dialog.setGeometry(200, 200, 400, 150)
        stat_lab = QLabel(dialog)
        stat_lab.setText('Вы уверены, что хотите удалять аккаунт пользователя?')
        stat_lab.move(10, 20)
        yes_btn = QPushButton(dialog)
        yes_btn.setText('Да')
        no_btn = QPushButton(dialog)
        no_btn.setText('Нет')
        yes_btn.move(130, 50)
        no_btn.move(200, 50)
        yes_btn.clicked.connect(yes_fnc)
        no_btn.clicked.connect(lambda: dialog.close())
        dialog.exec_()

    def accept_fnc(self):
        def yes_fnc():
            con = sqlite3.connect('profsouz.db')
            cur = con.cursor()
            res = cur.execute(f'UPDATE people SET autent = "True" WHERE fio == "{self.user_name.currentText()}"')
            con.commit()
            cur.close()
            con.close()
            dialog.close()

        dialog = QDialog()
        dialog.setGeometry(200, 200, 400, 150)
        stat_lab = QLabel(dialog)
        stat_lab.setText('Вы уверены, что хотите подтвердить аккаунт пользователя?')
        stat_lab.move(10, 20)
        yes_btn = QPushButton(dialog)
        yes_btn.setText('Да')
        no_btn = QPushButton(dialog)
        no_btn.setText('Нет')
        yes_btn.move(130, 50)
        no_btn.move(200, 50)
        yes_btn.clicked.connect(yes_fnc)
        no_btn.clicked.connect(lambda: dialog.close())
        dialog.exec_()

    def lgots_and_parts_func(self):
        ex.sia.auiw.close()
        self.user = self.user_name.currentText()
        self.al = Lgots_and_Parts_UI()
        self.al.show()

    def show_info_func(self):
        ex.sia.auiw.close()
        self.user = self.user_name.currentText()
        self.siui = Show_Info_UI()
        self.siui.show()


class Show_Info_UI(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('show_info_ui.ui', self)

        self.save.clicked.connect(self.save_func)
        self.back_btn.clicked.connect(self.back_fnc)

        con = sqlite3.connect('profsouz.db')
        cur = con.cursor()
        res = cur.execute(f'SELECT fio, date_born, date_enter, date_leave, doljnost, email, password'
                          f' FROM people WHERE fio == "{ex.sia.auiw.user}"').fetchall()[0]
        self.fio_lab.setText(res[0])
        if res[1]:
            self.date_born_edit.setText(res[1])
        if res[2]:
            self.date_enter_edit.setText(res[2])
        if res[3]:
            self.pol_edit.setText(res[3])
        if res[4]:
            self.dolj_edit.setText(res[4])
        if res[5]:
            self.email_edit.setText(res[5])
        if res[6]:
            self.password_edit.setText(res[6])
        cur.close()
        con.close()

    def save_func(self):
        con = sqlite3.connect('profsouz.db')
        cur = con.cursor()
        res = cur.execute(f'UPDATE people SET email = "{self.email_edit.text()}", '
                          f'date_enter = "{self.date_enter_edit.text()}", '
                          f'date_leave = "{self.pol_edit.text()}", '
                          f'doljnost = "{self.dolj_edit.text()}", '
                          f'date_born = "{self.date_born_edit.text()}", '
                          f'password = "{self.password_edit.text()}" '
                          f'WHERE fio == "{ex.sia.auiw.user}"')
        con.commit()
        cur.close()
        con.close()

    def back_fnc(self):
        ex.sia.auiw.siui.close()
        ex.sia.auiw.show()


class Lgots_and_Parts_UI(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('add_lgots_ui.ui', self)

        self.back_btn.clicked.connect(self.back_fnc)
        self.new_part_lgot.clicked.connect(self.new_lg_fnc)

        self.fio_lab.setText(ex.sia.auiw.user)

        con = sqlite3.connect('profsouz.db')
        cur = con.cursor()
        lgots = cur.execute(f'SELECT lgots FROM people WHERE fio == "{ex.sia.auiw.user}"').fetchall()
        if lgots[0][0]:
            self.lgots = eval(lgots[0][0])
            lay_lgots = QVBoxLayout()
            for i in self.lgots:
                lg_lb = QLabel(f'{i[0]} - {i[1]}')
                lg_lb.setStyleSheet('color: rgb(70, 70, 70); border: 0px')
                lg_lb.setFont(QFont('Gill Sans', 18))
                lay_lgots.addWidget(lg_lb)
            wid = QWidget()
            wid.setLayout(lay_lgots)
            self.lgots_area.setWidget(wid)
            self.lgots_area.setWidgetResizable(True)
        else:
            self.lgots = []
            lg_lb = QLabel(' Упс... Похоже, у пользователя нет партнеров и льгот!')
            lg_lb.setStyleSheet('color: rgb(70, 70, 70); border: 0px')
            lg_lb.setFont(QFont('Gill Sans', 18))
            self.lgots_area.setWidget(lg_lb)
        con.close()

    def new_lg_fnc(self):
        def ok_fnc():
            self.lgots.append([new_part.text(), new_lgot.text()])
            con = sqlite3.connect('profsouz.db')
            cur = con.cursor()
            res = cur.execute(f'UPDATE people SET lgots = "{str(self.lgots)}" WHERE fio == "{ex.sia.auiw.user}"')
            lay_lgots = QVBoxLayout()
            for i in self.lgots:
                lg_lb = QLabel(f'{i[0]} - {i[1]}')
                lg_lb.setStyleSheet('color: rgb(70, 70, 70); border: 0px')
                lg_lb.setFont(QFont('Gill Sans', 18))
                lay_lgots.addWidget(lg_lb)
            wid = QWidget()
            wid.setLayout(lay_lgots)
            self.lgots_area.setWidget(wid)
            self.lgots_area.setWidgetResizable(True)
            con.commit()
            cur.close()
            con.close()
            dialog.close()

        dialog = QDialog()
        dialog.resize(400, 150)
        new_part = QLineEdit(dialog)
        new_lgot = QLineEdit(dialog)
        new_lgot.setGeometry(150, 50, 200, 20)
        new_part.setGeometry(150, 20, 200, 20)
        part_lab = QLabel(dialog)
        lgot_lab = QLabel(dialog)
        lgot_lab.setText('Введите льготу:')
        part_lab.setText('Ведите партнера:')
        lgot_lab.move(10, 50)
        part_lab.move(10, 20)
        ok_btn = QPushButton(dialog)
        ok_btn.setText('Добавить')
        ok_btn.move(200, 100)
        ok_btn.clicked.connect(ok_fnc)
        dialog.exec_()

    def back_fnc(self):
        ex.sia.auiw.al.close()
        ex.sia.auiw.show()


class New_user_UI(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('add_user.ui', self)

        self.save.clicked.connect(self.save_new_user_fnc)
        self.back_btn.clicked.connect(self.back_fnc)

    def save_new_user_fnc(self):
        con = sqlite3.connect('profsouz.db')
        cur = con.cursor()
        res = cur.execute(f'INSERT INTO people(fio, date_born, date_enter, date_leave, doljnost, email, password) '
                          f'VALUES("{self.fio_edit.text()}", "{self.date_born_edit.text()}", "{self.date_enter_edit.text()}", '
                          f'"{self.pol_edit.text()}", "{self.dolj_edit.text()}", "{self.email_edit.text()}", '
                          f'"{self.password_edit.text()}")')
        res = cur.execute(f'SELECT fio FROM people').fetchall()
        self.list_fio = []
        ex.sia.auiw.user_name.clear()
        for i in res:
            self.list_fio.append(i[0])
        ex.sia.auiw.user_name.addItems(self.list_fio)
        con.commit()
        cur.close()
        con.close()

    def back_fnc(self):
        ex.sia.auiw.nu.close()
        ex.sia.auiw.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
