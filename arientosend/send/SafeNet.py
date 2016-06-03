from subprocess import Popen, PIPE
import sys
# The SafeNet wrapper for the Java API
# expects the user names and logins to be 
# passed into its standard in. We open it
# into a subprocess and whenever we want to authenticate,
# write to its stdin and read the result from stdout.

class SafeNet:
    def __init__(self):
        self.validated = []
        # This part is pretty hacked together, but basically for this to work
        # SafeNet.java and Main.java should be compiled into /usr/local/ariento
        # along with BSIDJavaAPI.jar. That allows us to call the java wrapper
        # from anywhere. 
        java_path = '/usr/local/ariento'
        java_classpath = java_path + '/BSIDJavaAPI.jar:' + java_path
        self.java_cmd = ['java', '-cp', java_classpath, 'Main']
        # Fork a process and run the java client.
        self.java_client = Popen(self.java_cmd, stdout=PIPE, stdin=PIPE, stderr=PIPE)

    def authenticate(self, user, pin):
        try:
            self.java_client.stdout.flush()
            userpin = user + " " + pin + "\n";
            self.java_client.stdin.write(userpin)
            out = self.java_client.stdout.readline()
        except IOError:
            print "SafeNet wrapper terminated unexpectedly."
            sys.exit(0)
        
        if 'true' in out:
            self.validated.append(user)
            return True
        else:
            return False

    def __del__(self):
        self.java_client.kill()

    # Returns users validated during this
    # session.
    def recently_validated(self):
        return self.validated


