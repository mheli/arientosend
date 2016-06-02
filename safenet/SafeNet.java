
import CRYPTOCard.API.*;

/*
 * Using the Java API to communicate with the SafeNet
 * Authentication Server. All the relevant files for this API
 * are in <prefix> = /usr/local/cryptocard/javaapi/.
 * 
 * - To configure the SafeNet server options, go to 
 *   <prefix>/ini/JCryptoWrapper.ini
 * - Make sure <prefix>/bin/x64/libJCryptoWrapper.so
 *   exists
 * - Save the relevant Key file from the server as
 *   <prefix>/bsidkey/Agent.bsidkey
 *
 * Note: To run this requires sudo until I figure out
 *       how to fix the permissions on libJCryptoWrapper.so
 */

public class SafeNet {
    
    private static int AUTH_FAILURE = 0;
    private static int AUTH_SUCCESS = 1;
    private static int CHALLENGE = 2;
    private static int SERVER_PIN_PROVIDED = 3;
    private static int USER_PIN_CHANGE = 4;
    private static int OUTER_WINDOW_AUTH = 5;
    private static int CHANGE_STATIC_PASSWORD = 6;
    private static int STATIC_CHANGE_FAILED = 7;
    private static int PIN_CHANGE_FAILED = 8;

    private static String osLoadLib = "/usr/local/cryptocard/javaapi/bin/x64/libJCryptoWrapper.so";
    private static String osIniPath = "/usr/local/cryptocard/javaapi/ini/JCryptoWrapper.ini";

    private CRYPTOCardAPI crypt;

    SafeNet() {
 
        crypt = CRYPTOCardAPI.getInstance();
        crypt.setINIPath(osIniPath);
        
        /* Try to load Library from API Manager */
        boolean load_succeed = false;
        try {

//            System.out.println("Loading JNI Library");
            crypt.LoadJNILibrary();
            load_succeed = true;

        } catch (UnsatisfiedLinkError ex) {
            System.out.println(ex.toString());
        } catch (Exception ex){
            System.out.println(ex.toString());
        }

        /* If LoadJNILibrary() fails, try hard coded path */
        if (!load_succeed) {
            System.out.println("Environment path does not contain libJCryptoWrapper.so, trying hardcoded paths");
            try {
 
                crypt.LoadJNILibrary(osLoadLib);
                load_succeed = true;

            } catch (UnsatisfiedLinkError ex) {
                System.out.println(ex.toString());
            } catch (Exception ex){
                System.out.println(ex.toString());
            }           
        }

        if (load_succeed) {
  //          System.out.println("libJCryptoWrapper.so successfully loaded.");
        } else {
            System.out.println("ERROR: Could not load libJCryptoWrapper.so");
            System.exit(1);
        }   
    
    }
    
    public boolean authenticate(String user, String pin) {
   
        // todo: sanitize inputs

        int numFields = 11;
        String[] arrData = new String[numFields];
        
        for (int i = 0; i < numFields; i++) {
            arrData[i] = "";
        }

        arrData[0] = user;
        arrData[2] = pin;
        
        crypt.Authenticate(arrData);
        
        return (Integer.parseInt(arrData[7]) == AUTH_SUCCESS);

    }

} 
