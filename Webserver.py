from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from collections import OrderedDict
from datetime import timedelta
PORT_NUMBER = 8080

#This class will handles any incoming request from
#the browser
class myHandler(BaseHTTPRequestHandler):

        #Handler for the GET requests
        def do_GET(self):
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                self.wfile.write("<html><head><title> Trabalho 1</title></head>")
                import time
                now=time.strftime("%c")
                self.wfile.write("<body><p> Data e hora do sistema: %s</p>" %now)
                with open('/proc/uptime','r') as f:
                        uptime_seconds = float(f.readline().split()[0])
                        uptime_string = str(timedelta(seconds=uptime_seconds))
                self.wfile.write("<body><p> Uptime: %s</p>" %uptime_string)

                with open('/proc/cpuinfo') as f:
                        for line in f:
        # Ignore the blank line separating the information between
        # details about two processing units
                                if line.strip():
                                        if line.rstrip('\n').startswith('model name'):
                                                model_name = line.rstrip('\n').split(':')[1]
                                                self.wfile.write("<body><p> Modelo do processador: %s</p>" %model_name)

               
                import os
                CPU_Pct=str(round(float(os.popen('''grep 'cpu ' /proc/stat | awk '{usage=($2+$4)*100/($2+$4+$5)} END {print usage }' ''').readline()),2))
                self.wfile.write("<body><p>Uso do processador = %s%%</p>" %CPU_Pct)
                def meminfo():
                        meminfo=OrderedDict()

                        with open('/proc/meminfo') as f:
                                for line in f:
                                        meminfo[line.split(':')[0]] = line.split(':')[1].strip()
                        return meminfo
                if __name__=='__main__':
                        meminfo = meminfo()
                        self.wfile.write("<body><p>%s</p>" %'Memoria Ram Total: {0}'.format(meminfo['MemTotal']))
                        self.wfile.write("<body><p>%s</p>" %'Memoria Ram Livre: {0}'.format(meminfo['MemFree']))
                def process_list():
                        pids = []
			for subdir in os.listdir('/proc'):
                                if subdir.isdigit():
                                        pids.append(subdir)
                        return pids
                pids = process_list()
                self.wfile.write("<body><p>%s</p>" %'Processos em execucao: {0}'.format(len(pids)))
               
try:
        server = HTTPServer(('', PORT_NUMBER), myHandler)
        print 'Started httpserver on port ' , PORT_NUMBER
        server.serve_forever()
except KeyboardInterrupt:
        print '^C received, shutting down the web server'
server.socket.close()
