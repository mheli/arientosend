import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {

    public SafeNet s;

    public class Authenticator implements Runnable { 

        public void run() {
            
            // inefficient implementation right now just sleeps a few
            // milleseconds between iterations.
            // todo: switch to polling using synchronization()
            
            BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
            while(true) {
                try {
                    String input;
                    input = br.readLine();
                    String[] userpass = input.split(" ", 2);
                    
                    // if userpass is not len == 2, then input was invalid.
                    if (userpass.length != 2) {
                        System.out.println("Please provide username and password");
                    } else {

                        String user = userpass[0];
                        String pass = userpass[1];
                        System.out.println(s.authenticate(user, pass));
                
                    }

                } catch (IOException e) {
                    e.printStackTrace();
                }
                try {
                  // Thread.sleep(100);
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }
        }
    }

    public static void main(String[] args) {
        try {
            Main obj = new Main();
            obj.run(args);

        } catch (Exception e) {
            e.printStackTrace();
        } 
    }

    public void run(String[] args) throws Exception {
        s = new SafeNet();
        (new Thread(new Authenticator())).start();
    }

}
