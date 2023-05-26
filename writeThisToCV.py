import socket ## link between client and sever though: sever la endpoint va client la openpoint 
import ssl ## secure socket layer : bao mat url 
from datetime import datetime
import pickle
import subprocess 
import platform


class Server():
    def __init__(self, name, port, connection, priority ):
        self.name = name
        self.port= port
        self.connection= connection.lower()
        self.priority= priority.lower()

        self.history =[]
        self.alert= False
    
   ## box && funcion 
    def check_connection(self):
        msg = ""
        success = False
        now = datetime.now()
        try:
             if self.connection  =="plain": ## plain: rõ ràng, đơn giản; neu ket noi success
                 socket.create_connection((self.name, self.port ), timeout=5)
                 msg= f"(self.name) is up. on port {self.port} with {self.connection}"
                 success= True
                 self.alert= False
             elif self.connection =="ssl":
                ssl.wrap_socket(socket.create_connection((self.name, self.port ), timeout=5))
                msg= f"(self.name) is up. on port {self.port} with {self.connection}"
                success= True
                self.alert= False
             else:
                if self.ping():
                     msg= f"(self.name) is up. on port {self.port} with {self.connection}"
                     succes= True
                self.alert= False
        except socket.timeout: 
                 msg= f"(self.name) is timeout. on port {self.port}"
        except (ConnectionRefusedError, ConnectionResetError) as t: 
                 msg= f"sever:{self.name}{t} "
        except Exception as t:
                msg= f"no clue??: {t}"
        self.create_history (msg, success, now )
    ## luot truy cap 

    def  create_history(self, msg, success, now ):
         history_max=101
         self.history.append((msg, success, now  )) ##bien: available    
         while len(self.history)> history_max:
            self.history.pop(0)
    def ping(self):
        try:
         output = subprocess.check_output("ping -{} 1 {} ".format('n'if platform.system().lower()=="window" else 'c', self.name), shell=True, universal_newlines=True)
         if 'unreachable' in output:
            return False
         else:
              return True
        except Exception:
            return False

    if __name__== "__main__  ":
         try:
          servers = pickle.load(open("servers.pickle", "rb"))
         except:
            servers=[
                ("facebook.com", 80, "plain", "high"),
                ("reddit.com", 80, "plain", "high"),
                ("gmail.com", 465, "ssl", "high"),
                ("192.168.102.3", 80, "ping", "high"), ##your ip wifi        
                    ]
         for server in servers:
             server.check_connection ()
             print(len(server.history[-1]))
             print(server.history[-1])

         pickle.dump(servers, open("servers.pickle", "wb"))