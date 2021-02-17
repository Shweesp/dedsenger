# Interfaces
import main_ui, login_ui

# Sys libs
import threading, socket
from datetime import datetime
from os import O_NONBLOCK as NBLOCK
from fcntl import fcntl, F_SETFL
import errno
from time import sleep

#Graphical libs
from PyQt5 import QtWidgets


# Main class for main window
class Messenger(QtWidgets.QMainWindow, main_ui.Ui_MainWindow):
	def __init__(self, nickname, ip):
		super().__init__()
		self.setupUi(self)

		self.nickname = nickname

		# Socket creating
		self._s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self._s.setblocking(0)

		# Receving thread
		self.recv_T_run = True
		self.recv_T = threading.Thread(target = self._receve_message)
		self.recv_T.start()

		# Server connect
		self.server = (ip, 5000)
		try:
			self._s.sendto("{0} --> join the chat.".format(self.nickname).encode("utf-8"), self.server)
		except Exception as err:
			print("Error:", err)

		# Button click handler
		self.pushButton.pressed.connect(self.send_message)


	# Handling server's messages
	def _receve_message(self):
		while self.recv_T_run:
			try:
				data, addr = self._s.recvfrom(1024)
			# If we have no info to extract in the socket
			except socket.error as e:
				err = e.args[0] # Extract error code
				# Is error about no info?
				if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
					# If it's
					sleep(0.3)
					continue
				else:
					# If it's not
					print("Error:", e)
			# If we have info in socket
			else:
				message = data.decode("utf-8")
				self._print_message(message)
				
		return None


	# Print message on the text browser
	def _print_message(self, message):
		self.textBrowser.append("[{0.hour}:{0.minute}] :: {1}".format(datetime.now(), message))


	# Send message to server
	def send_message(self):
		message = self.lineEdit.text()
		if message != "":
			try:
				self._s.sendto((self.nickname + " : " + message).encode("utf-8"), self.server)
			except Exception as err:
				print(err)
		self.lineEdit.setText("")


	# When you push red "X" in the left side of window
	def closeEvent(self, event):
		self.recv_T_run = False # We have to close the thread
		self.recv_T.join()
		self._s.close()
		event.accept() # Accept window closing


# Login window
class Login(QtWidgets.QMainWindow, login_ui.Ui_Form):
	def __init__(self):
		super().__init__()
		self.setupUi(self)

		# Button click handler
		self.pushButton.pressed.connect(self.button_handler)


	def button_handler(self):
		# Form - nickname, server's IP, user's port
		form = [self.lineEdit.text(), self.lineEdit_2.text()]

		# Is form valid?
		if self._check_valid(form):
			self.close() # Close login window
			main(form)  # Go to the messanger


	def _check_valid(self, form):
		for _ in form:
			if _ == "":
				return False
		return True


# Main window
def main(form):
	window = Messenger(form[0], form[1])
	window.show()

if __name__ == "__main__":
	app = QtWidgets.QApplication([])
	login_window = Login()
	login_window.show()
	app.exec()
