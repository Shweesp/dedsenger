# Interfaces
import main_ui, login_ui
import config

# Sys libs
import threading, socket
from datetime import datetime

#Graphical libs
from PyQt5 import QtWidgets


# Main class for app
class Messenger(QtWidgets.QMainWindow, main_ui.Ui_MainWindow):
	def __init__(self, nickname, ip, port):
		super().__init__()
		self.setupUi(self)
		
		self.nickname = nickname
		
		# Socket creating
		self._s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self._s.bind(("0.0.0.0", int(port)))
		self.join_status = False
		
		# Receving thread
		self.recv_T = threading.Thread(target = self._receve_message)
		self.recv_T.start()
		
		# Server connect
		self.server = (ip, 5000)
		try:
			self._s.sendto("{0} --> join the chat.".format(self.nickname).encode("utf-8"), self.server)
		except Exception as err:
			print(err)
		
		# Button click handler
		self.pushButton.pressed.connect(self.send_message)
		
	
	# Handling client messages	
	def _receve_message(self):
		try:
			while True:
				data, addr = self._s.recvfrom(1024)
				message = data.decode("utf-8")
				self._print_message(message)
		except Exception as err:
			print("Data reciving error:", err)

	
	# Print message on the window
	def _print_message(self, message):
		self.textBrowser.append("[{0.hour}:{0.minute}] :: {1}".format(datetime.now(), message))
		
	
	# Send message for server	
	def send_message(self):
		message = self.lineEdit.text()
		if message != "":
			try:
				self._s.sendto((self.nickname + " : " + message).encode("utf-8"), self.server)
			except Exception as err:
				print(err)
		self.lineEdit.setText("")


class Login(QtWidgets.QMainWindow, login_ui.Ui_Form):
	def __init__(self):
		super().__init__()
		self.setupUi(self)
		
		self.pushButton.pressed.connect(self.button_handler)
		
		
	def button_handler(self):
		form = [self.lineEdit.text(), self.lineEdit_2.text(), self.lineEdit_3.text()]
		if self._check_valid(form):
			self.close()
			main(form)
			
				
	def _check_valid(self, form):
		for _ in form:
			if _ == "":
				return False
		return True
				
def main(form):
	window = Messenger(form[0], form[1], form[2])
	window.show()

app = QtWidgets.QApplication([])
login_window = Login()
login_window.show()
app.exec()
