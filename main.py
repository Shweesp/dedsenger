import dedsenger
import threading, socket
from datetime import datetime
from PyQt5 import QtWidgets
import config


class Messenger(QtWidgets.QMainWindow, dedsenger.Ui_MainWindow):
	def __init__(self):
		super().__init__()
		self.setupUi(self)
		
		# Socket creating
		self._s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self._s.bind((config.host, config.port))
		self.join_status = False
		
		# Receving thread
		self.recv_T = threading.Thread(target = self._receve_message)
		self.recv_T.start()
		
		# Server connect
		self.server = config.server
		try:
			self._s.sendto("I've joined in the chat!".encode("utf-8"), self.server)
		except Exception as err:
			print(err)
		
		# Button click handler
		self.pushButton.pressed.connect(self.send_message)
		
		
	def _receve_message(self):
		try:
			while True:
				data, addr = self._s.recvfrom(1024)
				message = data.decode("utf-8")
				print(message)
				self._print_message(message)
		except Exception as err:
			print("Data reciving error:", err)

	
	def _print_message(self, message):
		self.textBrowser.append(datetime.now().strftime("%H:%M:%S") + " :: " + message)
		
		
	def send_message(self):
		message = self.lineEdit.text()
		if message != "":
			try:
				self._s.sendto(message.encode("utf-8"), self.server)
			except Exception as err:
				print(err)
		self.lineEdit.setText("")

app = QtWidgets.QApplication([])
window = Messenger()
window.show()
app.exec()
