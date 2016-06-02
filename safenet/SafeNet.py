from subprocess import Popen, PIPE

class SafeNet:
    def __init__(self):
        self.validated = []
        self.java_cmd = ['java', '-cp', '.:BSIDJavaAPI.jar', 'Main']
        # Fork a process and run the java client.
        self.java_client = Popen(self.java_cmd, stdout=PIPE, stdin=PIPE, stderr=PIPE)


    def authenticate(self, user, pin):
        self.java_client.stdout.flush()
        userpin = user + " " + pin + "\n";
        self.java_client.stdin.write(userpin)
        out = self.java_client.stdout.readline()
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


if __name__ == '__main__':
    s = SafeNet()
    print(s.authenticate("abc", "def"))
    print(s.authenticate("zeeshan", "779663"))
