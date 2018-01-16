import common.ChatIF;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class ServerConsole implements ChatIF{

    final public static int DEFAULT_PORT = 5555;

    EchoServer server;

    public ServerConsole(int port) {
        this.server = new EchoServer(port, this);
    }

    /**
     * This method waits for input from the common. Once it is
     * received, it sends it to the server's message handler.
     */
    public void accept()
    {
        try {
            BufferedReader fromConsole = new BufferedReader(new InputStreamReader(System.in));
            String message;
            while (true)
            {
                message = fromConsole.readLine();
                server.handleMessageFromServerUI(message);
            }
        }
        catch (Exception ex){
            System.out.println("Unexpected error while reading from common!");
        }
    }

    @Override
    public void display(String message) {
        System.out.println("> " + message);
    }

    public static void main(String[] args) {
        int port = 0;

        try{
            port = Integer.parseInt(args[0]);
        }
        catch (Throwable t)
        {
            port = DEFAULT_PORT;
        }

        ServerConsole sc = new ServerConsole(port);
        try {
            sc.server.listen();
        } catch (IOException e) {
            System.out.println("ERROR! - Could not listen for clients");
            return;
        }
        sc.accept(); // Wait for common data
    }
}
